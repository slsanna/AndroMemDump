

from utils.config import * # File .py that contains all necessary libraries and global parameters chosen by the user

from graphics.logo import show_logo  # Import the function to show the logo
from graphics.graphic_setup import reset_terminal_background # Import function to restore default terminal interface graphics

from modules.avd_creation import create_avd # Import the functions to create an AVD
from modules.avd_deletion import delete_avd # Import the functions to delete AVD
from modules.apk_install import install_apk # Import the function to install an .apk file
from modules.ram_functionality import ram_functionalities

def show_functionalities():
    
    while True:
        
        os.system("clear")
        
        show_logo()
        
        print("\n")

        # Show all possible options of functionality
        print("\033[1;33m1. Create and configure an AVD")
        print("\033[1;33m2. Delete an AVD")  
        print("\033[1;33m3. Install application .apk")  
        print("\033[1;33m4. RAM functionalities")  
        print("\033[1;31m5. Exit")
        print("\n")

        # Make a choice
        choice = input("\033[1;37mSelect an option (1-5): \033[0m")

        # Handle the possible choice
        if choice == "1":
            print("\nYou have selected: Create and configure an AVD")
            time.sleep(1)
            create_avd() # Functions to create an AVD
            
        elif choice == "2":
            print("\nYou have selected: Delete an AVD")
            time.sleep(1)
            delete_avd() # Functions to delete AVD
            
        elif choice == "3":
            print("\nYou have selected: Install application .apk")
            time.sleep(1)
            install_apk() # Function to install an .apk file
            
        elif choice == "4":
            print("\nYou have selected: RAM functionalities")
            time.sleep(1)
            ram_functionalities() # Function to choose RAM functionalities
            
        elif choice == "5":
            print("\nExit...")
            #reset_terminal_background() # Function to restore default terminal interface graphics
            break  # Exit from the program
        else:
            print("\n\033[1;31mInvalid choice. Please select a number between 1 and 5.\033[0m")
            time.sleep(1)