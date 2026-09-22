import duckdb
import pandas as pd

print("1. Menginisialisasi DuckDB & Menjalankan SQL Pipeline...")

# Menggunakan triple quotes (""") agar bisa menulis SQL multi-baris dengan rapi
sql_query = """
-- CTE 1: Menggabungkan (JOIN) 3 tabel inti untuk mendapatkan detail transaksi
WITH order_details AS (
    SELECT 
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp::TIMESTAMP AS order_date,
        p.payment_value
    FROM read_csv_auto('D:/PROJECT/ecommerce-rfm-churn-pipeline/data/raw/olist_customers_dataset.csv') c
    JOIN read_csv_auto('D:/PROJECT/ecommerce-rfm-churn-pipeline/data/raw/olist_orders_dataset.csv') o 
        ON c.customer_id = o.customer_id
    JOIN read_csv_auto('D:/PROJECT/ecommerce-rfm-churn-pipeline/data/raw/olist_order_payments_dataset.csv') p 
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
),

-- CTE 2: Melakukan Agregasi (GROUP BY) untuk mendapatkan nilai dasar RFM per Pelanggan
rfm_base AS (
    SELECT 
        customer_unique_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(payment_value) AS monetary
    FROM order_details
    GROUP BY customer_unique_id
),

-- CTE 3: Menentukan Titik Referensi Waktu (Hari 'Ini' berdasarkan data terakhir)
max_date AS (
    SELECT MAX(last_order_date) AS current_date FROM rfm_base
)

-- FINAL SELECT: Menghitung Recency dan Labeling Churn
SELECT 
    r.customer_unique_id,
    r.frequency,
    r.monetary,
    -- Menghitung selisih hari antara transaksi terakhir dengan tanggal referensi (Recency)
    date_diff('day', r.last_order_date, m.current_date) AS recency,
    -- Labeling Churn: Jika pelanggan tidak belanja selama lebih dari 180 hari (6 bulan)
    CASE 
        WHEN date_diff('day', r.last_order_date, m.current_date) > 180 THEN 1 
        ELSE 0 
    END AS is_churn
FROM rfm_base r
CROSS JOIN max_date m
"""

# Menjalankan query dan langsung mengubahnya menjadi Pandas DataFrame
df_rfm = duckdb.query(sql_query).to_df()

print("2. Preview Data Hasil Transformasi (One Big Table):")
print(df_rfm.head())
print(f"\nTotal Pelanggan Unik: {len(df_rfm)}")

print("\n3. Menyimpan Hasil ke Parquet...")

# Menyimpan data bersih ke folder processed untuk dipakai Data Scientist
df_rfm.to_parquet('D:/PROJECT/ecommerce-rfm-churn-pipeline/data/processed/rfm_churn_data.parquet', index=False)
print("Selesai! File rfm_churn_data.parquet berhasil dibuat di folder data/processed/")