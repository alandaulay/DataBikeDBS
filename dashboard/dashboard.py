import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard Pro",
    page_icon="🚲",
    layout="wide"
)

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>
.main {background-color: #F9FAFB;}
h1, h2, h3 {font-family: 'Segoe UI';}
.footer {text-align:center; color:gray; font-size:14px;}
</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])

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
except:
    st.error("Dataset tidak ditemukan.")
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
# METRICS + KPI GROWTH
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
col2.metric("Rata-rata", f"{df_filtered['cnt'].mean():.0f}")
col3.metric("Tertinggi", f"{df_filtered['cnt'].max():,}")
col4.metric("Jumlah Hari", df_filtered['dteday'].nunique())

# KPI Growth
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
    "🔥 Heatmap Jam",
    "📊 Weekday vs Weekend"
])

# ======================
# TAB 1: TREND
# ======================
with tab1:
    daily = df_filtered.groupby('dteday')['cnt'].sum().reset_index()

    fig = px.line(daily, x='dteday', y='cnt', markers=True)
    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)
    st.info("Terlihat pola kenaikan pada waktu tertentu.")

# ======================
# TAB 2: SEASON
# ======================
with tab2:
    season_avg = df_filtered.groupby('season_label')['cnt'].mean().reset_index()

    fig = px.bar(season_avg, x='season_label', y='cnt', text_auto=True)
    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)

# ======================
# TAB 3: WEATHER
# ======================
with tab3:
    weather_avg = df_filtered.groupby('weather_label')['cnt'].mean().reset_index()

    fig = px.pie(weather_avg, values='cnt', names='weather_label', hole=0.4)

    st.plotly_chart(fig, use_container_width=True)
    st.warning("Cuaca buruk menurunkan jumlah penyewaan.")

# ======================
# TAB 4: HEATMAP
# ======================
with tab4:
    st.subheader("Heatmap Jam vs Rental")

    heatmap = df_filtered.groupby(['hour','weekday'])['cnt'].mean().reset_index()
    pivot = heatmap.pivot(index='hour', columns='weekday', values='cnt')

    fig = px.imshow(pivot, aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

    st.info("Jam sibuk: pagi & sore hari kerja.")

# ======================
# TAB 5: WEEKDAY VS WEEKEND
# ======================
with tab5:
    compare = df_filtered.groupby('is_weekend')['cnt'].mean().reset_index()
    compare['type'] = compare['is_weekend'].map({True:"Weekend", False:"Weekday"})

    fig = px.bar(compare, x='type', y='cnt', text_auto=True, color='type')
    st.plotly_chart(fig, use_container_width=True)

    st.info("Weekend cenderung digunakan untuk leisure.")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown("<div class='footer'>Bike Sharing Dashboard • Dicoding Submission</div>", unsafe_allow_html=True)
