

from utils.config import *

def show_info():
    
    os.system("clear")
    
    project_dir = os.path.dirname(os.path.dirname(__file__))
    info_path = os.path.join(project_dir, "info.txt")
    
    with open(info_path, "r", encoding="utf-8") as file:
        text = file.read()
        print(text)    
    
    while True:
                    
        text = input(Fore.RED + "\n\nType 'exit' to quit: " + Style.RESET_ALL)
        
        # Check if the user wants to exit
        if text.lower() == "exit":
            print("Exit...")
            time.sleep(1)
            os.system("clear")
            break  # Exits the internal loop and returns to the main menu
            
    return