import os
import sys
import subprocess

# API KEY
os.environ["OPENAI_API_KEY"] = "Your api KEY"

# Define the relative path to the examples folder
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../examples"))

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".py"):
        file_path = os.path.join(folder_path, filename)
        print(f"Running {filename}...")

        try:
            # Use sys.executable to ensure we run under the same virtual environment
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            print(f"{filename} executed successfully!\nOutput:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error while executing {filename}:\n{e.stderr}")