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

    sheet_name="placement_stats"
)

df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# =========================
# Clean College Abbreviation
# =========================

if "college_abbrv" in df.columns:
    df["college_abbrv"] = (
        df["college_abbrv"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

# =========================
# Clean DTE Code
# =========================

if "dte_code" in df.columns:
    df["dte_code"] = pd.to_numeric(
        df["dte_code"],
        errors="coerce"
    )

# =========================
# Clean Year
# =========================

if "year" in df.columns:
    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

# =========================
# Clean Placement Percentage
# =========================

if "placement_percent" in df.columns:
    df["placement_percent"] = pd.to_numeric(
        df["placement_percent"],
        errors="coerce"
    ).round(2)

# =========================
# Clean Average Package (LPA)
# =========================

if "avg_package" in df.columns:
    df["avg_package"] = pd.to_numeric(
        df["avg_package"],
        errors="coerce"
    ).round(2)

# =========================
# Remove Fully Empty Rows
# =========================

df = df.dropna(how="all")

# =========================
# Check Duplicates
# =========================

duplicates = df[
    df.duplicated(
        subset=["dte_code", "year"],
        keep=False
    )
]

if not duplicates.empty:
    print("\nWARNING: Duplicate placement records found\n")
    print(duplicates)

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
        sheet_name="placement_stats",
        index=False
    )

print("placement_stats cleaned successfully")