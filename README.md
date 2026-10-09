# Royal Enfield Business Performance & ERP Analytics Dashboard 🏍️

An interactive, modular business intelligence dashboard and data science case study analyzing Royal Enfield's enterprise sales, dealership network, customer demographics, and after-sales service operations across India.

---

## 📌 Project Overview

**Royal Enfield** (Eicher Motors Limited) operates an extensive commercial footprint spanning over 200 dealerships and thousands of customer transactions across multiple motorcycle platforms (J-series 350cc, 452cc Liquid-Cooled Sherpa, and 650cc Parallel Twins).

This repository provides an end-to-end analytical framework and interactive web dashboard addressing core business challenges:
- **Sales & Volume Analytics**: Demand distribution across modern classic, cruiser, and adventure segments.
- **Geographic Penetration**: Regional and state-level revenue performance.
- **Dealership Performance**: Top-performing dealerships and channel distribution.
- **Customer Segmentation**: Revenue breakdown across key customer demographics.
- **After-Sales Operations**: Service workload demand across motorcycle models.

---

## 🚀 Key Features

- **Dynamic Cross-Filtering**: 6 interactive sidebar filters with cascading dependencies (Region &rarr; State &rarr; Dealer, Motorcycle Model, Category, and Transaction Month).
- **Executive KPI Cards**: Real-time computation of Total Revenue (₹ Cr), Units Sold, Average Selling Price (ASP), Active Dealers, Customer Footprint, and Average Discounts.
- **Interactive Visualizations (Plotly)**:
  - *Model Volume Bar Chart*: Unit sales distribution across motorcycle catalog.
  - *Monthly Sales Trend*: Time-series trendline capturing seasonal variations.
  - *Regional Revenue Analysis*: Revenue generated across North, South, East, West, and Central zones.
  - *Customer Segment Donut*: Revenue share by customer profile (e.g., Touring Enthusiasts, Commuters, Youth).
  - *Dealer Performance Leaderboard*: Top 10 dealerships ranked by revenue generation.
  - *Model × Region Heatmap*: Cross-tabulated density of motorcycle sales across geographic territories.
  - *After-Sales Service Demand*: Workload frequency by model in service centers.
- **Clean Modular Architecture**: Full decoupling of HTML templates, CSS stylesheets, data ingestion logic, and visualization components.

---

## 📁 Repository Structure

```
royal-enfield-analytics/
├── .streamlit/
│   └── config.toml               # Custom dashboard theme & server configuration
├── assets/
│   ├── header.html               # Modular HTML header component
│   ├── footer.html               # Modular HTML footer component
│   └── style.css                 # Custom CSS stylesheet for KPI cards & metrics
├── modules/
│   ├── __init__.py               # Python package marker
│   ├── utils.py                  # Static asset & template loaders (CSS, HTML)
│   ├── data_loader.py            # Cached data ingestion and relational joins
│   ├── filters.py                # Sidebar cross-filters & data slicing logic
│   ├── kpi_metrics.py            # Headline business KPI calculations & rendering
│   └── charts.py                 # Plotly visualization generation functions
├── notebooks/
│   ├── exploratory_data_analysis.ipynb # Case study business challenge solutions & EDA
│   ├── data_visualization.ipynb        # Data visualization and distribution charts
│   └── royal_enfield_case_study.ipynb  # Executive summary & dataset documentation
├── SQL_SCHEMA.sql                # Production DDL schema and relational views
├── app.py                        # Streamlit application entrypoint (~80 lines)
├── requirements.txt              # Python package dependencies
├── .gitignore                    # Environment & artifact exclusions
└── *.csv                         # ERP datasets (Sales, Dealers, Customers, etc.)
```

---

## 🛠️ Datasets

| File | Description |
| :--- | :--- |
| `Motorcycles.csv` | Master catalog of 15 motorcycle models (Engine CC, category, mileage, tank capacity, ex-showroom price). |
| `Dealers.csv` | 200 dealerships across India (Region, State, City, dealer format, rating, target). |
| `Customers.csv` | Customer demographic records (Age, income, occupation, customer segment). |
| `Sales.csv` | Vehicle transactions linking customer, dealer, bike, payment mode, discounts, and on-road price. |
| `Service.csv` | After-sales maintenance records (Parts cost, labor cost, total bill, service type, feedback score). |
| `Finance.csv` | Vehicle financing contracts, down payments, interest rates, tenure, and bank partners. |
| `Accessories.csv` | Genuine Motorcycle Accessories (GMA) transaction records. |
| `Inventory.csv` | Dealership stock on hand and reorder thresholds. |
| `TestRide.csv` | Test ride CRM pipeline and sales conversion tracking. |
| `WarrantyClaims.csv` | Warranty claims, failed component categories, and payout amounts. |
| `Employees.csv` | Dealership workforce profiles, targets, and experience. |

---

## ⚡ Quickstart & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/royal-enfield-analytics.git
cd royal-enfield-analytics
```

### 2. Set up a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```

The application will launch automatically in your default browser at `http://localhost:8501`.

---

## 📤 Pushing to GitHub

To publish this folder to your GitHub account:

```bash
cd royal-enfield-analytics
git init
git add .
git commit -m "Initial commit: Royal Enfield ERP Analytics Dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```
