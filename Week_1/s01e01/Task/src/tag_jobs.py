"""
Step 2: Tag job descriptions with an LLM using LiteLLM + Instructor (structured output).
Assigns tags from the task list; uses cache if output/tagged_people.json exists.
"""
import asyncio
import json
from pathlib import Path
from typing import Literal

import instructor
from litellm import acompletion
from pydantic import BaseModel

OUTPUT_DIR = Path(__file__).parent.parent / "output"

Tag = Literal[
    "IT",
    "transport",
    "edukacja",
    "medycyna",
    "praca z ludźmi",
    "praca z pojazdami",
    "praca fizyczna",
]

TAG_DESCRIPTIONS = """
- IT: informatyka, oprogramowanie, bazy danych, systemy
- transport: przewóz, logistyka, spedycja, dostawy
- edukacja: nauczanie, szkolenia, przekazywanie wiedzy
- medycyna: zdrowie, leczenie, diagnoza, pielęgnacja
- praca z ludźmi: obsługa klienta, opieka, praca w zespole
- praca z pojazdami: kierowanie, naprawa, obsługa pojazdów/maszyn
- praca fizyczna: praca ręczna, budowa, montaż, produkcja
"""

BATCH_SIZE = 25

# --- Prompt template: instruction + tag reference + job list ---
PROMPT_INSTRUCTION = """
Przypisz każdemu opisowi stanowiska tagi z poniższej listy. Możesz wybrać wiele tagów dla jednego opisu.

Dostępne tagi (z krótkim opisem):
{TAG_DESCRIPTIONS}

Opisy stanowisk (numer to indeks 0-based – zwróć go w polu index):
"""


class TaggingItem(BaseModel):
    index: int
    tags: list[Tag]


class BatchTaggingResponse(BaseModel):
    items: list[TaggingItem]


def _format_job_list(chunk: list[tuple[int, str]]) -> str:
    """Format numbered job descriptions for the prompt."""
    return "\n\n".join(
        f"[{idx}] {job}" for idx, job in chunk
    )


def _build_prompt(chunk: list[tuple[int, str]]) -> str:
    instruction = PROMPT_INSTRUCTION.format(TAG_DESCRIPTIONS=TAG_DESCRIPTIONS.strip())
    job_list = _format_job_list(chunk)
    return f"{instruction}\n{job_list}"


def _chunk_jobs(people: list[dict], batch_size: int):
    """Yield batches of (index, job_text) for LLM calls."""
    for start in range(0, len(people), batch_size):
        end = min(start + batch_size, len(people))
        yield [(i, people[i].get("job", "")) for i in range(start, end)]


async def _tag_chunk(client, chunk: list[tuple[int, str]]) -> dict[int, list[str]]:
    """Call LLM for one chunk; return mapping index -> list of tags."""
    prompt = _build_prompt(chunk)
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=BatchTaggingResponse,
        messages=[{"role": "user", "content": prompt}],
        max_retries=2,
    )
    return {item.index: item.tags for item in response.items}


async def _fetch_all_tags(client, filtered: list[dict]) -> dict[int, list[str]]:
    """Run LLM for each chunk; merge and return index -> tags."""
    index_to_tags: dict[int, list[str]] = {}
    for chunk in _chunk_jobs(filtered, BATCH_SIZE):
        index_to_tags.update(await _tag_chunk(client, chunk))
    return index_to_tags


def step_tag_jobs(output_dir: Path, filtered: list[dict] | None = None) -> list[dict]:
    """Tag each person's job with LLM; use cache if tagged_people.json exists."""
    if filtered is None:
        with open(output_dir / "filtered_people.json", encoding="utf-8") as f:
            filtered = json.load(f)

    cache_path = output_dir / "tagged_people.json"
    if cache_path.exists():
        with open(cache_path, encoding="utf-8") as f:
            tagged = json.load(f)
        print(f"  Using cached tags: {len(tagged)} persons ← {cache_path}")
        return tagged

    client = instructor.from_litellm(acompletion)
    index_to_tags = asyncio.run(_fetch_all_tags(client, filtered))

    # Build answer-shaped records only (no "job"); same format as final submit
    answer_fields = ("name", "surname", "gender", "born", "city")
    tagged = []
    for i, person in enumerate(filtered):
        tags = index_to_tags.get(i, [])
        tagged.append({
            **{k: person[k] for k in answer_fields},
            "tags": tags,
        })

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(tagged, f, ensure_ascii=False, indent=2)
    print(f"  Tagged: {len(tagged)} persons → {cache_path}")
    return tagged


if __name__ == "__main__":
    step_tag_jobs(OUTPUT_DIR)
