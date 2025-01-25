import json
from colorama import init, Fore
import sys
import os
from PIL import Image
init()

# Remove illegal chars from a directory to prevent potential errors
def clean_directory(directory):
    platform = sys.platform
    if platform == "win32": illegal_chars = ["*", "?", "\"", "<", ">", "|"]
    elif platform == "linux": illegal_chars = ["/"]
    elif platform == "darwin": illegal_chars = ["/", ":"]
    
    for char in illegal_chars: directory = directory.replace(char, "")
    return directory

# Ask for directory from user
# is_file == determines if the function should check if directory is a file or folder, default is a folder
# look_for_files == is a list type, checks to make sure folder directory has files and throws error if it doesn't
def ask_for_directory(is_file=False, look_for_files=None):
    while True:
        # Ask for directory
        directory = better_user_input(ask_directory=True)
        
        # Check if directory exists at all
        if not os.path.exists(directory):
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Directory does not exist")
            continue
        
        # If is_file is set to False, check if directory is a folder
        elif not os.path.isdir(directory) and not is_file:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Directory is not a folder")
            
        # If is_file is set to True, check if directory is a file
        elif not os.path.isfile(directory) and is_file:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Directory is not a file")
            
        # If look_for_files is given, check if all files in directory exist
        elif look_for_files != None and not is_file:
            file_list = os.listdir(directory)
            
            should_repeat = False
            for file in look_for_files:
                if file not in file_list:
                    print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Could not find {file} in directory")
                    should_repeat = True
                    break
            if should_repeat: continue # If error occurs, repeat loop
        
        # Return directory
        return directory

# Ask for JSON file to be read
# default_directory == directory to be input automatically if user enters nothing
# return_directroy == returns a tuple with json and directory together if set to True, otherwise only returns json
# silent == sent no message if error occurs if set to True
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
        if isinstance(jsonfile_contents, type(None)):
            continue
        elif return_directory:
            return (jsonfile_contents, directory)
        else:
            return jsonfile_contents

# Return JSON file contents safely
# directory == file directory to be read
# silent == sent no message if error occurs
def obtain_json_file_contents(directory="file.json", silent=False):
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
        return None

# Provides better input with color for user and has built in directory cleaning
# ask_directory == clean out illegal characters for directories if set to true
def better_user_input(ask_directory=False):
    if not ask_directory:
        return input(f"{Fore.RED}>>> {Fore.YELLOW}")
    else:
        return clean_directory(input(f"{Fore.RED}>>> {Fore.YELLOW}"))


# Return proper directory to open file inside of exe
def open_in_exe(relative_path="directory", is_main=None):
    #Get the absolute path to the resource, whether running as a script or as a bundled executable.
    if hasattr(sys, '_MEIPASS'):  # Running as a PyInstaller bundle
        base_path = sys._MEIPASS
    elif not is_main:
        base_path = os.path.abspath("./scripts")
    else:  # Running from function runner as a script alone
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Write to a file
# is_json == writes to file like a json
def write_to_file(towrite, directory, is_json=False, parent_dir=False):
    if parent_dir:
        directory = os.path.join(os.path.normpath(parent_dir + os.sep + os.pardir), directory)
        
        
    with open(directory, "w", encoding="utf-8") as file:
        if is_json:
            json.dump(towrite, file, indent=5)
        else:
            file.write(str(towrite))
        return True
    
def back_a_directory(directory):
    return os.path.normpath(directory + os.sep + os.pardir)

# Separate name and tag of properties line
# return_type == determines what should be returned
# if "name", return name, if "tag, return tag, otherwise return tuple of name and tag
def get_name_and_tag(user_input, return_type="both"):
    name, tag = user_input.replace("RTID(", "").replace(")", "").replace("$", "").split("@")
    
    return_type = return_type.lower()
    if return_type == "name": return name
    if return_type == "tag": return tag
    else: return (name, tag)

# Checks if file is an image or not
def if_is_image_file(directory):
    try:
        with Image.open(directory) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False