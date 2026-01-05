

from utils.config import * # File .py that contains all necessary libraries and global parameters chosen by the user
from graphics.logo import show_logo  # Import the function to show the logo
from utils.avd_manage import *
from utils.apk_manage import *


# Function to extract PID of a desired application using ADB
def check_process_adb(pkg_name):
	"""
	:param pkg_name: Real name of the APK file
	:return pid: PID value of pkg_name
	"""
	time.sleep(5)
	os.chdir(os.path.expanduser(SDK_PATH) + "/platform-tools")
	
	try:
		command = f"./adb shell ps -A | grep '{pkg_name}' | awk '{{print $2}}'"
		process_pid = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
		pid = process_pid.stdout.split("\n")[0]
		print(f"\n{pkg_name} running with PID {pid}")
  
	except subprocess.CalledProcessError as e:
		print(Fore.RED + f"Error finding the PID {pkg_name}: {e}" + Style.RESET_ALL)
		os.system("clear") # Clean the terminal window
		exit
  
	return pid
	
# Function to check the presence of a PID using Frida tool
def check_process_frida(pid):
	"""
	:param pid: PID of an application
	:return process_name: name of app with presented PID 
	"""
	print("\nConnecting and getting process name from Frida...")
 
	os.chdir(os.path.expanduser(FRIDA_PATH))
	
	try:
		command = f'./frida-ps -U | grep {pid}'
		get_pid_pname = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
		pattern = r"^\d+\s+(.+?)\s*$"
		match = re.match(pattern, get_pid_pname.stdout)
		process_name = match.group(1)
  
	except subprocess.CalledProcessError as e:
		print(Fore.RED + f"Error finding the app with PID {pid}: {e}" + Style.RESET_ALL)
		os.system("clear") # Clean the terminal window
		exit
  
	return process_name

# Function to check if 'frida-server' is running on a device
def run_frida_server_adb():
    
	os.chdir(os.path.expanduser(SDK_PATH) + "/platform-tools")
 
	# Check if 'frida-server' is running on a device
	command = "./adb shell ps -A | grep 'frida-server' | awk '{print $2}'"
	frida_pid_out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# Obtain of PID of process
	frida_pid = frida_pid_out.stdout.strip()
 
	# If a PID is been founded, 'frida_pid' content will be printed. Otherwise frida-server will be started in background.
	if frida_pid:
		print(f"\nFrida server is running on the device with PID: {frida_pid}")
	else:
		# frida-server is not running
		cmd_run_frida = ["./adb","shell","su 0 sh -c '/data/local/tmp/frida-server &'"]
		run_frida = subprocess.Popen(cmd_run_frida, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
		
		cmd_frida_ps = "./adb shell ps -A | grep 'frida-server' | awk '{print $2}'"
		frida_pid_out = subprocess.run(cmd_frida_ps, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		frida_pid = frida_pid_out.stdout.strip()
		print(f"\nStarted Frida server & running on the device with PID: {frida_pid}")

# Function to check if frida-server file is inside the AVD
def check_frida_server():
    
    print("\nChecking the presence of frida-server file in the selected AVD...")
    
    file_path = '/data/local/tmp'
    os.chdir(os.path.expanduser(SDK_PATH) + "/platform-tools")
    
    try:
        command = [
			'./adb', 
   			'shell', 
      		'ls', file_path
		]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if 'frida-server' in result.stdout:
            # Run frida-server
            print("\nRunning frida-server file in the selected AVD...")
            run_frida_server_adb()
        else:
            
            print("\nNo frida-server is inside the AVD. Including it...")
            
            # Include frida-server into AVD using adb
            frida_server_command = f'./adb push {os.path.expanduser(FRIDASERVER_PATH)} /data/local/tmp/'
            subprocess.run(frida_server_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            # Modify permissions of 'frida-server' file
            frida_server_perms = './adb shell "chmod 755 /data/local/tmp/frida-server"'
            subprocess.run(frida_server_perms, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            
            # Run frida-server
            print("\nRunning frida-server file in the selected AVD...")
            run_frida_server_adb()
        
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        os.system("clear") # Clean the terminal window
        return
 
# Function to creare the right path for each process
def create_dump_path(process_name):
	"""
	:param process_name: name of app with presented PID 
	:return dump_dir: final process's dump path
	"""
	out_dir_dump = os.path.expanduser(DUMP_PATH) + f'/Process/{process_name}'

	# Crea la struttura delle cartelle se non esiste
	if not os.path.exists(out_dir_dump):
		try:
			os.makedirs(out_dir_dump)
		except Exception as e:
			print(Fore.RED + f"Error creating directory {out_dir_dump}: {e}" + Style.RESET_ALL)
			return None

	# Trova il numero di versione per la cartella (1, 2, 3, ...)
	version = 1
	while os.path.exists(f"{out_dir_dump}/{version}"):
		version += 1

	# Creazione del percorso finale per la cartella
	dump_dir = os.path.join(out_dir_dump, str(version))

	# Crea la cartella finale per il dump
	try:
		os.makedirs(dump_dir)
		return dump_dir
	except Exception as e:
		print(Fore.RED + f"Error creating directory {dump_dir}: {e}" + Style.RESET_ALL)
		return None

# Function to dump the process with name 'process_name'
def dump_process(process_name):
    
    print(f"\nDumping memory of process {process_name}")   
    
    # Obtain the right path for dump the process 
    path = create_dump_path(process_name)
    if path == None:
        print(Fore.RED + f"Error creating process dump path" + Style.RESET_ALL)
        return
    
    os.chdir(os.path.expanduser(FRIDUMP_PATH))
    
    command = [
		"python3",        # Run the script using Python 3
		"fridump.py",     # The Fridump script for memory dumping
		"-U",             # Connect to a USB device (Android/iOS)
		"-s",             # Dump memory into a single file instead of multiple segments
		process_name,     # The target process name to dump memory from
		"-r",             # Attempt to dump read-only memory regions as well
		"-o", path        # Specify the output directory for the dumped memory
	]
    
    print("\n\n")
    run_fridump = subprocess.run(command)
    
    time.sleep(3)
    os.system("clear")
        
# Function to obtain the dump of desired process
def dump_single_process():
    
    show_logo()
        
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
        
        # Controll the presence of frida-server
        check_frida_server()
        
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
                 
        # Get pkg_name from filename   
        pkg_name = get_apkname(filename)
        
        # Get the pid of the running target app
        pid_pkg = None
        while pid_pkg is None:
            pid_pkg = check_process_adb(pkg_name)
            time.sleep(2)
            
        # Get process name of running target app
        process_name = check_process_frida(pid_pkg)
        
        # Make some automatic interactions
        automatic_interactions(pkg_name)
        
        # Dump the memory at the interesting addresses of the target process
        dump_process(process_name)
        
    else:
        print(Fore.RED + f"\nAVD doesn't exist" + Style.RESET_ALL)
        time.sleep(2)
        os.system("clear")
        return
