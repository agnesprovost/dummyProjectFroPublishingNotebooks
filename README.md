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
├── src/market_demo.py            # Reusable data and model functions
├── tests/test_market_demo.py     # Small deterministic tests
├── notebooks/market_walkthrough.ipynb
├── index.qmd                     # Website landing page
├── analysis.qmd                  # Reproducible narrative report
├── dashboard.qmd                 # Quarto dashboard
├── slides.qmd                    # Reveal.js presentation
├── _quarto.yml                   # Website, navigation, and execution settings
└── requirements.txt
```

## Run locally

Install Python dependencies and [Quarto](https://quarto.org/docs/get-started/).
From the project root:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
quarto render
```

The website is written to `_site/`. Open `_site/index.html` to browse the
rendered report, dashboard, slides, and executed notebook. Render individual
deliverables with `quarto render notebooks/market_walkthrough.ipynb --execute`,
`quarto render dashboard.qmd`, or `quarto render slides.qmd`.

## Work in VS Code

1. Install the [Quarto VS Code extension](https://marketplace.visualstudio.com/items?itemName=quarto.quarto).
   The extension provides Quarto editing and preview commands; install the
   [Quarto CLI](https://quarto.org/docs/get-started/) separately as well.
2. Open this project folder in VS Code and select your Anaconda Python
   interpreter. The `requirements.txt` dependencies, including Jupyter, must
   be installed in that same environment.
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

The Python module is deliberately kept separate from the Quarto documents.
That makes it easy to reuse the same analysis in another notebook/reporting
tool later, without copying the calculations.
