import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommendation-ocuk.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# =============================
# MODERN DARK UI
# =============================
st.markdown(
    """
<style>

/* =========================
   GLOBAL
========================= */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #071126 40%,
        #0f172a 100%
    );
    color: white;
}

/* =========================
   CONTAINER FIX
========================= */
.block-container {
    padding-top: 0.6rem !important;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Remove streamlit top spacing */
section.main > div {
    padding-top: 0rem !important;
}

/* Remove white skeleton loading bars */
[data-testid="stSkeleton"] {
    display: none !important;
}

/* =========================
   TEXT
========================= */
.small-muted {
    color: #94a3b8;
    font-size: 0.92rem;
}

/* =========================
   CARDS
========================= */
.card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* =========================
   MOVIE POSTERS
========================= */
.stImage img {
    border-radius: 14px;
}

.poster-wrap {
    transition: all 0.2s ease;
}

.poster-wrap:hover {
    transform: translateY(-6px);
}

.movie-title {
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.35rem;
    margin-top: 8px;
    min-height: 2.7rem;
}

.meta {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 4px;
}

/* =========================
   BUTTONS
========================= */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    color: white;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #38bdf8;
    color: #38bdf8;
    transform: translateY(-2px);
}

/* =========================
   INPUTS
========================= */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
}

/* =========================
   SIDEBAR
========================= */
section[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.95);
}

/* =========================
   HEADINGS
========================= */
h1, h2, h3 {
    color: white !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")

if qp_view in ("home", "details"):
    st.session_state.view = qp_view

if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


# =============================
# ROUTING
# =============================
def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"

    if "id" in st.query_params:
        del st.query_params["id"]

    st.rerun()


def goto_details(tmdb_id):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)

    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))

    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path, params=None):
    try:
        r = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=25,
        )

        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}"

        return r.json(), None

    except Exception as e:
        return None, str(e)


# =============================
# POSTER GRID
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):

    if not cards:
        st.info("No movies found.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0

    for r in range(rows):

        colset = st.columns(cols)

        for c in range(cols):

            if idx >= len(cards):
                break

            movie = cards[idx]
            idx += 1

            tmdb_id = movie.get("tmdb_id")
            title = movie.get("title", "Untitled")
            poster = movie.get("poster_url")

            with colset[c]:

                st.markdown("<div class='poster-wrap'>", unsafe_allow_html=True)

                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.write("🖼️ No Poster")

                year = (movie.get("release_date") or "")[:4]
                rating = movie.get("vote_average")

                meta_parts = []

                if year:
                    meta_parts.append(year)

                if rating:
                    meta_parts.append(f"⭐ {float(rating):.1f}")

                meta = " • ".join(meta_parts)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True,
                )

                if meta:
                    st.markdown(
                        f"<div class='meta'>{meta}</div>",
                        unsafe_allow_html=True,
                    )

                if st.button(
                    "View Details",
                    key=f"{key_prefix}_{tmdb_id}_{idx}",
                ):
                    goto_details(tmdb_id)

                st.markdown("</div>", unsafe_allow_html=True)


# =============================
# SEARCH PARSER
# =============================
def parse_tmdb_search_to_cards(data, keyword, limit=24):

    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:

        raw_items = []

        for m in data.get("results", []):

            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")

            if not title or not tmdb_id:
                continue

            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    elif isinstance(data, list):

        raw_items = []

        for m in data:

            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()

            if not title or not tmdb_id:
                continue

            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": m.get("poster_url"),
                    "release_date": m.get("release_date", ""),
                }
            )

    else:
        return [], []

    matched = [
        x for x in raw_items
        if keyword_l in x["title"].lower()
    ]

    final_list = matched if matched else raw_items

    suggestions = []

    for x in final_list[:10]:

        year = (x.get("release_date") or "")[:4]

        label = (
            f"{x['title']} ({year})"
            if year else x["title"]
        )

        suggestions.append((label, x["tmdb_id"]))

    cards = final_list[:limit]

    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:

    st.markdown("## 🎬 Movie Recommender")

    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")

    home_category = st.selectbox(
        "Category",
        [
            "trending",
            "popular",
            "top_rated",
            "now_playing",
            "upcoming",
        ],
        index=0,
    )

    grid_cols = st.slider(
        "Grid Columns",
        4,
        8,
        6,
    )


# =============================
# HEADER
# =============================
st.title("🎬 Movie Recommender")

st.markdown(
    """
<div class='small-muted'>
Search movies • Explore details • Get recommendations
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# =============================
# HOME PAGE
# =============================
if st.session_state.view == "home":

    typed = st.text_input(
        "Search Movie",
        placeholder="Avengers, Batman, Interstellar...",
    )

    if typed.strip():

        data, err = api_get_json(
            "/tmdb/search",
            params={"query": typed.strip()},
        )

        if err:
            st.error(err)

        else:

            suggestions, cards = parse_tmdb_search_to_cards(
                data,
                typed.strip(),
                limit=24,
            )

            if suggestions:

                labels = ["Select Movie"] + [
                    s[0] for s in suggestions
                ]

                selected = st.selectbox(
                    "Suggestions",
                    labels,
                    index=0,
                )

                if selected != "Select Movie":

                    label_to_id = {
                        s[0]: s[1]
                        for s in suggestions
                    }

                    goto_details(label_to_id[selected])

            st.markdown("## Results")

            poster_grid(
                cards,
                cols=grid_cols,
                key_prefix="search",
            )

        st.stop()

    # =============================
    # HOME FEED
    # =============================
    st.markdown(
        f"## {home_category.replace('_', ' ').title()}"
    )

    home_cards, err = api_get_json(
        "/home",
        params={
            "category": home_category,
            "limit": 24,
        },
    )

    if err:
        st.error(err)

    else:
        poster_grid(
            home_cards,
            cols=grid_cols,
            key_prefix="home",
        )

# =============================
# DETAILS PAGE
# =============================
elif st.session_state.view == "details":

    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected.")
        st.stop()

    top1, top2 = st.columns([4, 1])

    with top1:
        st.markdown("## 📄 Movie Details")

    with top2:
        if st.button("← Back to Home"):
            goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error("Could not load movie.")
        st.stop()

    left, right = st.columns([1, 2.3], gap="large")

    # =============================
    # POSTER
    # =============================
    with left:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if data.get("poster_url"):
            st.image(
                data["poster_url"],
                use_container_width=True,
            )
        else:
            st.write("🖼️ No Poster")

        st.markdown("</div>", unsafe_allow_html=True)

    # =============================
    # DETAILS
    # =============================
    with right:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown(f"# {data.get('title','')}")

        release = data.get("release_date") or "-"

        genres = ", ".join(
            [g["name"] for g in data.get("genres", [])]
        ) or "-"

        st.markdown(
            f"<div class='small-muted'>📅 Release: {release}</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div class='small-muted'>🎭 Genres: {genres}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("## Overview")

        st.write(
            data.get("overview")
            or "No overview available."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # =============================
    # BACKDROP
    # =============================
    if data.get("backdrop_url"):

        st.markdown("## Backdrop")

        st.image(
            data["backdrop_url"],
            use_container_width=True,
        )

    # =============================
    # RECOMMENDATIONS
    # =============================
    st.markdown("## Recommended Movies")

    title = (data.get("title") or "").strip()

    if title:

        bundle, err2 = api_get_json(
            "/movie/search",
            params={
                "query": title,
                "tfidf_top_n": 12,
                "genre_limit": 12,
            },
        )

        if not err2 and bundle:

            st.markdown("### 🔎 Similar Movies")

            tfidf_movies = []

            for x in bundle.get(
                "tfidf_recommendations",
                [],
            ):

                tmdb = x.get("tmdb") or {}

                if tmdb.get("tmdb_id"):

                    tfidf_movies.append(
                        {
                            "tmdb_id": tmdb["tmdb_id"],
                            "title": tmdb.get("title"),
                            "poster_url": tmdb.get("poster_url"),
                        }
                    )

            poster_grid(
                tfidf_movies,
                cols=grid_cols,
                key_prefix="tfidf",
            )

            st.markdown("### 🎭 More Like This")

            poster_grid(
                bundle.get(
                    "genre_recommendations",
                    [],
                ),
                cols=grid_cols,
                key_prefix="genre",
            )

        else:
            st.warning("No recommendations found.")