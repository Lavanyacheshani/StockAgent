import os
import shutil

# Paths
OUTPUTS_DIR = os.path.join(os.getcwd(), 'outputs')
FRONTEND_DATA_DIR = os.path.join(os.getcwd(), 'frontend', 'public', 'data')

# Create frontend data dir if not exists
if not os.path.exists(FRONTEND_DATA_DIR):
    os.makedirs(FRONTEND_DATA_DIR)

# Files to copy
FILES_TO_COPY = [
    'investment_thesis.json',
    'thesis_json.json',
    'investment_report.md'
]

print(f"Syncing data from {OUTPUTS_DIR} to {FRONTEND_DATA_DIR}...")

for filename in FILES_TO_COPY:
    src = os.path.join(OUTPUTS_DIR, filename)
    dst = os.path.join(FRONTEND_DATA_DIR, filename)

    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"  [OK]  {filename} copied.")
    else:
        print(f"  [SKIP] {filename} not found.")

print("Sync complete.")
