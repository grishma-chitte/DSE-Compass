import subprocess
import sys
from pathlib import Path

# =========================
# Project Paths
# =========================

if len(sys.argv) < 2:
    print("\nUSAGE: python load_all.py <city>")
    print("Example: python load_all.py nashik")
    sys.exit(1)

CITY = sys.argv[1].lower()
SCRIPT_DIR = Path(__file__).resolve().parent

scripts = [
    "load_college_details.py",
    "load_branches.py",
    "load_placement_stats.py"
]

print("=" * 50)
print(f"Starting database loading for: {CITY}")
print("=" * 50)

success = True

for script in scripts:
    print(f"\n>>> Running {script}...")
    
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / script), CITY]
    )
    
    if result.returncode != 0:
        print(f"\nERROR: {script} failed with return code {result.returncode}")
        success = False
        break

print("\n" + "=" * 50)
if success:
    print(f"Database loading for {CITY} completed successfully!")
else:
    print(f"Database loading for {CITY} failed.")
print("=" * 50)
