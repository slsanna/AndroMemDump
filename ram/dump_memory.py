

from utils.config import * # File .py that contains all necessary libraries and global parameters chosen by the user
from graphics.logo import show_logo  # Import the function to show the logo
from utils.avd_manage import *
from utils.apk_manage import *

# Function to check the presence of 'lime.ko' file inside AVD
def check_file():
    
    os.chdir(os.path.expanduser(SDK_PATH) + ("/platform-tools"))

    command = "./adb shell ls /sdcard/lime.ko"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Return a flag
    if "No such file or directory" in result.stderr:
        flag = None
    else:
        flag = True
        
    return flag


# Function to execute a entire full dump of RAM
def dump_all_memory():
    
    show_logo()
    
    text = """
    Before starting this procedure, it is necessary to have compiled the kernel,  
    following the guidelines provided, in order to be able to insert the LiME module into the AVD.
    Only through a compiled kernel is it possible to insert external modules! The LiME module will dump
    the RAM memory of the AVD specified by the user and save it in the ‘dump' folder of the project.
    """
    
    print(f"\033[1;33m{text}\033[0m")
    
    show_avd()
    
    avd_name = input("\nEnter the name of the AVD you want to start (or type 'exit' to quit): ")
    
    # Check if the user wants to exit
    if avd_name.lower() == "exit":
        print("\nExiting the procedure...")
        return  # Exits the function and returns to the main menu

    if avd_exists(avd_name):
        
        if check_avd_running() != 1:
            print ("\nProcedure to start an AVD with a compiled kernel")
            start_emulator(avd_name)
            print("\nWaiting for the AVD to fully start: ") # Add a delay to ensure the AVD has enough time to start
            progress_bar(90)  # You can increase this time if the AVD takes longer to start
        else:
            print (f"\nThe AVD called {avd_name} is already running!")
       
        time.sleep(3)
        
        filename = input("\nEnter the name of the application you want to start (or type 'exit' to quit): ")
        # Check if the user wants to exit
        if filename.lower() == "exit":
            print("\nExiting the procedure...")
            return  # Exits the function and returns to the main menu
        
        result_run = run_apk(filename)
        
        if result_run.returncode == 1:
            print(f"\nThe APK with name {filename} is not into {APK_PATH}")
            
            while True:
                
                choice = input("\nDo you want to continue with RAM acquisition procedure (Y|n): ")
                
                if choice == "n":
                    return
                elif choice == "Y":
                    break  # Continua l'esecuzione della procedura
                else:
                    print("\nChoice not available. Please retry..")
            
        # Procedure to open AVD shell and have a root access
        os.chdir(os.path.expanduser(SDK_PATH) + ("/platform-tools"))
        try:
            print(f"\nStarting a root AVD shell..")
            time.sleep(2)
            subprocess.run("./adb root", shell=True)
        except subprocess.CalledProcessError as e:
           print(Fore.RED + f"Error opening a channel: {e}" + Style.RESET_ALL)
        
        # Check if a 'lime-goldfish.ko' is inside the 'files' project's folder    
        os.chdir(os.path.expanduser(FILE_PATH))
        if os.path.exists("lime-goldfish.ko"):
              
            # Include into AVD 'lime.ko' file  
            os.chdir(os.path.expanduser(SDK_PATH) + ("/platform-tools"))
            
            # Procedure to include LiME module
            install_command = "./adb push " + os.path.expanduser(FILE_PATH + '/lime-goldfish.ko') + " /sdcard/lime.ko"
            try:
                print(f"\nIncluding LiME module...")
                time.sleep(2)
                subprocess.run(install_command, shell=True)
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error including LiME: {e}" + Style.RESET_ALL)
            
            
            # Procedure to transfer memory's dump
            transfer_command = ('./adb forward tcp:4444 tcp:4444')
            try:
                print(f"\nOpening channel to tranfer the memory dump...")
                time.sleep(2)
                subprocess.run(transfer_command, shell=True)
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error opening a channel: {e}" + Style.RESET_ALL)   
            
            
            # Procedure to obtain the .lime file   
            try:
                print(f"\nUsing LiME module..")
                time.sleep(2)
                # Remove old 'lime' module (if none is alredy there there won't be a error message because of DEVNULL argument)
                subprocess.run('./adb shell rmmod lime', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # Re-insert 'lime' module
                subprocess.Popen('./adb shell insmod /sdcard/lime.ko "path=tcp:4444 format=lime" ', shell=True)
                print(f"\nLime module included!")             
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error opening a channel: {e}" + Style.RESET_ALL)  
            
            # Procedure to receive the memory's dump
            os.chdir(os.path.expanduser(DUMP_PATH)) # moving to dump directory (inside project's directory)
            try:
                print("\nReceiving the dump of entire memory..")
                time.sleep(5)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                subprocess.Popen(f"nc localhost 4444 > ram_{timestamp}.lime", shell=True) # you should find the dump in the directory of your API and ARCH, in the project directory
                progress_bar(30)
                time.sleep(2)
                os.system("clear")
                return
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error with the dump transfer: {e}" + Style.RESET_ALL) 
        else:
            print(Fore.RED + f"\nLiME's file is not inside files folder!" + Style.RESET_ALL)
            print("Exit...")
            time.sleep(2)
            os.system("clear")
            return
    else:
        print(Fore.RED + f"\nAVD doesn't exist" + Style.RESET_ALL)
        time.sleep(2)
        os.system("clear")
        return
        
        
        