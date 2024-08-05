#%%
import os

def read_text_file(category, date, parent_folder=str()):
    # Define the path to the file
    file_name = category + '-' + date + '.txt'
    file_path = os.path.join(parent_folder, category, file_name)
    print(file_path)
    # Check if the file exists
    if not os.path.exists(file_path):
        return f"File {file_name} does not exist in the specified directory."

    # Open and read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content

# Example usage
category = 'gr-qc'
date = '2024-07-24'
text = read_text_file(category, date)
print(text)

# Split the text using "----" as the delimiter
text_array = text.strip().split("----")

print(text_array)