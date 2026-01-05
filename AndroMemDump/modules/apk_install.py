

from utils.config import * # File .py that contains all necessary libraries and global parameters chosen by the user
from utils.avd_manage import *


# Checks if the specified APK file exists in the designated APK folder
def check_apk_exists(apk_name):
    """
    :param apk_name: Name of the APK file (without the .apk extension).
    :return: Full file path if the APK exists, otherwise False.
    """
    apk_files = [f for f in os.listdir(os.path.expanduser(APK_PATH)) if f.endswith('.apk')]  # List of existing APK files
    apk_name = apk_name + '.apk'
    
    if apk_name in apk_files:
        return os.path.join(os.path.expanduser(APK_PATH), apk_name)  # Returns the full path if the file exists
    else:
        return False  # Returns False if the file is not found


# Guides the user through the process of selecting an .apk, chose an AVD and installing the file through adb.
def install_apk():
    
    apk_name = input("\n\nEnter the name of the application you want to install (or type 'exit' to quit): ")
    chosen_apk_path = check_apk_exists(apk_name) 
    
    # Check if the user wants to exit
    if apk_name.lower() == "exit":
        print("\nExiting the procedure...")
        return  # Exits the function and returns to the main menu

    # Check if the AVD exists
    if chosen_apk_path:  
        
        show_avd()  # Display all available AVD devices
        avd_name = input("\n\nEnter the name of the AVD you want to start (or type 'exit' to quit): ")
        
        # Check if the user wants to exit
        if avd_name.lower() == "exit":
            print("\nExiting the procedure...")
            return  # Exits the function and returns to the main menu
        
        if avd_exists(avd_name):
            
            # Function to check if avd_name is running or not. If not it's started
            if check_avd_running() != 1:
                
                start_emulator(avd_name) # Procedure to start the AVD
                print("\nWaiting for the AVD to fully start: ") 
                # Add a delay to ensure the AVD has enough time to start
                progress_bar(165)  # You can increase this time if the AVD takes longer to start
            
            
            # Procedure to install .apk
            os.chdir(os.path.expanduser(SDK_PATH) + ("/platform-tools")) # ADB is in platform
            
            command = [
                "./adb",
                "install",
                chosen_apk_path
            ]
            
            try:
                print(f"\nInstalling APK from {chosen_apk_path}...")
                subprocess.run(command, check=True)
                time.sleep(2)
                print("\nExit..")
                time.sleep(5)
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error installing APK: {e}" + Style.RESET_ALL)
                
            os.system("clear")
            return # Back to the main menù    
        
        else:
            print(Fore.RED + f"\n\nError: The AVD with the name '{avd_name}' does not exist." + Style.RESET_ALL)
            time.sleep(3)
            os.system("clear")
            return # Back to the main menù
        
    else:
        print(Fore.RED + f"Error: The APK '{apk_name}.apk' does not exist in the 'apk_file' folder." + Style.RESET_ALL)
        time.sleep(3)
        os.system("clear") 
        return # Back to the main menù
         
