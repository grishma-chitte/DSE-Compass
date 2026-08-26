# DSE-Compass

A web application that helps Direct Second Year Engineering (DSE) students compare engineering colleges and make informed admission decisions using cutoff trends, placement statistics, fees, and other college information.

---

## Setup & Installation

### 1. Environment Setup
Install the required dependencies:
```bash
pip install -r requirements.txt
```

---

## Database Setup & Data Pipeline

Follow these steps to clean raw Excel data and populate the database.

> **Note:** Ensure raw Excel files are closed in other programs (e.g. Microsoft Excel) before running cleaning scripts.

### Reset Database (Important)
If you have already created database before, it is requested to delete the existing database file before proceeding:
---

### Step 1: Reset Database (When Schema or Models Change)
If you already have an existing database or modified models, delete the old database file:
```bash
# Windows (PowerShell / Command Prompt)
del backend\dse_compass.db

# Linux / macOS
rm backend/dse_compass.db
```

or simply right-click and choose Delete

---

### Step 2: Initialize Database Tables
Create the database tables using the latest SQLAlchemy models:
```bash
# Run from project root or backend/db directory
python backend/db/create_db.py
```

---

### Step 3: Clean Raw Excel Data

Raw Excel files reside in `data/raw_data/<city>_raw_data.xlsx`. The cleaning scripts validate, clean, and output to `data/cleaned_data/<city>_cleaned_data.xlsx`.

#### Option A: Clean All Data (Recommended)
Cleans colleges, branches, placement stats, and cutoff sheets:
```bash
# Clean all sheets and all cutoff years for Nashik
python data/cleaned_data/cleaning_scripts/clean_all.py nashik all

# Clean specific cutoff year(s) alongside other sheets
python data/cleaned_data/cleaning_scripts/clean_all.py nashik 2025
python data/cleaned_data/cleaning_scripts/clean_all.py nashik 2025,2024
```

#### Option B: Run Cleaning Scripts Individually
```bash
# College Details
python data/cleaned_data/cleaning_scripts/clean_college_details.py nashik

# Branches
python data/cleaned_data/cleaning_scripts/clean_branches.py nashik

# Placement Stats (includes highest_package and avg_package)
python data/cleaned_data/cleaning_scripts/clean_placement_stats.py nashik

# Cutoffs (parses columns A-H, filters placeholder rows)
python data/cleaned_data/cleaning_scripts/clean_cutoffs.py nashik 2025
python data/cleaned_data/cleaning_scripts/clean_cutoffs.py nashik 2025,2024
python data/cleaned_data/cleaning_scripts/clean_cutoffs.py nashik all
```

---

### Step 4: Load Cleaned Data into Database

Loads the cleaned data from `data/cleaned_data/<city>_cleaned_data.xlsx` into the SQLite database `dse_compass.db`.

#### Option A: Load All Data (Recommended)
```bash
# Load all datasets including all cutoff years for Nashik
python backend/db/db_loading_scripts/load_all.py nashik all

# Load all datasets with specific cutoff year(s)
python backend/db/db_loading_scripts/load_all.py nashik 2025
python backend/db/db_loading_scripts/load_all.py nashik 2025,2024
```

#### Option B: Run Loading Scripts Individually
```bash
# College Details
python backend/db/db_loading_scripts/load_college_details.py nashik

# Branches
python backend/db/db_loading_scripts/load_branches.py nashik

# Placement Stats
python backend/db/db_loading_scripts/load_placement_stats.py nashik

# Cutoffs
python backend/db/db_loading_scripts/load_cutoffs.py nashik 2025
python backend/db/db_loading_scripts/load_cutoffs.py nashik 2025,2024
python backend/db/db_loading_scripts/load_cutoffs.py nashik all
```

---

## Running the Backend Server

Start the Flask backend server:
```bash
python backend/app.py
```