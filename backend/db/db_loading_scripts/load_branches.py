import sys
from pathlib import Path
import pandas as pd

# =========================
# Project Paths
# =========================

if len(sys.argv) < 2:
    print("\nUSAGE: python load_branches.py <city>")
    print("Example: python load_branches.py nashik")
    sys.exit(1)

CITY = sys.argv[1].lower()

DB_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = DB_DIR.parent.parent

sys.path.append(str(DB_DIR))

try:
    from database import SessionLocal
    from models import CollegeDetails, Branch
except ImportError:
    print("\nERROR: Could not import database or models. Ensure you are running from the correct directory.")
    sys.exit(1)

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "cleaned_data"
    / f"{CITY}_cleaned_data.xlsx"
)

if not INPUT_FILE.exists():
    print(f"\nERROR: Input file not found: {INPUT_FILE}")
    sys.exit(1)

# =========================
# Read Excel
# =========================

print(f"Reading {INPUT_FILE}...")
try:
    df = pd.read_excel(
        INPUT_FILE,
        sheet_name="branches"
    )
except ValueError:
    print(f"\nERROR: 'branches' sheet not found in {INPUT_FILE}")
    sys.exit(1)

# =========================
# Replace NaN with None
# =========================

df = df.where(pd.notnull(df), None)

# =========================
# Insert Data
# =========================

session = SessionLocal()

inserted = 0
skipped = 0
errors = 0

print(f"Loading branches into database...")

try:

    for _, row in df.iterrows():

        # 1. Look up the college
        college = None
        
        # Try by DTE code if available
        dte_code_val = int(row["dte_code"]) if pd.notnull(row["dte_code"]) else None
        
        if dte_code_val:
            college = session.query(CollegeDetails).filter(CollegeDetails.dte_code == dte_code_val).first()
        
        # Fallback to abbreviation
        if not college and row["college_abbrv"]:
             college = session.query(CollegeDetails).filter(
                 CollegeDetails.college_abbrv == row["college_abbrv"]
             ).first()
        
        if not college:
            print(f"  [SKIP] College not found for row: {row['college_abbrv']} (DTE: {row['dte_code']})")
            skipped += 1
            continue

        # 2. Check if branch already exists for this college
        branch_name = str(row["branch_name"]) if row["branch_name"] else None
        
        existing = (
            session.query(Branch)
            .filter(
                Branch.college_id == college.college_id,
                Branch.branch_name == branch_name
            )
            .first()
        )

        if existing:
            skipped += 1
            continue

        # 3. Create branch
        branch = Branch(
            college_id=college.college_id,
            branch_name=row["branch_name"],
            branch_abbrv=row["branch_abbrv"],
            regular_intake=row["regular_intake"],
            estimated_dse_intake=row["estimated_dse_intake"],
            dse_intake_2025=row["dse_intake_2025"]
        )

        session.add(branch)
        inserted += 1

    session.commit()

except Exception as e:
    session.rollback()
    print(f"\nFATAL ERROR: {e}")
    errors += 1

finally:
    session.close()

# =========================
# Summary
# =========================

print("\n========================================")
print(f"Branches Loading Completed ({CITY})")
print("========================================")
print(f"Inserted : {inserted}")
print(f"Skipped  : {skipped}")
print(f"Errors   : {errors}")
print("========================================")
