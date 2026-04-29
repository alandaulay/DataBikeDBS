#  Bike Sharing Data Analysis & Dashboard

##  Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis pola penggunaan sepeda berdasarkan faktor waktu, musim, dan kondisi cuaca menggunakan dataset **Bike Sharing**. 

Analisis dilakukan untuk menemukan insight yang dapat membantu dalam pengambilan keputusan operasional dan strategi peningkatan penggunaan layanan.

---

##  Pertanyaan Bisnis

### 1. 
Faktor apa saja yang memengaruhi penurunan jumlah penyewaan sepeda pada musim dingin dibanding musim lainnya?

### 2. 
Bagaimana pengaruh jam (hour) dan kondisi cuaca terhadap jumlah penyewaan sepeda?

---

##  Tahapan Analisis

### 1. Data Wrangling
- Mengumpulkan dataset (day.csv & hour.csv)
- Mengecek missing values, duplicate, dan tipe data
- Melakukan cleaning:
  - Konversi tipe data datetime
  - Menghapus data duplikat
  - Mengatasi outlier sederhana

### 2. Exploratory Data Analysis (EDA)
- Analisis berdasarkan musim
- Analisis pola penggunaan berdasarkan jam
- Analisis pengaruh kondisi cuaca

### 3. Visualization
- Bar chart untuk analisis musim
- Line chart untuk pola jam & cuaca
- Visualisasi tambahan untuk memperkuat insight

### 4. Advanced Analysis
- RFM Analysis (Recency, Frequency, Monetary)
- Binning / clustering sederhana untuk segmentasi

---

##  Insight Utama

###  Musim
Penggunaan sepeda paling rendah terjadi pada musim dingin, yang menunjukkan bahwa kondisi cuaca ekstrem sangat memengaruhi perilaku pengguna.

###  Jam Sibuk
Terjadi lonjakan penggunaan pada:
- Pagi (sekitar 08.00)
- Sore (sekitar 17.00)

Menunjukkan pola commuting (berangkat & pulang kerja).

###  Cuaca
Kondisi cuaca buruk secara signifikan menurunkan jumlah penyewaan, bahkan pada jam sibuk.

---

##  Rekomendasi

- Memberikan promo atau insentif pada musim dingin  
- Menambah jumlah sepeda pada jam sibuk  
- Menggunakan data cuaca untuk prediksi permintaan  
- Mengoptimalkan distribusi sepeda berdasarkan pola penggunaan  

---

##  Struktur Proyek

submission/
│
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
│
├── data/
│   ├── day.csv
│   └── hour.csv
│
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

---

---

##  Cara Menjalankan Dashboard

### 1. Install Dependencies

pip install -r requirements.txt

### 2. Masuk ke Folder Dashboard
cd dashboard

### 3. Jalankan Streamlit
streamlit run dashboard.py