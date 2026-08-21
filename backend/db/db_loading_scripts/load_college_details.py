import sys
from pathlib import Path

import pandas as pd

# =========================
# Project Paths
# =========================

if len(sys.argv) < 2:
    print("\nUSAGE: python load_college_details.py <city>")
    print("Example: python load_college_details.py nashik")
    sys.exit(1)

CITY = sys.argv[1].lower()

DB_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = DB_DIR.parent.parent

sys.path.append(str(DB_DIR))

try:
    from database import SessionLocal
    from models import CollegeDetails
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
df = pd.read_excel(
    INPUT_FILE,
    sheet_name="college_details"
)

# =========================
# Convert Yes/No columns
# =========================

boolean_columns = [
    "participates_in_cap",
    "autonomous",
    "aicte_approved",
    "ugc_recognized",
    "hostel_available",
    "transport_available"
]

for col in boolean_columns:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "yes": True,
                "no": False,
                "true": True,
                "false": False
            })
        )

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

print(f"Loading data into database...")

try:

    for _, row in df.iterrows():

        # Robust duplicate check: 
        # Check by (Name + City) AND (Abbreviation + City)
        existing = (
            session.query(CollegeDetails)
            .filter(
                (CollegeDetails.college_name == row["college_name"]) |
                (CollegeDetails.college_abbrv == row["college_abbrv"])
            )
            .filter(CollegeDetails.city == row["city"])
            .first()
        )

        if existing:
            # Update existing record's dte_code if it was missing
            if row["dte_code"] and not existing.dte_code:
                existing.dte_code = row["dte_code"]
                session.add(existing)
            skipped += 1
            continue

        college = CollegeDetails(
            dte_code=row["dte_code"],
            college_name=row["college_name"],
            college_abbrv=row["college_abbrv"],
            participates_in_cap=row["participates_in_cap"],
            address=row["address"],
            city=row["city"],
            district=row["district"],
            college_type=row["college_type"],
            autonomous=row["autonomous"],
            naac_grade=row["naac_grade"],
            aicte_approved=row["aicte_approved"],
            ugc_recognized=row["ugc_recognized"],
            ugc_approved_section=row["ugc_approved_section"],
            contact_no=row["contact_no"],
            hostel_available=row["hostel_available"],
            transport_available=row["transport_available"],
            estimated_fees=row["estimated_fees"],
            website_url=row["website_url"],
            establishment_year=row["establishment_year"]
        )

        session.add(college)
        inserted += 1

    session.commit()

except Exception as e:
    session.rollback()
    print(f"\nERROR: {e}")

finally:
    session.close()

# =========================
# Summary
# =========================

print("\n========================================")
print(f"College Details Loading Completed ({CITY})")
print("========================================")
print(f"Inserted : {inserted}")
print(f"Skipped  : {skipped}")
print("========================================")