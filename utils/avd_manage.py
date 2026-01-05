

from utils.config import *
#from utils.requirements import download_android # Import the function download_android


# Starts the AVD with the default snapshot if it exists; otherwise, launches normally.
def start_emulator(avd_name):
    """
    :param avd_name: Name of the AVD to start.
    """
    os.chdir(os.path.expanduser(FILE_PATH))
    
    if os.path.exists("kernel-ranchu"): # Check if a 'kernel-ranchu' is inside 'files' project's folder 
        print ("\nAVD will be started with a compiled kernel!")
        
        command = [
            "./emulator",
            "-avd", avd_name,  
            "-kernel", os.path.expanduser(FILE_PATH) + ("/kernel-ranchu"), # It is used to add the PATH of compiled kernel
            "-no-snapshot" # Disables snapshot usage and AVD starts fresh every time
        ]
    else:
        print(Fore.RED + f"\nKernel's file is not inside files folder!" + Style.RESET_ALL)
        print ("\nAVD will be started with its original kernel!")
        
        command = [
            "./emulator",
            "-avd", avd_name,
            "-no-snapshot" # Disables snapshot usage and AVD starts fresh every time
        ]
    
    print(f"\nStarting AVD: {avd_name}...")
        
    os.chdir(os.path.expanduser(SDK_PATH) + ("/emulator")) # Emulator exe is in emulator folder
    
    # Start the emulator
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)  # Wait for the emulator to boot

# Function to check if 'avd_name' is running or not
def check_avd_running():
    # Change directory to the folder containing ADB
    os.chdir(os.path.expanduser(SDK_PATH) + "/platform-tools")  # Ensure SDK_PATH is defined

    # Run the adb devices command to get the list of connected devices/emulators
    result = subprocess.run(['./adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Filter the output to find running emulators
    # The emulator name usually starts with "emulator" and should have the status "device" (indicating it is running)
    emulator_list = [line.split()[0] for line in result.stdout.splitlines() if 'emulator' in line and 'device' in line]

    # Return 1 if at least one emulator is running, otherwise return 0
    return 1 if emulator_list else 0


# Function to search by name for the presence of an AVD
def avd_exists(avd_name):
    """
    :param avd_name: Name of the AVD to start.
    """
    
    try:
        os.chdir(os.path.expanduser(SDK_PATH) + ("/cmdline-tools/latest/bin/")) # avdmanager is in cmdline-tools' directory
        
        # avdmanager is used to check which AVDs are already present in the system and under which names
        result = subprocess.run(["./avdmanager", "list", "avd"], capture_output=True, text=True)
        pattern = r"\b" + re.escape(avd_name) + r"\b"
        
        # It is used to check a match between the names of the devices present and the one you want to create
        flag = bool(re.search(pattern, result.stdout))
        return flag
    
    except FileNotFoundError:
        print(Fore.RED + "Error: avdmanager not found. Make sure the Android SDK is correctly installed and in the PATH." + Style.RESET_ALL)
        return False

  
# Displays a progress bar in the terminal to indicate the progress of a task.
def progress_bar(duration):
    """
    :param duration: The total duration (in seconds) for the progress bar.
    """
    
    for i in range(duration + 1):
        progress = (i / duration) * 100
        sys.stdout.write(f"\rProgress: [{int(progress)//2 * '='}{(50 - int(progress)//2) * ' '}] {progress:.2f}%")
        sys.stdout.flush()
        time.sleep(1)
    print("\nProcess completed!")  

    
# Function to show all available AVD devices with their features
def show_avd():
    
    try:
        os.chdir(os.path.expanduser(SDK_PATH) + ("/cmdline-tools/latest/bin/")) # avdmanager is in cmdline-tools' directory
        
        # avdmanager is used to check a list of all AVDs 
        result = subprocess.run(["./avdmanager", "list", "avd"], capture_output=True, text=True)
        print("\n\n", result.stdout)
    except FileNotFoundError:
        print(Fore.RED + "Error: avdmanager not found. Make sure the Android SDK is correctly installed and in the PATH." + Style.RESET_ALL)
        return False