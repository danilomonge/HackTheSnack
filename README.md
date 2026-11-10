# HackTheSnack

**Recreate your favourite supermarket products at home.** Enter a product's ingredient list, in label order, plus the percentages printed on the package. HackTheSnack estimates the missing percentages, shows nutrition facts per ingredient, and lets you save and compare recipes.

**Live app:** https://danilomonge.github.io/HackTheSnack/

Team project at the University of Tübingen by Katja Greiffenhagen, Jana Danner, Emilio Ribelles and Danilo Monge.

---

## Features

| Page | What it does |
|---|---|
| **Recipe Generator** | Enter ingredients from most to least used. Fill in the percentages you know and leave the others empty. *Submit Product* estimates the unknown shares (mean ± variation) and draws a pie chart. The 🔍 icon shows USDA nutrition facts; German names are translated with DeepL. *Save* stores the recipe. *Search* loads the ingredients of a saved product. |
| **My Recipes** | Every saved product. Click a card to see its ingredients per 100 g. A version picker appears when the recipe was saved more than once. |
| **Statistics** | How the estimated share of each ingredient changed across saved versions of a product, or how one ingredient is used across all products. |
| **About us** | The team and the project. |

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
   ├─▶ HackTheSnackDB API (Spring Boot on Render) ─▶ PostgreSQL on Supabase
   │      products, ingredients, recipes, saved evaluations
   │      repo: https://github.com/danilomonge/HackTheSnackDB
   │
   └─▶ Nutrition proxy (FastAPI on Render, this repo) ─▶ USDA FoodData Central, DeepL
          keeps the API keys out of the browser
```

The app reads both URLs from [`hts_lib/assets/runtime-config.json`](hts_lib/assets/runtime-config.json):

```json
{
  "user_management_url": "https://fakethesnackdb-api.onrender.com/user-management",
  "nutrition_proxy_url": "https://hackthesnack-nutrition-proxy.onrender.com"
}
```

The Render services are on the free plan and stop after 15 idle minutes. The app pings both when it starts, so they are usually awake by the time you click *Search* or *Save*. If one is still starting, the page shows a progress bar and waits up to about a minute.

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
│   ├── backend/
│   │   ├── recipe_generator.py     # chooses the exact solution or MCMC
│   │   ├── algorithm/              # constraints + slice sampling
│   │   ├── data_base_manager/      # HackTheSnackDB REST client
│   │   ├── nutrition_service.py    # USDA + DeepL calls (shared by app and proxy)
│   │   ├── nutrition_proxy_api.py  # FastAPI proxy deployed on Render
│   │   └── translation.py          # API responses -> UI data
│   └── Secure_env/                 # encrypted API keys for desktop runs (not in the web build)
├── test/                           # pytest suite (no network needed)
├── notebooks/MakerSpace.ipynb      # the algorithm, step by step
├── requirements-dev.txt            # pip setup for development
├── requirements-proxy.txt          # dependencies of the proxy
├── environment.yaml                # conda setup for development
├── render.yaml                     # Render Blueprint for the proxy
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

Nutrition facts on the desktop need `USDA_API_KEY` (free at https://fdc.nal.usda.gov/api-key-signup) and, for translation, `DEEPL_API_KEY`. Either export them, or decrypt `Secure_env/.env.enc` by setting `HTS_ENV_PASSWORD` (ask the team for the password). Alternatively, point `NUTRITION_PROXY_URL` at the deployed proxy.

### Test

```bash
pytest
```

The suite covers the algorithm, input validation, the database client (against an in-memory fake API), the generator page and the statistics page. It needs no network or keys. Two optional live tests run only when `LIVE_USDA_API_KEY` / `LIVE_DEEPL_API_KEY` are set.

---

## Deployment

### Web app → GitHub Pages

[`deploy.yml`](.github/workflows/deploy.yml) runs the tests and `flet build web` on every push and pull request, so a broken web build is caught before merging. On `main` it then publishes the build to the `gh-pages` branch, served at https://danilomonge.github.io/HackTheSnack/.

The Flet 0.28.3 build template lets the Dart package `web` float (`^1.0.0`); `hts_lib/pyproject.toml` pins it to `1.1.1` because newer releases need a newer Dart than Flutter 3.29.2 ships.

Optional repository **variables** (Settings → Secrets and variables → Actions → Variables) override the URLs in `runtime-config.json` at build time:

| Variable | Example |
|---|---|
| `USER_MANAGEMENT_URL` | `https://fakethesnackdb-api.onrender.com/user-management` |
| `NUTRITION_PROXY_URL` | `https://hackthesnack-nutrition-proxy.onrender.com` |

These URLs are public. **Never** put `USDA_API_KEY` or `DEEPL_API_KEY` into the web build: GitHub Pages serves everything to the browser.

### Nutrition proxy → Render

[`render.yaml`](render.yaml) defines the service, `uvicorn hts_lib.backend.nutrition_proxy_api:app`. Set these in the Render dashboard:

| Variable | Value |
|---|---|
| `USDA_API_KEY` | USDA FoodData Central key |
| `DEEPL_API_KEY` | DeepL key (Free keys end in `:fx`; the right endpoint is chosen automatically) |
| `ALLOWED_ORIGINS` | `https://danilomonge.github.io` |

Check it with:

```bash
curl https://hackthesnack-nutrition-proxy.onrender.com/health
curl "https://hackthesnack-nutrition-proxy.onrender.com/api/nutrition?ingredient=sugar"
curl -X POST https://hackthesnack-nutrition-proxy.onrender.com/api/translate \
     -H "Content-Type: application/json" -d '{"text":"Zucker"}'
```

Run it locally with `uvicorn hts_lib.backend.nutrition_proxy_api:app --reload` from the repository root.

### Database → Supabase

The API and its database live in [HackTheSnackDB](https://github.com/danilomonge/HackTheSnackDB). That README covers the Supabase setup, the schema and the API reference.

---

## Security notes

* API keys live only on the proxy (Render) or in your local environment. `Secure_env` is excluded from the web build (`tool.flet.app.exclude`).
* The browser only knows the public URLs of the API and the proxy. The API allows cross-origin calls only from the GitHub Pages origin and localhost.
* If a key may have leaked, rotate it at USDA / DeepL and update it on Render.
