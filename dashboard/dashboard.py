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
# LOAD DATA (AMAN STREAMLIT CLOUD)
# ======================
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    
    # coba 2 kemungkinan path
    possible_paths = [
        os.path.join(base_path, "dashboard", "main_data.csv"),
        os.path.join(base_path, "main_data.csv")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    else:
        raise FileNotFoundError("Dataset tidak ditemukan")

    df['dteday'] = pd.to_datetime(df['dteday'])

    # mapping label
    season_map = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
    weather_map = {1:"Clear",2:"Mist",3:"Light Rain/Snow",4:"Heavy Rain"}

    df['season_label'] = df['season'].map(season_map)
    df['weather_label'] = df['weathersit'].map(weather_map)

    df['weekday'] = df['dteday'].dt.day_name()
    df['is_weekend'] = df['weekday'].isin(['Saturday','Sunday'])
    df['month'] = df['dteday'].dt.to_period('M')

    return df

df = load_data()

# ======================
# HEADER
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis penggunaan sepeda berdasarkan musim, cuaca, dan perilaku pengguna")

# ======================
# METRICS
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{df['cnt'].mean():.0f}")
col3.metric("Puncak Rental", f"{df['cnt'].max():,}")
col4.metric("Total Hari", df['dteday'].nunique())

# ======================
# KPI GROWTH
# ======================
monthly = df.groupby('month')['cnt'].sum().reset_index()

if len(monthly) >= 2:
    growth = ((monthly['cnt'].iloc[-1] - monthly['cnt'].iloc[-2]) / monthly['cnt'].iloc[-2]) * 100
else:
    growth = 0

st.metric("📈 Growth Bulanan", f"{growth:.2f}%", delta=f"{growth:.2f}%")

st.markdown("---")

# ======================
# TABS
# ======================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren",
    "🌤️ Musim",
    "🌧️ Cuaca",
    "📊 Weekday vs Weekend"
])

# ======================
# TREND
# ======================
with tab1:
    daily = df.groupby('dteday')['cnt'].sum().reset_index()

    fig = px.line(
        daily,
        x='dteday',
        y='cnt',
        markers=True,
        title="Tren Penyewaan Sepeda"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)
    st.info("Terlihat pola peningkatan pada periode tertentu.")

# ======================
# SEASON
# ======================
with tab2:
    season_avg = df.groupby('season_label')['cnt'].mean().reset_index()

    fig = px.bar(
        season_avg,
        x='season_label',
        y='cnt',
        text_auto=True,
        title="Rata-rata Penyewaan per Musim"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)

# ======================
# WEATHER
# ======================
with tab3:
    weather_avg = df.groupby('weather_label')['cnt'].mean().reset_index()

    fig = px.pie(
        weather_avg,
        values='cnt',
        names='weather_label',
        hole=0.4,
        title="Distribusi Berdasarkan Cuaca"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.warning("Cuaca buruk menurunkan jumlah penyewaan.")

# ======================
# WEEKDAY VS WEEKEND
# ======================
with tab4:
    compare = df.groupby('is_weekend')['cnt'].mean().reset_index()
    compare['type'] = compare['is_weekend'].map({True:"Weekend", False:"Weekday"})

    fig = px.bar(
        compare,
        x='type',
        y='cnt',
        text_auto=True,
        color='type',
        title="Perbandingan Weekday vs Weekend"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("Weekend cenderung digunakan untuk aktivitas santai.")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("Bike Sharing Dashboard • Submission Dicoding")
