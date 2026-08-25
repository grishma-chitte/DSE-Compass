import subprocess
import sys
from pathlib import Path

# =========================
# Project Paths & Arguments
# =========================

CITY = sys.argv[1].lower() if len(sys.argv) > 1 else "nashik"
YEARS = sys.argv[2:] if len(sys.argv) > 2 else ["all"]

SCRIPT_DIR = Path(__file__).resolve().parent

single_city_scripts = [
    "load_college_details.py",
    "load_branches.py",
    "load_placement_stats.py"
]

print("=" * 50)
print(f"Starting database loading for: {CITY}")
print(f"Cutoff years target: {YEARS}")
print("=" * 50)

success = True

# 1. Run standard city scripts
for script in single_city_scripts:
    print(f"\n>>> Running {script} for {CITY}...")

    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / script), CITY]
    )

    if result.returncode != 0:
        print(f"\nERROR: {script} failed with return code {result.returncode}")
        success = False
        break

# 2. Run load_cutoffs.py
if success:
    print(f"\n>>> Running load_cutoffs.py for {CITY} ({YEARS})...")
    cutoff_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "load_cutoffs.py"),
        CITY
    ] + YEARS

    result = subprocess.run(cutoff_cmd)
    if result.returncode != 0:
        print(f"\nERROR: load_cutoffs.py failed with return code {result.returncode}")
        success = False

print("\n" + "=" * 50)
if success:
    print(f"Database loading for {CITY} completed successfully!")
else:
    print(f"Database loading for {CITY} encountered errors.")
print("=" * 50)

