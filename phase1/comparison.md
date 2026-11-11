# Phase I – Pair comparison

Pair A (AI-aided): [notebook](pair_A_ai/phase1_initial_vis.ipynb), [AI record](pair_A_ai/ai_interaction_record.md) · Pair B (human-only): [script](pair_B_human/vis4ai_phase1.py), [notebook](pair_B_human/phase1_vis.ipynb)

## Findings unique to each pair

- **A only:** Three intents (`calendar_query`, `calendar_set`, `email_query`) break down in every language, English included, which points to a task-level issue rather than a language-level one. Accuracy drops steadily from language to language with no obvious weak group; Japanese stands out as clearly the strongest non-English language. Script correlates with accuracy but doesn't account for it. `qa_factoid` acts as a catch-all label that incorrect predictions land in.
- **B only:** Confidence and calibration (A never examined confidence, even though it's central to our main question), consistency of predictions across translations, and specific example utterances (English versus German).
- **Shared:** `calendar_remove` is heavily language-dependent, and `qa_factoid` is a frequent incorrect prediction.

## Visualization approaches

A favored interactive Plotly charts, benchmarked everything against English, and restricted itself to intents that English can handle. B relied on static matplotlib plots, compared languages head-to-head, and drilled down to individual utterances.

## Scope versus detail

The AI mostly expanded A's breadth: roughly nine analyses, several offering fresh perspectives. A's depth came from additional checks the pair introduced on their own (paired tests, threshold sensitivity). B's coverage was narrower because hand-writing each plot was slower, so B pursued one intent (`calendar_remove`) in greater detail instead.

## Pace versus checking

A accomplished much more in roughly two days. Every one of the five interactions in their AI record was altered or partially rejected, and the record documents failures: the AI fabricated script/family data without citations, proposed an inappropriate statistical test, and produced code that failed between cells. B moved more slowly but grasped all of its own code.

## Strength of conclusions

A's assertions rest on statistical support (confidence intervals, sign tests, robustness checks). B's are descriptive and come with caveats: the calibration plot aggregates all languages, and the flip metric flags nearly every utterance as flipped. B's examples give concrete grounding to A's aggregate results.