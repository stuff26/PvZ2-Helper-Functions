import json
from colorama import init, Fore
import sys
import os
init()

# Remove illegal chars from a directory to prevent potential errors
def clean_directory(directory):
    platform = sys.platform
    if platform == "win32": illegal_chars = ["*", "?", "\"", "<", ">", "|"]
    elif platform == "linux": illegal_chars = ["/"]
    elif platform == "darwin": illegal_chars = ["/", ":"]
    
    for char in illegal_chars: directory = directory.replace(char, "")
    return directory

def get_json_file_contents(default_directory=0, return_directory=False, silent=False):
    while True:
        # Ask for directory
        directory = clean_directory(better_user_input())
        if directory == "" and default_directory != 0:
            directory = default_directory
        elif directory == "" and default_directory == 0:
            print(f"{Fore.LIGHTMAGENTA_EX}Enter a directory")
            continue
        elif "." not in directory:
            directory += ".json"
        
        jsonfile_contents = obtain_json_file_contents(directory, silent=silent)
        if isinstance(jsonfile_contents, type(None)): continue
        elif return_directory: return (jsonfile_contents, directory)
        else: return jsonfile_contents

        
def obtain_json_file_contents(directory, silent=False):
        try:
            # Attempt to open file and if successful, return the contents
            with open(directory, "r", encoding="utf-8") as file:
                return json.load(file)
        # List of errors
        except UnicodeDecodeError:
            if not silent: print(f"{Fore.LIGHTMAGENTA_EX}ERROR: file is not a JSON file")
        except json.decoder.JSONDecodeError:
            if not silent: print(f"{Fore.LIGHTMAGENTA_EX}ERROR: JSON file is invalid")
        except FileNotFoundError:
            if not silent: print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {directory} is not found or does not exist")
        except Exception as e:
            if not silent: print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
        if not silent: print(f"{Fore.LIGHTBLUE_EX}Enter the directory again")
        return None

# Provides better input with color for user and has built in directory cleaning
def better_user_input(ask_directory=False):
    if not ask_directory: return input(f"{Fore.RED}>>> {Fore.YELLOW}")
    else: return clean_directory(input(f"{Fore.RED}>>> {Fore.YELLOW}"))

        
def open_in_exe(relative_path):
    #Get the absolute path to the resource, whether running as a script or as a bundled executable.
    if hasattr(sys, '_MEIPASS'):  # Running as a PyInstaller bundle
        base_path = sys._MEIPASS
    else:  # Running from function runner as a script alone
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def write_to_file(towrite, directory, is_json=False):
    with open(directory, "w", encoding="utf-8") as file:
        if is_json:
            json.dump(towrite, file, indent=5)
        else:
            file.write(str(towrite))
        return True