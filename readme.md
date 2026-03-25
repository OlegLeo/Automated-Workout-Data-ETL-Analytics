# 📊 Workout Data ETL Pipeline & Analytics

This project is an automated analytics pipeline that collects, transforms, and prepares fitness data for analysis. It integrates:

- **Workout logs** from the Hevy app  
- **Automated scraping** using Selenium  
- **Data transformation** into clean, analysis‑ready tables  
- **A structured ETL workflow** for long‑term tracking and insights  

The goal is to maintain a reliable, automated system that keeps your fitness dataset up‑to‑date and ready for dashboards, analysis, and progress tracking.

---

## 🏗️ Architecture Overview

The project follows a lightweight but professional ETL structure:

### **1. Raw Layer**
- Direct exports from the Hevy app  
- Stored exactly as downloaded  
- No modifications  

### **2. Transform Layer**
- Cleans raw data  
- Selects relevant columns  
- Calculates derived metrics (e.g., training volume = weight × reps)  
- Produces clean, structured tables  

### **3. Analytics Layer**
- Final dataset used for:
  - Excel dashboards  
  - Power BI  
  - Pivot tables  
  - Trend analysis  

---


## 🔄 Data Flow

1. **Hevy App**
2. **Selenium Scraper**
3. **Raw CSV**
4. **Transform Script**
5. **Cleaned / Master Dataset**
6. **Excel / BI Dashboards & Insights**


---

## 🧰 Project Components

### **Automated Scraper**
Located in `hevy_scraper/`  
- Logs into Hevy  
- Downloads the latest workout export  
- Saves it into `data/raw/`  
- Renames the file with a timestamp  

### **Automated Ingest Google Sheets**
Located in `ingest/`  
- Ingests Google Sheets data 
- Downloads the latest daily nutrition (calories/protein) and body weight data
- Saves it into `data/raw/`   

### **Transform Pipeline**
Located in `transform/`  
- Cleans raw data  
- Normalizes column names  
- Computes metrics  
- Updates the master dataset  

### **Main Orchestrator**
`main.py`  
- Runs scraper  
- Renames raw file  
- Runs transform  
- Updates master dataset  

### **Utilities**
`utils/file_utils.py`  
- File handling  
- Timestamping  
- Directory management  

---

## 📂 Repository Structure

```
workout_analysis_project/
│
├── data/
│   ├── raw/                 # Raw Hevy exports
│   └── master/              # Cleaned + aggregated dataset
│
├── hevy_scraper/
│   ├── auth.py
│   ├── browser.py
│   ├── export.py
│   ├── main.py
│   └── __init__.py
│
├── transform/
│   ├── transform.py
│   └── __init__.py
│
├── ingest/
│   ├── google_sheets_ingest.py
│   └── __init__.py
│
├── utils/
│   └── file_utils.py
│
├── main.py                  # Orchestrates the full ETL pipeline
├── config.py                # Paths, settings, constants
├── Makefile                 # Convenience commands (run, scrape, transform)
├── .gitignore
└── README.md
```

--

##  🚀 How to Run

**Follow these steps to set up and run the project.**

1. Create a virtual environment
    `python3 -m venv workoutanalytics`

2. Activate the virtual environment
    `source workoutanalytics/bin/activate`

3. Install dependencies
    `pip3 install -r requirements.txt` OR `make install`

4. Run the hevy scrapper script from the root of the project
    `python3 -m hevy_scraper.main` OR `make scrape`

5. Run the transform script script from the root of the project
    `python3 -m transform.transform` OR `make transform data`

6. Run pipeline hevy scraper + transform
    `python3 -m ingest.google_sheets_ingest` OR `make ingest_data`

7. Run pipeline hevy scraper + transform
    `python3 -m main` OR `make run`

8. Clean local python cache
    `make clean`

--- 

## Data Analysis

- Trend of Body Weight:
    Analyse the direction of bodyweight over time. The idea is to group date weekly and in the line chart analyse the progress avarage over time.
- Maintenance calories =
the average calories you eat during weeks where your weight trend is flat.

- Calculate your surplus target (how much to eat to gain weight)

- Track weekly training volume

    “Do I gain weight faster when I eat more?”

    “Do I gain weight faster when volume is higher?”

    “Do I need more calories on high-volume weeks?”

- Consistency metrics 
    - Mark red the weeks when the goals was not achieved for workout days
    : +0.25 to +0.75 kg per week 
    “Am I gaining at the right speed?”
    
- Weekly weight change (main KPI)

## 🧭 Future Enhancements

- Add PR detection  
- Add weekly/monthly summaries  
- Add Power BI dashboard  
- Add predictive trend analysis  



