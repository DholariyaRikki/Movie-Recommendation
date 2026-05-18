# Movie Recommender

A small FastAPI + Streamlit movie recommendation demo using a local TF-IDF index and TMDB for posters/details.

## Features
- Search TMDB for movies and view details
- Local TF‑IDF recommendations (titles) with TMDB poster lookup
- Genre-based recommendations via TMDB discover

## Setup
1. Create a Python environment and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Add a `.env` file with your TMDB API key:

```
TMDB_API_KEY=your_tmdb_api_key_here
```

3. Ensure the pickles exist in the project root:
- `df.pkl`
- `indices.pkl`
- `tfidf_matrix.pkl`
- `tfidf.pkl`

These are generated during dataset preprocessing (not included here).

## Run
Start the FastAPI backend (from project root):

```bash
uvicorn main:app --reload
```

Start the Streamlit frontend (in another terminal):

```bash
streamlit run app.py
```

Open the browser at the address printed by Streamlit (usually http://localhost:8501).

## Notes & Troubleshooting
- If recommendations show empty results: check the logs for TF-IDF load errors and ensure `TMDB_API_KEY` is set.
- The TF-IDF endpoint now attaches TMDB cards for each recommended title; if TMDB lookups fail often consider caching `title -> tmdb_id` mappings.

## Development
- Edit `main.py` for backend changes and `app.py` for UI tweaks.
- Use `requirements.txt` to reproduce the environment.
