from pathlib import Path
import subprocess
import sys

CITY = sys.argv[1].lower() if len(sys.argv) > 1 else "nashik"
YEARS = sys.argv[2:] if len(sys.argv) > 2 else ["all"]

SCRIPT_DIR = Path(__file__).parent

single_city_scripts = [
    "clean_college_details.py",
    "clean_branches.py",
    "clean_placement_stats.py"
]

print("=" * 50)
print(f"Starting data cleaning for city: {CITY}")
print(f"Cutoff years target: {YEARS}")
print("=" * 50)

success = True

# 1. Run standard cleaning scripts
for script in single_city_scripts:
    print(f"\nRunning {script} for {CITY}...\n")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_DIR / script),
            CITY
        ]
    )

    if result.returncode != 0:
        print(f"\nERROR while executing {script}")
        success = False
        break

# 2. Run clean_cutoffs.py with years
if success:
    print(f"\nRunning clean_cutoffs.py for {CITY} ({YEARS})...\n")
    cutoff_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "clean_cutoffs.py"),
        CITY
    ] + YEARS

    result = subprocess.run(cutoff_cmd)
    if result.returncode != 0:
        print(f"\nERROR while executing clean_cutoffs.py")
        success = False

print("\n" + "=" * 50)

if success:
    print(f"All cleaning scripts executed successfully for {CITY}.")
else:
    print(f"Cleaning process terminated due to an error.")

print("=" * 50)