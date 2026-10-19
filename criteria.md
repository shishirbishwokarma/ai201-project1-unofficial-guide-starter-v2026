# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
I want the program to fetch the chunk with the right answer, so I can compare what the response looks like when it has the right answer vs. no answer. I picked 4 of 5 and not 5 of 5 because three of my questions have a lookalike document (add/drop vs. withdrawal deadline, library hours vs. library holds, and two different documents about campus jobs), so I expect retrieval to grab the wrong one at least once.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
I want every answer to name its source so I can go to that document and check that it's the correct one; if the source is wrong, I know I need to change the code logic. It's 5 of 5 and not 4 of 5 because every chunk already carries its source filename, so the model always has a source to name. If even one answer leaves it out, the prompt isn't doing its job.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
I don't want the system to make up an answer when my documents don't have the information. I picked 4 of 5 and not 5 of 5 because four of my out-of-scope questions (Mongolia, diesel engines, the World Cup, Rust) have nothing close in a campus-life corpus, but the ibuprofen question is near health_center.txt and might slip past the cutoff.
---

## 4. My chunks are the right size

Each document becomes exactly one chunk. Running python app.py index produces 88 chunks for the 88 documents, and every chunk is between 150 and 600 characters.



**Why this target:**

Every document in campus_life is between 183 and 554 characters and holds one self-contained review. A chunk is too big if it would merge two reviews, and too small if it splits one so the title line ends up apart from its facts. If the chunk count goes above 88, something got split. If any chunk is under 150 characters, it's probably a title with no content under it.



---

## 5. The answer states the right fact


For at least 4 of my 5 test questions, the generated answer contains the correct value from expects in questions.py ("six", "three", "2am", "20", "40").



**Why this target:**

Criterion 1 checks that the right chunk was retrieved, and criterion 2 checks that a source is named. Neither catches the model reading the right chunk and still giving the wrong number. I care about this because the facts here are short numbers sitting next to other numbers. The add/drop document has both "week two" and "week six." I chose 4 of 5 rather than 5 of 5 because a correct answer might be worded differently from my expects string, such as "40 minutes" vs. "every forty minutes."

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
