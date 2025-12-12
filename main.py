from pathlib import Path
from database import init_db, load_all_ssa_files, DB_PATH

BASE_DIR = Path(__file__).resolve().parent

def main():
    print("Initializing database...")
    init_db()
    print(f"Database created/verified at: {DB_PATH}")

    data_folder = BASE_DIR / "ssa_data" 

    if data_folder.exists():
        print(f"Loading SSA files from: {data_folder}")
        load_all_ssa_files(data_folder)
        print("Finished loading SSA data.")
    else:
        print(f"No SSA folder found at {data_folder}. Skipping data load.")

if __name__ == "__main__":
    main()