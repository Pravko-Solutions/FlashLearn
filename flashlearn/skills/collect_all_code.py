import os

def read_python_files_from_specific_folders(top_level_folder, target_folders):
    """
    Gathers all .py files from each of the specified folders (and subfolders),
    returning a single string with the path and source code.
    """
    code_collection = []

    # For each target folder, construct its full path, then walk only inside it.
    for folder_name in target_folders:
        folder_path = os.path.join(top_level_folder, folder_name)

        # Make sure the child folder actually exists before walking it.
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.py'):  # Only .py files
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_content = f.read()
                            # Get the path relative to top_level_folder for clarity
                            relative_path = os.path.relpath(file_path, top_level_folder)
                            # Append the file name and content
                            code_collection.append(f"File: {relative_path}\n{file_content}\n")
                        except (IOError, OSError) as e:
                            print(f"Could not read file {file_path}: {e}")
        else:
            print(f"Warning: Folder '{folder_name}' does not exist at '{folder_path}'.")

    # Combine all collected code into a single text
    return "\n".join(code_collection)


# Example usage
if __name__ == "__main__":
    top_level_folder = r'C:/Users/Gal/PycharmProjects/FlashLearn'
    target_folders = ['flashlearn/skills']
    code_as_string = read_python_files_from_specific_folders(top_level_folder, target_folders)
    print(code_as_string)