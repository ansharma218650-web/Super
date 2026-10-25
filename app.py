"""SuperTET PRT Practice - chalkboard & notebook themed exam practice app."""
import html
import json
import random
import time
import uuid

import pandas as pd
import streamlit as st

import utils as U

st.set_page_config(
    page_title="SuperTET PRT Practice",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)
S = st.session_state
NEW = "➕ Create new"


# =====================================================================
# STYLE
# =====================================================================
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600;700&display=swap');
:root{--board:#14342B;--board2:#1D4A3C;--chalk:#F2EFE4;--gold:#F2B01E;--paper:#EEF2EE;--card:#FFFFFF;--ink:#1A2422;--muted:#5E6B66;--line:#D8E0DA;--ok:#1E8A5E;--ok-bg:#E3F4EB;--bad:#C2413A;--bad-bg:#FBE9E7;--margin:#E8A9A4;--rule:#DDE7F1;--wood:#9A6B3E;}
.stApp,.stApp p,.stApp li,.stApp label,.stApp button,.stApp input,.stApp textarea,.stApp td,.stApp th,.stApp [data-testid="stMarkdownContainer"],.stApp [data-testid="stCaptionContainer"],.stApp [data-baseweb="select"] *,.stApp [data-baseweb="tab"]{font-family:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif !important;}
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.disp{font-family:'Bricolage Grotesque','Figtree',sans-serif !important;letter-spacing:-.015em;color:var(--ink);}
.stApp{background:var(--paper);}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}
.block-container{padding-top:2.2rem;padding-bottom:4rem;max-width:1120px;}
.stApp h3{font-size:1.45rem;margin-top:.4rem;}

/* sidebar */
section[data-testid="stSidebar"]{background:var(--board);border-right:6px solid var(--wood);}
section[data-testid="stSidebar"] *{color:var(--chalk);}
section[data-testid="stSidebar"] .stButton>button{background:transparent;border:1px solid transparent;justify-content:flex-start;text-align:left;font-weight:600;padding:.62rem .9rem;color:var(--chalk);}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.18);}
.brand{padding:.4rem .2rem 1.1rem;}
.brand b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-size:1.7rem;line-height:1.05;color:var(--gold);}
.brand span{font-size:.85rem;opacity:.75;}
.side-note{font-size:.8rem;opacity:.65;padding:.2rem .3rem;}

/* buttons / inputs */
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"]>button{width:100%;border-radius:10px;font-weight:600;min-height:2.7rem;}
[data-testid="stMetric"]{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:.8rem 1rem;}
[data-testid="stMetricLabel"]{color:var(--muted);}
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"]) {border-radius:16px;}
.stTabs [data-baseweb="tab-list"]{gap:.4rem;}
.stTabs [data-baseweb="tab"]{border-radius:10px 10px 0 0;font-weight:600;}

/* hero - the chalkboard */
.hero{background:radial-gradient(1200px 400px at 20% -10%,rgba(255,255,255,.07),transparent 60%),var(--board);border:7px solid var(--wood);border-radius:14px;box-shadow:inset 0 0 50px rgba(0,0,0,.4),0 18px 30px -22px rgba(20,52,43,.8);padding:2rem 2.2rem;display:flex;flex-wrap:wrap;gap:1.6rem 2.4rem;align-items:center;justify-content:space-between;margin-bottom:1.6rem;}
.hero-text{flex:1 1 340px;max-width:560px;}
.hero h1{font-size:2.6rem;line-height:1.08;color:var(--chalk) !important;margin:0 0 .7rem;padding:0;font-weight:800;}
.hero p{color:rgba(242,239,228,.82) !important;font-size:1.05rem;line-height:1.55;margin:0;}
.hero-stats{display:flex;gap:.9rem;flex-wrap:wrap;}
.hero-stat{border:2px dashed rgba(242,239,228,.45);border-radius:12px;padding:.8rem 1.1rem;min-width:104px;text-align:center;}
.hero-stat b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-size:2.1rem;color:var(--gold);line-height:1;}
.hero-stat span{font-size:.85rem;color:var(--chalk);opacity:.85;}

