# 🏏 IPL Analytics: End-to-End Automated Data Pipeline & Power BI Dashboard

## 📌 Overview

This project is a **fully automated end-to-end data pipeline** that ingests, processes, and visualizes IPL (Indian Premier League) data from 2008–2024.

A single command executes the entire workflow:
**Download → Clean → Load → Validate → Visualize**

The final output is a **4-page interactive Power BI dashboard**, including a **dynamic player comparison tool** using advanced DAX techniques.

---

## 🚀 Key Highlights

* Fully automated pipeline (no manual CSV handling)
* Processes 200,000+ ball-by-ball records
* PostgreSQL-based data storage (production-style)
* Interactive Power BI dashboard with 4 analytical pages
* Advanced DAX (TREATAS, RANKX, disconnected tables)

---

## 🛠 Tech Stack

| Tool                  | Purpose                        |
| --------------------- | ------------------------------ |
| Python (Pandas)       | Data cleaning & transformation |
| Kaggle API            | Automated dataset download     |
| PostgreSQL            | Data storage & querying        |
| SQLAlchemy + psycopg2 | Database integration           |
| Power BI              | Data visualization             |
| DAX                   | Analytical calculations        |
| python-dotenv         | Secure credential management   |

---

## ⚙️ Architecture

Kaggle API → Python ETL Pipeline → PostgreSQL → Power BI Dashboard

---

## 📂 Project Structure

```
ipl-analytics/
│
├── main.py
├── requirements.txt
├── .env
│
├── pipeline/
│   ├── download.py
│   ├── clean.py
│   ├── load.py
│   └── validate.py
│
├── sql/
│   └── queries.sql
│
├── data/
│   └── raw/
│
└── pbix/
    └── IPL_Dashboard.pbix
```

---

## 🔄 Pipeline Workflow

### 1. Data Extraction

* Uses Kaggle API to download dataset programmatically
* Eliminates manual file handling

### 2. Data Transformation

* Standardizes columns
* Adds enrichment features:

  * Match phases (Powerplay, Middle, Death)
  * Boundary flags (4s, 6s)
  * Dot balls
  * Toss impact

### 3. Data Loading

* Auto-creates PostgreSQL database
* Loads data into structured tables
* Creates indexes for performance

### 4. Data Validation

* Row count checks
* Null value validation
* Season coverage verification
* Ensures data quality before visualization

---

## 📊 Power BI Dashboard

### Page 1: Tournament Overview

* Team win %
* Toss impact
* Venue performance

### Page 2: Batting Analysis

* Top run scorers
* Strike Rate vs Average scatter plot
* Phase-wise performance
* Sixes trend over time

### Page 3: Bowling Analysis

* Top wicket takers
* Economy vs wickets
* Death over specialists
* Dismissal breakdown

### Page 4: Player Comparison Tool ⭐

* Compare any 2 players dynamically
* Independent slicers using disconnected tables
* KPI comparison (Runs, SR, Avg, Wickets)
* Phase-wise and trend comparison

---

## 🧠 Key Techniques Used

### Data Engineering

* Automated ETL pipeline
* Modular Python scripts
* Environment variable handling

### SQL

* Window functions
* Conditional aggregation (FILTER)
* Query optimization using indexes

### Power BI / DAX

* Disconnected tables for player comparison
* TREATAS for dynamic filtering
* RANKX for Top-N analysis
* Conditional formatting

---

## 📈 Key Insights

* Toss impact is minimal (~51%) — strategy matters more
* Six hitting has increased significantly over seasons
* Death overs (16–20) are most impactful
* Elite batters = high average + high strike rate
* ~60% dismissals are catches

---

## ▶️ How to Run

### 1. Clone Repo

```
git clone https://github.com/yourusername/ipl-analytics.git
cd ipl-analytics
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Create `.env`

```
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key

DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ipl_db
```

### 4. Run Pipeline

```
python main.py
```

### 5. Open Power BI

* Connect to PostgreSQL (`ipl_db`)
* Load `matches` and `deliveries`

---

## 🎯 Interview Talking Point

“I built a fully automated IPL analytics pipeline where one command downloads data using Kaggle API, processes 200K+ records, loads into PostgreSQL, and validates data quality. The Power BI dashboard includes a dynamic player comparison tool using disconnected tables and advanced DAX.”

---

## 📸 Screenshots

(Add dashboard screenshots here)

---

## 👤 Author

**Manish Acharya**
Aspiring Data Analyst / Data Engineer

---

## ⭐ Support

If you found this useful, give it a ⭐ on GitHub!
