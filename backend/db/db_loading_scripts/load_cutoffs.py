import re
import sys
from pathlib import Path
import openpyxl
import pandas as pd

# =========================
# Project Paths & Imports
# =========================

CITY = sys.argv[1].lower() if len(sys.argv) > 1 else "nashik"

DB_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = DB_DIR.parent.parent

sys.path.append(str(DB_DIR))

try:
    from database import SessionLocal
    from models import Branch, CollegeDetails, Cutoff
except ImportError:
    print("\n[ERROR] Could not import database or models. Ensure you are running from the correct directory.")
    sys.exit(1)

INPUT_FILE = PROJECT_ROOT / "data" / "cleaned_data" / f"{CITY}_cleaned_data.xlsx"

if not INPUT_FILE.exists():
    print(f"\n[ERROR] Cleaned data file not found: {INPUT_FILE}")
    sys.exit(1)

# =========================
# Determine Target Sheets
# =========================

wb = openpyxl.load_workbook(INPUT_FILE, read_only=True)
all_sheet_names = wb.sheetnames
wb.close()

raw_years_input = sys.argv[2:] if len(sys.argv) > 2 else ["all"]

parsed_year_args = []
for arg in raw_years_input:
    for part in arg.split(","):
        cleaned_part = part.strip()
        if cleaned_part:
            parsed_year_args.append(cleaned_part)

is_all = any(arg.lower() == "all" for arg in parsed_year_args)

target_sheets = []

if is_all:
    for name in all_sheet_names:
        if re.match(r"^cutoffs?_\d{4}$", name, re.IGNORECASE):
            target_sheets.append(name)
    if not target_sheets:
        print(f"[WARNING] No sheets matching 'cutoffs_<year>' found in {INPUT_FILE.name}")
else:
    for y in parsed_year_args:
        sheet_candidate = f"cutoffs_{y}" if not y.startswith("cutoffs_") else y
        if sheet_candidate in all_sheet_names:
            target_sheets.append(sheet_candidate)
        else:
            matched = False
            for s in all_sheet_names:
                if s.lower() == sheet_candidate.lower() or s.lower() == f"cutoff_{y}".lower():
                    target_sheets.append(s)
                    matched = True
                    break
            if not matched:
                print(f"[INFO] Sheet '{sheet_candidate}' not found in {INPUT_FILE.name}. Skipping.")

if not target_sheets:
    print(f"\n[INFO] No cutoff sheets to load for {CITY}.")
    sys.exit(0)

# =========================
# Load Cutoffs Data
# =========================

session = SessionLocal()

total_inserted = 0
total_skipped = 0
total_errors = 0

print(f"\nLoading cutoffs into database for {CITY}: {target_sheets}...")

try:
    for sheet_name in target_sheets:
        print(f"\n>>> Loading sheet: {sheet_name}")

        try:
            df = pd.read_excel(INPUT_FILE, sheet_name=sheet_name)
        except Exception as e:
            print(f"  [ERROR] Failed to read sheet '{sheet_name}': {e}")
            total_errors += 1
            continue

        df = df.where(pd.notnull(df), None)

        sheet_inserted = 0
        sheet_skipped = 0

        for _, row in df.iterrows():
            # 1. Look up College
            college = None
            dte_code_val = None
            if row["dte_code"] is not None and pd.notnull(row["dte_code"]):
                try:
                    dte_code_val = int(float(row["dte_code"]))
                except (ValueError, TypeError):
                    dte_code_val = None

            if dte_code_val:
                college = session.query(CollegeDetails).filter(CollegeDetails.dte_code == dte_code_val).first()

            if not college and row["college_abbrv"] and pd.notnull(row["college_abbrv"]):
                abbrv_str = str(row["college_abbrv"]).strip().upper()
                college = session.query(CollegeDetails).filter(
                    CollegeDetails.college_abbrv == abbrv_str
                ).first()

            if not college:
                sheet_skipped += 1
                continue

            # 2. Look up Branch
            branch_abbrv_val = str(row["branch_abbrv"]).strip().upper() if row["branch_abbrv"] and pd.notnull(row["branch_abbrv"]) else ""
            if not branch_abbrv_val:
                sheet_skipped += 1
                continue

            branch = session.query(Branch).filter(
                Branch.college_id == college.college_id,
                Branch.branch_abbrv == branch_abbrv_val
            ).first()

            if not branch:
                # Fallback: check if branch_name equals abbreviation
                branch = session.query(Branch).filter(
                    Branch.college_id == college.college_id,
                    Branch.branch_name == branch_abbrv_val
                ).first()

            if not branch:
                print(f"  [SKIP] Branch '{branch_abbrv_val}' not found for college {college.college_abbrv}")
                sheet_skipped += 1
                continue

            # 3. Validate Year, Round, Category, Percentage
            try:
                year_val = int(float(row["year"])) if row["year"] is not None and pd.notnull(row["year"]) else None
            except (ValueError, TypeError):
                year_val = None

            try:
                round_val = int(float(row["round"])) if row["round"] is not None and pd.notnull(row["round"]) else None
            except (ValueError, TypeError):
                round_val = None

            try:
                pct_val = float(row["percentage"]) if row["percentage"] is not None and pd.notnull(row["percentage"]) else None
            except (ValueError, TypeError):
                pct_val = None

            cat_val = str(row["category"]).strip().upper() if row["category"] and pd.notnull(row["category"]) else None

            if year_val is None or round_val is None or not cat_val or pct_val is None:
                sheet_skipped += 1
                continue

            # 4. Check for existing record
            existing = session.query(Cutoff).filter(
                Cutoff.college_id == college.college_id,
                Cutoff.branch_id == branch.branch_id,
                Cutoff.year == year_val,
                Cutoff.round == round_val,
                Cutoff.category == cat_val
            ).first()

            if existing:
                sheet_skipped += 1
                continue

            # 5. Insert record
            cutoff_record = Cutoff(
                college_id=college.college_id,
                branch_id=branch.branch_id,
                year=year_val,
                round=round_val,
                category=cat_val,
                percentage=pct_val
            )

            session.add(cutoff_record)
            sheet_inserted += 1

        session.commit()
        print(f"  Inserted : {sheet_inserted}")
        print(f"  Skipped  : {sheet_skipped}")

        total_inserted += sheet_inserted
        total_skipped += sheet_skipped

except Exception as e:
    session.rollback()
    print(f"\n[FATAL ERROR] {e}")
    total_errors += 1

finally:
    session.close()

# =========================
# Summary
# =========================

print("\n========================================")
print(f"Cutoffs Loading Completed ({CITY})")
print("========================================")
print(f"Total Inserted : {total_inserted}")
print(f"Total Skipped  : {total_skipped}")
print(f"Total Errors   : {total_errors}")
print("========================================")
