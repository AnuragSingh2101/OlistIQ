# OlistIQ Dashboard Gallery & Deployment Guide

This directory houses the visual assets and deployment guides for the **OlistIQ Interactive Dashboard**.

---

## 📸 Visual Previews

### 1. Executive Performance View
- **KPI Metrics**: Gross Merchandise Value (GMV), Total Orders, Average Order Value (AOV), Satisfaction Rating, and On-Time SLA.
- **Monthly Trajectory**: Dual-axis bar and line chart visualizing gross monthly revenue alongside volume growth.

### 2. Category Intelligence
- **Top Categories**: Horizontal ranking of top 12 revenue-generating sectors translated into English.
- **Demand Concentration**: Category volume comparisons.

### 3. Logistics & Regional Bottlenecks
- **Transit Duration**: State-by-state delivery duration analysis highlighting delivery disparities between the Southeast (SP, RJ, PR) and the North (RR, AP, AM).
- **SLA Breach Monitoring**: Real-time identification of regions suffering from elevated delay rates.
- **Freight Cost Burden**: Freight-to-price ratio choropleth mapping logistics cost intensity across all 27 Brazilian states.

---

## 📁 Screenshot Assets

Place your dashboard screenshots in `dashboard/dashboard_screenshots/` with these recommended filenames:

| Filename | Description |
|----------|-------------|
| `01_executive_kpis.png` | Top KPI scorecards (GMV, AOV, Review, On-Time %, Transit) |
| `02_revenue_trajectory.png` | Monthly revenue + order volume dual-axis chart with MoM growth |
| `03_category_revenue.png` | Top 12 categories by revenue (horizontal bar) |
| `04_category_volume.png` | Top 12 categories by order volume |
| `05_logistics_transit_map.png` | Choropleth: Average delivery days by state |
| `06_logistics_delay_map.png` | Choropleth: SLA breach rate by state |
| `07_logistics_freight_map.png` | Choropleth: Freight-to-price ratio by state |
| `08_logistics_rankings.png` | Bar rankings: Slowest states & highest delay rates |
| `09_payment_breakdown.png` | Payment method revenue share (donut) + AOV by method |
| `10_data_explorer.png` | Filtered data table with export button |

> **Tip**: Use `Win+Shift+S` (Windows) or `Cmd+Shift+4` (Mac) to capture screenshots. Recommended resolution: 1920x1080 or higher.

---

## 🚀 How to Launch the Dashboard

```bash
# 1. Activate your virtual environment
.\venv\Scripts\Activate.ps1

# 2. Launch the Streamlit application
streamlit run app.py
```

The application will automatically open at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud (Free Public URL)

1. Push your repository to GitHub: `git push origin main`.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Select this repository: `AnuragSingh2101/OlistIQ`.
4. Set **Main file path** to `app.py`.
5. Click **Deploy** to generate a live link for your portfolio or resume.

---

## 📋 Deployment Checklist

- [ ] `requirements.txt` includes all dependencies (streamlit, pandas, plotly, requests)
- [ ] `data/clean/orders_master.csv` exists (pre-generated, ~33 MB)
- [ ] `app.py` runs locally without errors: `streamlit run app.py`
- [ ] Screenshots added to `dashboard/dashboard_screenshots/`
- [ ] Repository pushed to GitHub with clean history
- [ ] Streamlit Cloud deployment successful

---

## 🔗 Quick Links

- **Live Demo** (after deploy): `https://olistiq.streamlit.app` (example)
- **GitHub Repo**: `https://github.com/AnuragSingh2101/OlistIQ`
- **Raw Dataset**: [Kaggle - Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)