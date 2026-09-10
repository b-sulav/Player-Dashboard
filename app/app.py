import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os

st.set_page_config(page_title="VCT Dashboard", layout="wide")

VAL_RED     = "#FF4655"
VAL_RED_DIM = "rgba(255, 70, 85, 0.35)"
VAL_DARK    = "#0F1923"
VAL_CARD_BG = "#141E28"
VAL_LIGHT   = "#ECE8E1"
VAL_TEAL    = "#00F0FF"

if "vct_year" not in st.session_state:
    st.session_state["vct_year"] = "21"

_SEARCH_HTML = """<input id="player-search-input" type="text" autocomplete="off" />"""

_SEARCH_CSS = """
#player-search-input {
    width: 100%;
    height: 48px;
    box-sizing: border-box;
    background-color: rgba(255,255,255,0.03);
    border: 1px solid rgba(255, 70, 85, 0.4);
    color: #ECE8E1;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 1px;
    font-size: 1rem;
    padding: 0 16px;
    outline: none;
}
#player-search-input:focus {
    border-color: #FF4655;
    box-shadow: 0 0 12px rgba(255,70,85,0.15);
}
#player-search-input::placeholder {
    color: rgba(236,232,225,0.22);
    letter-spacing: 3px;
    font-size: 0.82rem;
}
"""

_SEARCH_JS = """
let highlighted = -1;

function getResultButtons() {
    return Array.from(document.querySelectorAll('div[class*="st-key-searchres_"] button'));
}

function applyHighlight(buttons) {
    buttons.forEach((btn, i) => {
        btn.classList.toggle('kb-highlighted', i === highlighted);
    });
    if (highlighted >= 0 && buttons[highlighted]) {
        buttons[highlighted].scrollIntoView({ block: 'nearest' });
    }
}

export default function(component) {
    const { setStateValue, parentElement, data } = component;
    const input = parentElement.querySelector('#player-search-input');

    input.placeholder = data.placeholder ?? '';
    if (input.value !== (data.value ?? '')) {
        input.value = data.value ?? '';
    }

    highlighted = -1;

    input.oninput = (e) => {
        highlighted = -1;
        setStateValue('value', e.target.value);
    };

    input.onkeydown = (e) => {
        const buttons = getResultButtons();
        if (buttons.length === 0) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            highlighted = (highlighted + 1) % buttons.length;
            applyHighlight(buttons);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            highlighted = (highlighted - 1 + buttons.length) % buttons.length;
            applyHighlight(buttons);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            const target = highlighted >= 0 ? buttons[highlighted] : buttons[0];
            target.click();
        }
    };
}
"""

_live_search_component = st.components.v2.component(
    "live_player_search",
    html=_SEARCH_HTML,
    css=_SEARCH_CSS,
    js=_SEARCH_JS,
)


def live_search_input(placeholder="", *, default="", key=None):
    component_state = st.session_state.get(key, {})
    value = component_state.get("value", default)
    result = _live_search_component(
        data={"placeholder": placeholder, "value": value},
        default={"value": value},
        key=key,
        on_value_change=lambda: None,
    )
    return result.value

@st.cache_data
def load_data(year):
    expanded = os.path.expanduser(f"~/development/Player-Dashboard/data/clean/pstats{year}.csv")
    try:
        return pd.read_csv(expanded)
    except FileNotFoundError:
        return pd.DataFrame()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Teko:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Rajdhani', sans-serif;
}}
.stApp {{
    background: {VAL_DARK};
    color: {VAL_LIGHT};
}}
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {{
    display: none;
}}

[data-testid="stHeader"] {{
    display: none;
}}

.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] > div {{
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 0 !important;
    background: {VAL_CARD_BG} !important;
}}

div[data-baseweb="input"] > div {{
    background-color: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255, 70, 85, 0.4) !important;
    border-radius: 0 !important;
    clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px));
    height: 48px !important;
    transition: border-color 0.2s ease !important;
}}
div[data-baseweb="input"] > div:focus-within {{
    border-color: {VAL_RED} !important;
    box-shadow: 0 0 12px rgba(255,70,85,0.15) !important;
}}
input {{
    color: {VAL_LIGHT} !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    font-size: 1rem !important;
    caret-color: {VAL_RED} !important;
}}
input::placeholder {{
    color: rgba(236,232,225,0.22) !important;
    letter-spacing: 3px !important;
    font-size: 0.82rem !important;
}}

