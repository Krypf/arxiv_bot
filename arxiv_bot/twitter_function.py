import os

def load_credentials(category):
    """
    Reads and returns the text from keys in the directory.
    Args:
        category: The name of the file to read from.
    Returns:
        The dictionaries of the file as a string.
    """
    # Get the path to the home directory
    home_directory = os.path.expanduser("~")
    # Construct the full file path
    folder = 'twitter-keys'
    directory_path = os.path.join(home_directory, folder)
    file_path = os.path.join(directory_path, category)

    credentials = {}
    # Read the content of the file
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line by the first occurrence of ':'
                key, value = line.strip().split(': ', 1)
                credentials[key] = value
        return credentials
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':
    # Specify the file you want to read from
    category = credentials_file = "gr-qc"

    # Load the credentials into a dictionary
    credentials_dict = load_credentials(credentials_file)

    # Print the dictionary
    if credentials_dict:
        print(credentials_dict)
        print(credentials_dict['API Key'])

