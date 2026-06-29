# DSE-Compass

A web application that helps DSE students compare engineering colleges and make informed admission decisions using cutoff trends, placement statistics, fees, and other college information.

## Database Setup & Data Loading

Follow these steps to set up the database and load information from Excel files.

### 1. Reset Database (Important)
If you have already created database before, it is requested to delete the existing database file before proceeding:
```bash
# Windows
del backend\dse_compass.db

# Linux/Mac
rm backend/dse_compass.db
```
or simply right-click and choose Delete

### 2. Clean Raw Data
Process the raw Excel files (ensure they are not opened in any program) into the cleaned data format:
```bash
python data/cleaned_data/cleaning_scripts/clean_all.py
```

### 3. Initialize Database Tables
Run the creation script to set up the SQLite tables based on the latest models:
```bash
python backend/db/create_db.py
```

### 4. Load Cleaned Data
Load the cleaned information into the database for a specific city (e.g. nashik):
```bash
python backend/db/db_loading_scripts/load_all.py nashik
```