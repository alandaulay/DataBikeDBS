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
# LOAD DATA (SAFE PATH)
# ======================
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "main_data.csv")

    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])

    # Mapping
    season_map = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
    weather_map = {1:"Clear",2:"Mist",3:"Light Rain/Snow",4:"Heavy Rain"}

    df['season_label'] = df['season'].map(season_map)
    df['weather_label'] = df['weathersit'].map(weather_map)

    # Feature tambahan
    df['hour'] = df['hr'] if 'hr' in df.columns else 0
    df['weekday'] = df['dteday'].dt.day_name()
    df['is_weekend'] = df['weekday'].isin(['Saturday','Sunday'])
    df['month'] = df['dteday'].dt.to_period('M')

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error load data: {e}")
    st.stop()

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.title("⚙️ Filter")

    start_date, end_date = st.date_input(
        "Pilih Tanggal",
        [df['dteday'].min(), df['dteday'].max()]
    )

    season = st.multiselect(
        "Pilih Musim",
        df['season_label'].unique(),
        default=df['season_label'].unique()
    )

# ======================
# FILTER DATA
# ======================
df_filtered = df[
    (df['dteday'].dt.date >= start_date) &
    (df['dteday'].dt.date <= end_date) &
    (df['season_label'].isin(season))
]

# ======================
# HEADER
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.caption(f"Periode: {start_date} sampai {end_date}")

# ======================
# METRICS + GROWTH
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
col2.metric("Rata-rata", f"{df_filtered['cnt'].mean():.0f}")
col3.metric("Tertinggi", f"{df_filtered['cnt'].max():,}")
col4.metric("Jumlah Hari", df_filtered['dteday'].nunique())

monthly = df_filtered.groupby('month')['cnt'].sum().reset_index()

if len(monthly) >= 2:
    growth = ((monthly['cnt'].iloc[-1] - monthly['cnt'].iloc[-2]) / monthly['cnt'].iloc[-2]) * 100
else:
    growth = 0

st.metric("📈 Growth Bulanan", f"{growth:.2f}%", delta=f"{growth:.2f}%")

st.markdown("---")

# ======================
# TABS
# ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tren",
    "🌤️ Musim",
    "🌧️ Cuaca",
    "🔥 Heatmap",
    "📊 Weekday vs Weekend"
])

# ======================
# TREND
# ======================
with tab1:
    daily = df_filtered.groupby('dteday')['cnt'].sum().reset_index()
    fig = px.line(daily, x='dteday', y='cnt', markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ======================
# SEASON
# ======================
with tab2:
    season_avg = df_filtered.groupby('season_label')['cnt'].mean().reset_index()
    fig = px.bar(season_avg, x='season_label', y='cnt', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# ======================
# WEATHER
# ======================
with tab3:
    weather_avg = df_filtered.groupby('weather_label')['cnt'].mean().reset_index()
    fig = px.pie(weather_avg, values='cnt', names='weather_label', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ======================
# HEATMAP
# ======================
with tab4:
    heatmap = df_filtered.groupby(['hour','weekday'])['cnt'].mean().reset_index()
    pivot = heatmap.pivot(index='hour', columns='weekday', values='cnt')
    fig = px.imshow(pivot, aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

# ======================
# WEEKDAY VS WEEKEND
# ======================
with tab5:
    compare = df_filtered.groupby('is_weekend')['cnt'].mean().reset_index()
    compare['type'] = compare['is_weekend'].map({True:"Weekend", False:"Weekday"})
    fig = px.bar(compare, x='type', y='cnt', text_auto=True, color='type')
    st.plotly_chart(fig, use_container_width=True)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("Bike Sharing Dashboard • Submission Dicoding")