.stButton > button {{
    background: transparent !important;
    color: rgba(236,232,225,0.32) !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    font-family: 'Teko', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    height: 36px !important;
    padding: 0 6px !important;
    box-shadow: none !important;
    transition: color 0.15s, border-color 0.15s !important;
    width: 100% !important;
}}
.stButton > button:hover {{
    background: transparent !important;
    color: {VAL_LIGHT} !important;
    border-bottom: 2px solid rgba(236,232,225,0.15) !important;
    box-shadow: none !important;
}}
.stButton > button:focus:not(:focus-visible) {{
    box-shadow: none !important;
    outline: none !important;
}}
.stButton > button:active {{
    background: transparent !important;
    box-shadow: none !important;
}}

.st-key-yr_active button {{
    color: {VAL_RED} !important;
    border-bottom: 2px solid {VAL_RED} !important;
}}

.st-key-search_results_box {{
    margin-top: 2px !important;
}}
.st-key-search_results_box > div {{
    background: rgba(15, 25, 33, 0.98) !important;
    border: 1px solid rgba(255, 70, 85, 0.3) !important;
    border-radius: 0 !important;
    clip-path: polygon(0 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%) !important;
    box-shadow: 0 12px 28px rgba(0,0,0,0.45) !important;
    padding: 2px 0 !important;
    overflow: hidden !important;
}}

div[class*="st-key-searchres_"] {{
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}}
div[class*="st-key-searchres_"]:last-child {{
    border-bottom: none !important;
}}
div[class*="st-key-searchres_"] button {{
    background: transparent !important;
    color: rgba(236,232,225,0.75) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    font-family: 'Teko', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.15rem !important;
    height: 42px !important;
    padding: 0 18px !important;
    border: none !important;
    border-left: 2px solid transparent !important;
    border-radius: 0 !important;
    transition: color 0.12s ease, border-color 0.12s ease, background 0.12s ease, padding-left 0.12s ease !important;
}}
div[class*="st-key-searchres_"] button:hover,
div[class*="st-key-searchres_"] button.kb-highlighted {{
    background: rgba(255,70,85,0.09) !important;
    color: {VAL_RED} !important;
    border-left: 2px solid {VAL_RED} !important;
    padding-left: 22px !important;
}}

.st-key-back_btn button {{
    background: rgba(255,70,85,0.07) !important;
    color: {VAL_RED} !important;
    border: 1px solid rgba(255,70,85,0.38) !important;
    border-bottom: 1px solid rgba(255,70,85,0.38) !important;
    border-radius: 0 !important;
    clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%) !important;
    font-size: 1.05rem !important;
    letter-spacing: 3px !important;
    height: 40px !important;
    transition: background 0.15s, color 0.15s, box-shadow 0.15s !important;
}}
.st-key-back_btn button:hover {{
    background: {VAL_RED} !important;
    color: {VAL_DARK} !important;
    border-color: {VAL_RED} !important;
    box-shadow: 0 0 18px rgba(255,70,85,0.28) !important;
}}

[data-testid="stHorizontalBlock"] {{
    gap: 0.6rem !important;
    align-items: stretch !important;
}}

