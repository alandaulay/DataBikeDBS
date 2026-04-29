import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard Pro",
    page_icon="🚲",
    layout="wide"
)

# ======================
# STYLE (BIAR KELAS PRO)
# ======================
st.markdown("""
<style>
.main {background-color: #F9FAFB;}
.block-container {padding-top: 2rem;}
h1 {font-weight: 800;}
.metric-card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
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

    # 
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
    df['is_weekend'] = df['weekday'].isin(['Saturday','Sunday'])
    df['month'] = df['dteday'].dt.to_period('M')

    return df

df = load_data()

# ======================
# SIDEBAR (SCROLLABLE FILTER)
# ======================
with st.sidebar:
    st.title(" Filter Data")

    selected_season = st.multiselect(
        "Pilih Musim (Scroll)",
        options=sorted(df['season_label'].dropna().unique()),
        default=sorted(df['season_label'].dropna().unique())
    )

    st.markdown("---")
    st.info("Gunakan filter untuk eksplorasi data secara interaktif.")

df_filtered = df[df['season_label'].isin(selected_season)]

# ======================
# HEADER
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis penggunaan sepeda berbasis musim, cuaca, dan perilaku pengguna")

# ======================
# METRICS
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{df_filtered['cnt'].mean():.0f}")
col3.metric("Puncak Rental", f"{df_filtered['cnt'].max():,}")
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
# HIGHLIGHT MUSIM TERBAIK
# ======================
best_season = df_filtered.groupby('season_label')['cnt'].mean().idxmax()

st.success(f" Musim dengan performa terbaik: **{best_season}**")

# ======================
# LAYOUT
# ======================
col1, col2 = st.columns(2)

# ======================
# TREND
# ======================
with col1:
    st.subheader("📈 Tren Penyewaan")

    daily = df_filtered.groupby('dteday')['cnt'].sum().reset_index()

    fig = px.line(daily, x='dteday', y='cnt', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:**
    - Terlihat pola peningkatan pada periode tertentu
    - Menunjukkan adanya jam atau musim sibuk
    """)

# ======================
# MUSIM
# ======================
with col2:
    st.subheader("🌤️ Analisis Musim")

    season_avg = df_filtered.groupby('season_label')['cnt'].mean().reset_index()

    fig = px.bar(season_avg, x='season_label', y='cnt', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:**
    - Musim hangat cenderung memiliki penyewaan lebih tinggi
    - Musim dingin biasanya mengalami penurunan signifikan
    """)

# ======================
# ROW 2
# ======================
col3, col4 = st.columns(2)

# ======================
# CUACA
# ======================
with col3:
    st.subheader("🌧️ Kondisi Cuaca")

    weather_avg = df_filtered.groupby('weather_label')['cnt'].mean().reset_index()

    fig = px.pie(weather_avg, values='cnt', names='weather_label', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:**
    - Cuaca cerah mendominasi penggunaan sepeda
    - Cuaca buruk menurunkan minat pengguna
    """)

# ======================
# WEEKEND VS WEEKDAY
# ======================
with col4:
    st.subheader("📊 Perilaku Pengguna")

    compare = df_filtered.groupby('is_weekend')['cnt'].mean().reset_index()
    compare['type'] = compare['is_weekend'].map({True:"Weekend", False:"Weekday"})

    fig = px.bar(compare, x='type', y='cnt', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:**
    - Weekday digunakan untuk commuting
    - Weekend lebih ke aktivitas santai
    """)

# ======================
# KESIMPULAN
# ======================
st.markdown("---")
st.subheader(" Kesimpulan")

st.markdown(f"""
- Penggunaan sepeda sangat dipengaruhi oleh **musim dan cuaca**
- **{best_season}** menjadi periode dengan performa tertinggi
- Aktivitas pengguna terbagi antara:
  - **Weekday → transportasi**
  - **Weekend → rekreasi**
- Cuaca buruk menjadi faktor utama penurunan penggunaan
""")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("<div style='text-align:center;color:gray'>Bike Sharing Dashboard • Advanced Level Submission</div>", unsafe_allow_html=True)
