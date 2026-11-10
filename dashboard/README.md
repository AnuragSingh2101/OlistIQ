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

