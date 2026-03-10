---
name: People task minimal guidance
overview: "A self-directed learning path to complete the \"people\" task: filter CSV, tag jobs with an LLM (structured output), keep transport-only, then submit to the hub. Guidance only—no solution code."
todos: []
isProject: false
---

# Minimal guidance: People task ([task.md](http://task.md))

You’ll do the implementation; this plan is a **checklist and learning path** so you know what to do and in what order.

---

## 1. Understand the data

- Your CSV is at [Week_1/s01e01/Task/people.csv](Week_1/s01e01/Task/people.csv). It has columns: `name`, `surname`, `gender`, `birthDate`, `birthPlace`, `birthCountry`, `job`.
- **Your job:** Open the file (or load the first 20–30 rows in code) and confirm the exact column names and formats (e.g. is `birthDate` full date or year only? how is city written—e.g. “Grudziądz”?).

---

## 2. Filter step (you implement)

Criteria from the task:

- **Gender:** M  
- **Birth place:** Grudziądz (match the exact string used in the CSV)  
- **Age in 2026:** between 20 and 40 years → derive allowed **birth years** and filter by year.

**Hint:** Compute “year of birth” from `birthDate` and check `2026 - year in [20, 40]` (inclusive as in the task). No LLM needed here—pure logic/code.

---

## 3. Tagging with LLM (core learning goal)

- **Input:** For each filtered person, you only need the **job** text (and a way to link the result back to the person, e.g. index or id).
- **Output:** One or more tags per person from:  
`IT`, `transport`, `edukacja`, `medycyna`, `praca z ludźmi`, `praca z pojazdami`, `praca fizyczna`.
- **Requirement:** Use **Structured Output** (response schema) so the API returns valid JSON you can parse without regex. Pick one provider and read its docs:
  - [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs#supported-schemas)
  - [Anthropic structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
  - [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output?example=recipe)
- **Hint from task:** Use **batch tagging**—send many job descriptions in one request (e.g. numbered list), ask for a list of `{ index, tags }`, and map back to your filtered rows. Reduces API calls.
- **Extra hint:** In the prompt, give a short description of each tag (e.g. “transport – zawody związane z przewozem, logistyką, spedycją”) so the model classifies better.

---

## 4. Select and build answer payload

- Keep only people whose `tags` array **contains** `"transport"`.
- Build the **answer** array exactly as in the task: each item must have `name`, `surname`, `gender`, `born` (integer year), `city`, `tags` (array of strings).  
- **Important:** `city` should be the birth city (e.g. from `birthPlace`); `born` = year only (integer).

---

## 5. Submit to the hub

- **Endpoint:** `POST https://hub.ag3nts.org/verify`
- **Body:** JSON with `apikey`, `task`: `"people"`, and `answer`: the array from step 4.
- Get your API key from [https://hub.ag3nts.org/](https://hub.ag3nts.org/) (e.g. from [Week_1/s01e01/Task/.env](Week_1/s01e01/Task/.env) if you store it there; never commit real keys).

If the answer is correct, the response will contain a flag `{FLG:...}` to enter on the hub page.

---

## Suggested order of work

1. Write a small script to load the CSV and apply the **filter** (gender, city, age). Print the number of rows and a few examples to verify.
2. Add **one** LLM call with Structured Output that returns e.g. `[{ "index": 0, "tags": ["transport"] }, ...]` for a **small batch** of job strings (e.g. 5–10). Parse the JSON and confirm it matches your schema.
3. Scale to **batch tagging** for all filtered jobs (respect rate limits; chunk if needed).
4. **Merge** tags back with filtered rows, keep only `transport`, build the final array and **POST** to the hub.

---

## When you’re stuck

- **CSV parsing:** Use the standard library for your language (e.g. `csv` in Python, `fs` + split or a CSV lib in Node) and handle encoding (UTF-8 for Polish).
- **Structured Output:** If you prefer a library, the task mentions **Instructor** ([Python](https://python.useinstructor.com/), [JS/TS](https://js.useinstructor.com/)); otherwise use the provider’s `response_format` / schema parameter.
- **Exact format:** Re-read the example JSON in [task.md](Week_1/s01e01/Task/task.md) (lines 40–67) and match field names and types exactly (`born` as number, `tags` as array of strings).

If you want, we can next drill into **one** step only (e.g. “only help me with the filter” or “only with the LLM schema”) without giving you full code.