# 📊 Workout Data ETL Pipeline & Analytics

This project is an automated analytics pipeline that collects, transforms, and prepares fitness data for analysis. It integrates:

- **Workout logs** from the Hevy app  
- **Automated scraping** using Selenium  
- **Data transformation** into clean, analysis‑ready tables  
- **A structured ETL workflow** for long‑term tracking and insights  
- **AI Agent** (Local Ollama Server running AI Model mixtral:8x7b) as part of automated pipeline that  groups exercises by exercise name (like upper or lower body exercises).
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

## 📂 Repository Structure

```
workout_analysis_project/
│
├── data/
│   ├── raw/
│   │   ├── hevy/                 # Raw Hevy exports
│   │   ├── google_sheets/        # Raw Weight + Nutrition
│   │   └── README.md
│   │
│   └── master/
│       ├── hevy/                 # Cleaned Hevy dataset
│       ├── google_sheets/        # Cleaned Weight + Nutrition
│       └── README.md
│
├── hevy_scraper/
│   ├── auth.py
│   ├── browser.py
│   ├── export.py
│   ├── main.py                   # Scraper entrypoint
│   └── __init__.py
│
├── transform/
│   ├── common.py                 # Shared ETL utilities
│   ├── transform_hevy.py
│   ├── transform_weight.py
│   ├── transform_nutrition.py
│   └── __init__.py
│
├── ingest/
│   ├── google_sheets_ingest.py
│   └── __init__.py
│
├── analysis/
│   ├── ai/
│   │   ├── data_loader.py        # Loads master datasets for analysis
│   │   ├── exercise_classifier.py# AI model for exercise → muscle group classification
│   │   ├── ai_agent.py           # Orchestrates classification + updates exercise groups
│   │   ├── prompt.py             # LLM prompt templates
│   │   └── __init__.py
│   │
│   ├── exercise_groups.py        # Loads/validates grouped_exercises.json
│   ├── weekly_volume.py          # Weekly volume computation logic
│   ├── weekly_vol_summary.py     # CLI entrypoint for weekly volume summary
│   └── __init__.py
│
├── utils/
│   ├── file_utils.py
│   └── __init__.py
│
├── main.py                       # Full pipeline orchestrator
├── config.py                     # Paths, settings, constants
├── Makefile                      # Commands (scrape, transform, ingest, pipeline)
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
    `python3 -m transform.transform_{data_source_name}` OR `make transform_data`

6. Run pipeline hevy scraper + transform
    `python3 -m ingest.google_sheets_ingest` OR `make ingest_data`

7. Run AI Agent to get the weekly volume by upper/lower body split (LOCAL OLLAMA SETUP NEEDED BEFORE RUNNING: check config.py file for setup and usage details)
    `python3 -m analysis.weekly_vol_summary.py` OR `make ai_weekly`

8. Run pipeline hevy scraper + transform
    `python3 -m main` OR `make run`

9. Clean local python cache
    `make clean`

--- 

## Data Analysis

- Weekly Nutrition tracking
- Weekly Bodyweight tracking
- Weekly Wourkout Volume tracking (Total/Upper/Lower Volume)
- Prediction of desired weight gain overtime
- Weekly KPI Correlation Analysis (Nutrition + Bodyweight + Workout Volume)





