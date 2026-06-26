import pandas as pd
from pathlib import Path

CITY = "nashik"

INPUT_FILE = f"data/raw_data/{CITY}_raw_data.xlsx"
OUTPUT_FILE = f"data/cleaned_data/{CITY}_cleaned_data.xlsx"

# =========================
# Read Sheet
# =========================

df = pd.read_excel(
    INPUT_FILE,
    sheet_name="branches"
)

df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

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

# Standardize abbreviations

if "college_abbrv" in df.columns:
    df["college_abbrv"] = df["college_abbrv"].str.upper()

if "branch_abbrv" in df.columns:
    df["branch_abbrv"] = df["branch_abbrv"].str.upper()

# =========================
# Numeric Columns
# =========================

numeric_columns = [
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
# Remove Completely Empty Rows
# =========================

df = df.dropna(how="all")

# =========================
# Duplicate Check
# =========================

duplicates = df[
    df.duplicated(
        subset=["dte_code", "branch_name"],
        keep=False
    )
]

if not duplicates.empty:
    print("\nWARNING: Duplicate branches found:\n")
    print(duplicates)

# =========================
# Validation Checks
# =========================

if {
    "regular_intake",
    "estimated_dse_intake"
}.issubset(df.columns):

    invalid = df[
        df["estimated_dse_intake"] > df["regular_intake"]
    ]

    if not invalid.empty:
        print("\nWARNING: Estimated DSE intake exceeds regular intake:\n")
        print(invalid)

if {
    "estimated_dse_intake",
    "dse_intake_2025"
}.issubset(df.columns):

    invalid = df[
        df["dse_intake_2025"] > df["estimated_dse_intake"]
    ]

    if not invalid.empty:
        print("\nWARNING: Actual DSE intake exceeds estimated DSE intake:\n")
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
