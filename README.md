# HackTheSnack
A web platform to find and recreate the full recipes behind any supermarket product. Built for food hacking and ingredient exploration. 

Group Members: Katja Greiffenhagen, Jana Danner, Emilio Ribelles and Danilo Monge.


## Getting Started

### Prerequisites
Before you get started, ensure you have the following installed: 
- the latest version of [Git](https://git-scm.com/downloads)
- an IDE, such as [VS Code](https://code.visualstudio.com/), with the necessary Python extension installed
- [Miniconda3](https://www.anaconda.com/docs/getting-started/miniconda/install) (during installation , select "Add Miniconda3 to my PATH environment  variable" in the *Advanced Installation Options* window)

### Set up

1. Open Anaconda Prompt and initialize Conda by running: **conda init --all** 
2. Clone this repository into your IDE 
3. In your Command Line run the following command to create the necessary environment:  **conda env create -f environment.yaml**
4. Once the packages have finished downloading, activate the environment by running:  **conda activate mainEnv**

## Secrets and GitHub Pages

GitHub Pages can host only static files. That means your browser receives the full built app, so any API key injected into the web build would become visible to users. GitHub Secrets do not stay secret if they are baked into frontend code.

To keep `USDA_API_KEY` and `DEEPL_API_KEY` safe:

1. Deploy the Flet web app on GitHub Pages as usual.
2. Deploy the proxy API in `hts_lib/backend/nutrition_proxy_api.py` on a backend host such as Render, Railway, Fly.io, or a VPS.
3. Set `USDA_API_KEY` and `DEEPL_API_KEY` only on that backend host.
4. Set `ALLOWED_ORIGINS` on the proxy to your GitHub Pages origin, for example `https://<your-user>.github.io`.
5. In GitHub, add a repository variable called `NUTRITION_PROXY_URL` with the public URL of that proxy, for example `https://hackthesnack-proxy.onrender.com`.

The GitHub Actions deploy workflow writes that public URL into `hts_lib/assets/runtime-config.json` during build. That URL is public and safe to expose. The API keys remain only on the proxy server.

### Run the proxy locally

```bash
uvicorn hts_lib.backend.nutrition_proxy_api:app --reload
```

Then point `hts_lib/assets/runtime-config.json` to `http://127.0.0.1:8000` while testing the web build locally.

## Full setup checklist

### 1. Create the API keys

You need:

- `USDA_API_KEY`
- `DEEPL_API_KEY`

Do not put these into frontend code, `runtime-config.json`, or GitHub Pages files.

### 2. Deploy the proxy backend

This repo now includes:

- `hts_lib/backend/nutrition_proxy_api.py`
- `requirements-proxy.txt`
- `render.yaml`

#### Option A: Render

1. Push this repo to GitHub.
2. Open Render and create a new Blueprint or Web Service from the repo.
3. If Render detects `render.yaml`, accept it.
4. Add these environment variables in Render:
   - `USDA_API_KEY=...`
   - `DEEPL_API_KEY=...`
   - `ALLOWED_ORIGINS=https://<your-github-user>.github.io`
5. Deploy.
6. Copy the public URL Render gives you, for example:
   - `https://hackthesnack-nutrition-proxy.onrender.com`

#### Option B: Manual Python host

If you deploy on Railway, Fly.io, a VPS, or similar, use:

```bash
pip install -r requirements-proxy.txt
uvicorn hts_lib.backend.nutrition_proxy_api:app --host 0.0.0.0 --port 8000
```

Set the same environment variables there:

- `USDA_API_KEY`
- `DEEPL_API_KEY`
- `ALLOWED_ORIGINS=https://<your-github-user>.github.io`

### 3. Test the proxy before wiring the frontend

Open these URLs after deploy:

- `https://your-proxy-url/health`
- `https://your-proxy-url/api/nutrition?ingredient=sugar`

And test translation with:

```bash
curl -X POST https://your-proxy-url/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Zucker","source_lang":"DE","target_lang":"EN"}'
```

If that works, the secrets are correctly staying server-side.

### 4. Configure GitHub Pages to use the proxy

In GitHub:

1. Go to `Settings` -> `Pages`.
2. Ensure Pages is enabled and uses GitHub Actions as the source.
3. Go to `Settings` -> `Secrets and variables` -> `Actions` -> `Variables`.
4. Create this repository variable:
   - `NUTRITION_PROXY_URL=https://your-proxy-url`

Important:

- This is a variable, not a secret.
- The proxy URL is public and safe to expose.
- Do not store `USDA_API_KEY` or `DEEPL_API_KEY` in GitHub Pages variables for frontend use.

### 5. Keep secrets out of GitHub Pages

If you already created these in GitHub Secrets for the Pages build:

- `USDA_API_KEY`
- `DEEPL_API_KEY`

remove them from the Pages/frontend workflow path. They do not protect the keys in a static site. The keys should live only in the proxy host.

### 6. Redeploy the site

After `NUTRITION_PROXY_URL` is set:

1. Push to `main`, or
2. Open `Actions` in GitHub and manually rerun the Pages workflow.

The workflow writes the proxy URL into the generated `hts_lib/assets/runtime-config.json` during build.

### 7. Confirm in production

After GitHub Pages redeploys:

1. Open your Pages site.
2. Trigger the nutrition lookup in the UI.
3. Confirm it returns real data.
4. Open browser DevTools and verify requests go to your proxy domain, not directly to USDA or DeepL with your keys.

### 8. Security notes

- Users will see the proxy URL, which is fine.
- Users must never see `USDA_API_KEY` or `DEEPL_API_KEY`.
- Restrict `ALLOWED_ORIGINS` to your real GitHub Pages origin whenever possible.
- If you ever think a key was exposed, rotate it immediately in USDA or DeepL.
