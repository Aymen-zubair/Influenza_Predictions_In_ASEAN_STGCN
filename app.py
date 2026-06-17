import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="ASEAN Influenza Forecasting Demo",
    layout="wide"
)

# =====================================
# DARK STYLE
# =====================================

st.markdown("""
<style>

.stApp {
    background-color: #0f1117;
    color: #ffffff;
}

h1, h2, h3, h4 {
    color: #60a5fa;
}

section[data-testid="stSidebar"] {
    background-color: #161b22;
}

div[data-baseweb="select"] > div {
    background-color: #1f2937;
    color: white;
}

.stSelectbox label {
    color: #93c5fd !important;
    font-weight: 600;
}

.stMarkdown, .stText {
    color: #d1d5db;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv("saved/test_predictions.csv")
df["date"] = pd.to_datetime(df["date"])

# Remove Malaysia
df = df[df["country"] != "Malaysia"].copy()

# =====================================
# HEADER
# =====================================

st.title("STGCN-Based Short-Term Influenza Forecasting in ASEAN")

st.write(
    "Interactive forecasting demonstration using the trained "
    "Spatio-Temporal Graph Convolutional Network (STGCN)."
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("Forecast Controls")

countries = sorted(df["country"].unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

country_df = df[df["country"] == selected_country].copy()
country_df = country_df.sort_values("date")

# =====================================
# FULL FORECAST GRAPH
# =====================================

st.subheader(f"Actual vs Predicted Forecast — {selected_country}")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=country_df["date"],
    y=country_df["positivity_rate"],
    mode="lines+markers",
    name="Actual",
    line=dict(color="#60a5fa", width=3)
))

fig.add_trace(go.Scatter(
    x=country_df["date"],
    y=country_df["stgcn_pred"],
    mode="lines+markers",
    name="Predicted",
    line=dict(color="#94a3b8", width=3)
))

fig.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="white"),
    xaxis=dict(
        title="Date",
        gridcolor="#374151"
    ),
    yaxis=dict(
        title="Influenza Positivity Rate",
        gridcolor="#374151"
    ),
    legend=dict(
        bgcolor="#111827"
    ),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================
# DATE SELECTION
# =====================================

st.subheader("Single-Date Forecast Demonstration")

available_dates = sorted(country_df["date"].unique())

selected_date = st.selectbox(
    "Select Forecast Date",
    available_dates
)

selected_row = country_df[country_df["date"] == selected_date].iloc[0]

actual_value = selected_row["positivity_rate"]
predicted_value = selected_row["stgcn_pred"]

# =====================================
# FORECAST OUTPUT
# =====================================

st.markdown(f"""
<div style="
    background-color:#161b22;
    padding:25px;
    border-radius:15px;
    border:1px solid #374151;
    margin-top:10px;
">

<h3 style="color:#60a5fa;">
Forecast Result
</h3>

<p style="font-size:18px;">
<b>Country:</b> {selected_country}
</p>

<p style="font-size:18px;">
<b>Forecast Date:</b> {pd.to_datetime(selected_date).date()}
</p>

<p style="font-size:18px;">
<b>Actual Positivity Rate:</b> {actual_value:.4f}
</p>

<p style="font-size:18px;">
<b>STGCN Predicted Positivity Rate:</b> {predicted_value:.4f}
</p>

</div>
""", unsafe_allow_html=True)

# =====================================
# LOCAL CONTEXT GRAPH
# =====================================

st.subheader("Forecast Context Around Selected Date")

context_df = country_df[
    (country_df["date"] >= selected_date - pd.Timedelta(days=35)) &
    (country_df["date"] <= selected_date + pd.Timedelta(days=35))
].copy()

context_fig = go.Figure()

context_fig.add_trace(go.Scatter(
    x=context_df["date"],
    y=context_df["positivity_rate"],
    mode="lines+markers",
    name="Actual",
    line=dict(color="#60a5fa", width=3)
))

context_fig.add_trace(go.Scatter(
    x=context_df["date"],
    y=context_df["stgcn_pred"],
    mode="lines+markers",
    name="Predicted",
    line=dict(color="#94a3b8", width=3)
))

y_min = min(
    context_df["positivity_rate"].min(),
    context_df["stgcn_pred"].min()
)

y_max = max(
    context_df["positivity_rate"].max(),
    context_df["stgcn_pred"].max()
)

context_fig.add_shape(
    type="line",
    x0=selected_date,
    x1=selected_date,
    y0=y_min,
    y1=y_max,
    line=dict(
        color="#3b82f6",
        dash="dash",
        width=3
    )
)

context_fig.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(color="white"),
    xaxis=dict(
        title="Date",
        gridcolor="#374151"
    ),
    yaxis=dict(
        title="Influenza Positivity Rate",
        gridcolor="#374151"
    ),
    legend=dict(
        bgcolor="#111827"
    ),
    hovermode="x unified"
)

st.plotly_chart(context_fig, use_container_width=True)