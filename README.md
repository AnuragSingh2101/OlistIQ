# 🛒 OlistIQ — Brazilian E-Commerce Analytics Platform

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**OlistIQ** is an end-to-end data analytics and intelligence platform built on the **Brazilian E-Commerce Public Dataset by Olist** (~100,000 orders across 2016–2018). It translates commercial, logistic, and financial transaction records into actionable executive insights through an interactive **Streamlit dashboard**, **exploratory data analysis notebooks**, **production-grade SQL models**, and **executive performance reports**.

---

## 🎯 Key Project Highlights & Insights

- **Commercial Velocity:** Analyzed **R$ 16.0M** in Gross Merchandise Value (GMV) across **99,441 orders**, identifying peak demand surges during Black Friday (~70% MoM volume surge).
- **Executive KPI Dashboard:** Real-time metrics including GMV, Total Orders, Average Order Value (AOV ~R$ 160.85), Review Ratings (★ 4.09/5), and SLA on-time fulfillment rates (92.1%).
- **Category Intelligence:** Translated and ranked 70+ Portuguese product categories into English; identified *Health & Beauty*, *Watches & Gifts*, and *Bed, Bath & Table* as the top GMV drivers (>35% of total sales).
- **Logistics & Regional SLA Benchmarks:** Uncovered regional transit disparities between the Southeastern core (`SP`, `PR`, `RJ` averaging 8–12 days) and northern states (`RR`, `AP`, `AM` exceeding 25–30 days with SLA delay risks >15%).
- **Payment Economics:** Modeled payment method distributions, demonstrating that Credit Cards capture **75.8% of total revenue**, with Boleto Bancário accounting for **19.1%**.

---

## 📂 Repository Architecture

```text
OlistIQ/
├── app.py                                  # Modern Streamlit executive analytics dashboard
├── requirements.txt                        # Python dependencies (Streamlit, Pandas, Plotly, etc.)
│
├── data/
│   ├── raw/                                # 9 raw Olist CSV datasets (~126 MB)
│   └── clean/                              # Optimized analytics datasets & summaries
│
├── dashboard/
│   ├── README.md                           # Dashboard feature walkthrough & cloud guide
│   └── dashboard_screenshots/              # Visual UI captures and screenshots
│
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb  # End-to-end Jupyter EDA with visualizations
│
├── reports/
│   ├── executive_summary.md                # Comprehensive business insights and strategy
│   └── executive_report.html               # Standalone interactive HTML report
│
├── sql/
│   ├── 01_monthly_revenue_and_growth.sql   # MoM revenue growth with window functions
│   ├── 02_delivery_sla_by_state.sql        # State-by-state logistics bottleneck queries
│   └── 03_rfm_customer_segmentation.sql    # Quantile-based RFM customer loyalty scoring
│
├── src/
│   ├── load_data.py                        # Dataset verification and file-check pipeline
│   └── clean_data.py                       # Automated ETL and data transformation suite
│
├── tests/                                  # Unit tests for data loaders and metrics
└── README.md                               # Project documentation
```

---

## 🖥️ Interactive Dashboard Features (`app.py`)

The Streamlit dashboard includes:

1. **Executive Metric Scorecards**: Card components with custom accent borders highlighting GMV, AOV, Review Satisfaction, On-Time Fulfillment %, and Average Transit Duration.
2. **Dynamic Sidebar Controls**: Date range slider, customer state (UF) multi-select, product category selector, and order status filters.
3. **Tab 1: Revenue Trajectory**: Dual-axis Plotly charts visualizing gross monthly revenue alongside order volume, paired with Month-over-Month (MoM) growth percentages.
4. **Tab 2: Category & Catalog**: Horizontal rankings of the top 12 categories by gross revenue and order volume.
5. **Tab 3: Logistics & Delivery SLA**: State-by-state ranking of transit times (identifying shipping bottlenecks) and SLA breach rates.
6. **Tab 4: Payment Economics**: Interactive revenue-share donuts and transaction volume distributions across payment types.
7. **Tab 5: Data Explorer**: Tabular browser allowing users to inspect and filter individual transactions with a one-click **CSV Data Export** button.

---

## 🚀 Quickstart: Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/AnuragSingh2101/OlistIQ.git
cd OlistIQ
```

### 2. Set up virtual environment and install packages
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Launch the Streamlit Dashboard
```powershell
streamlit run app.py
```
The application will launch in your browser at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud (Free Live Demo)

To share a live public link with recruiters and collaborators:
1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: complete analytics platform"
   git push origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **"New app"**, select `AnuragSingh2101/OlistIQ`, set the main file path to `app.py`, and click **Deploy**.
4. Streamlit will generate a public URL (e.g., `https://olistiq.streamlit.app`) that anyone can open in their browser without installing anything.

---

## 📊 Analytical SQL Suite

The [`sql/`](sql/) directory contains production-ready analytical SQL scripts:
- **`01_monthly_revenue_and_growth.sql`**: Uses SQL window functions (`LAG()`) to compute Month-over-Month revenue expansion rates.
- **`02_delivery_sla_by_state.sql`**: Identifies carrier SLA breach rates and calculates average delivery days grouped by destination state.
- **`03_rfm_customer_segmentation.sql`**: Employs `NTILE(4)` quantile window functions across Recency, Frequency, and Monetary dimensions to segment customers into *Champions*, *Loyal*, *At-Risk*, and *Lost*.

---

## 📄 License
This project is licensed under the MIT License — feel free to use and adapt it for your own portfolios and analyses.
