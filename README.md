# 🎬 CartoonStream Stremio Addon

All-in-one Stremio addon for **PirateXPlay**, **ToonStream** and **Animelok** — Cartoons & Anime in Hindi/English, with streams routed through MediaFlow Proxy.

## 📺 Sources
- 🏴 **PirateXPlay** — Cartoons & Anime
- 📺 **ToonStream** — Cartoons & Anime
- 🎌 **Animelok** — Anime (Sub & Dubbed)

## 🚀 Deploy on Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set environment variables:

| Variable | Value |
|---|---|
| `MEDIAFLOW_URL` | `https://devonwhite1020-media-proxy.hf.space` |
| `MEDIAFLOW_PASSWORD` | your HF space API_PASSWORD |
| `TMDB_API_KEY` | optional, from themoviedb.org |

5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn -c gunicorn_config.py run:app`

## 🔧 Local Setup

```bash
git clone <your-repo>
cd cartoon-stremio-addon
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
python run.py
```

Then open: `http://localhost:5000`

## 📋 Install in Stremio

1. Open your deployed URL
2. Click **Install in Stremio**
3. Done!
