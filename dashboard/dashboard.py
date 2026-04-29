import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ======================
# CUSTOM CSS (BIAR BAGUS)
# ======================
st.markdown("""
<style>
.main {
    background-color: #F8FAFC;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)

    paths = [
        os.path.join(base_path, "dashboard", "main_data.csv"),
        os.path.join(base_path, "main_data.csv")
    ]

    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    else:
        raise FileNotFoundError("Dataset tidak ditemukan")

    df['dteday'] = pd.to_datetime(df['dteday'])

    # ✅ MAPPING LABEL (INI YANG DIMINTA REVIEWER)
    season_map = {
        1: "Spring 🌸",
        2: "Summer ☀️",
        3: "Fall 🍂",
        4: "Winter ❄️"
    }

    weather_map = {
        1: "Clear",
        2: "Mist",
        3: "Light Rain/Snow",
        4: "Heavy Rain"
    }

    df['season_label'] = df['season'].map(season_map)
    df['weather_label'] = df['weathersit'].map(weather_map)

    df['weekday'] = df['dteday'].dt.day_name()
    df['is_weekend'] = df['weekday'].isin(['Saturday', 'Sunday'])
    df['month'] = df['dteday'].dt.to_period('M')

    return df

df = load_data()

# ======================
# SIDEBAR (FILTER MUSIM)
# ======================
with st.sidebar:
    st.title("🔎 Filter Data")

    selected_season = st.multiselect(
        "Pilih Musim",
        options=df['season_label'].unique(),
        default=df['season_label'].unique()
    )

# filter
df_filtered = df[df['season_label'].isin(selected_season)]

# ======================
# HEADER
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis penggunaan sepeda berdasarkan musim dan kondisi lingkungan")

# ======================
# METRICS
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{df_filtered['cnt'].mean():.0f}")
col3.metric("Maksimum Rental", f"{df_filtered['cnt'].max():,}")
col4.metric("Total Hari", df_filtered['dteday'].nunique())

# ======================
# KPI GROWTH
# ======================
monthly = df_filtered.groupby('month')['cnt'].sum().reset_index()

if len(monthly) >= 2:
    growth = ((monthly['cnt'].iloc[-1] - monthly['cnt'].iloc[-2]) / monthly['cnt'].iloc[-2]) * 100
else:
    growth = 0

st.metric("📈 Growth Bulanan", f"{growth:.2f}%", delta=f"{growth:.2f}%")

st.markdown("---")

# ======================
# LAYOUT (2 KOLOM BIAR ENAK)
# ======================
col1, col2 = st.columns(2)

# ======================
# TREND
# ======================
with col1:
    st.subheader("📈 Tren Penyewaan")

    daily = df_filtered.groupby('dteday')['cnt'].sum().reset_index()

    fig = px.line(
        daily,
        x='dteday',
        y='cnt',
        markers=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# MUSIM
# ======================
with col2:
    st.subheader("🌤️ Berdasarkan Musim")

    season_avg = df_filtered.groupby('season_label')['cnt'].mean().reset_index()

    fig = px.bar(
        season_avg,
        x='season_label',
        y='cnt',
        text_auto=True,
        color='cnt',
        color_continuous_scale='Blues'
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# BARIS 2
# ======================
col3, col4 = st.columns(2)

# ======================
# CUACA
# ======================
with col3:
    st.subheader("🌧️ Kondisi Cuaca")

    weather_avg = df_filtered.groupby('weather_label')['cnt'].mean().reset_index()

    fig = px.pie(
        weather_avg,
        values='cnt',
        names='weather_label',
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# WEEKEND VS WEEKDAY
# ======================
with col4:
    st.subheader("📊 Weekday vs Weekend")

    compare = df_filtered.groupby('is_weekend')['cnt'].mean().reset_index()
    compare['type'] = compare['is_weekend'].map({True:"Weekend", False:"Weekday"})

    fig = px.bar(
        compare,
        x='type',
        y='cnt',
        text_auto=True,
        color='type'
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:gray'>Bike Sharing Dashboard • Advanced Submission</div>",
    unsafe_allow_html=True
)
