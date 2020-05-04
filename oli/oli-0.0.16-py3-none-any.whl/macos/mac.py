import importlib
from .command import print_choice, check_input, run_input

switcher = {
        1: "Homebrew",
        2: "Oh-my-zsh"
    }

def run():
    """Main Function"""
    
    print("You are running MacOS")
    print_choice(switcher)
    value = check_input()
    exit_value = run_input(switcher, value)
    if exit_value == 0:
        run()
    else: 
        quit()