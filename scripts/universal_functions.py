import json
from colorama import init, Fore
import sys
import os
from PIL import Image
import re
import xmltodict
init()

# Remove illegal characters from a directory to prevent potential errors
# - directory == given directory to clean out and return
# Returns: directory with illegal characters removed
def clean_directory(directory) -> str:
    platform = sys.platform
    if platform == "win32": illegal_chars = {"*", "?", "\"", "<", ">", "|"}
    elif platform == "linux": illegal_chars = {"/"}
    elif platform == "darwin": illegal_chars = {"/", ":"}
    
    for char in illegal_chars: directory = directory.replace(char, "")
    return directory

# Remove ANSI code from given, primarily for if text needs to be written to a file
# - text == text to be stripped of ANSI codes
# Returns: text without ANSI codes
def strip_ansi_codes(text) -> str:
    ansi_escape = re.compile(r'\x1B\[[0-9;]*[mGK]')
    return ansi_escape.sub('', text)

# Ask for directory from user safely
# - is_file == determines if the function should check if directory is a file or folder, default is a folder
# - look_for_files == is a list type, checks to make sure folder directory has files and throws error if it doesn't
# - accept_any == ignores is_file, causes function to not not check if directory is specifically a file or folder
# Returns: directory given inputted by user
def ask_for_directory(is_file:bool=False, look_for_files:tuple=None, accept_any:bool=False, is_case_sensitive:bool=False) -> str:
    while True:
        # Ask for directory
        directory = better_user_input(ask_directory=True)
        
        # Check if directory exists at all
        if not os.path.exists(directory):
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Directory does not exist")
            continue
        
        if not accept_any:
            # If is_file is set to False, check if directory is a folder
            if not os.path.isdir(directory) and not is_file:
                print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Directory is not a folder")
                
            # If is_file is set to True, check if directory is a file
            elif not os.path.isfile(directory) and is_file:
                print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Directory is not a file")
            
        # If look_for_files is given, check if all files in directory exist
        if look_for_files != None and os.path.isdir(directory):
            file_list = os.listdir(directory)
            if not is_case_sensitive:
                for i in range(0, len(file_list)):
                    file_list[i] = file_list[i].lower()
                    
            should_repeat = False
            for file in look_for_files:
                file = file.lower()
                if file not in file_list:
                    print(f"{Fore.LIGHTMAGENTA_EX}ERROR: Could not find {file} in directory")
                    should_repeat = True
                    break
            if should_repeat: continue # If error occurs, repeat loop
        
        # Return directory
        return directory

# Ask for JSON file to be read
# - default_directory == if user inputs nothing, set inputted directory to this to this
# - return_directroy == returns a tuple with JSON contents and directory together if set to True, otherwise only returns JSON contents
# - silent == sent no message if error occurs if set to True
# Returns: contents of a JSON file in the form of a dictionary
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
# - directory == file directory to be read
# - silent == send no message if error occurs if set to True, otherwise print out errors in console
# Returns: JSON file contents in the form of a dictionary, note keys that start with "@" are not nested dictionaries
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

# Returns contents of an XML file
# - directory == given directory to be taken from
# - silent == send no message if error occurs if set to True, otherwise print out errors in console
# Returns: XML file contents in the form of a dictionary
def open_xml_file(directory, silent=False):
    try:
        with open(directory, "r") as file:
            return xmltodict.parse(file.read())
    except FileNotFoundError:
        if not silent: print(f"{Fore.LIGHTMAGENTA_EX}ERROR: could not find {directory}")
    except Exception as e:
        if not silent: print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
        
    return None

# Provides better input with color for user and has built in directory cleaning
# - ask_directory == clean out illegal characters for directories if set to True if a directory is expected
# Returns: String that user inputs
def better_user_input(ask_directory=False):
    if not ask_directory:
        return input(f"{Fore.RED}>>> {Fore.YELLOW}")
    else:
        return clean_directory(input(f"{Fore.RED}>>> {Fore.YELLOW}"))


# Return proper directory to open file inside of exe
# - relative_path == directory to open
# - is_main == determines if being run as pyinstaller bundle or not
# Returns: path to desired directory
def open_in_exe(relative_path="directory", is_main=None):
    if hasattr(sys, '_MEIPASS'):  # Running as a PyInstaller bundle
        base_path = sys._MEIPASS
    elif not is_main:
        base_path = os.path.abspath("./scripts")
    else:  # Running from function runner as a script alone
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Write to a file
# - is_json == writes to file like a JSON
# - is_xml == writes to file like an XML
# - parent_dir == write to parent directory
# Returns: True or False depending on if the execution is completed without errors
def write_to_file(towrite, directory, is_json=False, is_xml=False, parent_dir=False):
    if parent_dir:
        directory = os.path.join(back_a_directory(parent_dir), directory)
        
    try:
        with open(directory, "w", encoding="utf-8") as file:
            if is_json:
                json.dump(towrite, file, indent=5)
            elif is_xml:
                xmltodict.unparse(towrite, output=file, encoding='utf-8', pretty=True)
            else:
                file.write(str(towrite))
            return True
    except Exception as e:
        print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
        return False

# Goes back a directory
# - directory == directory to go back on
# Returns: parent directory of given directory
def back_a_directory(directory):
    return os.path.normpath(directory + os.sep + os.pardir)

# Separate name and tag of properties line
# - user_input == props line to split
# - return_type == determines what should be returned, is either "name", "tag", or "both"
# Returns: either name, tag, or both parts of a property line
def get_name_and_tag(user_input, return_type="both"):
    name, tag = user_input.replace("RTID(", "").replace(")", "").replace("$", "").split("@")
    
    return_type = return_type.lower()
    if return_type == "name": return name
    if return_type == "tag": return tag
    else: return (name, tag)

# Checks if file is an image or not to ensure no errors are found when checking file
# - directory == directory to check if it is a file or not
# Returns: True if the file is found to be an image file, otherwise False
def if_is_image_file(directory):
    try:
        with Image.open(directory) as img:
            img.verify()
            return True
    except (IOError, SyntaxError, FileNotFoundError):
        return False

def fix_layer_or_frame_list(input_list, to_layer=False):
    if isinstance(input_list, list):
        if len(input_list) == 1 and not to_layer:
            return input_list[0]
    
    elif isinstance(input_list, dict) and to_layer:
        return [input_list]
    
    return input_list
