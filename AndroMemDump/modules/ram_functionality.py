

from utils.config import * # File .py that contains all necessary libraries and global parameters chosen by the user

from graphics.logo import show_logo  # Imports the function to show the logo
from graphics.graphic_setup import * # Import the function to change terminal graphics

from ram.info import show_info
from ram.dump_memory import dump_all_memory
from ram.dump_process import dump_single_process

def ram_functionalities():
    
    while True:
        
        os.system("clear")

        show_logo()
        
        print("\n")

        # Show all possible options of functionality
        print("\033[1;33m1. Dump entire RAM")  
        print("\033[1;33m2. Dump single process")  
        print("\033[1;33m3. Info functionalities")      
        print("\033[1;31m4. Exit")
        print("\n")

        # Make a choice
        choice = input("\033[1;37mSelect an option (1-4): \033[0m")

        # Handle the possible choice
        if choice == "1":
            print("\nYou have selected: Dump entire RAM")
            time.sleep(1)
            dump_all_memory()
            
        elif choice == "2":
            print("\nYou have selected: Dump single process")
            time.sleep(1)
            dump_single_process()
            
        elif choice == "3":
            print("\nYou have selected: Info functionalities")
            time.sleep(1)
            show_info() # Shows information on functionality
            
        elif choice == "4":
            print("\nExit...")
            break  # Exit from the program
        
        else:
            print("\n\033[1;31mInvalid choice. Please select a number between 1 and 4.\033[0m")
            time.sleep(1)