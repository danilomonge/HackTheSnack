# HackTheSnack

**Recreate your favourite supermarket products at home.** Enter a product's ingredient list, in label order, plus the percentages printed on the package. HackTheSnack estimates the missing percentages, shows nutrition facts per ingredient, and lets you save and compare recipes.

**Live app:** https://danilomonge.github.io/HackTheSnack/

Team project at the University of Tübingen by Katja Greiffenhagen, Jana Danner, Emilio Ribelles and Danilo Monge.

---

## Features

| Page | What it does |
|---|---|
| **Recipe Generator** | Enter ingredients from most to least used. Fill in the percentages you know and leave the others empty. *Submit Product* estimates the unknown shares (mean ± variation) and draws a pie chart. The 🔍 icon shows USDA nutrition facts; German names are translated with Azure AI Translator. *Save* stores the recipe. *Search* loads the ingredients of a saved product. |
| **My Recipes** | Every saved product. Click a card to see its ingredients per 100 g. A version picker appears when the recipe was saved more than once. |
| **Statistics** | How the estimated share of each ingredient changed across saved versions of a product, or how one ingredient is used across all products. |
| **About us** | The team and the project. |

The layout adapts to phones (below 640 px the navigation wraps, ingredient rows stack name / percentage, and dialogs fill the screen).

### How the estimation works

Food labels in the EU list ingredients in descending order of weight, and only some percentages are printed. The unknown shares therefore satisfy linear constraints:

* every share is > 0 and the shares sum to 100 %,
* each ingredient is at least as large as the next one,
* the printed percentages are fixed.

`backend/algorithm` samples uniformly from that polytope with **slice sampling**, a Markov chain Monte Carlo method. A linear program finds the starting point (SciPy's `linprog` on the desktop; in the browser, where SciPy is not available, an equivalent NumPy barrier method); random directions are restricted to the null space of the equality constraints. The mean of the samples is the estimate and twice the standard deviation is the "variation". Simple cases, like a single unknown or all values given, are solved exactly without sampling (`backend/algorithm_skipper.py`). The derivation is in [`notebooks/MakerSpace.ipynb`](notebooks/MakerSpace.ipynb).

---

## Architecture

```
GitHub Pages ─ static Flet web app (Python running in the browser via Pyodide)
   │
   └─▶ HackTheSnackDB API (Spring Boot on Render) ─▶ PostgreSQL on Supabase
          products, ingredients, recipes, saved evaluations
          + nutrition facts / translation ─▶ USDA FoodData Central, Azure AI Translator
            (the API keys stay on the server, never in the browser)
          repo: https://github.com/danilomonge/HackTheSnackDB
```

The app reads its backend URLs from [`hts_lib/assets/runtime-config.json`](hts_lib/assets/runtime-config.json). Both point at the API, which also serves `/api/nutrition` and `/api/translate`:

```json
{
  "user_management_url": "https://fakethesnackdb-api.onrender.com/user-management",
  "nutrition_proxy_url": "https://fakethesnackdb-api.onrender.com/user-management"
}
```

The API runs on Render's free plan, which stops a service after 15 idle minutes. The API keeps itself awake around the clock (it is the workspace's only free service, so this fits the free instance hours), so *Search*, *Save* and nutrition lookups answer immediately. If it ever has to start again (e.g. right after a deploy), the app pings it as soon as the page loads and shows a progress bar while it waits.

### Repository layout