/* cards & chips */
.card-title{font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:1.2rem;color:var(--ink);line-height:1.2;}
.card-sub{color:var(--muted);font-size:.9rem;margin:.2rem 0 .6rem;}
.chips{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.5rem;}
.chip{display:inline-block;background:#E6EEE9;color:var(--board2);border-radius:999px;padding:.18rem .7rem;font-size:.82rem;font-weight:600;}
.chip.gold{background:#FBEFC9;color:#7A5600;}
.chip.red{background:var(--bad-bg);color:var(--bad);}
.chip.green{background:var(--ok-bg);color:var(--ok);}
.page-title{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:2rem;margin:0 0 .2rem;color:var(--ink);}
.page-sub{color:var(--muted);margin:0 0 1.1rem;}
[class*="st-key-sub_"],[class*="st-key-ser_"]{background:var(--card);}

/* the notebook page that holds each question */
.st-key-qcard{position:relative;background-color:#FEFEFC;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 33px,var(--rule) 33px,var(--rule) 34px);border:1px solid var(--line);border-left:0;border-radius:6px 16px 16px 6px;padding:.3rem 1.4rem 1.1rem 4.4rem !important;box-shadow:0 14px 26px -20px rgba(20,52,43,.55);gap:0 !important;margin-bottom:.9rem;}
.st-key-qcard::before{content:"";position:absolute;left:3.1rem;top:0;bottom:0;width:2px;background:var(--margin);}
.st-key-qcard::after{content:"";position:absolute;left:.8rem;top:0;bottom:0;width:16px;background:radial-gradient(circle at 8px 50%,var(--paper) 0 6.5px,transparent 7.5px) 0 0/16px 130px repeat-y;}
.st-key-qcard [data-testid="stMarkdownContainer"] p{font-size:1.14rem;line-height:34px;margin:0;color:var(--ink);}
.qmeta{height:34px;line-height:34px;font-size:.85rem;color:var(--muted);font-weight:600;}

/* radio options styled as answer cards */
.st-key-optbox div[role="radiogroup"]{gap:.55rem;}
.st-key-optbox div[role="radiogroup"]>label{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:.8rem 1rem;margin:0;width:100%;transition:border-color .15s,background .15s;}
.st-key-optbox div[role="radiogroup"]>label:hover{border-color:var(--board2);}
.st-key-optbox div[role="radiogroup"]>label:has(input:checked){border-color:var(--board2);background:#E6F0EA;}

/* revealed option cards */
.opt{display:flex;align-items:center;gap:.85rem;padding:.72rem 1rem;margin:.5rem 0;background:#fff;border:1.5px solid var(--line);border-radius:12px;color:var(--ink);}
.opt .ltr{flex:0 0 auto;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-weight:700;font-size:.9rem;background:#E9EFEB;color:var(--board2);}
.opt .tag{margin-left:auto;font-size:.78rem;font-weight:700;white-space:nowrap;}
.opt.ok{background:var(--ok-bg);border-color:var(--ok);}
.opt.ok .ltr{background:var(--ok);color:#fff;}
.opt.ok .tag{color:var(--ok);}
.opt.bad{background:var(--bad-bg);border-color:var(--bad);}
.opt.bad .ltr{background:var(--bad);color:#fff;}
.opt.bad .tag{color:var(--bad);}
.verdict{border-radius:12px;padding:.75rem 1rem;font-weight:600;margin:.4rem 0 .6rem;}
.verdict.ok{background:var(--ok-bg);color:#126343;border:1px solid #A8DCC3;}
.verdict.bad{background:var(--bad-bg);color:#8E2A24;border:1px solid #EDB6B1;}

/* timer */
.timer{background:var(--board);color:var(--chalk);border-radius:14px;border:3px solid var(--wood);padding:.45rem 1rem;text-align:center;}
.timer small{display:block;font-size:.75rem;opacity:.75;}
.timer b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.9rem;font-variant-numeric:tabular-nums;line-height:1.1;}
.timer.warn{background:#7A1F1A;}
.timer.warn b{color:#FFD9A0;}

/* score ring and tiles */
.ring{width:158px;height:158px;border-radius:50%;background:conic-gradient(var(--ok) calc(var(--p) * 1%),#D8E0DA 0);display:grid;place-items:center;margin:0 auto;}
.ring-in{width:124px;height:124px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.ring-in b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.9rem;line-height:1;color:var(--ink);}
.ring-in span{font-size:.8rem;color:var(--muted);}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.7rem;}
.tile{background:#F4F7F5;border:1px solid var(--line);border-radius:12px;padding:.7rem .9rem;}
.tile b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-size:1.6rem;line-height:1.1;}
.tile span{font-size:.82rem;color:var(--muted);}
.tile.ok b{color:var(--ok);} .tile.bad b{color:var(--bad);}
.legend{display:flex;flex-wrap:wrap;gap:.5rem .9rem;font-size:.8rem;color:var(--muted);margin-top:.5rem;}
.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:.3rem;vertical-align:-1px;border:1px solid var(--line);}
@media (max-width:640px){.hero{padding:1.3rem;}.hero h1{font-size:1.9rem;}.st-key-qcard{padding-left:3.6rem !important;}.st-key-qcard::before{left:2.5rem;}}
@media (prefers-reduced-motion:reduce){*{transition:none !important;}}
"""


def H(s: str) -> str:
    """Collapse an indented HTML snippet so markdown never mistakes it for a code block."""
    return "".join(line.strip() for line in s.splitlines())


def esc(x) -> str:
    return html.escape(str(x))


def md(s: str) -> None:
    st.markdown(H(s), unsafe_allow_html=True)


def show_df(data) -> None:
    try:
        st.dataframe(data, width="stretch", hide_index=True)
    except Exception:  # older Streamlit versions
        st.dataframe(data, use_container_width=True, hide_index=True)


def page_head(title: str, sub: str = "") -> None:
    md(f'<div class="page-title">{esc(title)}</div><div class="page-sub">{esc(sub)}</div>')


def option_cards(q: dict, picked=None) -> None:
    """Revealed answer options: green for correct, red for the wrong pick."""
    rows = []
    for k, o in enumerate(q["options"]):
        cls, tag = "opt", ""
        if k == q["answer"]:
            cls += " ok"
            tag = "Your answer" if picked == k else "Correct answer"
        elif k == picked:
            cls += " bad"
            tag = "Your answer"
        tag_html = f'<span class="tag">{tag}</span>' if tag else ""
        rows.append(f'<div class="{cls}"><span class="ltr">{chr(65 + k)}</span><span>{esc(o)}</span>{tag_html}</div>')
    md("".join(rows))


def opt_fmt(opts):
    return lambda k: f"{chr(65 + k)}.  {opts[k]}"


def ring(pct: float, big: str, small: str) -> str:
    pct = max(0.0, min(100.0, pct))
    return H(f'<div class="ring" style="--p:{pct:.0f}"><div class="ring-in"><b>{esc(big)}</b><span>{esc(small)}</span></div></div>')


def mmss(sec: int) -> str:
    sec = max(0, int(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def go(page: str) -> None:
    S.page = page


# =====================================================================
# HOME
# =====================================================================
def open_subject(slug):
    S.p_subject = slug
    S.page = "practice"


def open_series(series):
    S.t_series = series
    S.page = "tests"


def load_demo():
    U.seed_sample()


def home_page():
    subjects = U.list_subjects()
    series = U.list_series()
    pcount = {slug: len(U.load_practice(slug)["questions"]) for slug, _ in subjects}
    n_q = sum(pcount.values())
    n_t = sum(len(U.list_tests(s)) for s in series)

    md(f"""
        <div class="hero">
          <div class="hero-text">
            <h1>Practice like the paper is tomorrow.</h1>
            <p>Subject-wise MCQs with instant explanations, and timed mock tests that feel like the real exam.</p>
          </div>
          <div class="hero-stats">
            <div class="hero-stat"><b>{len(subjects)}</b><span>subjects</span></div>
            <div class="hero-stat"><b>{n_q}</b><span>questions</span></div>
            <div class="hero-stat"><b>{n_t}</b><span>mock tests</span></div>
          </div>
        </div>""")

    if not U.has_content():
        with st.container(border=True):
            st.markdown("#### Nothing here yet")
            st.write("Add your own questions from the **Admin** page, or load a small demo set to see how the app looks.")
            a, b = st.columns(2)
            a.button("Load demo questions", type="primary", on_click=load_demo)
            b.button("Go to Admin", on_click=go, args=("admin",))
        return

    if subjects:
        st.markdown("### Practice by subject")
        for r in range(0, len(subjects), 3):
            cols = st.columns(3)
            for col, (slug, name) in zip(cols, subjects[r:r + 3]):
                with col:
                    with st.container(border=True, key=f"sub_{slug}"):
                        md(f'<div class="card-title">{esc(name)}</div><div class="card-sub">{pcount[slug]} questions</div>')
                        st.button("Start practice", key=f"go_{slug}", on_click=open_subject, args=(slug,),
                                  disabled=pcount[slug] == 0)

    if series:
        st.markdown("### Mock test series")
        for r in range(0, len(series), 3):
            cols = st.columns(3)
            for col, s in zip(cols, series[r:r + 3]):
                with col:
                    with st.container(border=True, key=f"ser_{s}"):
                        n = len(U.list_tests(s))
                        md(f'<div class="card-title">{esc(U.pretty(s))}</div><div class="card-sub">{n} test{"s" if n != 1 else ""}</div>')
                        st.button("Open series", key=f"gs_{s}", on_click=open_series, args=(s,))

    hist = U.load_results()
    if hist:
        st.markdown("### Your recent mock scores")
        df = _history_df(hist)
        c1, c2 = st.columns([2, 1])
        with c1:
            st.line_chart(df.iloc[::-1].reset_index(drop=True)["Score %"], height=220)
        with c2:
            md(f"""<div class="tiles">
                <div class="tile"><b>{len(df)}</b><span>tests attempted</span></div>
                <div class="tile ok"><b>{df['Score %'].max():.0f}%</b><span>best score</span></div>
                <div class="tile"><b>{df['Score %'].mean():.0f}%</b><span>average</span></div></div>""")


def _history_df(hist) -> pd.DataFrame:
    df = pd.DataFrame(hist)
    for c in ("score", "max_score", "correct", "wrong", "unattempted"):
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df["Score %"] = (df["score"] / df["max_score"].where(df["max_score"] > 0, 1) * 100).clip(lower=0).round(1)
    return df


# =====================================================================
# PRACTICE
# =====================================================================
def _new_practice_state(n, shuffle):
    order = list(range(n))
    if shuffle:
        random.shuffle(order)
    S.p = {"order": order, "i": 0, "picked": {}, "checked": {}, "run": uuid.uuid4().hex[:6]}


def _p_go(d):
    S.p["i"] = max(0, min(len(S.p["order"]) - 1, S.p["i"] + d))


def _p_jump(j):
    S.p["i"] = j


def _p_restart(n, shuffle):
    _new_practice_state(n, shuffle)


def practice_page():
    page_head("Practice questions", "Pick a subject, answer, and see the explanation straight away.")
    subjects = U.list_subjects()
    if not subjects:
        st.info("No subjects yet. Add questions from the Admin page.")
        return
    names = dict(subjects)
    # keep widget values alive when the user visits other pages and comes back
    if S.get("p_subject") not in names:
        S.pop("p_subject", None)
    if "p_shuffle" in S:
        S.p_shuffle = S.p_shuffle
    if "p_subject" in S:
        S.p_subject = S.p_subject

    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 1], vertical_alignment="bottom")
        slug = c1.selectbox("Subject", list(names), format_func=names.get, key="p_subject")
        shuffle = c2.checkbox("Shuffle", key="p_shuffle")
        qs = U.load_practice(slug)["questions"]
        if not qs:
            st.warning("This subject has no questions yet.")
            return
        sig = (slug, shuffle, len(qs))
        if S.get("p_sig") != sig:
            S.p_sig = sig
            _new_practice_state(len(qs), shuffle)
        c3.button("Restart", on_click=_p_restart, args=(len(qs), shuffle))

    P = S.p
    n, i = len(P["order"]), P["i"]
    q = qs[P["order"][i]]
    done = len(P["checked"])
    correct = sum(1 for k in P["checked"] if P["picked"][k] == qs[P["order"][k]]["answer"])
    acc = f"{correct / done * 100:.0f}%" if done else "–"
    md(f"""<div class="chips" style="margin:.2rem 0 .5rem">
        <span class="chip">Attempted {done}/{n}</span>
        <span class="chip green">Correct {correct}</span>
        <span class="chip red">Wrong {done - correct}</span>
        <span class="chip gold">Accuracy {acc}</span></div>""")
    st.progress(done / n)

    if done == n:
        _practice_summary(correct, n, shuffle)

    checked = i in P["checked"]
    with st.container(key="qcard"):
        md(f'<div class="qmeta">Question {i + 1} of {n}</div>')
        st.markdown(q["question"])

    if checked:
        option_cards(q, P["picked"][i])
        choice = P["picked"][i]
    else:
        with st.container(key="optbox"):
            choice = st.radio(
                "Options", list(range(len(q["options"]))), index=P["picked"].get(i),
                format_func=opt_fmt(q["options"]), key=f"p_{P['run']}_{slug}_{i}",
                label_visibility="collapsed",
            )

    b1, b2, b3 = st.columns(3)
    b1.button("⬅ Previous", disabled=(i == 0), on_click=_p_go, args=(-1,))
    if b2.button("Check answer", disabled=checked, type="primary"):
        if choice is None:
            st.warning("Select an option first.")
        else:
            P["picked"][i] = choice
            P["checked"][i] = True
            st.rerun()
    b3.button("Next ➡", disabled=(i == n - 1), on_click=_p_go, args=(1,))

    if checked:
        if P["picked"][i] == q["answer"]:
            md('<div class="verdict ok">Correct. Well done!</div>')
        else:
            md('<div class="verdict bad">Not quite. The correct answer is highlighted above.</div>')
        with st.expander("💡 Explanation", expanded=P["picked"][i] != q["answer"]):
            st.write(q["explanation"] or "No explanation added for this question.")

    with st.expander("Jump to a question"):
        per = 10
        for r in range(0, n, per):
            cols = st.columns(per)
            for off, col in enumerate(cols):
                j = r + off
                if j >= n:
                    break
                mark = ""
                if j in P["checked"]:
                    mark = "✓" if P["picked"][j] == qs[P["order"][j]]["answer"] else "✗"
                col.button(f"{j + 1}{mark}", key=f"pj_{j}", on_click=_p_jump, args=(j,),
                           type="primary" if j == i else "secondary")


def _practice_summary(correct, n, shuffle):
    pct = correct / n * 100
    with st.container(border=True):
        a, b = st.columns([1, 3], vertical_alignment="center")
        a.markdown(ring(pct, f"{pct:.0f}%", "accuracy"), unsafe_allow_html=True)
        with b:
            msg = "Excellent work!" if pct >= 80 else "Good effort. Review the wrong answers." if pct >= 50 else "Keep going. Read the explanations and try again."
            st.markdown(f"#### Set complete: {correct} of {n} correct")
            st.write(msg)
            st.button("Practice this set again", key="again", type="primary", on_click=_p_restart, args=(n, shuffle))


# =====================================================================
# TEST SERIES
# =====================================================================
def _start_test(series, test):
    d = U.load_test(series, test)
    now = time.time()
    S.t = {
        "series": series, "test": test, "title": d["title"], "qs": d["questions"],
        "marks": d.get("marks_per_question", 1), "neg": d.get("negative_marks", 0),
        "start": now, "end": now + d.get("duration_minutes", 30) * 60, "finished": None,
        "answers": {}, "flags": set(), "cur": 0, "submitted": False, "saved": False,
        "run": uuid.uuid4().hex[:6],
    }


def _t_goto(j):
    S.t["cur"] = max(0, min(len(S.t["qs"]) - 1, j))


def _t_submit():
    S.t["submitted"] = True
    S.t["finished"] = min(time.time(), S.t["end"])


def _t_clear(cur, key):
    S.t["answers"].pop(cur, None)
    S.pop(key, None)


def _t_flag(cur):
    f = S.t["flags"]
    f.discard(cur) if cur in f else f.add(cur)


def _t_exit():
    S.t = None


def test_menu():
    series = U.list_series()
    if not series:
        st.info("No test series yet. Add one from the Admin page.")
        return
    if S.get("t_series") not in series:
        S.pop("t_series", None)
    elif "t_series" in S:
        S.t_series = S.t_series
    s = st.selectbox("Test series", series, format_func=U.pretty, key="t_series")
    tests = U.list_tests(s)
    hist = U.load_results()
    if not tests:
        st.warning("This series has no tests yet.")
    for slug, title in tests:
        d = U.load_test(s, slug)
        nq, mpq = len(d["questions"]), d.get("marks_per_question", 1)
        mine = [r for r in hist if r["series"] == U.pretty(s) and r["test"] == title]
        best = ""
        if mine:
            b = max(mine, key=lambda r: float(r["score"]))
            best = f'<span class="chip green">Best {float(b["score"]):g}/{float(b["max_score"]):g}</span>'
        with st.container(border=True):
            a, b = st.columns([4, 1], vertical_alignment="center")
            with a:
                md(f"""<div class="card-title">{esc(title)}</div>
                    <div class="chips"><span class="chip">{nq} questions</span>
                    <span class="chip">{d.get('duration_minutes', 30)} min</span>
                    <span class="chip gold">+{mpq:g} / -{d.get('negative_marks', 0):g}</span>{best}</div>""")
            b.button("Start test", key=f"start_{s}_{slug}", type="primary", disabled=not nq,
                     on_click=_start_test, args=(s, slug))
    if hist:
        with st.expander("📈 My previous attempts", expanded=False):
            df = _history_df(hist)
            show_df(df.rename(columns={"time": "When", "series": "Series", "test": "Test", "score": "Score",
                                       "max_score": "Out of", "correct": "Correct", "wrong": "Wrong",
                                       "unattempted": "Skipped"}))


@st.fragment(run_every=1)
def timer_box():
    t = S.t
    left = int(t["end"] - time.time())
    if left <= 0:
        t["submitted"] = True
        t["finished"] = t["end"]
        st.rerun()  # full app rerun -> shows the result
    cls = "timer warn" if left <= 300 else "timer"
    md(f'<div class="{cls}"><small>Time left</small><b>{mmss(left)}</b></div>')


def _palette_css(t) -> str:
    rules = []
    for j in range(len(t["qs"])):
        if j == t["cur"]:
            style = "background:#14342B !important;color:#F2B01E !important;border:2px solid #F2B01E !important;"
        elif j in t["flags"]:
            style = "background:#F2B01E !important;color:#3D2C00 !important;border-color:#C98F0A !important;"
        elif j in t["answers"]:
            style = "background:#CFEBDD !important;color:#0F5236 !important;border-color:#8CCBAE !important;"
        else:
            continue
        rules.append(f".st-key-pal_{j} button{{{style}}}.st-key-pal_{j} button p{{color:inherit !important;}}")
    return "<style>" + "".join(rules) + "</style>"


def test_running():
    t = S.t
    qs, n, cur = t["qs"], len(t["qs"]), t["cur"]
    h1, h2 = st.columns([3, 1], vertical_alignment="center")
    h1.markdown(f"### {t['title']}")
    with h2:
        timer_box()

    st.markdown(_palette_css(t), unsafe_allow_html=True)
    main, side = st.columns([3, 1.1])

    with side:
        with st.container(border=True):
            st.markdown("**Question palette**")
            per = 5
            for r in range(0, n, per):
                cols = st.columns(per)
                for off, col in enumerate(cols):
                    j = r + off
                    if j < n:
                        col.button(str(j + 1), key=f"pal_{j}", on_click=_t_goto, args=(j,))
            md("""<div class="legend">
                <span><i style="background:#14342B"></i>Current</span>
                <span><i style="background:#CFEBDD"></i>Answered</span>
                <span><i style="background:#F2B01E"></i>For review</span>
                <span><i style="background:#fff"></i>Not visited</span></div>""")
            st.caption(f"{len(t['answers'])} answered  •  {len(t['flags'])} flagged  •  {n - len(t['answers'])} left")

    with main:
        q = qs[cur]
        with st.container(key="qcard"):
            flag = " 🚩" if cur in t["flags"] else ""
            md(f'<div class="qmeta">Question {cur + 1} of {n}{flag}</div>')
            st.markdown(q["question"])
        key = f"t_{t['run']}_{cur}"
        with st.container(key="optbox"):
            choice = st.radio("Options", list(range(len(q["options"]))), index=t["answers"].get(cur),
                              format_func=opt_fmt(q["options"]), key=key, label_visibility="collapsed")
        if choice is not None:
            t["answers"][cur] = choice

        b1, b2, b3, b4, b5 = st.columns([1, 1.3, 1, 1, 1.3])
        b1.button("⬅ Prev", disabled=cur == 0, on_click=_t_goto, args=(cur - 1,))
        b2.button("Unflag" if cur in t["flags"] else "🚩 Mark for review", on_click=_t_flag, args=(cur,))
        b3.button("Clear", on_click=_t_clear, args=(cur, key))
        b4.button("Next ➡", disabled=cur == n - 1, on_click=_t_goto, args=(cur + 1,))
        with b5.popover("Submit test"):
            left = n - len(t["answers"])
            st.write(f"Answered **{len(t['answers'])}** of **{n}**.")
            if left:
                st.write(f"**{left}** question{'s' if left != 1 else ''} left unanswered.")
            if t["flags"]:
                st.write(f"**{len(t['flags'])}** marked for review.")
            st.button("Yes, submit now", type="primary", on_click=_t_submit)


def test_result():
    t = S.t
    qs, ans = t["qs"], t["answers"]
    correct = sum(1 for j, a in ans.items() if a == qs[j]["answer"])
    wrong = len(ans) - correct
    skipped = len(qs) - len(ans)
    score = correct * t["marks"] - wrong * t["neg"]
    max_score = len(qs) * t["marks"]
    pct = (score / max_score * 100) if max_score else 0
    taken = int((t["finished"] or time.time()) - t["start"])
    if not t["saved"]:
        U.save_result({"series": U.pretty(t["series"]), "test": t["title"], "score": round(score, 2),
                       "max_score": max_score, "correct": correct, "wrong": wrong, "unattempted": skipped})
        t["saved"] = True

    st.markdown(f"### Result: {t['title']}")
    with st.container(border=True):
        a, b = st.columns([1, 3], vertical_alignment="center")
        a.markdown(ring(pct, f"{score:g}", f"out of {max_score:g}"), unsafe_allow_html=True)
        with b:
            verdict = ("Outstanding. You are exam-ready." if pct >= 80 else
                       "Good progress. A little more revision will push you higher." if pct >= 60 else
                       "Getting there. Study the explanations below and retake." if pct >= 40 else
                       "Time to revise the basics. Every attempt makes the next one better.")
            st.write(verdict)
            md(f"""<div class="tiles">
                <div class="tile ok"><b>{correct}</b><span>correct</span></div>
                <div class="tile bad"><b>{wrong}</b><span>wrong</span></div>
                <div class="tile"><b>{skipped}</b><span>skipped</span></div>
                <div class="tile"><b>{mmss(taken)}</b><span>time taken</span></div></div>""")
    r1, r2 = st.columns(2)
    r1.button("Retake this test", type="primary", on_click=_start_test, args=(t["series"], t["test"]))
    r2.button("⬅ Back to test series", on_click=_t_exit)

    st.markdown("### Review & explanations")
    flt = st.radio("Show", ["All", "Wrong", "Correct", "Skipped"], horizontal=True, label_visibility="collapsed")
    shown = 0
    for j, q in enumerate(qs):
        your = ans.get(j)
        state = "Skipped" if your is None else ("Correct" if your == q["answer"] else "Wrong")
        if flt != "All" and state != flt:
            continue
        shown += 1
        icon = {"Skipped": "⚪", "Correct": "✅", "Wrong": "❌"}[state]
        with st.expander(f"{icon}  Q{j + 1}. {q['question'][:90]}"):
            st.markdown(f"**{q['question']}**")
            option_cards(q, your)
            st.info(q["explanation"] or "No explanation added.")
    if not shown:
        st.caption("Nothing to show for this filter.")


def test_page():
    t = S.get("t")
    if t is None:
        page_head("Test series", "Timed mock tests with a question palette, review flags and full solutions.")
        test_menu()
    elif t["submitted"]:
        test_result()
    else:
        test_running()


# =====================================================================
# ADMIN
# =====================================================================
def _admin_password():
    try:
        return st.secrets["ADMIN_PASSWORD"]
    except Exception:
        return "admin123"


def target_selector(prefix):
    """Pick where questions go. Returns a dict or None."""
    kind = st.radio("Add to", ["Practice (subject-wise)", "Test Series"], horizontal=True, key=f"{prefix}_kind")
    if kind.startswith("Practice"):
        subs = U.list_subjects()
        names = [n for _, n in subs]
        ch = st.selectbox("Subject", names + [NEW], key=f"{prefix}_sub")
        name = st.text_input("New subject name", key=f"{prefix}_subnew") if ch == NEW else ch
        return {"kind": "practice", "subject": name} if name.strip() else None

    series = U.list_series()
    sc = st.selectbox("Test series", series + [NEW], format_func=lambda s: s if s == NEW else U.pretty(s),
                      key=f"{prefix}_ser")
    sname = st.text_input("New test series name", key=f"{prefix}_sernew") if sc == NEW else sc
    if not sname.strip():
        return None
    tmap = dict(U.list_tests(sc)) if sc != NEW else {}
    tc = st.selectbox("Test", list(tmap) + [NEW], format_func=lambda s: s if s == NEW else tmap[s],
                      key=f"{prefix}_test_{sc}")
    settings = None
    if tc == NEW:
        tname = st.text_input("New test name (e.g. Mock Test 1)", key=f"{prefix}_testnew")
        a, b, c = st.columns(3)
        settings = {
            "duration_minutes": a.number_input("Duration (min)", 1, 300, 150, key=f"{prefix}_dur"),
            "marks_per_question": b.number_input("Marks / question", 0.0, 10.0, 1.0, 0.25, key=f"{prefix}_mk"),
            "negative_marks": c.number_input("Negative marks", 0.0, 10.0, 0.0, 0.25, key=f"{prefix}_neg"),
        }
    else:
        tname = tc
    return {"kind": "test", "series": sname, "test": tname, "settings": settings} if tname.strip() else None


def save_to_target(tg, questions):
    if tg["kind"] == "practice":
        return U.add_practice(tg["subject"], questions)
    return U.add_test(tg["series"], tg["test"], questions, tg["settings"])


SAMPLE_CSV = (
    "question,option_a,option_b,option_c,option_d,answer,explanation\n"
    "Capital of India?,Mumbai,New Delhi,Kolkata,Chennai,B,New Delhi is the capital of India.\n"
)
SAMPLE_JSON = json.dumps([{
    "question": "Capital of India?", "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
    "answer": "B", "explanation": "New Delhi is the capital of India."}], indent=2)


def _admin_login():
    page_head("Admin", "Sign in to add and manage questions.")
    with st.form("login"):
        pw = st.text_input("Admin password", type="password")
        ok = st.form_submit_button("Log in", type="primary")
    if ok:
        if pw == _admin_password():
            S.admin = True
            st.rerun()
        else:
            st.error("Wrong password.")


def admin_page():
    if not S.get("admin"):
        _admin_login()
        return

    page_head("Admin", "Add questions, import in bulk, and keep your content tidy.")
    if _admin_password() == "admin123":
        st.warning("You are using the default password. Change `ADMIN_PASSWORD` in `.streamlit/secrets.toml`.")

    t1, t2, t3 = st.tabs(["➕ Add one question", "📤 Bulk upload", "🗂 Manage"])

    with t1:
        tg = target_selector("one")
        with st.form("add_q", clear_on_submit=True):
            question = st.text_area("Question")
            o = [st.text_input(f"Option {c}") for c in "ABCD"]
            ans = st.selectbox("Correct answer", list("ABCD"))
            expl = st.text_area("Explanation / solution")
            ok = st.form_submit_button("Add question", type="primary")
        if ok:
            if not tg:
                st.error("Choose or type a target subject / test first.")
            else:
                try:
                    q = U.normalize_question({"question": question, "options": o, "answer": ans, "explanation": expl})
                    save_to_target(tg, [q])
                    st.success("Question added ✅")
                except Exception as e:
                    st.error(f"Could not add: {e}")

    with t2:
        st.caption("Upload a CSV or JSON file with many questions at once.")
        d1, d2 = st.columns(2)
        d1.download_button("⬇ CSV template", SAMPLE_CSV, "template.csv", "text/csv")
        d2.download_button("⬇ JSON template", SAMPLE_JSON, "template.json", "application/json")
        tg2 = target_selector("bulk")
        up = st.file_uploader("Upload file", type=["csv", "json"])
        if up:
            qs, errs = U.parse_upload(up.name, up.getvalue())
            st.write(f"Valid questions found: **{len(qs)}**")
            for e in errs:
                st.warning(e)
            if qs:
                with st.expander("Preview first questions"):
                    for q in qs[:3]:
                        st.markdown(f"**{q['question']}**")
                        option_cards(q, None)
            if qs and st.button("Import questions", type="primary"):
                if not tg2:
                    st.error("Choose or type a target subject / test first.")
                else:
                    save_to_target(tg2, qs)
                    st.success(f"Imported {len(qs)} questions ✅")

    with t3:
        _admin_manage()

    st.sidebar.divider()
    st.sidebar.button("Log out of admin", key="logout", on_click=lambda: S.update(admin=False))


def _admin_manage():
    sets = U.all_sets()
    if not sets:
        st.info("Nothing to manage yet.")
        return
    labels = [l for l, _ in sets]
    label = st.selectbox("Select set", labels)
    path = dict(sets)[label]
    data = U.read_set(path)
    qs = data["questions"]
    st.write(f"**{len(qs)}** questions")
    show_df([{"No.": i + 1, "Question": q["question"], "Answer": chr(65 + q["answer"])} for i, q in enumerate(qs)])
    st.download_button("⬇ Download backup (JSON)", json.dumps(data, ensure_ascii=False, indent=2),
                       file_name=path.name, mime="application/json")

    if qs:
        st.markdown("##### Edit or delete a question")
        num = int(st.number_input("Question number", 1, len(qs), 1, key="manage_num"))
        q = qs[num - 1]
        with st.form(f"edit_form_{num}_{len(qs)}"):
            new_q = st.text_area("Question", q["question"])
            new_o = [st.text_input(f"Option {chr(65 + k)}", o) for k, o in enumerate(q["options"])]
            new_a = st.selectbox("Correct answer", [chr(65 + k) for k in range(len(q["options"]))], index=q["answer"])
            new_e = st.text_area("Explanation", q["explanation"])
            save = st.form_submit_button("Save changes", type="primary")
        if save:
            try:
                qs[num - 1] = U.normalize_question({"id": q["id"], "question": new_q, "options": new_o,
                                                     "answer": new_a, "explanation": new_e})
                U.write_set(path, data)
                st.success("Saved ✅")
                st.rerun()
            except Exception as e:
                st.error(f"Could not save: {e}")
        if st.button("🗑 Delete this question"):
            qs.pop(num - 1)
            U.write_set(path, data)
            st.rerun()

    st.divider()
    if st.checkbox("I want to delete this entire set"):
        if st.button("❌ Delete set", type="primary"):
            U.delete_set(path)
            st.rerun()


# =====================================================================
# NAVIGATION
# =====================================================================
PAGES = {
    "home": ("🏠", "Home", home_page),
    "practice": ("📝", "Practice", practice_page),
    "tests": ("🧪", "Test Series", test_page),
    "admin": ("⚙️", "Admin", admin_page),
}
if S.get("page") not in PAGES:
    S.page = "home"

with st.sidebar:
    md('<div class="brand"><b>SuperTET PRT</b><span>Practice &amp; mock tests</span></div>')
    for key, (icon, label, _) in PAGES.items():
        st.button(f"{icon}  {label}", key=f"nav_{key}", on_click=go, args=(key,))
    # active page highlight
    st.markdown(
        f"<style>.st-key-nav_{S.page} button{{background:#F2B01E !important;color:#2B2100 !important;"
        f"border-color:#F2B01E !important;}}.st-key-nav_{S.page} button *{{color:#2B2100 !important;}}</style>",
        unsafe_allow_html=True,
    )
    if S.get("t") and not S.t["submitted"] and S.page != "tests":
        md('<div class="side-note">⏱ A test is running. The timer keeps counting.</div>')

st.markdown(f"<style>{H(CSS)}</style>", unsafe_allow_html=True)
PAGES[S.page][2]()
