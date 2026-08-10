import streamlit as st
import os
import google.generativeai as genai
import plotly.graph_objects as go
from dotenv import load_dotenv
from core_functions import load_match, extract_innings

# ---------------- ENV ----------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API key missing")
    st.stop()

# ---------------- GEMINI ----------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-3-flash-preview")

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Cricket Analyzer", layout="wide")

# ---------------- ANIMATED + GLASS UI ----------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c1c1c);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}

@keyframes gradientMove {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

.stMetric {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("# 🏏 Cricket Intelligence Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

files = os.listdir("matches")
selected_file = st.sidebar.selectbox("📂 Select Match", files)

action = st.sidebar.radio(
    "🎯 Choose Action",
    ["📊 Full Analysis", "🔥 Turning Points", "🎙️ Match Story"]
)

if "Match Story" in action:
    tone = st.sidebar.selectbox(
        "🎭 Commentary Style",
        ["Dramatic Commentator", "Angry Fan", "Expert Analyst", "Casual Viewer"]
    )
else:
    tone = "Expert Analyst"

# ---------------- RUN ----------------
if st.sidebar.button("🚀 Analyze Match"):

    data = load_match("matches/" + selected_file)

    info = data.get("info", {})
    teams = info.get("teams", ["Team A", "Team B"])
    venue = info.get("venue", "Unknown Venue")
    date = info.get("dates", ["Unknown"])[0]

    innings_data = extract_innings(data)

    inning1 = innings_data[0]
    inning2 = innings_data[1]

    # ---------------- HEADER ----------------
    st.markdown(f"## 🏏 {teams[0]} vs {teams[1]}")
    st.markdown(f"📍 {venue} | 📅 {date}")

    # ---------------- METRICS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🏏 Runs", inning1['runs'])
        st.metric("🎯 Wickets", inning1['wickets'])

    with col2:
        st.metric("🏏 Runs", inning2['runs'])
        st.metric("🎯 Wickets", inning2['wickets'])

    # ---------------- INTERACTIVE GRAPH ----------------
    st.subheader("📈 Run Progression (Hover Enabled)")

    fig = go.Figure()

    # Team 1 line
    fig.add_trace(go.Scatter(
        x=list(range(len(inning1['run_progression']))),
        y=inning1['run_progression'],
        mode='lines+markers',
        name=inning1['team'],
        hovertemplate="Over: %{x}<br>Runs: %{y}<extra></extra>"
    ))

    # Team 2 line
    fig.add_trace(go.Scatter(
        x=list(range(len(inning2['run_progression']))),
        y=inning2['run_progression'],
        mode='lines+markers',
        name=inning2['team'],
        hovertemplate="Over: %{x}<br>Runs: %{y}<extra></extra>"
    ))

    # 🔥 Wickets markers
    for w in inning1['wicket_overs']:
        if w < len(inning1['run_progression']):
            fig.add_trace(go.Scatter(
                x=[w],
                y=[inning1['run_progression'][w]],
                mode='markers',
                marker=dict(size=10),
                showlegend=False,
                hovertemplate="WICKET!<br>Over: %{x}<extra></extra>"
            ))

    for w in inning2['wicket_overs']:
        if w < len(inning2['run_progression']):
            fig.add_trace(go.Scatter(
                x=[w],
                y=[inning2['run_progression'][w]],
                mode='markers',
                marker=dict(size=10),
                showlegend=False,
                hovertemplate="WICKET!<br>Over: %{x}<extra></extra>"
            ))

    fig.update_layout(
        xaxis_title="Overs",
        yaxis_title="Runs",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- CONTEXT ----------------
    context = f"""
    Match: {teams[0]} vs {teams[1]}
    Venue: {venue}
    Date: {date}

    Inning 1: {inning1}
    Inning 2: {inning2}
    """

    # ---------------- LLM ----------------
    with st.spinner("🤖 Generating insights..."):

        if "Full Analysis" in action:
            prompt = f"You are an expert analyst.\nAnalyze both innings.\n{context}"
            title = "🧠 Analysis"

        elif "Turning Points" in action:
            prompt = f"Identify turning points.\n{context}"
            title = "🔥 Turning Points"

        else:
            prompt = f"You are a {tone}. Narrate match.\n{context}"
            title = "🎙️ Match Story"

        output = model.generate_content(prompt).text

    st.subheader(title)
    st.write(output)