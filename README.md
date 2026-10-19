# A tiny quantitative-finance project with Quarto

This project follows one small, reproducible example from data generation to a
report, a dashboard, and a slide deck. It uses a synthetic price series, so it
needs no data download or API key.

## The analysis

1. Generate a seeded five-year daily price series using a geometric Brownian
   motion (GBM).
2. Calculate daily log returns and inspect their distribution.
3. Estimate annualized GBM drift and volatility from those returns.
4. Simulate paths using the estimated parameters and compare them with the
   synthetic history.

The numbers are deliberately illustrative, not a forecast or investment
recommendation.

## Project layout

```text
.
├── .github/workflows/
│   ├── pages.yml                 # Render and publish the Quarto website
│   └── tests.yml                 # Run the Python unit tests
├── src/
│   ├── market_demo.py            # NBDev-exported reusable functions
│   ├── __init__.py               # Exported library version
│   └── _modidx.py                # Generated notebook-to-symbol index
├── tests/test_market_demo.py     # Small deterministic tests
├── nbs/market_demo.ipynb         # NBDev source for the Python module
├── notebooks/market_walkthrough.ipynb
├── index.qmd                     # Website landing page
├── analysis.qmd                  # Reproducible narrative report
├── dashboard.qmd                 # Quarto dashboard
├── slides.qmd                    # Reveal.js presentation
├── _quarto.yml                   # Website, navigation, and execution settings
├── pyproject.toml                # NBDev export and notebook settings
├── requirements.txt
└── requirements-dev.txt          # Development and notebook tooling
```

## Run locally

Install Python dependencies and [Quarto](https://quarto.org/docs/get-started/).
From the project root:

```powershell
python -m pip install -r requirements-dev.txt
nbdev-export
nbdev-test
python -m unittest discover -s tests -v
quarto render --no-clean
```

The website is written to `_site/`. Open `_site/index.html` to browse the
rendered report, dashboard, slides, and notebooks. `nbs/market_demo.ipynb` is
the literate source for `src/market_demo.py`: mark exported code cells with
`#| export`, then run `nbdev-export` after editing the notebook. The same
notebook is tested by `nbdev-test` and rendered by Quarto as the **Literate
module** website page. Render individual deliverables with
`quarto render nbs/market_demo.ipynb`,
`quarto render notebooks/market_walkthrough.ipynb --execute`,
`quarto render dashboard.qmd`, or `quarto render slides.qmd`.
The `--no-clean` flag avoids an output-rename error when rerendering the
existing notebook on Windows; it preserves any old files in `_site/`.

## Work in VS Code

1. Install the [Quarto VS Code extension](https://marketplace.visualstudio.com/items?itemName=quarto.quarto).
   The extension provides Quarto editing and preview commands; install the
   [Quarto CLI](https://quarto.org/docs/get-started/) separately as well.
2. Open this project folder in VS Code and select your Anaconda Python
   interpreter. Install `requirements-dev.txt` in that same environment so
   Quarto, Jupyter, and NBDev are available together.
3. Open `analysis.qmd` and use its **Render** button, or open the Command
   Palette and run **Quarto: Preview**. Edit a sentence or parameter, save,
   and preview again to see the report update.
4. Repeat with `dashboard.qmd` and `slides.qmd` to explore the other Quarto
   formats. The rendered website entry point is `_site/index.html`.

To produce an editable PowerPoint instead of the browser-based Reveal.js
presentation, use Quarto's PowerPoint output:

```powershell
quarto render slides.qmd --to pptx
```

## Publish on GitHub Pages

1. Create a GitHub repository and push this project to its `main` branch.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions**.
3. The workflow in `.github/workflows/pages.yml` renders the site and deploys
   `_site/` on each push to `main`.

The notebook in `nbs/` is the editable source for the Python module; use
`nbdev-export` rather than editing the generated module directly. The existing
Quarto analysis and dashboard continue to reuse that module as separate
presentation formats.
