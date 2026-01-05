

""" 
It is a file for defining functions that will change the design and appearance of the terminal window on which the tool will run. 
This decision was made because there are error messages and graphical choices that may not be visible depending on the visual 
configurations of each user
"""
import sys

# Set black background
def set_terminal_background():
    sys.stdout.write("\033[40m")  #dnwmdnw= black background
    sys.stdout.flush()

# Restore default background
def reset_terminal_background():
    sys.stdout.write("\033[49m")  # 49 = default background
    sys.stdout.flush()