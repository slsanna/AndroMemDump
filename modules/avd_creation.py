

from utils.config import *  # File .py that contains all necessary libraries and global parameters chosen by the user
from utils.avd_manage import *
from utils.requirements import download_android # Import the function download_android

# Function to create the AVD
def create_avd():
    
    # Download Android version requested 
    download_android()
    
    while True:
        # Requests the user to enter the name for the new AVD
        avd_name = input("\n\nEnter a name for the new AVD. IT MUST BE WITHOUT SPACES (or type 'exit' to quit): ")
        
        # Check if the user wants to exit
        if avd_name.lower() == "exit":
            print("Exiting the procedure...")
            break  # Exits the internal loop and returns to the main menu
        
        # Check if the name contains only spaces
        if avd_name.strip() == "":
            print(Fore.RED + "Name cannot be empty or contain only spaces. Please enter a valid name." + Style.RESET_ALL)
            continue  # Skip the rest and ask for the name again
        
        # Check if the name contains spaces
        if " " in avd_name:
            print(Fore.RED + "Name cannot contain spaces. Please enter a valid name." + Style.RESET_ALL)
            continue  # Skip the rest and ask for the name again
        
        # Check if the AVD name already exists
        if avd_exists(avd_name):
            print(Fore.RED + f"Name '{avd_name}' already used! Please choose another name." + Style.RESET_ALL)
            continue  # Skip the rest and ask for the name again
        else:
            print(f"\nCreating an AVD named {avd_name}...")
            
            command = [
                "./avdmanager", 
                "create", 
                "avd", 
                "-n", avd_name, 
                "-k", f"system-images;android-{API};google_apis;{ARCH}", 
                "--device", "pixel_5", "--force"
            ]
            
            try:
                # Run the command to create the AVD
                subprocess.run(command,check=True)                
                print("\n\nAVD created successfully [✓]")
                print("\nThe device created has the following characteristics:", f"* Name: {avd_name} ", f" * Android OS API: {API}", f" * Architecture: {ARCH}")
                time.sleep(5)
                os.system("clear") # Clean the terminal window
                break  # Exits the internal loop and returns to the main menu
            
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error creating AVD: {e}" + Style.RESET_ALL)
                os.system("clear") # Clean the terminal window
                break  # Exits the internal loop and returns to the main menu
            




