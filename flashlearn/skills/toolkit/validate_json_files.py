import os
import json


def validate_json_files():
    # Get the current working directory
    folder_path = os.getcwd()

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            try:
                # Load JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Check if 'function_definition' is a dictionary
                if not isinstance(data.get("function_definition"), dict):
                    print(f"Deleting {filename}: 'function_definition' is not a dictionary")
                    os.remove(file_path)
                else:
                    print(f"Validated {filename}: 'function_definition' is a dictionary")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error processing {filename}: {e}")
                # Optionally delete invalid JSON files
                os.remove(file_path)


# Run the validation function
validate_json_files()
