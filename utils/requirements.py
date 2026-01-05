

from utils.config import * # File .py that contains all necessary libraries and global parameters chosen by the user


# Function used to start the installation of all required SDK packages 
def install_sdk():
    
    print(f"\n\nDownloading SDK packages...")
    try:
        os.chdir(os.path.expanduser(SDK_PATH) + ("/cmdline-tools/latest/bin/")) # sdkmanager is in cmdline-tools' directory
        
        command = [
            "./sdkmanager",  # Runs the sdkmanager tool to manage Android SDKs
            "platform-tools",  # Installs platform tools (adb, fastboot, etc.)
            f"platforms;android-{API}",  # Installs the SDK for the specified Android version
            "emulator",  # Installs the Android emulator
            f"build-tools;{BUILD_VERSION}",  # Installs the specified version of build tools
            "tools"  # Installs additional tools (deprecated in newer SDKs)
        ]

        
        subprocess.run(command, check=True) # Installation of all necessary functions for AVD
        print("\nAll packages were successfully downloaded [✓]")
        time.sleep(3)
        os.system("clear") # Clean the terminal window
        return
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error downloading system image: {e}" + Style.RESET_ALL)
        return
    

# Function to download the desired Android version for the AVD
def download_android():
    
    print(f"\n\nDownloading Android OS with API {API}...")
    try:
        os.chdir(os.path.expanduser(SDK_PATH) + ("/cmdline-tools/latest/bin/")) # sdkmanager is in cmdline-tools' directory
        
        command = [
            "./sdkmanager",
            "--install",
            f"system-images;android-{API};google_apis;{ARCH}"
        ]
        
        subprocess.run(command, check=True)
        print("\nThe required Android version was successfully downloaded [✓]")
        time.sleep(3)
        os.system("clear") # Clean the terminal window
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error downloading system image: {e}" + Style.RESET_ALL)
        return