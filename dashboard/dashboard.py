import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

sns.set_style("whitegrid")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("main_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# ======================
# MAPPING LABEL (FIX REVIEWER)
# ======================
season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_map = {
    1: "Clear",
    2: "Mist",
    3: "Light Rain/Snow",
    4: "Heavy Rain"
}

df['season_label'] = df['season'].map(season_map)
df['weather_label'] = df['weathersit'].map(weather_map)

# ======================
# TITLE
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penggunaan sepeda berdasarkan musim, waktu, dan kondisi cuaca.")

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🔎 Filter Data")

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=df['season_label'].unique(),
    default=df['season_label'].unique()
)

df_filtered = df[df['season_label'].isin(selected_season)]

# ======================
# METRICS
# ======================
st.subheader("📊 Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
col2.metric("Rata-rata Rental", f"{df_filtered['cnt'].mean():.0f}")
col3.metric("Max Rental", f"{df_filtered['cnt'].max():,}")

# ======================
# TIME SERIES
# ======================
st.subheader("📈 Tren Penyewaan Sepeda")

st.line_chart(df_filtered.set_index('dteday')['cnt'])

st.caption("📌 Terlihat pola peningkatan pada waktu tertentu (jam sibuk).")

# ======================
# SEASON ANALYSIS
# ======================
st.subheader("🌤️ Penyewaan Berdasarkan Musim")

season_data = df_filtered.groupby('season_label')['cnt'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(8,5))
sns.barplot(x='season_label', y='cnt', data=season_data, palette="Blues", ax=ax1)

ax1.set_title("Rata-rata Penyewaan per Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig1)

st.caption("📌 Musim dingin memiliki jumlah penyewaan paling rendah.")

# ======================
# WEATHER ANALYSIS
# ======================
st.subheader("🌦️ Pengaruh Cuaca")

weather_data = df_filtered.groupby('weather_label')['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(8,5))
sns.barplot(x='weather_label', y='cnt', data=weather_data, palette="Reds", ax=ax2)

ax2.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig2)

st.caption("📌 Cuaca buruk menurunkan jumlah penyewaan secara signifikan.")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("📊 Dibuat untuk submission analisis data - Bike Sharing Dataset")