

from utils.config import *
from utils.avd_manage import progress_bar

# Function to remove non-printable Unicode characters
def clean_text(text):
	return ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C')

# Function to set an app as default
def set_default_app(device):
	# Connect to the device
	# device = u2.connect()  # or u2.connect('device_ip')
	
 	# Step 1: Identify the app name from the generalized dialog title
	title_element = device(textMatches=r".*as your default .* app\?")
	print(title_element)
	
	if title_element.exists:
		# Extract the app name and clean it
		dialog_text = title_element.get_text()
		cleaned_text = clean_text(dialog_text)
		app_name = cleaned_text.split("Set ")[1].split(" as your default")[0]
		print(f"App name extracted and cleaned: {app_name}")
		
		# Step 2: Look for the app name in the list of options
		app_option_found = False
		app_options = device(className="android.widget.LinearLayout")
		for app_option in app_options:
			app_name_element = app_option.child(className="android.widget.TextView")
			if app_name_element.exists:
				app_name_text = clean_text(app_name_element.get_text())
				if app_name_text == app_name:
					print(f"Matching app option found: {app_name_text}")
					# Find and click the radio button by simulating a click on the parent layout
					radio_button = app_option.child(className="android.widget.RadioButton")
					if radio_button.exists:
						# Try clicking on the radio button's parent layout if direct clicking doesn't work
						app_option.click()  # Click on the layout containing the radio button
						print(f"Clicked on the layout containing the radio button for: {app_name_text}")
						app_option_found = True
						break
  
		if not app_option_found:
			print(f"App '{app_name}' was not found in the list.")
			exit(1)
			
		# Step 3: Click on "SET AS DEFAULT" if it's enabled
		set_default_button = device(resourceId="android:id/button1")
		if set_default_button.exists and set_default_button.info['enabled']:
			set_default_button.click()
			print("Clicked 'SET AS DEFAULT'.")
		else:
			print("'SET AS DEFAULT' button is not enabled.")
	else:
		print("The dialog is not displayed.")

# Function to obtain all permissions
def grant_permissions():
	device = u2.connect()
	device.reset_uiautomator()
	time.sleep(2)
	while True:
		window_detected=False
		
		if device.xpath(f"//*[contains(@text, 'Allow')]").exists:
			if device.xpath(f"//*[contains(@text, 'WHILE USING THE APP')]").exists:
				device(text="WHILE USING THE APP").click()
				window_detected=True
				time.sleep(1)
			elif device.xpath(f"//*[contains(@text, 'ALLOW')]").exists:
				device(text="ALLOW").click()
				window_detected=True
				time.sleep(1)	
			elif device.xpath(f"//*[contains(@text, 'ALWAYS')]").exists:
				device(text="ALWAYS").click()
				window_detected=True
				time.sleep(1)
			elif device.xpath(f"//*[contains(@text, 'always')]").exists:
				device(text="always").click()
				window_detected=True
				time.sleep(1)
			elif device.xpath(f"//*[contains(@text, 'Allow')]").exists:
				device(text="Allow").click()
				window_detected=True
				time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 'full screen')]").exists:
			device(text="GOT IT").click()
			window_detected=True
			time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 'Activating this admin app will allow')]").exists:
			device(text="Activate this device admin app").click()
			window_detected=True
			time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 't responding')]").exists:
			device(text="Close app").click()
			window_detected=True
			time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 'Choose what to allow')]").exists:
			device(text="CONTINUE").click()
			window_detected=True
			time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 'older version')]").exists:
			device(text="OK").click()
			window_detected=True
			time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 'run in background')]").exists:
			device(text="ALLOW").click()
			window_detected=True
			time.sleep(1)
		elif device(textMatches=r".*as your default .* app\?").exists:
			print("Setting the app as the default one \n")
			set_default_app(device)
			window_detected=True
			time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 'keeps stopping')]").exists:
			print("Keeps stopping \n")
			window_detected=False
			time.sleep(1)
		elif device.xpath(f"//*[contains(@text, 'Permission')]").exists:
			device(text="OK").click()
			window_detected = True
			time.sleep(2)
		if not window_detected:
			print("No more windows detected to handle. Exiting loop.")
			break

""" ---------------------------------------------------------------------------------------------------------------"""

# Function to return the full path of the specified APK file
def get_apkpath(filename):
    """
    :param filename: Name of the APK file
    :return: Full path of the APK file if it exists, otherwise None
    """
    apkpath = os.path.join(os.path.expanduser(APK_PATH) + f"/{filename}.apk" )
    
    if os.path.isfile(apkpath):
        return apkpath
    else:
        return None
    
# Function to obain the real name of APK file
def get_apkname(filename):
    """
    :param filename: Name of the APK file
    :return pkg_name: Real name of 'filename' APK file
    """

    # Call to obtain the full path of apk
    apkpath = get_apkpath(filename)
    
    if apkpath == None:
        return None
    
    # Move to the folder where 'aapt' exe is cointained
    os.chdir(os.path.expanduser(SDK_PATH) + f"/build-tools/{BUILD_VERSION}")
        
    # Find real name of the packet
    manifest_info = subprocess.run(f'./aapt d badging "{apkpath}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pkg_name = manifest_info.stdout.split("package: name='")[1].split("' versionCode=")[0]
    return pkg_name

# Function to start an application
def run_apk(filename):
	"""
	:param filename: Name of the APK file
	"""

	# Obtain real packet name of 'filename' APK file
	pkg_name = get_apkname(filename)

	if pkg_name == None:
		return None

	os.chdir(os.path.expanduser(SDK_PATH) + "/platform-tools")

	try:
		command = f"./adb shell monkey -p {pkg_name} -c android.intent.category.LAUNCHER 1 "
		run_apk = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
		#subprocess.run(f'adb shell am start -n {pkg_name}/{launch_activity}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
 
	except subprocess.CalledProcessError as e:
		print(Fore.RED + f"Error opening the application {pkg_name}: {e}" + Style.RESET_ALL)
		os.system("clear") # Clean the terminal window
		return

	progress_bar(25)
 
	# Function to obtain all permissions
	grant_permissions()
	time.sleep(3)
	return run_apk

""" ---------------------------------------------------------------------------------------------------------------"""

# Function to execute automatic interactions	
def automatic_interactions(pkg_name):
    """
    :param filename: Name of the APK file
    """
    os.chdir(os.path.expanduser(SDK_PATH) + ("/platform-tools")) # ADB is in platform    
    auto_click = subprocess.run(f'adb shell monkey -p {pkg_name} -v 500', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

