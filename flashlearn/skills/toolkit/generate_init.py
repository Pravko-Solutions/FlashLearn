import os
import json


def add_json_to_init(folder_path):
    init_file_path = os.path.join(folder_path, "__init__.py")

    with open(init_file_path, 'w', encoding='utf-8') as init_file:
        init_file.write("# Auto-generated Python dictionaries from JSON files\n\n")

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                json_path = os.path.join(folder_path, filename)
                try:
                    # Load JSON data
                    with open(json_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)

                    # Convert JSON file name to valid Python variable name
                    variable_name = filename.replace(".json", "").replace("-", "_")

                    # Write Python-friendly dictionary
                    init_file.write(f"{variable_name} = {repr(data)}\n\n")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Error processing {filename}: {e}")


# Run the function in the current directory
add_json_to_init(os.getcwd())
