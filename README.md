# End-to-End E-Commerce Advanced Analytics & ML Pipeline

## Deskripsi Proyek
Proyek ini adalah sistem analitik data *end-to-end* yang dirancang untuk memecahkan masalah bisnis nyata di industri E-Commerce (menggunakan *Olist Brazilian E-Commerce Dataset*). Proyek ini membangun *pipeline* Data Engineering berbasis SQL untuk menyatukan *Relational Database*, dilanjutkan dengan pengembangan 4 pemodelan *Machine Learning* komprehensif mulai dari segmentasi pelanggan, prediksi *churn*, sistem rekomendasi *cross-selling*, hingga peramalan (*forecasting*) pendapatan masa depan.

## Tech Stack & Tools
- **Bahasa Pemrograman:** Python 3
- **Data Engineering & ELT:** DuckDB (In-Process SQL OLAP), SQL (Window Functions, CTEs), PyArrow (Parquet)
- **Machine Learning:** Scikit-Learn (Random Forest Regressor & Classifier, K-Means), mlxtend (Apriori)
- **Time-Series Analysis:** Feature Engineering (Lag, Rolling/Moving Average), Chronological Splitting
- **Visualisasi Data:** Matplotlib, Seaborn

## Struktur Repositori
```text
├── data/
│   ├── raw/                 # Dataset mentah CSV (Customers, Orders, Payments, Items, dll.)
│   └── processed/           # One Big Table (OBT) berformat Parquet hasil transformasi
├── notebooks/
│   ├── 01_rfm_clustering.ipynb        # Unsupervised Learning: Customer Segmentation
│   ├── 02_churn_prediction.ipynb      # Supervised Learning: Churn Classification
│   ├── 03_recommendation_engine.ipynb # Market Basket Analysis (Apriori)
│   └── 04_revenue_forecasting.ipynb   # Time-Series Revenue Forecasting
├── src/
│   └── etl_rfm.py           # Script ELT (Extract, Load, Transform) menggunakan DuckDB
└── README.md
```
## Modul 1: Data Engineering (ETL Pipeline)
Menggunakan DuckDB, data mentah dari 9 tabel relasional yang diekstrak dan ditransformasikan menggunakan *Advanced SQL Query*.
- Melakukan operasi JOIN multi-tabel untuk menggabungkan metrik Customers, Orders, dan Payments.
- Menggunakan operasi agregasi tingkat lanjut (CTEs) untuk merumuskan matriks RFM (Recency, Frequency, Monetary).
- Menyimpan hasil transformasi menjadi One Big Table (OBT) berformat .parquet untuk efisiensi komputasi tahap Data Science.

## Modul 2: Machine Learning Suite
Data bersih yang dihasilkan dari pipeline ETL diproses menjadi 4 solusi analitik yang dapat langsung diterapkan oleh tim bisnis/*marketing*
1. **Customer Segmentation (K-Means Clustering):** Membagi 93.000+ pelanggan ke dalam 4 segmen berdasarkan RFM. Berhasil mengidentifikasi segmen "VIP/Sultan" yang mendominasi profitabilitas meskipun frekuensi belanja rendah, serta memisahkan pelanggan baru dan pelanggan churn.
2. **Churn Prediction (Random Forest Classifier):** Membangun klasifikasi probabilitas pelanggan berhenti berbelanja. Dengan mengatasi permasalahan *Data Leakage* (menghapus variabel *Recency*), model ini mencapai metrik performa di dunia nyata dengan *Precision* 79% dan *Recall* 76% untuk kelas target (Churn).
3. **Recommendation Engine (Apriori Algorithm):** Mengimplementasikan *Market Basket Analysis* untuk merekomendasikan produk pelengkap. Berhasil menemukan aturan asosiasi (*Association Rules*) dengan metrik Lift > 1, memberikan rekomendasi UI/UX berbasis data untuk fitur "*Frequently Bought Together*" (contoh: *Home Comfort & Bed/Bath*).
4. **Revenue Forecasting (Time-Series Random Forest):** Meramal omzet harian perusahaan menggunakan regresi *Time-Series*. Model dilatih dengan teknik *Chronological Splitting* (80% masa lalu, 20% masa depan) serta injeksi *Feature Engineering* berwujud *Lag Variables* dan *Moving Averages*, guna memetakan tren dan musiman pendapatan perusahaan.

## Cara Menjalankan Proyek
1. Clone repositori ini
```bash
git clone https://github.com/rafiffrhn/ecommerce-advanced-analytics-pipeline
cd ecommerce-advanced-analytics-pipeline
```
2. Download dataset Olist dari Kaggle dan letakkan seluruh file .csv di folder data/raw/
3. Install semua kebutuhan modul (requirements):
```bash
python -m pip install duckdb pandas numpy scikit-learn matplotlib seaborn mlxtend
```
4. Jalankan pipeline ETL untuk memproduksi data analitik:
```bash
python src/etl_rfm.py
```
5. Buka eksperimen di dalam folder notebooks/ secara berurutan.
