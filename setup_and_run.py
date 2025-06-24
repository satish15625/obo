import os
import subprocess
import sys
import venv
import csv

VENV_DIR = "venv"
CSV_FILE = "input.csv"
REQUIREMENTS_FILE = "requirements.txt"


def create_virtualenv():
    if not os.path.isdir(VENV_DIR):
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("Virtual environment already exists.")


def install_requirements():
    if os.path.exists(REQUIREMENTS_FILE):
        print("Installing dependencies...")
        subprocess.check_call([os.path.join(VENV_DIR, "Scripts", "pip"), "install", "-r", REQUIREMENTS_FILE])
    else:
        print("No requirements.txt found. Skipping installation.")


def read_csv():
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"{CSV_FILE} not found.")
    
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            return row["file"], row["start_date"], row["end_date"]
    raise ValueError("CSV file is empty or not formatted correctly.")


def run_script_in_env(script, start_date, end_date):
    python_executable = os.path.join(VENV_DIR, "Scripts", "python.exe")
    command = [python_executable, script, start_date, end_date]
    print(f"Running: {' '.join(command)}")
    subprocess.run(command)


def main():
    create_virtualenv()
    install_requirements()
    script, start_date, end_date = read_csv()
    run_script_in_env(script, start_date, end_date)


if __name__ == "__main__":
    main()
