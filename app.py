import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommendation-ocuk.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================
# GLOBAL STYLES — Cinematic Dark Luxury
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── ROOT ── */
:root {
    --black:      #080A0E;
    --surface:    #10131A;
    --surface2:   #181C26;
    --border:     rgba(255,255,255,0.07);
    --gold:       #C9A84C;
    --gold-light: #E8C97A;
    --text:       #E8E4DC;
    --muted:      #7A7669;
    --accent:     #C9A84C;
    --radius:     10px;
}

/* ── GLOBAL RESET ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main,
[data-testid="stHeader"] {
    background-color: var(--black) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"] { border-bottom: 1px solid var(--border); }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label { color: var(--muted) !important; font-size: 0.78rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* ── MAIN CONTAINER ── */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1500px !important;
}

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: var(--text) !important;
    letter-spacing: -0.01em;
}

/* ── HERO HEADER ── */
.site-header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin-bottom: 0.25rem;
}
.site-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: -0.02em;
    line-height: 1;
}
.site-tagline {
    font-size: 0.82rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 300;
}
.gold-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--gold) 0%, transparent 80%);
    margin: 0.6rem 0 1.6rem 0;
}

/* ── CATEGORY PILLS ── */
.pill-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1.2rem; }
.pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    font-weight: 500;
    cursor: pointer;
    border: 1px solid var(--border);
    color: var(--muted);
    background: var(--surface2);
    transition: all 140ms ease;
}
.pill.active {
    border-color: var(--gold);
    color: var(--gold);
    background: rgba(201,168,76,0.08);
}

/* ── SECTION LABELS ── */
.section-label {
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--gold);
    font-weight: 500;
    margin-bottom: 0.8rem;
    margin-top: 0.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── POSTER CARD ── */
.card-wrap {
    position: relative;
    border-radius: var(--radius);
    overflow: hidden;
    background: var(--surface2);
    border: 1px solid var(--border);
    transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease;
    cursor: pointer;
}
.card-wrap:hover {
    transform: translateY(-5px) scale(1.015);
    box-shadow: 0 20px 48px rgba(0,0,0,0.65), 0 0 0 1px var(--gold);
    border-color: var(--gold);
    z-index: 10;
}
.card-wrap:hover .card-overlay { opacity: 1; }

.poster-img {
    width: 100%;
    display: block;
    aspect-ratio: 2/3;
    object-fit: cover;
}
.poster-placeholder {
    width: 100%;
    aspect-ratio: 2/3;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface2);
    color: var(--muted);
    font-size: 2rem;
}
.card-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(8,10,14,0.92) 30%, transparent 70%);
    opacity: 0;
    transition: opacity 200ms ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 12px;
}
.overlay-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem;
    color: #fff;
    line-height: 1.25;
    font-weight: 700;
}
.overlay-meta {
    font-size: 0.74rem;
    color: var(--gold-light);
    margin-top: 3px;
}

/* ── CARD FOOTER ── */
.card-foot {
    padding: 8px 10px 10px;
}
.card-title {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-meta {
    font-size: 0.73rem;
    color: var(--muted);
    margin-top: 2px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.star { color: var(--gold); font-size: 0.68rem; }

/* ── DETAIL PAGE ── */
.detail-hero {
    border-radius: 14px;
    overflow: hidden;
    position: relative;
    margin-bottom: 1.8rem;
}
.detail-backdrop {
    width: 100%;
    max-height: 360px;
    object-fit: cover;
    display: block;
    filter: brightness(0.45);
}
.detail-backdrop-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to right, var(--black) 18%, transparent 60%),
                linear-gradient(to top, var(--black) 0%, transparent 35%);
}

.detail-poster {
    border-radius: 10px;
    border: 2px solid var(--border);
    box-shadow: 0 24px 60px rgba(0,0,0,0.8);
    overflow: hidden;
}
.detail-poster img { width: 100%; display: block; }

