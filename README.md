# Olist Data Quality & Analytics Pipeline

**Building a reliable analytical database through data profiling, cleaning, automated validation and business intelligence.**

## 📦 Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd olist-data-quality-analytics-pipeline
```

### 2. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install -r requirements.txt
```

### 3. Download Dataset
**Manual (easiest):**
1. Go to: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Download `archive.zip`
3. Extract all 9 CSV files into `data/raw/`

**Expected files in `data/raw/`:**
```
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_customers_dataset.csv
olist_sellers_dataset.csv
olist_products_dataset.csv
olist_geolocation_dataset.csv
product_category_name_translation.csv
```

### 4. Verify Data Load
```bash
python src/load_data.py
```

### 5. Run Tests
```bash
pytest tests/ -v
```

## 📁 Repository Structure
```
olist-data-quality-analytics-pipeline/
│
├── data/
│   ├── raw/           # Original Kaggle CSVs (gitignored)
│   ├── clean/         # Cleaned CSVs (gitignored)
│   └── README.md
│
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_data_quality_summary.ipynb
│
├── src/
│   ├── load_data.py
│   ├── profile_data.py
│   ├── clean_data.py
│   ├── validate_data.py
│   └── database.py
│
├── sql/
│   ├── schema.sql
│   ├── data_quality_checks.sql
│   └── business_analysis.sql
│
├── reports/
│   ├── data_quality_report.md
│   ├── cleaning_log.csv
│   └── validation_results.csv
│
├── tests/
│   └── test_data_quality.py
│
├── dashboard/
│   └── dashboard_screenshots/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 🎯 Project Phases
1. **Data Collection & Setup** ← *You are here*
2. Data Profiling
3. Data Cleaning & Standardization
4. Cleaning Logs & Audit Trail
5. SQLite Database Design
6. SQL Data Quality Validation
7. Automated Testing (pytest)
8. Exploratory Data Analysis
9. Business SQL Analysis
10. Data Quality Report
11. Optional: Power BI Dashboard

## 📊 Dataset Description
The **Olist Brazilian E-Commerce** dataset contains 100k+ orders from 2016-2018 across multiple tables:
- **Customers, Orders, Order Items, Payments, Reviews**
- **Products, Sellers, Geolocation, Category Translations**

## 🛠 Tech Stack
Python • Pandas • NumPy • Jupyter • SQLite • SQL • Matplotlib • Seaborn • pytest • Git

## 📝 License
Educational portfolio project. Dataset © Olist (Kaggle).