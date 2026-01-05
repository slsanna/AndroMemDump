

from graphics.logo import show_logo  # Imports the function to show the logo
from graphics.graphic_setup import set_terminal_background # Import the function to change terminal graphics
from utils.functionalities import show_functionalities  # Imports the function to show the menu
from utils.requirements import install_sdk # Import the function to install all packages of SDK

def main():
    
    #set_terminal_background() # Function that sets the terminal graphics to black for correct display

    #show_logo() # Function showing the initial programme logo

    #install_sdk() # Function to install all packages of SDK
    
    show_functionalities() # Function displaying the list of tool functionalities

    """

    1. Create and configure an AVD       
    2. Delete an AVD                     
    3. Install application .apk          
    4. RAM functionalities               
    5. Exit                              

    """
    
if __name__ == "__main__":
    main()