.detail-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--text);
    margin-bottom: 0.4rem;
}
.detail-meta-row {
    display: flex; gap: 16px; align-items: center; flex-wrap: wrap;
    margin-bottom: 0.9rem;
}
.badge {
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 0.73rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--muted);
}
.badge-gold {
    background: rgba(201,168,76,0.12);
    border-color: rgba(201,168,76,0.35);
    color: var(--gold);
}
.overview-text {
    font-size: 0.96rem;
    color: #BDB8AE;
    line-height: 1.75;
    font-weight: 300;
    max-width: 600px;
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 10px 16px !important;
    transition: border-color 150ms;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
}
[data-testid="stTextInput"] label { color: var(--muted) !important; font-size: 0.78rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
[data-testid="stSelectbox"] label { color: var(--muted) !important; font-size: 0.78rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* ── BUTTONS ── */
[data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 7px !important;
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 7px 18px !important;
    transition: all 150ms ease !important;
}
[data-testid="stButton"] button:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
    background: rgba(201,168,76,0.06) !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── INFO / WARNING / ERROR ── */
[data-testid="stAlert"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--black); }
::-webkit-scrollbar-thumb { background: #2a2d38; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ── SIDEBAR MENU ── */
.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: -0.01em;
    margin-bottom: 0.2rem;
}
.sidebar-version {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
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
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            year = (m.get("release_date") or "")[:4]
            rating = m.get("vote_average")

            star_str = f'<span class="star">★</span> {float(rating):.1f}' if rating is not None else ""
            year_str = year if year else ""
            meta_html = " &nbsp;·&nbsp; ".join(filter(None, [year_str, star_str]))
            link = f"?view=details&id={tmdb_id}" if tmdb_id else "#"

            with colset[c]:
                if poster:
                    card_html = f"""
<a href="{link}" style="text-decoration:none;">
  <div class="card-wrap">
    <img src="{poster}" class="poster-img" loading="lazy"/>
    <div class="card-overlay">
      <div class="overlay-title">{title}</div>
      <div class="overlay-meta">{meta_html}</div>
    </div>
  </div>
  <div class="card-foot">
    <div class="card-title">{title}</div>
    <div class="card-meta">{meta_html}</div>
  </div>
</a>"""
                else:
                    card_html = f"""
<a href="{link}" style="text-decoration:none;">
  <div class="card-wrap">
    <div class="poster-placeholder">🎬</div>
    <div class="card-overlay">
      <div class="overlay-title">{title}</div>
    </div>
  </div>
  <div class="card-foot">
    <div class="card-title">{title}</div>
    <div class="card-meta">{meta_html}</div>
  </div>
</a>"""
                st.markdown(card_html, unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
CATEGORY_LABELS = {
    "trending":    "🔥 Trending",
    "popular":     "📈 Popular",
    "top_rated":   "⭐ Top Rated",
    "now_playing": "🎭 Now Playing",
    "upcoming":    "🗓 Upcoming",
}

with st.sidebar:
    st.markdown("<div class='sidebar-logo'>🎬 CineMatch</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-version'>Discover · Explore · Recommend</div>", unsafe_allow_html=True)

    if st.button("← Home"):
        goto_home()

    st.markdown("---")
    st.markdown("<div class='section-label'>Browse</div>", unsafe_allow_html=True)

    home_category = st.selectbox(
        "Category",
        list(CATEGORY_LABELS.keys()),
        format_func=lambda k: CATEGORY_LABELS[k],
        index=0,
    )

    st.markdown("<div class='section-label'>Display</div>", unsafe_allow_html=True)
    grid_cols = st.slider("Columns", 3, 8, 6)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.7rem;color:#3d3d3d;text-align:center;'>Powered by TMDB</div>",
        unsafe_allow_html=True,
    )


# =============================
# SITE HEADER
# =============================
st.markdown("""
<div class="site-header">
  <span class="site-logo">CineMatch</span>
  <span class="site-tagline">Curated film discovery</span>
</div>
<div class="gold-rule"></div>
""", unsafe_allow_html=True)


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":

    # Search bar
    search_col, _ = st.columns([2, 1])
    with search_col:
        typed = st.text_input(
            "Search",
            placeholder="Title, keyword, director…",
            label_visibility="collapsed",
        )

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            with st.spinner("Searching…"):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                if suggestions:
                    labels = ["— select a title —"] + [s[0] for s in suggestions]
                    sel_col, _ = st.columns([2, 1])
                    with sel_col:
                        selected = st.selectbox("Suggestions", labels, index=0, label_visibility="collapsed")
                    if selected != "— select a title —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found.")

                st.markdown("<div class='section-label' style='margin-top:1.4rem;'>Search Results</div>", unsafe_allow_html=True)
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
        st.stop()

    # Category pills (visual only — actual filter is sidebar select)
    pills_html = "<div class='pill-row'>"
    for k, v in CATEGORY_LABELS.items():
        active = "active" if k == home_category else ""
        pills_html += f"<span class='pill {active}'>{v}</span>"
    pills_html += "</div>"
    st.markdown(pills_html, unsafe_allow_html=True)

    # Home feed
    with st.spinner("Loading…"):
        home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})

    if err or not home_cards:
        st.error(f"Could not load feed: {err or 'Unknown error'}")
        st.stop()

    label = CATEGORY_LABELS.get(home_category, home_category)
    st.markdown(f"<div class='section-label'>{label}</div>", unsafe_allow_html=True)
    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    with st.spinner("Loading details…"):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # ── Backdrop hero ──────────────────────────────────────
    if data.get("backdrop_url"):
        st.markdown(f"""
<div class="detail-hero">
  <img src="{data['backdrop_url']}" class="detail-backdrop"/>
  <div class="detail-backdrop-overlay"></div>
</div>""", unsafe_allow_html=True)

    # ── Poster + Info layout ───────────────────────────────
    back_col, _ = st.columns([1, 4])
    with back_col:
        if st.button("← Back"):
            goto_home()

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    poster_col, info_col = st.columns([1, 2.6], gap="large")

    with poster_col:
        st.markdown("<div class='detail-poster'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.markdown("<div style='padding:2rem;text-align:center;color:#555;font-size:2rem;'>🎬</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with info_col:
        title = data.get("title", "")
        release = data.get("release_date") or ""
        year = release[:4] if release else ""
        genres = data.get("genres", [])
        genre_str = " &nbsp;·&nbsp; ".join([g["name"] for g in genres]) if genres else "—"
        rating = data.get("vote_average")
        overview = data.get("overview") or "No overview available."

        st.markdown(f"<div class='detail-title'>{title}</div>", unsafe_allow_html=True)

        badges = ""
        if year:
            badges += f"<span class='badge'>{year}</span>"
        if rating:
            badges += f"<span class='badge badge-gold'>★ {float(rating):.1f}</span>"
        if genre_str:
            badges += f"<span class='badge'>{genre_str}</span>"

        st.markdown(f"<div class='detail-meta-row'>{badges}</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-label'>Synopsis</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='overview-text'>{overview}</p>", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)

    # ── Recommendations ────────────────────────────────────
    title_str = (data.get("title") or "").strip()
    if title_str:
        with st.spinner("Finding recommendations…"):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title_str, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            st.markdown("<div class='section-label'>Similar Films</div>", unsafe_allow_html=True)
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>More in This Genre</div>", unsafe_allow_html=True)
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.markdown("<div class='section-label'>Genre Picks</div>", unsafe_allow_html=True)
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="details_genre_fallback")
            else:
                st.info("No recommendations available right now.")
    else:
        st.warning("No title available for recommendations.")