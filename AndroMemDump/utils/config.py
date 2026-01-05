

"""
This file contains all the parameters used by the MemoryTool script that can be modified by the user for the 
correct operation of this tool in its environment.    
"""

import os
import re
import subprocess
import time
from colorama import Fore, Style, init
import sys
import threading
import uiautomator2 as u2
import unicodedata


API = "28"  # Android version to install on the AVD  
ARCH = "x86_64"  # CPU architecture for the AVD  
SUBARCH = "x86"  # Sub-architecture type  

SDK_PATH = "~/Library/ANDROID_DEBUG/sdk"  # Path to the Android SDK  
AVD_PATH = "~/.android/avd/"  # Path where AVD configurations are stored  

APK_PATH = "~/Desktop/progetto/apk_file"  # Directory containing the APK file  
FILE_PATH = "~/Desktop/progetto/files"  # General files directory  
DUMP_PATH = "~/Desktop/progetto/dump"  # Path for dump files  

BUILD_VERSION = "35.0.0"
FRIDUMP_PATH = "~/Downloads/fridump"
FRIDASERVER_PATH = "~/Downloads/frida-server"