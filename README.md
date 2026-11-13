# 🛒 OlistIQ — Brazilian E-Commerce Analytics Platform

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Tests](https://img.shields.io/badge/Tests-19%20passed-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Objective

**OlistIQ** is an end-to-end data analytics and intelligence platform built on the **Brazilian E-Commerce Public Dataset by Olist** (~100,000 orders across 2016–2018). The project demonstrates a complete **data engineering + analytics workflow** — from raw CSV ingestion to production-grade interactive dashboard — showcasing skills required for Data Analyst / Data Engineer roles.

**Core Goals:**
- Transform 9 messy raw CSV files into a clean, analysis-ready dataset
- Build a relational data model with proper PK/FK relationships
- Implement automated data quality validation (19 pytest tests)
- Create an executive-level interactive dashboard with geographic insights
- Document the entire pipeline for reproducibility and portfolio showcase

---

## 🏗️ System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   DATA SOURCE   │     │  ETL PIPELINE    │     │   ANALYTICS LAYER   │
│  (Kaggle Olist) │────▶│  (src/clean_     │────▶│  (data/clean/       │
│  9 CSV files    │     │   data.py)       │     │   orders_master.csv)│
└─────────────────┘     └──────────────────┘     └──────────┬──────────┘
                                                             │
                        ┌────────────────────────────────────┼────────────┐
                        ▼                                    ▼            ▼
               ┌─────────────────┐              ┌─────────────────┐ ┌──────────────┐
               │  STREAMLIT DASH │              │   SQL QUERIES   │ │  PYTEST SUITE │
               │   (app.py)      │              │   (sql/*.sql)   │ │  (tests/)    │
               └─────────────────┘              └─────────────────┘ └──────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  DEPLOYMENT     │
               │  (Streamlit     │
               │   Cloud)        │
               └─────────────────┘
```

### Data Flow Summary
1. **Extract**: 9 raw CSVs from `data/raw/` (126 MB total)
2. **Transform**: `src/clean_data.py` → timestamp parsing, category translation, aggregations, KPI derivations
3. **Load**: Clean master dataset → `data/clean/orders_master.csv` (33 MB, 99,441 rows, 25 columns)
4. **Analyze**: Streamlit dashboard + SQL queries + automated tests
5. **Visualize**: 5-tab executive dashboard with geographic choropleth maps

---

## 📊 Dataset Description

**Source**: [Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

| File | Records | Description |
|------|---------|-------------|
| `olist_orders_dataset.csv` | 99,441 | Order lifecycle (purchase → delivery) |
| `olist_order_items_dataset.csv` | 112,650 | Items per order (price, freight, product) |
| `olist_order_payments_dataset.csv` | 103,886 | Payment transactions (type, installments, value) |
| `olist_order_reviews_dataset.csv` | 99,224 | Customer review scores (1–5) |
| `olist_customers_dataset.csv` | 99,441 | Customer info (city, state, unique ID) |
| `olist_products_dataset.csv` | 32,951 | Product catalog (category in Portuguese) |
| `olist_sellers_dataset.csv` | 3,095 | Seller info (city, state) |
| `olist_geolocation_dataset.csv` | 1,000,000+ | ZIP code → lat/long mapping |
| `product_category_name_translation.csv` | 71 | Portuguese → English category mapping |

---

## 🔧 Tech Stack

| Layer | Tools |
|-------|-------|
| **Language** | Python 3.10+ |
| **Data Processing** | Pandas 2.0, NumPy |
| **Visualization** | Plotly 5.15+, Streamlit 1.30+ |
| **Database/Query** | SQLite (via SQL files), Pandas SQL-like ops |
| **Testing** | Pytest 7+ (19 automated tests) |
| **Geospatial** | GeoJSON (Brazil states), Plotly Choropleth |
| **Deployment** | Streamlit Community Cloud (free) |
| **Version Control** | Git + GitHub |

---

## 📁 Repository Structure

```text
OlistIQ/
├── app.py                              # Main Streamlit dashboard (5 tabs, 3 choropleth maps)
├── requirements.txt                    # Minimal dependencies for zero-error deploy
├── .gitignore                          # Excludes venv, raw/clean data, cache
├── README.md                           # This file
│
├── data/
│   ├── raw/                            # 9 original Kaggle CSVs (gitignored)
│   └── clean/                          # Pre-computed analytics datasets
│       ├── orders_master.csv           # 99,441 rows × 25 cols (33 MB)
│       └── category_summary.csv        # 74 categories × 5 metrics
│
├── src/
│   ├── load_data.py                    # Raw file verification utility
│   └── clean_data.py                   # ETL pipeline (run once to generate clean data)
│
├── sql/                                # Production-ready analytical SQL
│   ├── 01_monthly_revenue_and_growth.sql      # MoM revenue with LAG()
│   ├── 02_delivery_sla_by_state.sql           # State-level logistics KPIs
│   └── 03_rfm_customer_segmentation.sql       # NTILE(4) RFM segmentation
│
├── tests/
│   └── test_pipeline_and_metrics.py    # 19 automated data quality tests
│
├── dashboard/
│   ├── README.md                       # Dashboard feature guide + deploy instructions
│   └── dashboard_screenshots/          # Visual assets for portfolio (10 PNGs)
│
└── verify_clean.py                     # (temp) Data validation script
```

---

## ⚙️ How We Built It — Step by Step

### Phase 1: Data Ingestion & Verification (`src/load_data.py`)
- Verifies all 9 CSV files exist in `data/raw/`
- Checks file sizes, row counts, column names, dtypes, missing values
- Outputs structured summary for audit trail

### Phase 2: ETL Pipeline (`src/clean_data.py`)
**Single script transforms 9 raw CSVs → 1 clean master dataset:**

| Transformation | Details |
|----------------|---------|
| **Timestamp Parsing** | 5 datetime columns parsed with `errors='coerce'` |
| **Delivery Metrics** | `delivery_days` (actual), `estimated_days` (promised), `is_delayed` (boolean flag) |
| **Category Translation** | Portuguese → English via mapping table; fallback to original; title-case formatting |
| **Order Aggregations** | Items: count, total price, total freight, dominant category<br>Payments: total value, max installments, dominant type<br>Reviews: mean score |
| **Customer Enrichment** | Join customer city/state for geographic analysis |
| **Defaults & Cleanup** | Fill missing payment = items + freight; fill missing category = "Other"; ensure types |

**Outputs:**
- `data/clean/orders_master.csv` — 99,441 orders, 25 analytical columns
- `data/clean/category_summary.csv` — 74 categories, sorted by revenue

### Phase 3: Automated Testing (`tests/test_pipeline_and_metrics.py`)
**19 tests across 6 categories:**

| Category | Tests | Purpose |
|----------|-------|---------|
| Raw Files | 2 | Existence, non-empty, expected columns |
| Cleaning Logic | 3 | Non-negative delivery days, parsed timestamps, edge cases |
| KPI Calculations | 5 | GMV, AOV, on-time %, review avg, no division-by-zero |
| Category Translation | 3 | Coverage >90%, English names, summary structure |
| Data Quality | 4 | PK uniqueness, non-negative financials, state coverage |
| Structure | 2 | Expected columns, row count consistency |

Run: `pytest tests/ -v` → **19 passed in ~1s**

### Phase 4: Analytical SQL (`sql/`)
Three production-ready queries using window functions:

| Query | Techniques | Business Question |
|-------|------------|-------------------|
| `01_monthly_revenue_and_growth.sql` | `LAG()`, `strftime()`, CTEs | Monthly revenue trend + MoM growth % |
| `02_delivery_sla_by_state.sql` | `julianday()`, conditional aggregation | State-level delivery speed & SLA breach |
| `03_rfm_customer_segmentation.sql` | `NTILE(4)`, quantile scoring | Customer loyalty tiers (Champions → Lost) |

### Phase 5: Interactive Dashboard (`app.py`)
**5 tabs with executive-grade visualizations:**

| Tab | Visualizations | Key Insights |
|-----|----------------|--------------|
| **📈 Revenue Trajectory** | Dual-axis bar/line (revenue + orders), MoM growth %, AOV trend | Black Friday 70% MoM surge; seasonality patterns |
| **🏷️ Category & Catalog** | Top 12 revenue (horizontal bar), Top 12 volume | Health & Beauty, Watches & Gifts, Bed Bath Table = 35% GMV |
| **🚚 Logistics & Delivery SLA** | **3 choropleth maps** (transit days, delay %, freight/price), 3 bar rankings | North states (RR, AP, AM): 25-30d transit, >15% delay, >25% freight ratio |
| **💳 Payment Economics** | Revenue share donut, AOV by method | Credit Card 75.8% revenue; Boleto 19.1% |
| **📋 Data Explorer** | Filtered table (500 rows), CSV export | Ad-hoc investigation with sidebar filters |

**Sidebar Filters:** Date range, 27 states multi-select, 74 categories multi-select, order status

---

## 📈 Key Results & Metrics

| Metric | Value |
|--------|-------|
| **Total Orders Analyzed** | 99,441 |
| **Gross Merchandise Value (GMV)** | R$ 16,009,015.58 |
| **Delivered Orders** | 96,478 (97%) |
| **Average Order Value (AOV)** | R$ 165.94 |
| **Average Review Score** | 4.09 / 5.0 |
| **On-Time Delivery Rate** | 92.1% |
| **Average Transit Time** | 12.3 days |
| **Categories Translated** | 74 (Portuguese → English) |
| **States Covered** | 27 (all Brazilian UFs) |
| **Automated Tests** | 19 / 19 passing |

---

## 🚀 Quickstart: Running Locally

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
# 1. Clone repository
git clone https://github.com/AnuragSingh2101/OlistIQ.git
cd OlistIQ

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 4. Activate (macOS/Linux)
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
```

### Generate Clean Data (One-time)
```bash
# Run ETL pipeline to create data/clean/orders_master.csv
python src/clean_data.py
```
> **Note**: Pre-generated files already exist in `data/clean/`. Run only if you modify `clean_data.py`.

### Launch Dashboard
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

### Run Tests
```bash
pytest tests/ -v
```

---

## 🌐 Deploy to Streamlit Community Cloud (Free)

1. **Push to GitHub** (ensure `data/clean/orders_master.csv` is committed or regenerate via GitHub Actions)
2. Visit [share.streamlit.io](https://share.streamlit.io/) → Log in with GitHub
3. Click **"New app"**
4. Select repository: `AnuragSingh2101/OlistIQ`
5. Main file path: `app.py`
6. Click **Deploy**

Your live URL: `https://olistiq.streamlit.app` (example)

> **Tip**: For large `orders_master.csv` (33 MB), enable Git LFS or use GitHub Actions to regenerate on deploy.

---

## 🧪 Testing Strategy

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test class
pytest tests/test_pipeline_and_metrics.py::test_gmv_calculation -v

# Run with HTML report
pytest tests/ --html=reports/test_report.html --self-contained-html
```

**Test Categories:**
- **Critical** (fail = block deploy): PK uniqueness, non-negative financials, timestamp parsing
- **Warning** (fail = investigate): Category translation coverage, row count drift
- **Info** (fail = log): Edge cases (delivery before purchase)

---

## 📊 Dashboard Feature Walkthrough

### Executive KPI Scorecards (All Tabs)
| KPI | Formula | Visual |
|-----|---------|--------|
| **GMV** | `SUM(total_payment_value)` | Blue accent card |
| **AOV** | `GMV / COUNT(DISTINCT order_id)` | Emerald accent card |
| **Satisfaction** | `AVG(review_score)` | Amber accent card |
| **On-Time %** | `COUNT(!is_delayed) / COUNT(delivered) * 100` | Purple accent card |
| **Avg Transit** | `AVG(delivery_days)` | Rose accent card |

### Logistics Tab — Geographic Intelligence (NEW)
Three **choropleth maps** using Brazil states GeoJSON:

1. **Average Delivery Duration** — Reds color scale; hover shows exact days
2. **SLA Breach Rate** — YlOrRd scale; % orders past estimated date
3. **Freight-to-Price Ratio** — Purples scale; avg freight as % of item price

**Bar Rankings** (below maps):
- Slowest 12 states by transit time
- Highest 12 states by delay rate
- Highest 12 states by freight cost burden

**Key Finding**: Northern states (RR, AP, AM, RO, AC) suffer 2-3× worse logistics vs. Southeast (SP, PR, RJ, SC).

---

## 📝 Data Quality & Cleaning Decisions

| Issue | Decision | Rationale |
|-------|----------|-----------|
| Missing `product_category_name` | Fill with "Other" via translation fallback | Preserves order rows; minimal impact (0.3%) |
| Delivery before purchase (negative days) | Flag but keep | Data entry errors; < 0.1% of delivered orders |
| Payment total ≠ items + freight | Use payment total as GMV source | Includes installments, discounts, fees |
| Duplicate order_items (exact rows) | Keep all | May represent legitimate multiple units |
| Unmapped categories (7/71) | Fallback to Portuguese name → title case | No data loss; readable |

Full cleaning log: Run `src/clean_data.py` → console output shows row counts at each stage.

---

## 🔮 Future Improvements

| Area | Idea |
|------|------|
| **Real-time** | Kafka → Streamlit with `st.experimental_fragment` |
| **ML** | Demand forecasting (Prophet), churn prediction (XGBoost) |
| **Geospatial** | Route optimization with `geolocation_dataset` + OSRM |
| **CI/CD** | GitHub Actions: lint → test → build → deploy |
| **Database** | PostgreSQL + dbt for production modeling |
| **Auth** | Streamlit Authenticator for multi-user access |

---

## 📄 License

MIT License — Free to use, modify, and distribute for learning and portfolio purposes.

Dataset © Olist (Kaggle) — Used under [Kaggle Terms of Use](https://www.kaggle.com/competitions/olist-brazilian-ecommerce/overview).

---

## 🙏 Acknowledgments

- **Olist** for releasing the Brazilian E-Commerce dataset
- **Kaggle** for hosting and community kernels
- **Streamlit, Plotly, Pandas** teams for excellent open-source tools
- **Community** for Brazil states GeoJSON (codeforamerica/click_that_hood)

---

## 📞 Contact

**Anurag Singh** — Data Analyst / Data Engineer Aspirant
- GitHub: [@AnuragSingh2101](https://github.com/AnuragSingh2101)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

> **Built as a portfolio project to demonstrate end-to-end data analytics competency.**  
> If you're hiring for Data Analyst / Data Engineer internships — let's talk!