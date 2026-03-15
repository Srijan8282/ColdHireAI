import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import streamlit.components.v1 as components
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

#-----------------------
#  PAGE CONFIG
#-----------------------
st.set_page_config(
    layout="wide",
    page_title="ColdHire AI",
    page_icon="❄️",
    initial_sidebar_state="expanded",
)

#-----------------------
#  GLOBAL CSS
#-----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

:root {
    --bg:       #070b12;
    --surface:  #0c1120;
    --surface2: #101827;
    --surface3: #162032;
    --border:   #1c2d44;
    --border2:  #243548;
    --cyan:     #22d3ee;
    --indigo:   #818cf8;
    --emerald:  #34d399;
    --amber:    #fbbf24;
    --rose:     #fb7185;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --muted2:   #94a3b8;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Brand ── */
.brand-wrap { padding: 24px 0 16px; display:flex; align-items:center; gap:12px; }
.brand-gem {
    width:44px; height:44px; border-radius:12px; flex-shrink:0;
    background: linear-gradient(135deg, var(--cyan) 0%, var(--indigo) 100%);
    display:flex; align-items:center; justify-content:center;
    font-size:20px; box-shadow: 0 0 28px rgba(34,211,238,.3);
}
.brand-name {
    font-family:'Syne',sans-serif; font-weight:800; font-size:1.45rem;
    background: linear-gradient(90deg, var(--cyan), var(--indigo));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    line-height:1;
}
.brand-tagline { font-size:.68rem; color:var(--muted); letter-spacing:.1em; text-transform:uppercase; margin-top:3px; }

/* ── Nav button overrides ── */
[data-testid="stButton"] > button {
    background: transparent !important;
    color: var(--muted2) !important;
    font-family:'DM Sans',sans-serif !important;
    font-weight:500 !important; font-size:.88rem !important;
    border: 1px solid transparent !important;
    border-radius:10px !important;
    padding:10px 14px !important;
    text-align:left !important;
    transition: all .2s !important;
    box-shadow: none !important;
    background-color: #2b1364 !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
    transform: none !important;
}

/* ── Primary CTA override ── */
.primary-btn > button {
    background: linear-gradient(135deg, var(--cyan), var(--indigo)) !important;
    color: #070b12 !important;
    font-family:'Syne',sans-serif !important;
    font-weight:700 !important; font-size:.87rem !important;
    letter-spacing:.04em !important;
    border: none !important; border-radius:10px !important;
    padding:11px 22px !important;
    box-shadow: 0 4px 22px rgba(34,211,238,.28) !important;
    transition: opacity .2s, transform .15s, box-shadow .2s !important;
}
.primary-btn > button:hover {
    opacity:.9 !important; transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(34,211,238,.38) !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius:10px !important;
    color: var(--text) !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:.92rem !important;
    padding:11px 15px !important;
    transition: border-color .2s, box-shadow .2s;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(34,211,238,.1) !important;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius:10px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family:'Syne',sans-serif !important;
    font-weight:600 !important; font-size:.82rem !important;
    color: var(--muted) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom-color: var(--cyan) !important;
}
[data-testid="stExpander"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius:12px !important;
}
hr { border-color: var(--border) !important; margin:22px 0 !important; }

/* ── Hero ── */
.hero {
    text-align:center; padding:52px 24px 36px; position:relative;
}
.hero::before {
    content:''; position:absolute; top:0; left:50%; transform:translateX(-50%);
    width:700px; height:300px;
    background: radial-gradient(ellipse, rgba(34,211,238,.07) 0%, transparent 70%);
    pointer-events:none;
}
.hero h1 {
    font-family:'Syne',sans-serif; font-size:clamp(2rem,5vw,3.2rem);
    font-weight:800; letter-spacing:-.03em; line-height:1.1; margin-bottom:14px;
    background: linear-gradient(140deg, #ffffff 25%, var(--cyan) 60%, var(--indigo) 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero p { font-size:1rem; color:var(--muted2); max-width:520px; margin:0 auto; line-height:1.7; font-weight:300; }
.badge-row { display:flex; justify-content:center; gap:8px; margin-top:20px; flex-wrap:wrap; }
.badge {
    display:inline-flex; align-items:center; gap:5px;
    padding:4px 13px; border-radius:999px; font-size:.75rem; font-weight:500;
    border:1px solid var(--border); background:var(--surface); color:var(--muted2);
}
.badge.c { border-color:rgba(34,211,238,.35); color:var(--cyan); }
.badge.i { border-color:rgba(129,140,248,.35); color:var(--indigo); }
.badge.e { border-color:rgba(52,211,153,.35); color:var(--emerald); }

/* ── Cards ── */
.card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:16px; padding:26px 28px; margin-bottom:18px; position:relative; overflow:hidden;
}
.card::before {
    content:''; position:absolute; inset:0;
    background: linear-gradient(135deg, rgba(34,211,238,.025) 0%, transparent 55%);
    pointer-events:none;
}
.card-label {
    font-family:'Syne',sans-serif; font-size:.72rem; font-weight:700;
    letter-spacing:.12em; text-transform:uppercase; color:var(--cyan);
    margin-bottom:14px; display:flex; align-items:center; gap:7px;
}

/* ── Steps ── */
.steps { display:flex; align-items:center; justify-content:center; gap:0; margin:20px 0 28px; }
.step { display:flex; flex-direction:column; align-items:center; gap:6px; }
.step-circle {
    width:34px; height:34px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-family:'Syne',sans-serif; font-weight:700; font-size:.82rem;
    border:2px solid var(--border); background:var(--surface2); color:var(--muted);
    transition:all .3s;
}
.step-circle.active { border-color:var(--cyan); background:rgba(34,211,238,.1); color:var(--cyan); box-shadow:0 0 14px rgba(34,211,238,.22); }
.step-circle.done   { border-color:var(--emerald); background:rgba(52,211,153,.1); color:var(--emerald); }
.step-label { font-size:.68rem; color:var(--muted); text-align:center; max-width:68px; line-height:1.3; }
.step-conn  { width:52px; height:2px; background:var(--border); margin:0 4px 22px; }
.step-conn.done { background:linear-gradient(90deg,var(--emerald),var(--cyan)); }

/* ── Job card ── */
.jcard {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:12px; padding:18px 20px; margin-bottom:14px; position:relative;
}
.jcard::after {
    content:''; position:absolute; left:0; top:0; width:3px; height:100%;
    background:linear-gradient(180deg,var(--cyan),var(--indigo));
    border-radius:3px 0 0 3px;
}
.j-role { font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700; color:var(--text); margin-bottom:4px; }
.j-meta { font-size:.8rem; color:var(--emerald); font-weight:500; margin-bottom:8px; }
.j-desc { font-size:.82rem; color:var(--muted2); line-height:1.55; margin-bottom:10px; }
.skill-pill {
    display:inline-block; padding:3px 10px; border-radius:6px; margin:2px;
    background:rgba(34,211,238,.08); border:1px solid rgba(34,211,238,.2);
    color:var(--cyan); font-size:.72rem; font-weight:500;
}

/* ── Email output ── */
.email-output {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:12px; padding:22px 24px; font-size:.88rem;
    line-height:1.8; color:var(--text); white-space:pre-wrap;
    position:relative; overflow:hidden;
}
.email-output::before {
    content:''; position:absolute; left:0; top:0; width:3px; height:100%;
    background:linear-gradient(180deg,var(--cyan),var(--indigo));
}

/* ── Chat ── */
.chat-wrap { display:flex; flex-direction:column; gap:16px; padding:8px 0; }
.msg { display:flex; gap:10px; }
.msg.user { flex-direction:row-reverse; }
.av {
    width:32px; height:32px; border-radius:50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-size:.8rem;
    border:2px solid var(--border);
}
.av-ai  { background:rgba(34,211,238,.12); border-color:rgba(34,211,238,.3); }
.av-usr { background:rgba(129,140,248,.12); border-color:rgba(129,140,248,.3); }
.bubble { max-width:80%; padding:11px 15px; border-radius:14px; font-size:.87rem; line-height:1.65; }
.bubble-ai  {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:4px 14px 14px 14px; color:var(--text);
}
.bubble-usr {
    background:linear-gradient(135deg,rgba(34,211,238,.12),rgba(129,140,248,.12));
    border:1px solid rgba(34,211,238,.22); border-radius:14px 4px 14px 14px; color:var(--text);
}

/* ── Mode tabs for chat ── */
.mode-bar {
    display:flex; gap:8px; margin-bottom:18px;
    padding:5px; background:var(--surface2); border-radius:12px; border:1px solid var(--border);
}
.mode-btn {
    flex:1; text-align:center; padding:8px 12px; border-radius:9px;
    font-family:'Syne',sans-serif; font-size:.78rem; font-weight:700;
    letter-spacing:.04em; cursor:pointer; transition:all .2s; color:var(--muted);
}
.mode-btn.on {
    background:linear-gradient(135deg,rgba(34,211,238,.15),rgba(129,140,248,.15));
    color:var(--cyan); border:1px solid rgba(34,211,238,.3);
}

/* ── Fit score ring ── */
.fit-wrap { text-align:center; padding:20px 0; }
.fit-score-num {
    font-family:'Syne',sans-serif; font-size:3.5rem; font-weight:800;
    background:linear-gradient(135deg,var(--cyan),var(--indigo));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.fit-verdict {
    font-family:'Syne',sans-serif; font-size:.9rem; font-weight:700;
    margin-top:6px;
}
.verdict-strong  { color:var(--emerald); }
.verdict-good    { color:var(--cyan); }
.verdict-partial { color:var(--amber); }
.verdict-weak    { color:var(--rose); }

/* ── Stat mini ── */
.stat-mini { display:flex; gap:10px; margin-bottom:16px; flex-wrap:wrap; }
.scard {
    flex:1; min-width:80px; background:var(--surface); border:1px solid var(--border);
    border-radius:10px; padding:14px 16px; text-align:center;
}
.scard-val {
    font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:800;
    background:linear-gradient(135deg,var(--cyan),var(--indigo));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.scard-lbl { font-size:.7rem; color:var(--muted); margin-top:3px; }

/* ── Interview Q card ── */
.q-card {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:12px; padding:16px 18px; margin-bottom:12px; position:relative;
}
.q-type-badge {
    display:inline-block; padding:2px 9px; border-radius:5px; font-size:.7rem; font-weight:600;
    margin-bottom:8px; text-transform:uppercase; letter-spacing:.06em;
}
.q-technical   { background:rgba(34,211,238,.1);  color:var(--cyan);    border:1px solid rgba(34,211,238,.25); }
.q-behavioral  { background:rgba(129,140,248,.1); color:var(--indigo);  border:1px solid rgba(129,140,248,.25); }
.q-situational { background:rgba(52,211,153,.1);  color:var(--emerald); border:1px solid rgba(52,211,153,.25); }
.q-hard   { color:var(--rose); }
.q-medium { color:var(--amber); }
.q-easy   { color:var(--emerald); }
.q-text { font-size:.9rem; color:var(--text); font-weight:500; margin-bottom:8px; line-height:1.5; }
.q-tip  { font-size:.8rem; color:var(--muted2); font-style:italic; line-height:1.4; }

/* ── Info box ── */
.infobox {
    display:flex; align-items:flex-start; gap:11px;
    background:rgba(34,211,238,.05); border:1px solid rgba(34,211,238,.18);
    border-radius:10px; padding:13px 15px; font-size:.84rem; color:var(--muted2);
    margin-bottom:16px; line-height:1.55;
}
.infobox-icon { font-size:1rem; flex-shrink:0; margin-top:1px; }

/* ── Sidebar stats ── */
.sb-stat {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:10px; padding:13px 15px; margin-bottom:8px;
}
.sb-stat-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:5px; }
.sb-stat-label { font-size:.8rem; color:var(--muted); }
.sb-stat-val {
    font-family:'Syne',sans-serif; font-weight:700; font-size:.95rem;
    background:linear-gradient(90deg,var(--cyan),var(--indigo));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
/* Force input+button on same line */
[data-testid="stTextInput"] {
    margin-bottom: 0 !important;
}
            
            [data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--cyan) !important;
    border: 1px solid var(--cyan) !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: .87rem !important;
    transition: all .2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, var(--cyan), var(--indigo)) !important;
    color: #070b12 !important;
    border-color: transparent !important;
    box-shadow: 0 4px 22px rgba(34,211,238,.28) !important;
}
            
/* ── Tip chips ── */
.tip-grid { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; }
.tip-chip {
    padding:7px 14px; border-radius:999px; font-size:.78rem; font-weight:500;
    border:1px solid var(--border); background:var(--surface); color:var(--muted2);
    cursor:pointer; transition:all .2s; white-space:nowrap;
}
.tip-chip:hover { border-color:var(--cyan); color:var(--cyan); background:rgba(34,211,238,.06); }

/* ── Progress ── */
.pbar { width:100%; height:4px; background:var(--border); border-radius:999px; overflow:hidden; margin:8px 0 16px; }
.pfill { height:100%; border-radius:999px; background:linear-gradient(90deg,var(--cyan),var(--indigo)); transition:width .5s ease; }

/* ── Page heading ── */
.pg-head { padding:26px 0 14px; }
.pg-title {
    font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:800;
    background:linear-gradient(135deg, #fff 25%, var(--cyan) 65%, var(--indigo));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin-bottom:6px;
}
.pg-sub { color:var(--muted2); font-size:.9rem; }

/* ── Pill tag ── */
.tag-match   { background:rgba(52,211,153,.1);  color:var(--emerald); border:1px solid rgba(52,211,153,.25);  border-radius:6px; padding:3px 10px; font-size:.75rem; font-weight:500; margin:2px; display:inline-block; }
.tag-missing { background:rgba(251,113,133,.1); color:var(--rose);    border:1px solid rgba(251,113,133,.25); border-radius:6px; padding:3px 10px; font-size:.75rem; font-weight:500; margin:2px; display:inline-block; }
</style>
""", unsafe_allow_html=True)


#-----------------------------------------------------
#  SESSION STATE
#-----------------------------------------------------
def init_state():
    defs = {
        "page":            "generator",
        "jobs":            [],
        "emails":          [],
        "active_job_idx":  0,
        "chat_history_generic": [],
        "chat_history_job":     [],
        "chat_mode":       "generic",   # "generic" | "job"
        "job_url":         "",
        "generated":       False,
        "gen_count":       0,
        "history":         [],
        # Profile
        "profile_name":    "Srijan Kundu Chowdhury",
        "profile_company": "Lorem Ipsum Technology",
        "profile_role":    "Software Developer Engineer",
        "profile_skills":  "Python, Machine Learning, Data Science, Cloud, APIs",
        "profile_exp":     "1+ years",
        "profile_achievements": "Led ML pipeline reducing costs by 30%, Built 10+ client integrations",
        "tone":            "Professional",
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


#-----------------------------------------------------
#  SIDEBAR
#-----------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-wrap">
        <div class="brand-gem">❄️</div>
        <div>
            <div class="brand-name">ColdHire AI</div>
            <div class="brand-tagline">Outreach Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    nav_items = [
        ("generator",  "✉️",  "Email Generator"),
        ("chatbot",    "💬",  "AI Assistant"),
        ("interview",  "🎯",  "Interview Prep"),
        ("fit",        "📊",  "Job Fit Analyser"),
        ("tools",      "🛠️", "More Tools"),
        ("history",    "🗂️", "History"),
        ("settings",   "⚙️",  "Settings"),
    ]
    for pid, icon, label in nav_items:
        is_active = st.session_state.page == pid
        btn_label = f"{'▶ ' if is_active else ''}{icon}  {label}"
        if st.button(btn_label, key=f"nav_{pid}", use_container_width=True):
            st.session_state.page = pid
            st.rerun()

    st.markdown("---")

    # Active job pill
    if st.session_state.jobs:
        job = st.session_state.jobs[st.session_state.active_job_idx]
        st.markdown(f"""
        <div style="font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;">Active Job</div>
        <div style="background:rgba(34,211,238,.06);border:1px solid rgba(34,211,238,.2);
             border-radius:9px;padding:10px 12px;">
            <div style="font-family:'Syne',sans-serif;font-size:.85rem;font-weight:700;color:var(--cyan);margin-bottom:2px;">
                {(job.get('role') or 'N/A')[:32]}
            </div>
            <div style="font-size:.75rem;color:var(--muted);">{job.get('company','') or ''}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")

    st.markdown(f"""
    <div class="sb-stat">
        <div style="font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;">Session</div>
        <div class="sb-stat-row">
            <span class="sb-stat-label">Emails generated Now</span>
            <span class="sb-stat-val">{st.session_state.gen_count}</span>
        </div>
        <div class="sb-stat-row" style="margin-bottom:0">
            <span class="sb-stat-label">Jobs analysed</span>
            <span class="sb-stat-val">{len(st.session_state.jobs)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:.7rem;color:var(--muted);line-height:1.7;padding:4px;">
        Powered by <b style="color:var(--cyan)">Groq · LLaMA 3.1</b><br>
        Vector search by <b style="color:var(--indigo)">ChromaDB</b><br>
        Developed by <b style="color:var(--red)">Srijan</b><br>
        <span style="color:var(--emerald)">v1.0.1</span>
    </div>
    """, unsafe_allow_html=True)


    components.html("""
    <style>
    .link-wrap { display:flex; gap:16px; align-items:center; padding:8px 0; }
    .link-icon {
        width:42px; height:42px; border-radius:10px;
        display:flex; align-items:center; justify-content:center;
        background:#101827; border:1px solid #1c2d44;
        transition:all .2s; text-decoration:none;
    }
    .link-icon:hover { transform:translateY(-2px); }
    .li:hover { border-color:#0a66c2; background:rgba(10,102,194,.15); }
    .gm:hover { border-color:#ea4335; background:rgba(234,67,53,.15); }
    .vr:hover { border-color:#22d3ee; background:rgba(34,211,238,.15); }
    .fb:hover { border-color:#1877f2; background:rgba(24,119,242,.15); }
    </style>
    <div class="link-wrap">
        <a href="https://www.linkedin.com/in/srijankunduchowdhury/" target="_blank" class="link-icon li">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" width="18" style="filter:invert(0.6) sepia(1) saturate(5) hue-rotate(180deg);">
        </a>
        <a href="mailto:srijankunduchowdhury@gmail.com" class="link-icon gm">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/gmail.svg" width="18" style="filter:invert(0.6) sepia(1) saturate(5) hue-rotate(320deg);">
        </a>
        <a href="https://srijankunduchowdhury.vercel.app/" target="_blank" class="link-icon vr">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/vercel.svg" width="18" style="filter:invert(0.7);">
        </a>
        <a href="https://www.facebook.com/srijan.kunduchowdhury" target="_blank" class="link-icon fb">
            <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/facebook.svg" width="18" style="filter:invert(0.6) sepia(1) saturate(5) hue-rotate(200deg);">
        </a>
    </div>
    """, height=80)


#------------------------------------
#  RESOURCES
#------------------------------
@st.cache_resource
def load_resources():
    return Chain(), Portfolio()

try:
    chain, portfolio = load_resources()
except Exception as e:
    st.error(f"❌ Startup error: {e}")
    st.info("Ensure `.env` has `GROQ_API_KEY` and `my_portfolio.csv` exists.")
    st.stop()


#-------------------------------
#  SHARED HELPER: JOB LOADER
#------------------------------
def load_job_from_url(url: str):
    """Scrape & extract. Returns list of job dicts or raises."""
    loader = WebBaseLoader([url])
    data   = clean_text(loader.load().pop().page_content)
    portfolio.load_portfolio()
    return chain.extract_jobs(data)


#--------------------------------------
#  PAGE: EMAIL GENERATOR
#----------------------------------------
def page_generator():
    st.markdown("""
    <div class="hero">
        <h1>Turn Job Posts Into<br>Winning Cold Emails</h1>
        <p>Paste any job listing URL — ColdHire AI extracts the role,
           matches your portfolio, and writes a personalised cold email in seconds.</p>
        <div class="badge-row">
            <span class="badge c">⚡ Groq-Powered</span>
            <span class="badge i">🧠 LLaMA 3.1</span>
            <span class="badge e">✅ Portfolio Matched</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Step tracker
    s1 = "done" if st.session_state.generated else "active"
    s2 = "done" if st.session_state.generated else ""
    s3 = "active" if st.session_state.generated else ""
    conn = "done" if st.session_state.generated else ""
    st.markdown(f"""
    <div class="steps">
        <div class="step"><div class="step-circle {s1}">{"✓" if st.session_state.generated else "1"}</div><div class="step-label">Paste URL</div></div>
        <div class="step-conn {conn}"></div>
        <div class="step"><div class="step-circle {s2}">{"✓" if st.session_state.generated else "2"}</div><div class="step-label">AI Extracts</div></div>
        <div class="step-conn {conn}"></div>
        <div class="step"><div class="step-circle {s3}">3</div><div class="step-label">Email Ready</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input ──
    st.markdown('<div class="card"><div class="card-label">🔗 Job Listing URL</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; gap:10px; align-items:center; margin-bottom:12px;">
        <div style="flex:5;">
    """, unsafe_allow_html=True)    
    url = st.text_input("URL", value=st.session_state.job_url,
                        placeholder="https://careers.company.com/job/…",
                        label_visibility="collapsed",
                        key="url_input")
    st.markdown('</div>', unsafe_allow_html=True)
    go = st.button("Generate ✨", use_container_width=False, key="gen_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="infobox">
        <span class="infobox-icon">💡</span>
        Works with LinkedIn, Glassdoor, company career pages (Accenture, Infosys, TCS, Amazon, Google…).
        The AI auto-extracts role, skills, and experience.
    </div>
    """, unsafe_allow_html=True)

    # Sample URLs
    st.markdown("<div style='font-size:.76rem;color:var(--muted);margin-bottom:6px;'>Quick samples:</div>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    samples = [
        ("Accenture SWE", "https://www.accenture.com/in-en/careers/jobdetails?id=ATCI-5394594-S1962992_en"),
        ("Amazon SDE",    "https://www.amazon.jobs/en/jobs/2778012/software-development-engineer"),
        ("Infosys",       "https://career.infosys.com/jobdesc?jobReferenceCode=INFSYS-EXTERNAL-108880"),
    ]
    for col, (lbl, su) in zip([sc1, sc2, sc3], samples):
        with col:
            if st.button(f"📎 {lbl}", key=f"smp_{lbl}", use_container_width=True):
                st.session_state.job_url = su
                st.rerun()

    # Options row
    oc1, oc2, oc3 = st.columns(3)
    with oc1:
        tone = st.selectbox("Email Tone", ["Professional","Friendly","Confident","Concise","Storytelling"],
                            index=["Professional","Friendly","Confident","Concise","Storytelling"].index(st.session_state.tone))
        st.session_state.tone = tone
    with oc2:
        max_emails = st.selectbox("Max emails", [1, 2, 3, 5], index=0)
    with oc3:
        include_subject = st.checkbox("Include subject line", value=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ─-----------------------─ Generate ---------------------------──
    if go and url.strip():
        st.session_state.job_url = url
        prog = st.progress(0, text="🔍 Scraping job page…")
        try:
            jobs = load_job_from_url(url)
        except Exception as e:
            st.error(f"❌ Failed to load URL: {e}")
            prog.empty()
            return
        prog.progress(40, text="🧠 Extracting job details…")

        emails = []
        for i, job in enumerate(jobs[:max_emails]):
            prog.progress(40 + int(50 * (i+1) / max(len(jobs[:max_emails]),1)),
                          text=f"✉️ Writing email {i+1}/{len(jobs[:max_emails])}…")
            skills = job.get("skills", [])
            links  = portfolio.query_links(skills)
            email_text = chain.write_mail(
                job, links, tone=tone,
                name=st.session_state.profile_name,
                role=st.session_state.profile_role,
            )
            if not include_subject and email_text.startswith("Subject:"):
                lines = email_text.split("\n", 2)
                email_text = lines[2].strip() if len(lines) > 2 else email_text
            emails.append({"job": job, "email": email_text})

        prog.progress(100, text="✅ Done!")
        prog.empty()

        st.session_state.jobs            = jobs
        st.session_state.active_job_idx  = 0
        st.session_state.emails          = emails
        st.session_state.generated       = True
        st.session_state.gen_count      += len(emails)
        st.session_state.history.append({"url": url, "emails": emails})
        st.rerun()

    elif go:
        st.warning("⚠️ Please enter a valid URL.")

    # ─------------------------------------─ Results -----------------------------------─
    if st.session_state.generated and st.session_state.emails:
        st.markdown("---")
        st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:700;
             background:linear-gradient(90deg,var(--cyan),var(--indigo));
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:18px;">
             ✅ Generated Emails</div>""", unsafe_allow_html=True)

        tab_labels = [f"Email {i+1} — {(e['job'].get('role') or 'Role')[:26]}"
                      for i, e in enumerate(st.session_state.emails)]
        tabs = st.tabs(tab_labels)

        for i, (tab, entry) in enumerate(zip(tabs, st.session_state.emails)):
            with tab:
                job  = entry["job"]
                mail = entry["email"]

                skills_html = " ".join(f'<span class="skill-pill">{s}</span>'
                                       for s in (job.get("skills") or [])[:14])
                loc  = job.get("location") or "N/A"
                sal  = job.get("salary")   or "Not listed"
                co   = job.get("company")  or "N/A"

                st.markdown(f"""
                <div class="jcard">
                    <div class="j-role">💼 {job.get('role','N/A')}</div>
                    <div class="j-meta">🏢 {co} &nbsp;·&nbsp; 📍 {loc} &nbsp;·&nbsp; 💰 {sal}</div>
                    <div class="j-meta">📅 Experience: {job.get('experience','N/A')}</div>
                    <div class="j-desc">{str(job.get('description',''))[:300]}…</div>
                    <div>{skills_html}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="card-label" style="margin-top:14px;">✉️ Cold Email</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="email-output">{mail}</div>', unsafe_allow_html=True)

                a1, a2, a3, a4 = st.columns(4)
                with a1:
                    if st.button("📋 Copy", key=f"cp_{i}", use_container_width=True):
                        st.code(mail)
                with a2:
                    st.download_button("⬇️ .txt", data=mail,
                                       file_name=f"coldhire_email_{i+1}.txt",
                                       mime="text/plain", key=f"dl_{i}",
                                       use_container_width=True)
                with a3:
                    if st.button("🔄 Regenerate", key=f"rg_{i}", use_container_width=True):
                        with st.spinner("Rewriting…"):
                            new_mail = chain.write_mail(
                                job, portfolio.query_links(job.get("skills",[])),
                                tone=tone,
                                name=st.session_state.profile_name,
                                role=st.session_state.profile_role,
                            )
                        st.session_state.emails[i]["email"] = new_mail
                        st.rerun()
                with a4:
                    # Quick navigate to chatbot with this job loaded
                    if st.button("💬 Ask AI", key=f"ask_{i}", use_container_width=True):
                        st.session_state.active_job_idx = i
                        st.session_state.page = "chatbot"
                        st.session_state.chat_mode = "job"
                        st.rerun()


#------------------------------------------------
#  PAGE: AI ASSISTANT  (dual-mode)
#--------------------------------------------
def page_chatbot():
    st.markdown('<div class="pg-head"><div class="pg-title">💬 AI Assistant</div>'
                '<div class="pg-sub">General career advice OR deep-dive into your loaded job.</div></div>',
                unsafe_allow_html=True)

    # ─---------------─ Mode selector ─---------------------
    has_job = bool(st.session_state.jobs)
    m_gen = "on" if st.session_state.chat_mode == "generic" else ""
    m_job = "on" if st.session_state.chat_mode == "job" else ""

    st.markdown(f"""
    <div class="mode-bar">
        <div class="mode-btn {m_gen}" id="mode_generic">🌐 General Assistant</div>
        <div class="mode-btn {m_job}" id="mode_job">{'🎯 Job: ' + ((st.session_state.jobs[st.session_state.active_job_idx].get('role') or 'N/A')[:22] if has_job else 'No job loaded') }</div>
    </div>
    """, unsafe_allow_html=True)

    mc1, mc2 = st.columns(2)
    with mc1:
        if st.button("🌐 General Mode", use_container_width=True, key="mode_btn_gen"):
            st.session_state.chat_mode = "generic"
            st.rerun()
    with mc2:
        if has_job:
            if st.button(f"🎯 Job Mode — {st.session_state.jobs[st.session_state.active_job_idx].get('role','N/A')[:20]}",
                         use_container_width=True, key="mode_btn_job"):
                st.session_state.chat_mode = "job"
                st.rerun()
        else:
            st.button("🎯 Job Mode (load a job first)", disabled=True,
                      use_container_width=True, key="mode_btn_job_dis")

    # Job selector if multiple jobs loaded
    if has_job and len(st.session_state.jobs) > 1:
        job_labels = [f"{i+1}. {j.get('role','N/A')}" for i, j in enumerate(st.session_state.jobs)]
        chosen = st.selectbox("Active job for Job Mode:", job_labels,
                              index=st.session_state.active_job_idx)
        st.session_state.active_job_idx = job_labels.index(chosen)

    # ─-----------------─ Context banner ─-------------------─
    mode = st.session_state.chat_mode
    if mode == "generic":
        st.markdown("""
        <div class="infobox">
            <span class="infobox-icon">🌐</span>
            <b style="color:var(--text)">General Mode</b> — Ask me anything about cold emailing,
            outreach strategy, career tips, salary negotiation, portfolio advice, and more.
        </div>
        """, unsafe_allow_html=True)
        history_key = "chat_history_generic"
        quick_prompts = [
            "How do I write a killer subject line?",
            "Best follow-up strategy after no reply?",
            "How to personalise cold emails at scale?",
            "Tips for salary negotiation?",
            "How to stand out with my portfolio?",
            "What's a good cold email open rate?",
        ]
    else:
        job = st.session_state.jobs[st.session_state.active_job_idx]
        st.markdown(f"""
        <div class="infobox" style="border-color:rgba(129,140,248,.25);background:rgba(129,140,248,.05);">
            <span class="infobox-icon">🎯</span>
            <b style="color:var(--indigo)">Job Mode</b> — I'll answer questions specifically about
            <b style="color:var(--text)">{job.get('role','this role')}</b> at
            <b style="color:var(--text)">{job.get('company','the company') or 'the company'}</b>.
            Ask about skills, responsibilities, requirements, culture clues — anything from the posting.
        </div>
        """, unsafe_allow_html=True)
        history_key = "chat_history_job"
        quick_prompts = [
            "What skills are required for this role?",
            "What experience level does this job need?",
            "What are the main responsibilities?",
            "What tech stack is mentioned?",
            "Any culture clues from this posting?",
            "What salary range is mentioned?",
        ]

    # ─-------------─ Chat history ─--------------─
    history = st.session_state[history_key]

    if not history:
        welcome = ("Hi! I'm ColdHire AI 👋 Ask me anything about cold outreach, "
                   "job hunting, or career strategy!" if mode == "generic"
                   else f"Hi! I'm ready to answer your questions about the **{st.session_state.jobs[st.session_state.active_job_idx].get('role','') if has_job else 'loaded'}** role. "
                        "What would you like to know?")
        st.markdown(f"""
        <div class="msg">
            <div class="av av-ai">❄️</div>
            <div class="bubble bubble-ai">{welcome}</div>
        </div>
        """, unsafe_allow_html=True)

    for msg in history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg user">
                <div class="av av-usr">🧑</div>
                <div class="bubble bubble-usr">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg">
                <div class="av av-ai">❄️</div>
                <div class="bubble bubble-ai">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)

    # ─--------------─ Quick prompts ─----------------─
    if not history:
        st.markdown("<div style='font-size:.76rem;color:var(--muted);margin:14px 0 8px;'>Quick questions:</div>",
                    unsafe_allow_html=True)
        qc = st.columns(3)
        for qi, qp in enumerate(quick_prompts):
            with qc[qi % 3]:
                if st.button(qp, key=f"qp_{mode}_{qi}", use_container_width=True):
                    history.append({"role": "user", "content": qp})
                    with st.spinner("Thinking…"):
                        if mode == "generic":
                            reply = chain.chat_generic(qp, history[:-1])
                        else:
                            reply = chain.chat_job(qp, history[:-1],
                                                   st.session_state.jobs[st.session_state.active_job_idx])
                    history.append({"role": "assistant", "content": reply})
                    st.session_state[history_key] = history
                    st.rerun()

    st.markdown("---")
    user_msg = st.text_input("Message", placeholder="Type your question…",
                         label_visibility="collapsed", key=f"chat_inp_{mode}")
    col_l, col_mid, col_r = st.columns([2, 1, 2])
    with col_mid:
        send = st.button("Send →", use_container_width=True, key=f"send_{mode}")

    if send and user_msg.strip():
        history.append({"role": "user", "content": user_msg})
        with st.spinner("❄️ Thinking…"):
            if mode == "generic":
                reply = chain.chat_generic(user_msg, history[:-1])
            else:
                reply = chain.chat_job(user_msg, history[:-1],
                                       st.session_state.jobs[st.session_state.active_job_idx])
        history.append({"role": "assistant", "content": reply})
        st.session_state[history_key] = history
        st.rerun()

    cl1, cl2 = st.columns(2)
    with cl1:
        if history and st.button("🗑️ Clear this chat", use_container_width=True):
            st.session_state[history_key] = []
            st.rerun()
    with cl2:
        if history and st.button("📥 Export chat (.txt)", use_container_width=True):
            export = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history])
            st.download_button("⬇️ Download", data=export,
                               file_name="coldhire_chat.txt", mime="text/plain")


#--------------------------------------------
#  PAGE: INTERVIEW PREP
#-----------------------------------------------
def page_interview():
    st.markdown('<div class="pg-head"><div class="pg-title">🎯 Interview Prep</div>'
                '<div class="pg-sub">AI-generated interview questions tailored to the job.</div></div>',
                unsafe_allow_html=True)

    if not st.session_state.jobs:
        st.markdown("""
        <div class="card" style="text-align:center;padding:44px 24px;">
            <div style="font-size:2.5rem;margin-bottom:12px;">🎯</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:var(--muted);margin-bottom:8px;">No job loaded yet</div>
            <div style="font-size:.85rem;color:var(--muted);">Generate an email first to load a job.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("→ Go to Email Generator"):
            st.session_state.page = "generator"
            st.rerun()
        return

    job = st.session_state.jobs[st.session_state.active_job_idx]
    if len(st.session_state.jobs) > 1:
        jlabels = [f"{i+1}. {j.get('role','N/A')}" for i, j in enumerate(st.session_state.jobs)]
        chosen = st.selectbox("Select job:", jlabels, index=st.session_state.active_job_idx)
        st.session_state.active_job_idx = jlabels.index(chosen)
        job = st.session_state.jobs[st.session_state.active_job_idx]

    st.markdown(f"""
    <div class="jcard" style="margin-bottom:20px;">
        <div class="j-role">💼 {job.get('role','N/A')}</div>
        <div class="j-meta">🏢 {job.get('company','N/A') or 'N/A'} · 📅 {job.get('experience','N/A')}</div>
    </div>
    """, unsafe_allow_html=True)

    col_type, col_btn = st.columns([3, 1])
    with col_type:
        q_type = st.selectbox("Question type", ["mixed", "technical", "behavioral", "situational"])
    with col_btn:
        st.markdown("")
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        gen_q = st.button("Generate Questions ✨", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if gen_q:
        with st.spinner("🧠 Generating tailored interview questions…"):
            questions = chain.generate_interview_questions(job, q_type)
        if questions:
            st.session_state["interview_questions"] = questions
            st.rerun()
        else:
            st.error("Could not generate questions. Try again.")

    questions = st.session_state.get("interview_questions", [])
    if questions:
        st.markdown("---")
        st.markdown(f"""
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
             color:var(--cyan);margin-bottom:16px;">
             {len(questions)} Questions Generated
        </div>
        """, unsafe_allow_html=True)

        all_qs = "\n\n".join([f"Q{i+1}: {q['question']}\nTip: {q.get('tip','')}"
                              for i, q in enumerate(questions)])
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        st.download_button("⬇️ Export questions (.txt)", data=all_qs,
                        file_name="interview_prep.txt", mime="text/plain")
        st.markdown('</div>', unsafe_allow_html=True)

        for i, q in enumerate(questions):
            qtype = q.get("type", "technical").lower()
            diff  = q.get("difficulty", "medium").lower()
            diff_class = {"hard": "q-hard", "medium": "q-medium", "easy": "q-easy"}.get(diff, "q-medium")
            st.markdown(f"""
            <div class="q-card">
                <div>
                    <span class="q-type-badge q-{qtype}">{qtype}</span>
                    <span style="font-size:.72rem;margin-left:8px;" class="{diff_class}">● {diff}</span>
                </div>
                <div class="q-text">Q{i+1}. {q.get('question','')}</div>
                <div class="q-tip">💡 {q.get('tip','')}</div>
            </div>
            """, unsafe_allow_html=True)


#--------------------------------------
#  PAGE: JOB FIT ANALYSER
#------------------------------------
def page_fit():
    st.markdown('<div class="pg-head"><div class="pg-title">📊 Job Fit Analyser</div>'
                '<div class="pg-sub">See how well you match the job requirements.</div></div>',
                unsafe_allow_html=True)

    if not st.session_state.jobs:
        st.markdown("""
        <div class="card" style="text-align:center;padding:44px 24px;">
            <div style="font-size:2.5rem;margin-bottom:12px;">📊</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:var(--muted);">No job loaded yet</div>
        </div>""", unsafe_allow_html=True)
        if st.button("→ Go to Email Generator"):
            st.session_state.page = "generator"
            st.rerun()
        return

    job = st.session_state.jobs[st.session_state.active_job_idx]

    st.markdown('<div class="card"><div class="card-label">👤 Your Profile for Analysis</div>',
                unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        skills_input = st.text_area("Your skills (comma-separated)",
                                    value=st.session_state.profile_skills,
                                    height=100, placeholder="Python, React, SQL…")
    with cb:
        exp_input = st.text_input("Your experience",
                                  value=st.session_state.profile_exp,
                                  placeholder="e.g. 3 years backend development")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    analyse = st.button("Analyse My Fit 🔍", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

    if analyse:
        skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
        with st.spinner("🔍 Analysing fit…"):
            result = chain.analyse_job_fit(job, skills_list, exp_input)
        st.session_state["fit_result"] = result

    result = st.session_state.get("fit_result")
    if result:
        st.markdown("---")
        score   = result.get("fit_score", 0)
        verdict = result.get("verdict", "")
        v_class = {"Strong Fit": "verdict-strong", "Good Fit": "verdict-good",
                   "Partial Fit": "verdict-partial", "Weak Fit": "verdict-weak"}.get(verdict, "verdict-good")

        r1, r2, r3 = st.columns([1, 2, 2])
        with r1:
            st.markdown(f"""
            <div class="fit-wrap">
                <div class="fit-score-num">{score}</div>
                <div style="font-size:.7rem;color:var(--muted);margin-bottom:4px;">/ 100</div>
                <div class="fit-verdict {v_class}">{verdict}</div>
            </div>
            """, unsafe_allow_html=True)
            # Progress bar
            fill = max(0, min(100, score))
            st.markdown(f'<div class="pbar"><div class="pfill" style="width:{fill}%"></div></div>',
                        unsafe_allow_html=True)

        with r2:
            matches = result.get("matching_skills", [])
            st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:.8rem;font-weight:700;
                 color:var(--emerald);margin-bottom:8px;">✅ Matching Skills</div>""", unsafe_allow_html=True)
            if matches:
                st.markdown(" ".join(f'<span class="tag-match">{s}</span>' for s in matches),
                            unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:var(--muted);font-size:.82rem;'>None detected</span>",
                            unsafe_allow_html=True)

        with r3:
            missing = result.get("missing_skills", [])
            st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:.8rem;font-weight:700;
                 color:var(--rose);margin-bottom:8px;">❌ Skill Gaps</div>""", unsafe_allow_html=True)
            if missing:
                st.markdown(" ".join(f'<span class="tag-missing">{s}</span>' for s in missing),
                            unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:var(--muted);font-size:.82rem;'>No major gaps 🎉</span>",
                            unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div class="card">
            <div class="card-label">💡 AI Recommendation</div>
            <div style="font-size:.9rem;color:var(--text);line-height:1.7;">{result.get('recommendation','')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Strengths & Gaps
        sg1, sg2 = st.columns(2)
        with sg1:
            strengths = result.get("strengths", [])
            st.markdown('<div class="card-label">💪 Strengths</div>', unsafe_allow_html=True)
            for s in strengths:
                st.markdown(f"<div style='font-size:.84rem;color:var(--text);margin-bottom:6px;'>✦ {s}</div>",
                            unsafe_allow_html=True)
        with sg2:
            gaps = result.get("gaps", [])
            st.markdown('<div class="card-label" style="color:var(--amber);">⚠️ Gaps to Address</div>',
                        unsafe_allow_html=True)
            for g in gaps:
                st.markdown(f"<div style='font-size:.84rem;color:var(--text);margin-bottom:6px;'>▸ {g}</div>",
                            unsafe_allow_html=True)


#-----------------------------
#  PAGE: MORE TOOLS
#-----------------------------
def page_tools():
    st.markdown('<div class="pg-head"><div class="pg-title">🛠️ More Tools</div>'
                '<div class="pg-sub">Cover letter, LinkedIn note, salary negotiation, and job summary.</div></div>',
                unsafe_allow_html=True)

    if not st.session_state.jobs:
        st.markdown("""
        <div class="card" style="text-align:center;padding:44px 24px;">
            <div style="font-size:2.5rem;margin-bottom:12px;">🛠️</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:var(--muted);">Load a job first</div>
        </div>""", unsafe_allow_html=True)
        if st.button("→ Go to Email Generator"):
            st.session_state.page = "generator"
            st.rerun()
        return

    job = st.session_state.jobs[st.session_state.active_job_idx]

    tool_tabs = st.tabs(["📄 Cover Letter", "🔗 LinkedIn Note", "💰 Salary Script", "🔍 Job Summary"])

    # ── Cover Letter ──
    with tool_tabs[0]:
        st.markdown('<div class="card-label">📄 AI Cover Letter Generator</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="infobox">
            <span class="infobox-icon">📄</span>
            Generates a professional cover letter tailored to the job, using your profile information.
        </div>
        """, unsafe_allow_html=True)
        cl1, cl2 = st.columns(2)
        with cl1:
            cl_name   = st.text_input("Your name",    value=st.session_state.profile_name)
            cl_role   = st.text_input("Current role", value=st.session_state.profile_role)
            cl_exp    = st.text_input("Years of exp.", value=st.session_state.profile_exp)
        with cl2:
            cl_skills = st.text_input("Your skills",  value=st.session_state.profile_skills)
            cl_achiev = st.text_area("Key achievements", value=st.session_state.profile_achievements, height=100)

        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        gen_cl = st.button("Generate Cover Letter ✨", key="gen_cl")
        st.markdown("</div>", unsafe_allow_html=True)

        if gen_cl:
            with st.spinner("📄 Writing cover letter…"):
                cl_text = chain.write_cover_letter(job, {
                    "name": cl_name, "current_role": cl_role,
                    "skills": [s.strip() for s in cl_skills.split(",")],
                    "years_exp": cl_exp, "achievements": cl_achiev,
                })
            st.session_state["cover_letter"] = cl_text

        if st.session_state.get("cover_letter"):
            st.markdown(f'<div class="email-output" style="margin-top:16px;">{st.session_state["cover_letter"]}</div>',
                        unsafe_allow_html=True)
            st.download_button("⬇️ Download Cover Letter",
                               data=st.session_state["cover_letter"],
                               file_name="cover_letter.txt", mime="text/plain")

    # ─-----------─ LinkedIn Note ─-----------─
    with tool_tabs[1]:
        st.markdown('<div class="card-label">🔗 LinkedIn Connection Note</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="infobox">
            <span class="infobox-icon">🔗</span>
            A 300-character personalised note for a LinkedIn connection request to the hiring manager.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        gen_li = st.button("Generate LinkedIn Note ✨", key="gen_li")
        st.markdown("</div>", unsafe_allow_html=True)

        if gen_li:
            with st.spinner("🔗 Crafting your note…"):
                li_note = chain.write_linkedin_note(job,
                                                     st.session_state.profile_name,
                                                     st.session_state.profile_company)
            st.session_state["linkedin_note"] = li_note

        if st.session_state.get("linkedin_note"):
            note = st.session_state["linkedin_note"]
            char_count = len(note)
            color = "var(--emerald)" if char_count <= 300 else "var(--rose)"
            st.markdown(f"""
            <div class="email-output" style="margin-top:16px;">{note}</div>
            <div style="font-size:.75rem;color:{color};margin-top:6px;text-align:right;">{char_count}/300 characters</div>
            """, unsafe_allow_html=True)
            if st.button("📋 Copy note", key="cp_li"):
                st.code(note)

    # ──------------- Salary Script ---------------──
    with tool_tabs[2]:
        st.markdown('<div class="card-label">💰 Salary Negotiation Script</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="infobox">
            <span class="infobox-icon">💰</span>
            Generates a professional salary counter-offer email/script after receiving a job offer.
        </div>
        """, unsafe_allow_html=True)
        sa1, sa2 = st.columns(2)
        with sa1:
            curr_sal = st.text_input("Current/Offered salary", placeholder="e.g. ₹12 LPA or $80,000")
        with sa2:
            exp_sal  = st.text_input("Expected salary",        placeholder="e.g. ₹16 LPA or $95,000")

        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        gen_sal = st.button("Generate Negotiation Script ✨", key="gen_sal")
        st.markdown("</div>", unsafe_allow_html=True)

        if gen_sal and curr_sal and exp_sal:
            with st.spinner("💰 Writing negotiation script…"):
                sal_script = chain.generate_salary_script(job, curr_sal, exp_sal)
            st.session_state["salary_script"] = sal_script

        if st.session_state.get("salary_script"):
            st.markdown(f'<div class="email-output" style="margin-top:16px;">{st.session_state["salary_script"]}</div>',
                        unsafe_allow_html=True)
            st.download_button("⬇️ Download script",
                               data=st.session_state["salary_script"],
                               file_name="salary_negotiation.txt", mime="text/plain")

    # ──-------- Job Summary ─-----------------─
    with tool_tabs[3]:
        st.markdown('<div class="card-label">🔍 Job TL;DR + Red Flags</div>', unsafe_allow_html=True)
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        gen_sum = st.button("Summarise Job ✨", key="gen_sum")
        st.markdown("</div>", unsafe_allow_html=True)

        if gen_sum:
            with st.spinner("🔍 Summarising…"):
                summary = chain.summarise_job(job)
            st.session_state["job_summary"] = summary

        summary = st.session_state.get("job_summary")
        if summary:
            st.markdown("---")
            su1, su2, su3 = st.columns(3)
            with su1:
                st.markdown('<div class="card-label">📌 TL;DR</div>', unsafe_allow_html=True)
                for pt in summary.get("tldr", []):
                    st.markdown(f"<div style='font-size:.85rem;color:var(--text);margin-bottom:8px;line-height:1.5;'>✦ {pt}</div>",
                                unsafe_allow_html=True)
            with su2:
                st.markdown('<div class="card-label" style="color:var(--indigo);">🏢 Culture Hints</div>',
                            unsafe_allow_html=True)
                for pt in summary.get("culture_hints", []):
                    st.markdown(f"<div style='font-size:.85rem;color:var(--text);margin-bottom:8px;line-height:1.5;'>✦ {pt}</div>",
                                unsafe_allow_html=True)
            with su3:
                red_flags = summary.get("red_flags", [])
                st.markdown('<div class="card-label" style="color:var(--rose);">🚩 Red Flags</div>',
                            unsafe_allow_html=True)
                if red_flags:
                    for pt in red_flags:
                        st.markdown(f"<div style='font-size:.85rem;color:var(--rose);margin-bottom:8px;line-height:1.5;'>⚠ {pt}</div>",
                                    unsafe_allow_html=True)
                else:
                    st.markdown("<div style='font-size:.85rem;color:var(--emerald);'>No red flags detected 🎉</div>",
                                unsafe_allow_html=True)


#-----------------------------------------
#  PAGE: HISTORY
#-----------------------------------
def page_history():
    st.markdown('<div class="pg-head"><div class="pg-title">🗂️ History</div>'
                '<div class="pg-sub">All emails generated in this session.</div></div>',
                unsafe_allow_html=True)

    history = st.session_state.get("history", [])
    if not history:
        st.markdown("""
        <div class="card" style="text-align:center;padding:52px 24px;">
            <div style="font-size:3rem;margin-bottom:12px;">📭</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:var(--muted);margin-bottom:8px;">
                No history yet
            </div>
            <div style="font-size:.85rem;color:var(--muted);">Generate your first cold email to see it here.</div>
        </div>""", unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="stat-mini">
        <div class="scard"><div class="scard-val">{len(history)}</div><div class="scard-lbl">Sessions</div></div>
        <div class="scard"><div class="scard-val">{sum(len(s.get('emails',[])) for s in history)}</div><div class="scard-lbl">Total Emails</div></div>
    </div>
    """, unsafe_allow_html=True)

    for idx, session in enumerate(reversed(history)):
        url    = session.get("url", "N/A")
        emails = session.get("emails", [])
        label  = f"📌 Session {len(history)-idx}  ·  {len(emails)} email(s)  ·  {url[:55]}…"
        with st.expander(label, expanded=(idx == 0)):
            for j, entry in enumerate(emails):
                role = entry.get("job", {}).get("role", "N/A")
                st.markdown(f"<div class='j-role' style='margin-bottom:8px;'>💼 {role}</div>",
                            unsafe_allow_html=True)
                st.code(entry.get("email", ""), language="markdown")
                st.download_button(
                    "⬇️ Download",
                    data=entry.get("email", ""),
                    file_name=f"email_s{len(history)-idx}_j{j+1}.txt",
                    key=f"hist_{idx}_{j}",
                )
                st.markdown("---")


#--------------------------------------
#  PAGE: SETTINGS
#-------------------------------------
def page_settings():
    st.markdown('<div class="pg-head"><div class="pg-title">⚙️ Settings</div>'
                '<div class="pg-sub">Personalise your identity, tone, and preferences.</div></div>',
                unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-label">👤 Your Profile</div>',
                unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        pname    = st.text_input("Your Name",      value=st.session_state.profile_name)
        pcompany = st.text_input("Company Name",   value=st.session_state.profile_company)
        prole    = st.text_input("Your Role",      value=st.session_state.profile_role)
    with s2:
        pskills  = st.text_input("Your Skills",    value=st.session_state.profile_skills)
        pexp     = st.text_input("Experience",     value=st.session_state.profile_exp)
        pachiev  = st.text_area("Key Achievements", value=st.session_state.profile_achievements, height=80)

    ptone = st.selectbox("Default Tone",
                         ["Professional","Friendly","Confident","Concise","Storytelling"],
                         index=["Professional","Friendly","Confident","Concise","Storytelling"].index(st.session_state.tone))

    if st.button("💾 Save Profile"):
        st.session_state.profile_name         = pname
        st.session_state.profile_company      = pcompany
        st.session_state.profile_role         = prole
        st.session_state.profile_skills       = pskills
        st.session_state.profile_exp          = pexp
        st.session_state.profile_achievements = pachiev
        st.session_state.tone                 = ptone
        st.success("✅ Profile saved!")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:14px;"><div class="card-label">🧹 Data Management</div>',
                unsafe_allow_html=True)
    if st.button("🗑️ Clear All Session Data & History"):
        for k in ["jobs","emails","chat_history_generic","chat_history_job",
                  "history","generated","gen_count","fit_result",
                  "cover_letter","linkedin_note","salary_script","job_summary","interview_questions"]:
            st.session_state.pop(k, None)
        init_state()
        st.success("✅ Cleared!")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top:14px;">
        <div class="card-label">ℹ️ About</div>
        <div style="font-size:.87rem;color:var(--muted2);line-height:1.9;">
            <b style="color:var(--text)">ColdHire AI v3.0</b> — Intelligent outreach platform.<br>
            <b style="color:var(--cyan)">LangChain</b> · <b style="color:var(--indigo)">Groq LLaMA 3.1</b> ·
            <b style="color:var(--emerald)">ChromaDB</b> · <b style="color:var(--text)">Streamlit</b><br><br>
            Features: Cold Email · Dual-Mode Chatbot · Interview Prep ·<br>
            Job Fit Analysis · Cover Letter · LinkedIn Note · Salary Negotiation
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    


#--------------------------------
#  ROUTER
#-----------------------------------
page = st.session_state.page
if   page == "generator": page_generator()
elif page == "chatbot":   page_chatbot()
elif page == "interview": page_interview()
elif page == "fit":       page_fit()
elif page == "tools":     page_tools()
elif page == "history":   page_history()
elif page == "settings":  page_settings()