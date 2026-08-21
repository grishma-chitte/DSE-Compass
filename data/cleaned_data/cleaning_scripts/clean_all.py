from pathlib import Path
import subprocess
import sys

CITY = "nashik"

SCRIPT_DIR = Path(__file__).parent

scripts = [
    "clean_college_details.py",
    "clean_branches.py",
    "clean_placement_stats.py",
    # "clean_cutoffs.py",
]

print("=" * 50)
print("Starting data cleaning...")
print("=" * 50)

success = True

for script in scripts:
    print(f"\nRunning {script}...\n")

    result = subprocess.run(
        [
            sys.executable,
            SCRIPT_DIR / script,
            CITY
        ]
    )

    if result.returncode != 0:
        print(f"\nERROR while executing {script}")
        success = False
        break

print("\n" + "=" * 50)

if success:
    print("All cleaning scripts executed successfully.")
else:
    print("Cleaning process terminated due to an error.")

print("=" * 50)