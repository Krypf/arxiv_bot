#%%
from datetime import datetime
from printlog import printlog
from arxiv_function import ArxivSearch, ArxivText, ArxivSoup, categories_content, read_inner_file

#%%
def confirm_initialize(obj: ArxivText):
    # Print current date and time to stdout
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current date and time: {current_date}")
    print(f"The date you select is {obj.date}")
    print(f"The category you select is {obj.category}")

    # Ask for user confirmation with y/n input
    while True:
        user_input = input("Do you want to continue? (y/n): ").strip().lower()
        if user_input in ['y', 'n']:
            if user_input == 'y':
                print("You chose yes.")
            else:
                print("You chose no.")
            break
        else:
            print("Please enter 'y' or 'n'.")

    # Create an empty file
    open(obj.file_path, 'w').close()
    # Open the file in write mode
    with open(obj.file_path, 'w') as file:
        # You can write to the file here if needed
        file.write("")
        printlog(f"File {obj.file_name} has been initialized.")
        # security: do not use the absolute file_path

    return None

def sub(obj: ArxivText):
    confirm_initialize(obj)
    
    search = ArxivSearch(obj.category, submissions = 'recent')
    soup = ArxivSoup(search.read_HTML())
    
    item_numbers = search.extract_skip_numbers(obj.date, _printlog=False)
    for i in range(*item_numbers):
        item_number = str(i)
        text = soup.get_one_post(item_number)
        # print(i, text)
        obj.append_to_path(text)# save_text_append
        
    # Display the result
    printlog(f"{obj.file_name} has been saved.")
    return 0

def main():
    dates = read_inner_file(file='date', folder='arxiv_bot')
    date = dates[-1]
    for category in categories_content:
        obj = ArxivText(category, date)
        sub(obj)
    return 0

if __name__ == '__main__':
    # today = datetime.now().strftime('%Y-%m-%d')
    main()
    
