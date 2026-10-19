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

The dashboard uses Observable JavaScript inputs, so the selected synthetic
asset, calibration lookback, volatility, and forecast update directly in the
browser. Python creates the report and presentation at render time; GitHub
Pages serves their generated static files. No live Python server is required
for these controls. By contrast, server-backed Shiny controls would need a
separate hosting service.

The notebook also has its own Python widget controls for experimenting with
the asset, calibration window, and forecast horizon. Run the interactive cell
in VS Code with the selected Jupyter kernel; changing a control redraws its
metrics and charts. The published notebook is a static snapshot because
GitHub Pages does not host a Python kernel; use the browser-side dashboard for
live website interaction. The notebook uses `ipywidgets`, included in
`requirements.txt`.

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
4. Open `notebooks/market_walkthrough.ipynb` and run the interactive cell to
   experiment with its controls. Repeat with `dashboard.qmd` and `slides.qmd`
   to explore the other Quarto formats. The slides have edge arrows and also
   respond to the left/right arrow keys. The rendered notebook has its own HTML theme in
   `notebooks/_metadata.yml`; this affects Quarto's notebook output, not VS
   Code's notebook editor theme. The rendered website entry point is
   `_site/index.html`.

To produce an editable PowerPoint instead of the browser-based Reveal.js
presentation, use Quarto's PowerPoint output:

```powershell
quarto render slides.qmd --to pptx
```

## Publish on GitHub Pages

The publishing sequence is:

1. Create the repository on GitHub, then connect the local project and push
   its source files to `main`.
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions**
   as the source. The first deployment will not work until Pages is enabled
   for the repository.
3. Push to `main` (or manually start **Publish Quarto site** from the Actions
   tab). GitHub Actions renders and deploys the site.
4. Open the published URL shown on the successful workflow run or under
   **Settings → Pages**.

That is what happened here: the initial Pages action could not deploy because
Pages had not yet been configured. Selecting **GitHub Actions** in Pages
settings and rerunning the workflow resolved it. After that, a push to `main`
automatically rebuilt the site.

### What the two workflow files do

[`pages.yml`](.github/workflows/pages.yml) builds and publishes the website:

1. It starts on pushes to `main`; `workflow_dispatch` also allows a manual
   run from GitHub's Actions tab.
2. It starts a temporary Ubuntu runner, checks out the repository, installs
   Python 3.11 and `requirements-dev.txt`, then installs Quarto.
3. `nbdev-export` generates the Python module from `nbs/market_demo.ipynb`.
   The Quarto render step then executes the documents and notebooks, writing
   the rendered site into `_site/`.
4. The Pages steps configure deployment, upload `_site/` as a Pages artifact,
   and publish that artifact. The `github-pages` environment records the
   resulting site URL. Required `permissions` authorize the upload and
   deployment; `concurrency` prevents an older queued deployment from
   replacing a newer one.

[`tests.yml`](.github/workflows/tests.yml) is separate from publishing. It
runs `nbdev-export`, executes the literate notebook tests with `nbdev-test`,
and runs the Python unit tests on every push and pull request. A test failure
marks that run as failed; it does not upload or deploy a website.

The notebook is source code too: the Pages runner installs its Python
dependencies, Quarto executes its cells with Jupyter, and the resulting HTML
is included in `_site/`. `ipywidgets` lets the notebook recalculate when you
run it with a Python kernel in VS Code. GitHub Pages serves static files and
does not keep that kernel running, so the published notebook shows its saved
state rather than running Python callbacks. The dashboard's Observable
JavaScript controls do work on Pages because they run in the browser.

### Repository, build, and site are different things

- The GitHub repository stores the source: `.qmd` documents, the `.ipynb`
  notebook, Python code, styles, and workflow definitions.
- `_site/` is generated output and is ignored by Git. The Actions runner
  creates it for each deployment, uploads it as an artifact, and publishes
  that artifact; it does not commit the rendered site back into the source
  branch.
- The Pages URL is a separate public website. If an Enterprise organization
  permits a public Pages site from a private repository, the source can remain
  private, but everything rendered into the public site is visible to the
  public. Check the organization's Pages policy and never render secrets or
  private data into it.

This demo's GitHub Pages site is:
https://agnesprovost.github.io/dummyProjectFroPublishingNotebooks/

### What Quarto does and does not automate

Quarto renders the report, notebook, dashboard, and slides, and the site
navbar in `_quarto.yml` links those pages. It does not infer all navigation
from figures, code cells, or widgets. Those need authored headings, anchors,
captions, links, or a table of contents.

The current dashboard and slide styles are a compact starting point, not
automatic Quarto styling. The Observable controls, chart sizing, slide colors,
and slide arrows are configured in the documents and the small files under
`styles/`. Remaining improvements, if we want to keep polishing this demo:

- Add clearer in-page navigation to longer reports and the notebook, such as
  a table of contents and links to important figures or interactive controls.
- Refine the CSS/SCSS only where the current responsive dashboard and slide
  theme still need visual polish.
- Decide whether the static notebook snapshot is enough, or whether a
  separately hosted Python service is worth the cost and complexity for
  interactive notebook output on the public site.

The first two items are presentation choices, not blockers for GitHub Pages.
The site already builds and deploys; the most important setup lessons were
creating/pushing the repository and enabling GitHub Pages with **GitHub
Actions**.

The notebook in `nbs/` is the editable source for the Python module; use
`nbdev-export` rather than editing the generated module directly. The existing
Quarto analysis and dashboard continue to reuse that module as separate
presentation formats.

## Where to edit the presentation

- `_quarto.yml` controls the site-wide navigation and default HTML theme.
- In `dashboard.qmd`, the `##` headings create dashboard rows; their
  `{height=...}` values divide the available page height. The nearby
  `Plot.plot({ height: ... })` values size each chart inside its row.
- `styles/dashboard.css` makes each chart fill its card without overflowing.
  It is a small layout fix, not a requirement for every Quarto dashboard.
- `slides.qmd` contains the slide content and navigation settings;
  `styles/slides.scss` sets the slide colors and typography.
- `notebooks/market_walkthrough.ipynb` contains the Python widget controls.
  Run the notebook top-to-bottom in VS Code, then change the widgets to
  recalculate the displayed values and plots.

Quarto supplies the rendering and output formats. The dashboard's browser
controls are Observable JavaScript, while its page layout and the slide theme
use a small amount of CSS/SCSS. Start with the headings and values above;
you can ignore the styling files until you want to change the appearance.
