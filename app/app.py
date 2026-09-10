import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox
import plotly.graph_objects as go

st.set_page_config(page_title="VCT Dashboard", page_icon="🎯", layout="wide")


VAL_RED = "#FF4655"
VAL_RED_DIM = "rgba(255, 70, 85, 0.35)"
VAL_DARK = "#0F1923"
VAL_DARK2 = "#1A242D"
VAL_LIGHT = "#ECE8E1"
VAL_TEAL = "#00F0FF"
VAL_GREY = "#768079"


@st.cache_data
def load_data():
    return pd.read_csv("~/development/Player-Dashboard/data/clean/pstats21.csv")


df = load_data()


st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Teko:wght@500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Rajdhani', sans-serif;
    }}

    .stApp {{
        background: {VAL_DARK};
        color: {VAL_LIGHT};
    }}

    h1, h2, h3 {{
        font-family: 'Teko', 'Rajdhani', sans-serif;
        color: {VAL_LIGHT};
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }}

    [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
        display: none;
    }}

    div[data-testid="stMetricValue"] {{
        color: {VAL_LIGHT} !important;
        font-family: 'Teko', sans-serif;
        font-size: 2rem !important;
        font-weight: 600;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {VAL_RED} !important;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-size: 0.8rem !important;
    }}
    div[data-testid="stMetricDelta"] {{
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    hr {{
        border-color: rgba(255,70,85,0.25) !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        background: linear-gradient(160deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-left: 3px solid {VAL_RED} !important;
        padding: 22px !important;
        transition: border-color 0.25s ease, transform 0.2s ease, box-shadow 0.25s ease;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
        border-color: rgba(255,70,85,0.45) !important;
        border-left: 3px solid {VAL_TEAL} !important;
        box-shadow: 0 0 24px rgba(255,70,85,0.12);
    }}

    div[data-baseweb="input"] > div {{
        background-color: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,70,85,0.35) !important;
        border-radius: 4px !important;
    }}
    input {{
        color: {VAL_LIGHT} !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    .stButton > button {{
        background: transparent;
        color: {VAL_RED};
        border: 1px solid {VAL_RED};
        border-radius: 2px;
        font-family: 'Teko', sans-serif;
        font-size: 1.1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 6px 22px;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        background: {VAL_RED};
        color: {VAL_DARK};
        box-shadow: 0 0 18px rgba(255,70,85,0.5);
    }}

    .val-banner {{
        position: relative;
        background: linear-gradient(90deg, {VAL_DARK2} 0%, rgba(255,70,85,0.15) 100%);
        border-left: 4px solid {VAL_RED};
        clip-path: polygon(0 0, 100% 0, 98% 100%, 0% 100%);
        padding: 10px 28px;
        margin-bottom: 6px;
    }}
    .val-banner span {{
        font-family: 'Teko', sans-serif;
        font-size: 1rem;
        letter-spacing: 4px;
        color: {VAL_TEAL};
        text-transform: uppercase;
    }}

    .val-title {{
        font-family: 'Teko', sans-serif;
        font-weight: 700;
        font-size: 4rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: {VAL_LIGHT};
        line-height: 1;
        margin: 0;
    }}
    .val-title span {{
        color: {VAL_RED};
    }}

    .val-subtitle {{
        color: {VAL_GREY};
        font-size: 1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 4px;
    }}

    .val-roster-label {{
        font-family: 'Teko', sans-serif;
        color: {VAL_RED};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }}

    .val-roster-row {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
    }}

    .val-roster-name {{
        font-family: 'Teko', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 2.4rem;
        color: {VAL_LIGHT};
        opacity: 0.55;
        flex: 1;
        text-align: center;
        padding: 4px 10px;
    }}

    .val-roster-name.active {{
        color: {VAL_RED};
        opacity: 1;
        border-bottom: 2px solid {VAL_RED};
    }}

    .val-team-tag {{
        font-family: 'Teko', sans-serif;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 1.3rem;
        color: {VAL_TEAL};
        border: 1px solid rgba(0, 240, 255, 0.4);
        border-radius: 2px;
        padding: 2px 12px;
        white-space: nowrap;
    }}

    .val-pct-box {{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 4px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 6px;
        padding: 4px 8px;
        height: 100%;
        width: 100%;
    }}

    .val-pct-arrow {{
        font-size: 0.85rem;
        line-height: 1;
    }}

    .val-pct-num {{
        font-family: 'Teko', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        line-height: 1.1;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"] {{
        align-items: center !important;
        justify-content: center !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

def home():
    st.markdown(
        """
        <div style="text-align:center; margin-top:40px; margin-bottom:10px;">
            <div class="val-banner" style="display:inline-block; clip-path:none; margin-bottom:16px;">
                <span>VCT // PLAYER INTEL</span>
            </div>
            <h1 class="val-title">VALORANT <span>STATS</span></h1>
            <div class="val-subtitle">Search a player to pull up their combat profile</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def search_players(search_term: str, **kwargs):
        if not search_term:
            return []
        matches = df[
            df["Player"].astype(str).str.lower().str.startswith(search_term.lower())
        ]
        return matches["Player"].drop_duplicates().tolist()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        selected_player = st_searchbox(
            search_players,
            key="player_search",
            placeholder="SEARCH PLAYERS...",
            clear_on_submit=False,
        )

        if selected_player:
            st.session_state["selected_player"] = selected_player
            st.switch_page(player_page)


def player():
    selected_player = st.session_state.get("selected_player")

    if not selected_player or selected_player not in df["Player"].values:
        st.warning("No player selected. Please search for a player first.")
        st.page_link(home_page, label="← Back to Search")
        return

    p_data = df[df["Player"] == selected_player].iloc[0]
    team_name = p_data.get("Teams")
    players = df[df["Teams"] == team_name]["Player"].drop_duplicates().tolist()

    categories = ["ACS", "K/D", "ADR", "H%"]
    scores = [
        p_data.get("ACS Percentile", 0),
        p_data.get("K/D Percentile", 0),
        p_data.get("ADR Percentile", 0),
        p_data.get("Headshot Percentile", 0),
    ]
    categories_closed = categories + [categories[0]]
    scores_closed = scores + [scores[0]]
    overall_scores = p_data.get("Average Percentile", 0)

    st.page_link(home_page, label="← Back to Search")

    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
                    <h1 class="val-title" style="font-size:3.2rem; margin:0;">{p_data['Player']}</h1>
                    <span class="val-team-tag">{team_name if team_name else ""}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.metric(label="Rating", value=str(p_data.get("Rating", "N/A")))

    def pct_badge(pct):
        try:
            diff = float(pct) - 50 
        except (TypeError, ValueError):
            return
        positive = diff >= 0
        arrow = "▲" if positive else "▼"
        color = "#3DDC84" if positive else VAL_RED
        st.markdown(
            f"""
            <div class="val-pct-box" style="border-color:{color}55; flex-direction:row; gap:4px; padding:4px 8px;">
                <span class="val-pct-arrow" style="color:{color}; font-size:0.85rem;">{arrow}</span>
                <span class="val-pct-num" style="color:{color};">{diff:+.0f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.markdown("<div style='display:flex; align-items:center; justify-content:center; gap:10px;'>", unsafe_allow_html=True)
            inner1, inner2 = st.columns([3, 1])
            with inner1:
                st.metric("Average Combat Score", str(p_data.get("Average Combat Score", "N/A")))
            with inner2:
                pct_badge(scores[0])
            st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        with st.container(border=True):
            st.markdown("<div style='display:flex; align-items:center; justify-content:center; gap:10px;'>", unsafe_allow_html=True)
            inner1, inner2 = st.columns([3, 1])
            with inner1:
                st.metric("K/D Ratio", str(p_data.get("Kills:Deaths", "N/A")))
            with inner2:
                pct_badge(scores[1])
            st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        with st.container(border=True):
            st.markdown("<div style='display:flex; align-items:center; justify-content:center; gap:10px;'>", unsafe_allow_html=True)
            inner1, inner2 = st.columns([3, 1])
            with inner1:
                st.metric("Average Damage Per Round", str(p_data.get("Average Damage Per Round", "N/A")))
            with inner2:
                pct_badge(scores[2])
            st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        with st.container(border=True):
            st.markdown("<div style='display:flex; align-items:center; justify-content:center; gap:10px;'>", unsafe_allow_html=True)
            inner1, inner2 = st.columns([3, 1])
            with inner1:
                st.metric("Headshot %", str(p_data.get("Headshot %", "N/A")))
            with inner2:
                pct_badge(scores[3])
            st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            fig = go.Figure(
                data=go.Scatterpolar(
                    r=scores_closed,
                    theta=categories_closed,
                    fill="toself",
                    name="Player Stats",
                    line=dict(color=VAL_RED, width=2),
                    fillcolor="rgba(255, 70, 85, 0.25)",
                    hovertemplate="<b>%{theta}</b>: %{r:.1f}%<extra></extra>",
                )
            )
            fig.update_layout(
                title=dict(text="PERFORMANCE RADAR", font=dict(family="Teko", size=20, color=VAL_LIGHT)),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                width=300,
                height=300,
                margin=dict(l=30, r=30, t=50, b=30),
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        showticklabels=False,
                        linecolor="rgba(255,255,255,0.2)",
                        gridcolor="rgba(255,255,255,0.15)",
                    ),
                    angularaxis=dict(
                        tickfont=dict(color=VAL_TEAL, size=12, family="Rajdhani"),
                        linecolor="rgba(255,255,255,0.2)",
                        gridcolor="rgba(255,255,255,0.15)",
                    ),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        with st.container(border=True):

            def create_overall_gauge(score, title_text=""):
                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=score,
                        number={"suffix": "%", "font": {"color": VAL_LIGHT, "size": 34, "family": "Teko"}},
                        title={"text": title_text, "font": {"color": VAL_LIGHT, "size": 16}, "align": "center"},
                        gauge={
                            "axis": {
                                "range": [0, 100],
                                "tickwidth": 1,
                                "tickcolor": VAL_RED_DIM,
                                "tickfont": {"color": "rgba(255,255,255,0.5)", "size": 10},
                            },
                            "bar": {"color": VAL_RED},
                            "bgcolor": "rgba(255,255,255,0.05)",
                            "borderwidth": 1,
                            "bordercolor": "rgba(255,255,255,0.15)",
                            "threshold": {
                                "line": {"color": VAL_TEAL, "width": 4},
                                "thickness": 1,
                                "value": 80,
                            },
                        },
                    )
                )
                fig.update_layout(
                    title=dict(text="PERFORMANCE GAUGE", font=dict(family="Teko", size=20, color=VAL_LIGHT)),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=300,
                    margin=dict(t=60, b=30),
                )
                return fig

            fig_overall = create_overall_gauge(overall_scores)
            st.plotly_chart(fig_overall, use_container_width=True, config={"displayModeBar": False})

    with st.container(border=True):
        roster_html = "".join(
            f'<div class="val-roster-name{" active" if name == selected_player else ""}">{name}</div>'
            for name in players
        )
        st.markdown(
            f"""
            <div class="val-roster-row">{roster_html}</div>
            """,
            unsafe_allow_html=True,
        )


home_page = st.Page(home, title="Dashboard", icon="🔍", default=True)
player_page = st.Page(player, title="Player", icon="👤")

pg = st.navigation([home_page, player_page])
pg.run()