[data-testid="column"] > div {{
    padding: 0 !important;
}}
</style>
""", unsafe_allow_html=True)

def pct_badge_html(pct):
    if pct is None or (isinstance(pct, float) and pd.isna(pct)):
        return ""
    try:
        diff = float(pct) - 50
    except (TypeError, ValueError):
        return ""
    color = "#3DDC84" if diff >= 0 else VAL_RED
    return (
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'background:rgba(255,255,255,0.03);border:1px solid {color}44;'
        f'padding:1px 10px;min-width:52px;">'
        f'<span style="font-family:\'Teko\',sans-serif;font-weight:600;font-size:1.05rem;'
        f'line-height:1;color:{color};">{diff:+.0f}</span></span>'
    )


def stat_card(label, value, pct=None):
    badge = pct_badge_html(pct) if pct is not None else ""
    st.markdown(
        f'<div style="padding:4px 0 6px;">'
        f'  <div style="font-family:\'Teko\',sans-serif;color:{VAL_RED};font-weight:600;'
        f'  text-transform:uppercase;letter-spacing:1.5px;font-size:0.82rem;'
        f'  margin-bottom:6px;opacity:0.85;">{label}</div>'
        f'  <div style="display:flex;align-items:baseline;justify-content:space-between;gap:8px;">'
        f'    <div style="color:{VAL_LIGHT};font-family:\'Teko\',sans-serif;font-size:2.4rem;'
        f'    font-weight:600;line-height:1;">{value}</div>'
        f'    {badge}'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )

def home():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:4px;">
            <span style="font-family:'Teko',sans-serif;font-weight:700;font-size:3.6rem;
                         letter-spacing:6px;text-transform:uppercase;color:{VAL_LIGHT};
                         line-height:1;">VCT</span><span
                  style="font-family:'Teko',sans-serif;font-weight:700;font-size:3.6rem;
                         letter-spacing:6px;text-transform:uppercase;color:{VAL_RED};
                         line-height:1;"> STATS</span>
        </div>
        <div style="text-align:center;font-family:'Rajdhani',sans-serif;font-size:0.72rem;
                    letter-spacing:5px;color:rgba(236,232,225,0.2);text-transform:uppercase;
                    margin-bottom:36px;">
            VALORANT CHAMPIONS TOUR
        </div>
        """, unsafe_allow_html=True)

        df = load_data(st.session_state["vct_year"])
        years = ["21", "22", "23", "24", "25", "26"]
        yr_cols = st.columns(len(years), gap="small")
        for yr, c in zip(years, yr_cols):
            with c:
                btn_key = "yr_active" if st.session_state["vct_year"] == yr else f"yr_{yr}"
                if st.button(f"20{yr}", key=btn_key, use_container_width=True):
                    st.session_state["vct_year"] = yr
                    st.rerun()

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        query = live_search_input(
            "SEARCH PLAYER...",
            key="player_search_input",
        )

        selected_player = None
        if query and not df.empty:
            mask = df["Player"].astype(str).str.lower().str.startswith(query.lower())
            matches = df[mask]["Player"].drop_duplicates().tolist()[:8]
            if matches:
                with st.container(border=True, key="search_results_box"):
                    for name in matches:
                        if st.button(name, key=f"searchres_{name}", use_container_width=True):
                            selected_player = name
        if df.empty:
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="padding:14px 18px;border:1px solid {VAL_RED}44;
                        background:rgba(255,70,85,0.04);
                        font-family:'Rajdhani',sans-serif;font-size:0.92rem;
                        color:rgba(236,232,225,0.55);letter-spacing:0.5px;">
                No data found for VCT 20{st.session_state["vct_year"]}.
                Check your data files.
            </div>""", unsafe_allow_html=True)
            return

        if selected_player:
            st.session_state["selected_player"] = selected_player
            st.switch_page(player_page)

def player():
    selected_player = st.session_state.get("selected_player")
    current_year    = st.session_state.get("vct_year", "21")
    df              = load_data(current_year)

    if not selected_player or df.empty or selected_player not in df["Player"].values:
        st.switch_page(home_page)
        return

    p_data    = df[df["Player"] == selected_player].iloc[0]
    team_name = p_data.get("Teams", "")
    players   = df[df["Teams"] == team_name]["Player"].drop_duplicates().tolist()

    scores = [
        p_data.get("ACS Percentile", 0),
        p_data.get("K/D Percentile", 0),
        p_data.get("ADR Percentile", 0),
        p_data.get("Headshot Percentile", 0),
    ]
    categories    = ["ACS", "K/D", "ADR", "H%"]
    overall_score = p_data.get("Average Percentile", 0)

    col_back, col_badge = st.columns([1, 5], gap="small")

    with col_back:
        if st.button("← BACK", key="back_btn", use_container_width=True):
            st.session_state["selected_player"] = None
            st.session_state.pop("player_search_input", None)
            st.switch_page(home_page)

    with col_badge:
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;
                    height:40px;
                    border:1px solid rgba(255,70,85,0.18);
                    background:rgba(255,255,255,0.015);
                    clip-path:polygon(0 0,calc(100% - 10px) 0,100% 10px,100% 100%,0 100%);">
            <span style="font-family:'Teko',sans-serif;font-size:0.95rem;font-weight:700;
                         letter-spacing:3.5px;color:{VAL_RED};text-transform:uppercase;">
                VALORANT CHAMPIONS TOUR
            </span>
            <span style="font-family:'Teko',sans-serif;font-size:0.95rem;font-weight:700;
                         letter-spacing:3.5px;color:{VAL_LIGHT};text-transform:uppercase;
                         margin-left:8px;">
                20{current_year}
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        h_left, h_right = st.columns([5, 1])
        with h_left:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;'
                f'padding:6px 0;">'
                f'<span style="font-family:\'Teko\',sans-serif;font-weight:700;font-size:3rem;'
                f'letter-spacing:3px;text-transform:uppercase;color:{VAL_LIGHT};line-height:1;">'
                f'{p_data["Player"]}</span>'
                f'<span style="font-family:\'Teko\',sans-serif;font-weight:600;letter-spacing:2.5px;'
                f'text-transform:uppercase;font-size:1.1rem;color:{VAL_TEAL};'
                f'border:1px solid rgba(0,240,255,0.3);padding:3px 14px;white-space:nowrap;">'
                f'{team_name}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with h_right:
            stat_card("Rating", str(p_data.get("Rating", "—")))

    sc1, sc2, sc3, sc4 = st.columns(4, gap="small")
    stat_defs = [
        ("ACS",        "Average Combat Score",    "Average Combat Score",    scores[0]),
        ("K/D",        "K/D Ratio",               "Kills:Deaths",            scores[1]),
        ("ADR",        "Avg Damage / Round",       "Average Damage Per Round",scores[2]),
        ("HS%",        "Headshot %",               "Headshot %",              scores[3]),
    ]
    for col, (_, label, key, score) in zip([sc1, sc2, sc3, sc4], stat_defs):
        with col:
            with st.container(border=True):
                stat_card(label, str(p_data.get(key, "—")), score)

    ch1, ch2 = st.columns(2, gap="small")

    cats_closed   = categories + [categories[0]]
    scores_closed = scores + [scores[0]]

    with ch1:
        with st.container(border=True):
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=scores_closed,
                theta=cats_closed,
                fill="toself",
                line=dict(color=VAL_RED, width=2),
                fillcolor="rgba(255,70,85,0.2)",
                hovertemplate="<b>%{theta}</b>: %{r:.1f}<extra></extra>",
            ))
            fig_radar.update_layout(
                title=dict(
                    text="PERFORMANCE RADAR",
                    font=dict(family="Teko", size=17, color=VAL_LIGHT),
                    x=0.5, xanchor="center",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=320,
                margin=dict(l=40, r=40, t=48, b=20),
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(
                        visible=True, range=[0, 100],
                        showticklabels=False,
                        linecolor="rgba(255,255,255,0.1)",
                        gridcolor="rgba(255,255,255,0.08)",
                    ),
                    angularaxis=dict(
                        tickfont=dict(color=VAL_TEAL, size=13, family="Rajdhani"),
                        linecolor="rgba(255,255,255,0.1)",
                        gridcolor="rgba(255,255,255,0.08)",
                    ),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    with ch2:
        with st.container(border=True):
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=overall_score,
                number=dict(
                    suffix="%",
                    font=dict(color=VAL_LIGHT, size=38, family="Teko"),
                    valueformat=".0f",
                ),
                title=dict(text="", font=dict(color=VAL_LIGHT, size=14)),
                gauge=dict(
                    axis=dict(
                        range=[0, 100], tickwidth=1,
                        tickcolor="rgba(255,255,255,0.1)",
                        tickfont=dict(color="rgba(255,255,255,0.35)", size=9),
                    ),
                    bar=dict(color=VAL_RED, thickness=0.5),
                    bgcolor="rgba(255,255,255,0.04)",
                    borderwidth=1,
                    bordercolor="rgba(255,255,255,0.1)",
                    steps=[
                        dict(range=[0,  50], color="rgba(255,255,255,0.02)"),
                        dict(range=[50, 80], color="rgba(255,255,255,0.04)"),
                        dict(range=[80,100], color="rgba(0,240,255,0.04)"),
                    ],
                    threshold=dict(
                        line=dict(color=VAL_TEAL, width=2),
                        thickness=0.8,
                        value=80,
                    ),
                ),
            ))
            fig_gauge.update_layout(
                title=dict(
                    text="OVERALL PERCENTILE",
                    font=dict(family="Teko", size=17, color=VAL_LIGHT),
                    x=0.5, xanchor="center",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=320,
                margin=dict(l=30, r=30, t=48, b=10),
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    with st.container(border=True):
        items = []
        for name in players:
            active      = name == selected_player
            color       = VAL_RED if active else VAL_LIGHT
            opacity     = "1" if active else "0.38"
            border_bot  = f"border-bottom:2px solid {VAL_RED};" if active else "border-bottom:2px solid transparent;"
            items.append(
                f'<div style="flex:1;min-width:80px;text-align:center;padding:6px 8px;{border_bot}">'
                f'<span style="font-family:\'Teko\',sans-serif;font-weight:600;letter-spacing:1.5px;'
                f'text-transform:uppercase;font-size:1.6rem;line-height:1;'
                f'color:{color};opacity:{opacity};">'
                f'{name}</span></div>'
            )
        st.markdown(
            f'<div style="display:flex;flex-wrap:wrap;align-items:center;'
            f'justify-content:space-evenly;gap:0;">{"".join(items)}</div>',
            unsafe_allow_html=True,
        )


home_page   = st.Page(home,   title="Dashboard", default=True)
player_page = st.Page(player, title="Player")
st.navigation([home_page, player_page]).run()