import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="darkgrid")

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

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

    season_map = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
    weather_map = {1:"Clear",2:"Mist",3:"Light Rain/Snow",4:"Heavy Rain"}

    df['season_label'] = df['season'].map(season_map)
    df['weather_label'] = df['weathersit'].map(weather_map)
    df['weekday'] = df['dteday'].dt.day_name()
    df['is_weekend'] = df['weekday'].isin(['Saturday','Sunday'])

    return df

df = load_data()

# ======================
# HEADER
# ======================
st.header("🚲 Bike Sharing Dashboard")
st.subheader("Analisis Penyewaan Sepeda")

# ======================
# METRICS
# ======================
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Rental", f"{df['cnt'].sum():,}")

with col2:
    st.metric("Rata-rata Harian", f"{df['cnt'].mean():.0f}")

# ======================
# TREND HARIAN
# ======================
st.subheader("Daily Rental Trend")

daily = df.groupby('dteday')['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(16,6))
ax.plot(daily['dteday'], daily['cnt'], marker='o')
ax.set_title("Tren Penyewaan Sepeda")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Rental")

st.pyplot(fig)

# ======================
# MUSIM
# ======================
st.subheader("Rental Berdasarkan Musim")

season = df.groupby('season_label')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x='season_label', y='cnt', data=season, ax=ax)
ax.set_title("Rata-rata Rental per Musim")

st.pyplot(fig)

# ======================
# CUACA
# ======================
st.subheader("Pengaruh Cuaca")

weather = df.groupby('weather_label')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x='weather_label', y='cnt', data=weather, ax=ax)
ax.set_title("Rata-rata Rental Berdasarkan Cuaca")

st.pyplot(fig)

# ======================
# WEEKDAY VS WEEKEND
# ======================
st.subheader("Weekday vs Weekend")

compare = df.groupby('is_weekend')['cnt'].mean().reset_index()
compare['type'] = compare['is_weekend'].map({True:"Weekend", False:"Weekday"})

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x='type', y='cnt', data=compare, ax=ax)
ax.set_title("Perbandingan Penggunaan")

st.pyplot(fig)

# ======================
# FOOTER
# ======================
st.caption("Bike Sharing Dashboard • Dicoding Style")
