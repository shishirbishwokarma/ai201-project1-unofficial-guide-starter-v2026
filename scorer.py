"""
Decides whether one answer passed. run_eval.py finds this file and calls
`judge` once per question per run.
"""

from store import Result


def judge(question: str, expects: str, answer: str, results: list[Result]) -> bool:
    """
    Return True if this answer counts as correct, False if it doesn't.

    question  the test question, from questions.py
    expects   the word or phrase a correct answer must contain, e.g. "six"
    answer    what the system said; gate.REFUSAL if the gate stopped it
    results   the chunks retrieval returned, nearest first. Each has
              .text, .source, .distance
    """
    return expects.lower() in answer.lower()


if __name__ == "__main__":
    import config
    import questions as qs
    from run_eval import run_once

    items = qs.answered()
    passed = 0
    for item in items:
        answer, results, _ = run_once(
            item["question"], config.TOP_K, config.THRESHOLD, config.CORPUS, "default"
        )
        ok = judge(item["question"], item["expects"], answer, results)
        passed += ok
        print(f"{'pass' if ok else 'FAIL'}  {item['question']}")
    print(f"\n{passed}/{len(items)} passed")
