import pandas as pd

CITY = "nashik"

INPUT_FILE = f"data/raw_data/{CITY}_raw_data.xlsx"
OUTPUT_FILE = f"data/cleaned_data/{CITY}_cleaned_data.xlsx"

df = pd.read_excel(
    INPUT_FILE,
    sheet_name="college_details"
)

# Remove leading/trailing spaces from text fields
text_columns = [
    "college_name",
    "college_abbrv",
    "address",
    "city",
    "district",
    "college_type",
    "naac_grade",
    "website_url",
    "ugc_approved_section"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# Standardize yes/no fields
yes_no_columns = [
    "participates_in_cap",
    "autonomous",
    "aicte_approved",
    "ugc_recognized",
    "hostel_available",
    "transport_available"
]

for col in yes_no_columns:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

# Clean contact number
if "contact_no" in df.columns:
    df["contact_no"] = (
        df["contact_no"]
        .astype(str)
        .str.replace("-", "", regex=False)
        .str.strip()
    )

# Ensure fee is numeric
if "estimated_fees" in df.columns:
    df["estimated_fees"] = pd.to_numeric(
        df["estimated_fees"],
        errors="coerce"
    ).round(2)

# Remove duplicate colleges by DTE code
if "dte_code" in df.columns:
    df = df.drop_duplicates(
        subset=["dte_code"],
        keep="first"
    )

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:
    df.to_excel(
        writer,
        sheet_name="college_details",
        index=False
    )

print("Cleaning completed successfully.")