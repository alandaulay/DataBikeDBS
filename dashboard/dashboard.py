import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================
# CONFIG & STYLING
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard Pro",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan lebih modern
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
    }
    h1 { color: #1E3A8A; font-family: 'Inter', sans-serif; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# ======================
# LOAD DATA (WITH CACHE)
# ======================
@st.cache_data
def load_data():
    # Pastikan file dashboard/main_data.csv tersedia
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Mapping Label agar tampilan lebih manusiawi
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {1: "Cerah/Berawan", 2: "Kabut/Mendung", 3: "Hujan Ringan/Salju", 4: "Hujan Deras/Badai"}
    
    df['season_label'] = df['season'].map(season_map)
    df['weather_label'] = df['weathersit'].map(weather_map)
    
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File 'dashboard/main_data.csv' tidak ditemukan. Pastikan path file benar.")
    st.stop()

# ======================
# SIDEBAR FILTER
# ======================
with st.sidebar:
    st.title("🚲 Bike Rental Filters")
    st.markdown("---")
    
    # Date Range Filter
    min_date, max_date = df['dteday'].min(), df['dteday'].max()
    date_range = st.date_input(
        "📅 Pilih Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Season Filter
    selected_season = st.multiselect(
        "🌸 Pilih Musim",
        options=df['season_label'].unique(),
        default=df['season_label'].unique()
    )

    st.markdown("---")
    st.info("Dashboard ini memvisualisasikan tren penggunaan sepeda berdasarkan data historis.")

# Terapkan Filter
if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df[
        (df['dteday'].dt.date >= start_date) & 
        (df['dteday'].dt.date <= end_date) &
        (df['season_label'].isin(selected_season))
    ]
else:
    df_filtered = df.copy()

# ======================
# HEADER SECTION
# ======================
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown(f"Menampilkan data dari **{date_range[0]}** hingga **{date_range[1]}**")

# --- METRIC CARDS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{df_filtered['cnt'].mean():.0f}")
with col3:
    st.metric("Puncak Penyewaan", f"{df_filtered['cnt'].max():,}")
with col4:
    st.metric("Total Hari", f"{df_filtered['dteday'].nunique()}")

st.markdown("---")

# ======================
# VISUALIZATION TABS
# ======================
tab1, tab2, tab3 = st.tabs(["📈 Tren Waktu", "🌤️ Analisis Musim", "🌦️ Kondisi Cuaca"])

with tab1:
    st.subheader("Tren Penyewaan Sepeda")
    daily_rent = df_filtered.groupby('dteday')['cnt'].sum().reset_index()
    fig_line = px.line(
        daily_rent, x='dteday', y='cnt',
        labels={'cnt': 'Jumlah Rental', 'dteday': 'Tanggal'},
        template="plotly_white",
        line_shape="spline", # Membuat garis melengkung halus
    )
    fig_line.update_traces(line_color='#2563EB', line_width=2)
    st.plotly_chart(fig_line, use_container_width=True)
    st.write("📌 *Gunakan mouse untuk drag dan zoom pada area tertentu di grafik.*")

with tab2:
    st.subheader("Rata-rata Penyewaan per Musim")
    season_avg = df_filtered.groupby('season_label')['cnt'].mean().sort_values(ascending=False).reset_index()
    
    fig_season = px.bar(
        season_avg, x='season_label', y='cnt',
        color='cnt',
        color_continuous_scale='Blues',
        labels={'cnt': 'Rata-rata Rental', 'season_label': 'Musim'}
    )
    fig_season.update_layout(showlegend=False)
    st.plotly_chart(fig_season, use_container_width=True)

with tab3:
    st.subheader("Pengaruh Cuaca terhadap Pengguna")
    weather_avg = df_filtered.groupby('weather_label')['cnt'].mean().reset_index()
    
    fig_weather = px.pie(
        weather_avg, values='cnt', names='weather_label',
        hole=0.4, # Membuat Donut Chart
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_weather, use_container_width=True)
    st.warning("Insight: Penyewaan turun drastis saat kondisi cuaca ekstrem.")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280;'>Data Analytics Submission - Bike Sharing Dataset</div>", 
    unsafe_allow_html=True
)
