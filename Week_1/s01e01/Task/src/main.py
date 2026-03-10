"""
Main pipeline for the people task: filter → tag → build answer → submit.
"""
from pathlib import Path

from build_answer import step_build_answer
from filter_people import step_filter_people
from submit import step_submit
from tag_jobs import step_tag_jobs

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def main():
    print("Step 1: Filter people (M, Grudziądz, age 20–40)")
    filtered = step_filter_people(OUTPUT_DIR)

    print("Step 2: Tag jobs with LLM (LiteLLM + Instructor)")
    tagged = step_tag_jobs(OUTPUT_DIR, filtered)

    print("Step 3: Keep only transport, build answer")
    answer = step_build_answer(tagged)

    print("Step 4: POST to hub")
    result = step_submit(answer)
    print("  Response:", result)

    print("Done.")


if __name__ == "__main__":
    main()
