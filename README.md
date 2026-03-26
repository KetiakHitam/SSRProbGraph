# Umamusume SSR Gacha Probability Graph

Visualized probability of obtaining SSR in Umamusume, rates and probability taken from the Kitasan Black Probability Spreadsheet by u/xSacrificer on reddit.

## What This Shows

Five probability curves plotting your chance of reaching each Limit Break stage as a function of total pulls, with the rate-up at **0.75%**.

| Line          | Meaning                        |
| ------------- | ------------------------------ |
| **0LB**       | At least 1 copy                |
| **1LB**       | At least 2 copies              |
| **2LB**       | At least 3 copies              |
| **3LB**       | At least 4 copies              |
| **4LB / MLB** | All 5 copies (Max Limit Break) |

Sparking is guaranteed at 200, 400, and 600 pulls are annotated on the graph and cause visible probability jumps.

## How to Regenerate

Requires Python 3 with `pandas`, `openpyxl`, and `plotly`.

```bash
python ssr_prob_graph.py
```

This reads the Excel spreadsheet and outputs `index.html`, which opens automatically in your browser.

## Data Source

Probability data is sourced from the included Excel spreadsheet (`Umamusume_ Kitasan Black Gacha Probabilities.xlsx`), which contains pre-calculated cumulative probabilities for each pull count (10 to 1000) across all LB stages, including spark adjustments.

The same rates apply to all SSR rate-up cards, not just Kitasan Black. Character probabilities might differ since cards share a rate up as they run 2 in 1 banners however characters are always run in 1s.