```
HackTheSnack/
├── hts_lib/                        # the Flet application (build root)
│   ├── main.py                     # entry point and routing
│   ├── pyproject.toml              # app metadata + `flet build web` settings
│   ├── assets/                     # images, icon, runtime-config.json
│   ├── frontend/src/
│   │   ├── views/                  # Home, My Recipes, Statistics, About pages
│   │   ├── add_product_table/      # Recipe Generator input table (UI + validation)
│   │   ├── create_result_table/    # generated recipe table + pie chart
│   │   ├── product_action_handler.py   # Search / autofill / Save
│   │   ├── product_submit_handler.py   # Submit -> recipe generation
│   │   ├── handle_nutritional_info.py  # nutrition dialog
│   │   ├── navbar.py, styles.py
│   └── backend/
│       ├── recipe_generator.py     # chooses the exact solution or MCMC
│       ├── algorithm/              # constraints + slice sampling
│       ├── data_base_manager/      # HackTheSnackDB REST client
│       ├── nutrition_service.py    # USDA + Azure Translator calls for desktop runs (the web uses the API)
│       └── translation.py          # API responses -> UI data
├── test/                           # pytest suite (no network needed)
├── notebooks/MakerSpace.ipynb      # the algorithm, step by step
├── requirements-dev.txt            # pip setup for development
├── environment.yaml                # conda setup for development
└── .github/workflows/deploy.yml    # tests + GitHub Pages deployment
```

---

## Getting started

### Prerequisites

* Python **3.11+**
* [Git](https://git-scm.com/downloads)
* Optional: [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) if you prefer conda

### Install

```bash
git clone https://github.com/danilomonge/HackTheSnack.git
cd HackTheSnack

# pip
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# or conda
conda env create -f environment.yaml && conda activate mainEnv
```

### Run

```bash
cd hts_lib
python main.py                  # desktop window
flet run --web main.py          # in the browser (http://localhost:8550)
```

By default the app talks to the **production API** configured in `runtime-config.json`. To use a local HackTheSnackDB instead (see that repository's README):

```bash
USER_MANAGEMENT_BASE_URL=http://localhost:8087/user-management python main.py
```

Nutrition facts on the desktop need `USDA_API_KEY` (free at https://fdc.nal.usda.gov/api-key-signup) and, for translation, `AZURE_TRANSLATOR_KEY` (free F0 tier of [Azure AI Translator](https://azure.microsoft.com/pricing/details/translator/), 2 M characters / month) plus `AZURE_TRANSLATOR_REGION` if the resource is regional. Export them in your shell; keys are never committed to this repository.

### Test

```bash
pytest
```

The suite covers the algorithm, input validation, the database client (against an in-memory fake API), the generator page and the statistics page. It needs no network or keys. Two optional live tests run only when `LIVE_USDA_API_KEY` / `LIVE_AZURE_TRANSLATOR_KEY` (+ `LIVE_AZURE_TRANSLATOR_REGION`) are set.

---

## Deployment

### Web app → GitHub Pages

[`deploy.yml`](.github/workflows/deploy.yml) runs the tests and `flet build web` on every push and pull request, so a broken web build is caught before merging. On `main` it then publishes the build to the `gh-pages` branch, served at https://danilomonge.github.io/HackTheSnack/.

The Flet 0.28.3 build template lets the Dart package `web` float (`^1.0.0`); `hts_lib/pyproject.toml` pins it to `1.1.1` because newer releases need a newer Dart than Flutter 3.29.2 ships.

Optional repository **variables** (Settings → Secrets and variables → Actions → Variables) override the URLs in `runtime-config.json` at build time:

| Variable | Example |
|---|---|
| `USER_MANAGEMENT_URL` | `https://fakethesnackdb-api.onrender.com/user-management` |
| `NUTRITION_PROXY_URL` | `https://fakethesnackdb-api.onrender.com/user-management` (base URL serving `/api/nutrition`, `/api/translate`) |

These URLs are public. **Never** put `USDA_API_KEY` or `AZURE_TRANSLATOR_KEY` into the web build: GitHub Pages serves everything to the browser.

### Database → Supabase

The API and its database live in [HackTheSnackDB](https://github.com/danilomonge/HackTheSnackDB). That README covers the Supabase setup, the schema, the API reference (including the nutrition endpoints) and the Render configuration (`USDA_API_KEY`, `AZURE_TRANSLATOR_KEY`, `AZURE_TRANSLATOR_REGION`).

---

## Security notes

* API keys live only on the API's Render service or in your local environment; none are stored in this repository.
* The browser only knows the public URL of the API, which allows cross-origin calls only from the GitHub Pages origin and localhost.
* If a key may have leaked, rotate it at USDA / Azure and update it on Render.
