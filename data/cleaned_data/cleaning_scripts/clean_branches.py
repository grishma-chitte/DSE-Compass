import pandas as pd
import sys
from pathlib import Path

CITY = sys.argv[1] if len(sys.argv) > 1 else "nashik"

INPUT_FILE = f"data/raw_data/{CITY}_raw_data.xlsx"
OUTPUT_FILE = f"data/cleaned_data/{CITY}_cleaned_data.xlsx"

# =========================
# Read Sheet
# =========================

df = pd.read_excel(
    INPUT_FILE,
    sheet_name="branches"
)

# Remove accidental Excel columns like "Unnamed: 6"
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Remove completely empty rows
df = df.dropna(how="all")

# =========================
# Clean Text Columns
# =========================

text_columns = [
    "college_abbrv",
    "branch_name",
    "branch_abbrv"
]

for col in text_columns:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
        )

if "college_abbrv" in df.columns:
    df["college_abbrv"] = df["college_abbrv"].str.upper()

if "branch_abbrv" in df.columns:
    df["branch_abbrv"] = df["branch_abbrv"].str.upper()

# =========================
# Numeric Columns
# =========================

numeric_columns = [
    "branch_id",
    "dte_code",
    "regular_intake",
    "estimated_dse_intake",
    "dse_intake_2025"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# =========================
# Duplicate Check
# =========================

# We check for duplicates using (college_abbrv, branch_name) 
# as it's more reliable when dte_code is missing
duplicates = df[
    df.duplicated(
        subset=["college_abbrv", "branch_name"],
        keep=False
    )
]

if not duplicates.empty:
    print("\nWARNING: Duplicate branches found (by abbreviation):\n")
    print(duplicates)

# =========================
# Optional sanity check
# =========================

invalid = df[
    df["estimated_dse_intake"] > df["regular_intake"]
]

if not invalid.empty:
    print("\nWARNING: Estimated DSE intake exceeds regular intake:\n")
    print(invalid)

# =========================
# Save Sheet
# =========================

file_exists = Path(OUTPUT_FILE).exists()

writer_args = {
    "engine": "openpyxl",
    "mode": "a" if file_exists else "w"
}

if file_exists:
    writer_args["if_sheet_exists"] = "replace"

with pd.ExcelWriter(
    OUTPUT_FILE,
    **writer_args
) as writer:
    df.to_excel(
        writer,
        sheet_name="branches",
        index=False
    )

print("branches cleaned successfully")