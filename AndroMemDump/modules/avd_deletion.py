

from utils.config import * # File .py that contains all necessary libraries and global parameters chosen by the user
from utils.avd_manage import show_avd, avd_exists # Function to show all available AVD devices with their features

    
# Function to delete an AVD device by name
def delete_avd():
    
    """ Infinite loop that has the task of asking the user for the name of the device to be deleted. 
    The user has the option of terminating the loop via ‘exit’. """
    while True:
        
        show_avd() # Show all available AVD devices
        
        # Requests the user to enter the name for the AVD that want delete
        avd_name = input("\n\nEnter the name for the AVD you want to delete (or type 'exit' to quit): ")

        # Check if the user wants to exit
        if avd_name.lower() == "exit":
            print("Ending the procedure...")
            break  # Exits the internal loop and returns to the main menu
        
        # Check if the AVD exists
        if avd_exists(avd_name): 
            try:
                # Command to delete the AVD
                command = [
                    "./avdmanager",
                    "delete",
                    "avd",
                    "-n", avd_name
                ]
                
                # If all went well, the value 0 is returned
                result = subprocess.run(command, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"\nAVD '{avd_name}' deleted successfully!")
                    time.sleep(3)
                    os.system("clear")
                    continue
                else:
                    print(f"\nError deleting AVD '{avd_name}': {result.stderr}")
                    time.sleep(3)
                    os.system("clear")
                    break # Exit from the program
                
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
                break # Exit from the program
        else:
            print(Fore.RED + f"AVD '{avd_name}' not found. Please check the name or try again." + Style.RESET_ALL)
            time.sleep(3)
            os.system("clear")
            continue # Repeat the procedure 
        