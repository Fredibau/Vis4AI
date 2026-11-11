# AI Interaction Record

## Log
| Date | Prompt (important ones) | AI suggestion | Accepted / modified / rejected – why | Effect on analysis |
|---|---|---|---|---|
| **9 Nov** | *I'm analysing intent classification across 52 languages. 6 intents fail across all languages, including English. Let's collaborate to investigate whether this is a language issue or a model architecture limitation.* | Confirmed 3 intents hit 0.00 median accuracy while 3 others vary (0.09–0.23). Challenged our initial framing: universal failure points to a language-invariant task bug rather than translation quality. | **Modified.** Accepted the analytical reframing, but rejected proposed model retraining experiments to keep the work strictly black-box on existing predictions. | Ensuring the analysis focuses on the correct aspects. | 
| **9 Nov** | *Here is our heatmap code and observations: (a) some intents fail universally, (b) others vary by language, (c) weak languages form a separate group. Can you test these claims and suggest next exploratory steps?* | Confirmed (a) and (b); refuted (c), showing weak languages form a continuous tail (max gap 0.06). Proposed ranking languages using only the 13 English-solvable intents ($Acc_{EN} \ge 0.5$). | **Modified.** Accepted the 13-intent filter, but changed the sorting logic in the Plotly heatmap to sort rows dynamically by mean accuracy rather than alphabetical locale names. | Prevented false categorisation of languages into arbitrary tiers and created a much clearer visual gradient across languages. | 
| **10 Nov** | *We want to plot accuracy per language on English-solvable intents with 95% confidence intervals. Write the Plotly code and check if Japanese significantly outperforms European languages.* | Provided dot-plot code using $N\_GROUP = 13$ default. Suggested running unpaired t-tests between Japanese and top Latin languages. | **Rejected** the unpaired t-test suggestion and **modified** code parameter defaults by changing $N\_GROUP$ from 13 to 10 after testing cutoff sensitivity. | Replaced unpaired t-tests with a **paired sign test on identical utterances** ($p = 0.0052$), proving `ja-JP`'s superiority far more rigorously while exposing threshold sensitivity. | 
| **10 Nov** | *We noticed Latin-script languages dominate the top ranks. Can you generate script/family metadata for all 52 locales and write code to test if script type drives accuracy?* | Generated metadata mapping table and a Plotly strip plot grouped by script and colored by family. Claimed script type is the primary explanatory driver. | **Modified.** Integrated the strip plot code into our master notebook, but **rejected the AI's causal explanation**, adding explicit sanity checks on base rates for Latin script (28/51 languages). | Highlighted script bias as a secondary correlation rather than root cause, emphasising counter-examples like `cy-GB` (0.24) and `ja-JP` (0.75). | 
| **10 Nov** | *Where do model predictions go when it fails on English-solvable intents? Compare error destinations for the 10 weakest vs 10 strongest languages.* | Provided grouped horizontal bar chart code. Identified `qa_factoid` as the dominant error sink (62% of errors in weak languages, 51% in strong ones). | **Modified.** Adapted the AI's script to filter out true predictions entirely so the chart strictly isolates wrong-label destinations rather than overall prediction distribution. | Identified the **"sink label" phenomenon**: weak languages collapse into a few high-frequency fallback intents (`qa_factoid`, `social_post`). | 


## Failure patterns observed

* **Unverified metadata generation:** The AI generated script and language family mappings from memory without listing sources, requiring explicit manual verification flags in the notebook.

* **Flawed statistical recommendations:** The AI initially proposed unpaired t-tests to compare language accuracies, ignoring that the dataset contained identical paired utterances across languages.

* **Default parameter bias:** The AI presented arbitrary cutoffs as standard defaults, which directly influenced statistical significance levels until challenged.

* **Blind text generation:** The AI drafted chart observations from raw numerical summaries rather than rendered visual plots, occasionally missing visual patterns apparent only upon inspection.

* **Code execution dependencies:** Multi-cell snippet suggestions frequently failed on first run due to scope and state assumptions across notebook cells.

## Emerging best practices

* **Human hypothesis first, AI testing second:** Provide human readings of visuals first, using the AI as a sparring partner to validate or refute claims with quantitative checks.

* **Challenge default hyper-parameters:** Explicitly question AI defaults and run sensitivity checks across alternative cutoffs.

* **Enforce paired testing for aligned datasets:** Ensure comparative statistical claims across multilingual parallel corpora utilise paired tests on matching utterance IDs.

* **Separate observation from explanation:** Maintain strict separation between direct data observations in section cells and theoretical explanations in the summary.
