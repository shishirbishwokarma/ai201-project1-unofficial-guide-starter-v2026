# The Unofficial Guide

**Shishir Bishwokarma** — corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This answers questions about student life at one university, using `campus_life`: 88 short, student-written posts about courses, dining halls, residence halls, campus jobs, transit and registrar rules. You ask something like "Until what week can I drop a course?" or "How late is the library open during term?". It finds the posts closest to your question, and a language model answers using only those posts, naming the file the answer came from. If nothing in the posts is close enough, or the posts don't actually cover the question, it says it doesn't have enough information instead of guessing.

## Chunking Strategy

**Chunk size:** 600
**Overlap:** 0

Every `campus_life` post is short — 183 to 554 characters — and covers one place, course or policy, with the subject named only in the title line ("Halden Hall", "On the add/drop deadline"); the body just says "here" or "this". Splitting a post would separate facts like "closes at 7:00pm" or "Expect 8 to 10 hours a week" from the name they belong to, so `split_documents` keeps one post as one chunk. 600 sits just above the longest post (554), so nothing is cut today, and overlap is 0 because there are no cut edges to overlap. If a longer post is ever added, it gets split at sentence boundaries with the title repeated on each piece. The starter's 800/120 already produced 88 chunks from 88 documents — I kept that outcome on purpose, but with a cap that fits the corpus and an overlap that isn't pretending to do anything.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->





## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Until what week can I drop a course?

**Answer:**

```
  (best distance 0.305, cutoff 0.6)

You can drop a course through the end of week six, though a drop after week two shows as a W on your transcript. 

Source: admin_add_drop_deadline.txt (also mentioned in admin_withdrawal_deadline.txt)

Sources retrieved: admin_add_drop_deadline.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_withdrawal_deadline.txt, advising_registration.txt
```

**Grounding instruction:** I read `GROUNDING_INSTRUCTION` in `generate.py` with `--show-prompt` and tested it on two campus questions my documents don't answer ("What time does the gym open on weekdays?" at 0.535, "How much does a replacement student ID cost?" at 0.584). Both got past the 0.6 gate, and the model refused both. The refusal rule works. The drift I saw was different: the first answer to the question above said only "through the end of week six" and dropped the catch that a drop after week two shows as a W. In this corpus the catch is usually the point of the post, so I added one rule: *"If the document attaches a condition or catch to the fact (a "but", an exception, a cost), include it."* The answer above is from after that change. The gym question still refuses.

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

**0.6.** My five in-corpus questions scored between 0.249 and 0.461; the five out-of-scope questions scored between 0.825 and 0.934, so there's a clean gap of about 0.36. I kept 0.6 rather than the midpoint (~0.64) because my out-of-scope questions are from a completely different world. A campus question my documents don't cover would land closer, and I'd rather refuse it than let the model invent a campus fact.

**What 0.6 gets wrong:** campus questions my documents don't cover still get through. "What time does the gym open on weekdays?" scored 0.535 and "How much does a replacement student ID cost?" scored 0.584, so the gate alone won't stop them, and the grounding instruction has to. My library question passed at 0.461 on the wrong document (`admin_library_holds.txt`), so passing the gate doesn't mean retrieval found the right one. And with only 0.14 between that question and the cutoff, a real question worded differently from the document could be refused.

| Question | In corpus? | Best distance |
|---|---|---|
| Until what week can I drop a course? | Yes | 0.306 |
| How long does an official transcript take electronically? | Yes | 0.249 |
| How late is the library open during term? | Yes | 0.461 |
| What is the maximum number of hours a week I can work on campus during term? | Yes | 0.380 |
| How often does the campus shuttle run on weekends? | Yes | 0.411 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.896 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to write `split_documents` in `chunker.py` from my notes: campus_life posts are 183–554 characters, and the subject is named only in the title line. It wrote a version that keeps each post as one chunk and splits a longer post only at sentence ends, repeating the title on each piece. I'd already set `CHUNK_SIZE = 600` and `CHUNK_OVERLAP = 0` in `config.py` myself, so the code used my numbers. Before indexing, I checked it with `python chunker.py`: 88 chunks from 88 documents, 178–549 characters, all labelled `split_documents`.

**2.** I asked Claude whether my sample answer to "Until what week can I drop a course?" stayed within the sources. At first it said citing `admin_withdrawal_deadline.txt` was wrong. When I printed the prompt with `--show-prompt`, that file did say "Dropping ends at week six," so that claim was wrong and I kept the citation. The real problem was that the answer dropped the catch that a drop after week two shows as a W. I added one rule to `GROUNDING_INSTRUCTION` to include conditions and exceptions, re-ran the question, and the W caveat appeared. I also re-ran "What time does the gym open?" to confirm it still refused.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

## Stretch Features

**Declared before building: Metadata filtering.** Every campus_life filename starts with a category (`admin_`, `course_`, `dining_`, `housing_`, `study_`, `transit_`, `money_`…). I'm adding a `--category` option to `ask` and `retrieve` that narrows retrieval to chunks from that category only. I'll show the same query run with and without the filter, and what changed in the results.

**Built.** At index time each chunk gets a `category` metadata field: the filename prefix before the first underscore, from `category_of` in `store.py`. `search` passes `where={"category": ...}` to Chroma when one is given. `python app.py retrieve "..." --category study` and `python app.py ask "..." --category study` use it. I re-indexed after the change (still 88 chunks).

**Same query, without and with the filter:** `How late is the library open during term?`

Without filter:
```
#   distance   source                           preview
1   0.4614     admin_library_holds.txt          On the library holds  You can place a hold on a chec...
2   0.5081     study_library_hours.txt          Library hours and where to actually sit  Open until ...
3   0.5082     housing_calder_annexe_noise.txt  Noise levels in Calder Annexe  Asked about this a lo...
4   0.5304     course_cs_340.txt                CS 340 Databases  I'm a junior and I've done this tw...
5   0.5552     admin_study_abroad.txt           On the study abroad  Applications open in October fo...
```

With `--category study`:
```
#   distance   source                           preview
1   0.5081     study_library_hours.txt          Library hours and where to actually sit  Open until ...
2   0.6455     study_group_rooms.txt            Booking a group study room  Rooms book two weeks ahe...
```

**What changed:** the wrong document (`admin_library_holds.txt`, which only shares the word "library") drops out, and the document with the answer moves from #2 to #1. The three unrelated chunks (a noise review, a CS course, study abroad) are gone, and only two chunks come back because the `study` category has only two documents. Both versions answered "open until 2am" from `study_library_hours.txt`. Unfiltered, the model picked the right chunk out of the noise. Filtered, the model only sees the two study documents. One side effect: the best distance the gate sees goes **up** from 0.461 to 0.508, because the closest overall match was the wrong document. The filter makes the result list cleaner, but brings this question nearer the 0.6 cutoff, not further from it.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. 88 chunks, each 150–600 characters | 88, 150–600 | 88, 178–549 | 88, 178–549 | 88, 178–549 | MET |
| 5. Answer contains the `expects` value | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

Full log: `results/run_2026-10-20_0012.md`, written by `run_eval.py::main`. Verdicts for criterion 5 come from `scorer.py::judge` (does the answer contain `expects`). Criterion 1 was checked by testing whether any retrieved chunk from `store.py::search` contains `expects`. Criterion 2 was checked by testing whether each of the 15 answers names a `.txt` file.

**Criteria 1, 2 and 5:** one answer from run 2 (`run_eval.py::main`):

```
### Until what week can I drop a course? — run 2

- Best distance: 0.3055 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_withdrawal_deadline.txt, advising_registration.txt

You can drop a course through the end of week six, but a drop after week two shows as a W on your transcript. 

Source: admin_add_drop_deadline.txt (and admin_withdrawal_deadline.txt)
```

The chunk with "six" was retrieved (criterion 1), the answer names a `.txt` source (criterion 2), and it contains `expects` = "six" (criterion 5).

**Criterion 3:** `run_eval.py::check_out_of_scope`, cutoff 0.6, refused 5 of 5:

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |
```

**Criterion 4:** `python chunker.py` (`chunker.py::describe` over `chunker.py::split_documents`):

```
88 chunks, 317 characters on average (shortest 178, longest 549), produced by chunker.py::split_documents
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | 5 of 5 in every run against a target of 4 of 5. Retrieval is deterministic, so all three runs are identical. The library answer only came back at #2, behind `admin_library_holds.txt`, so it counts but is the closest to failing. |
| 2 | Every answer names a source | MET | All 15 answers name at least one `.txt` file. Library run 3 also cited `housing_calder_annexe_noise.txt`, which looked wrong until I read it: that post does say the library is open until 2am. |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 refused against a target of 4 of 5. Not close: the nearest out-of-scope question was 0.825 against a 0.6 cutoff. |
| 4 | 88 chunks, each 150–600 characters | MET | `python chunker.py` reports 88 chunks, shortest 178, longest 549. It's deterministic, so it's the same in every run. |
| 5 | Answer contains the `expects` value | MET | `scorer.py::judge` passed 15 of 15. Because it's a substring test, I also read all 15 answers to check for false passes (e.g. "20" inside "2020"). Every one states the right fact. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
