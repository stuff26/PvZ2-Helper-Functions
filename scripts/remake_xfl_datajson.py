from PIL import Image
from os import listdir, path, getcwd
import json
from sys import exit
from colorama import Fore, init
from readchar import readchar
init()

def main():
    # Necessary variables
    filepath = get_filepath()
    file_list = get_file_list(filepath)
    print(f"{Fore.LIGHTBLUE_EX}Obtained list of media")
    scale = 0.78125 # What to multiply dimensions in data.json by
    datajson_filename = "data.json"

    # Get contents of data.json
    datajson = get_datajson_contents(datajson_filename, filepath)
    print(f"{Fore.LIGHTGREEN_EX}data.json {Fore.LIGHTBLUE_EX}contents read")
    
    # Ask for prefix to include
    prefix = ask_for_prefix(datajson_filename, file_list[0])
        
    # Clear image dictionary
    datajson["image"] = {}
    # Go through each image, take dimensions, calculate, and add to data.json
    library_path = path.join(filepath, ".\\library\\media")
    for x in file_list:
        # Open image
        try: image = Image.open(path.join(library_path, x + ".png"))
        except: continue
        
        # Remove .png at end
        x = x.split(".")[0]
        
        # Calculate new image sizes
        width = int(image.width * scale)
        height = int(image.height * scale)
        
        # Make ID
        image_id = prefix + x.upper()
        
        # Create new image info
        image_info = {
            "id": image_id,
            "dimension": {
                "width": width,
                "height": height
            },
            "additional": None
        }
        # Add to datajson + give message
        datajson["image"][x] = image_info
        print(f"{Fore.LIGHTBLUE_EX}Added {Fore.GREEN}{x}")

    # Add new stuff to data.json
    with open(path.join(filepath, "data.json"), "w", encoding="utf-8") as file:
        json.dump(datajson, file, indent=3)
        
def get_filepath():
    # Checks if folder this is in is an xfl, if it is then use current directory
    if path.exists("data.json") and path.exists("./library/media"):
        return getcwd()
    
    # If not, ask user for input
    else:
        print(f"{Fore.LIGHTBLUE_EX}Drag the xfl folder you want to go through to here")
        while True:
            # Remove double quotes from user input and join with current working directory
            filepath = get_folder_input(input(f"{Fore.RED}>>> {Fore.YELLOW}"))
            
            # If path does not exist
            if not path.exists(filepath):
                print(f"{Fore.LIGHTMAGENTA_EX}Path does not exist, enter another folder")
                continue
            
            # If path is a valid xfl, return the path
            if path.join(filepath, "data.json") and path.join(filepath, "./library/media"):
                return filepath
            
            # If path exists but is not an xfl
            print(f"{Fore.LIGHTMAGENTA_EX}Path is not an xfl folder, enter another folder")
            
def get_folder_input(folder_name):
    # Remove " from user input if they drag the folder in
    new_name = ""
    for x in folder_name:
        if not x == '"':
            new_name += x
    return new_name
        
def get_file_list(filepath):
    # Get list of files
    file_list = listdir(path.join(filepath, "library\\media"))
    
    # Check if there is media
    if len(file_list) == 0:
        print(f"{LIGHTMAGENTA_EX}ERROR: no media found in library")
        readchar()
        exit()
        
    # Remove files that aren't .pngs
    new_file_list = []
    for file in file_list:
        if "." in file and file.endswith(".png"):
            # Add file w/o extenstion
            new_file_list.append(file.split(".")[0])
            
    return new_file_list
    
def get_datajson_contents(file_name, filepath):
    try:
        # Find and get data.json contents
        with open(path.join(filepath, file_name), "r", encoding="utf-8") as file:
            datajson = json.loads(file.read())
    # If JSON is invalid
    except json.JSONDecodeError:
        print(f"{Fore.MAGENTA}ERROR: data.json is an invalid JSON")
        readchar()
        exit()
    return datajson

def ask_for_prefix(datajson_filename, example_file):
    while True:
        # User prompt
        print(f"{Fore.LIGHTBLUE_EX}What prefix do you want, or enter nothing to take the prefix of what is already in {Fore.GREEN}{datajson_filename}")
        prefix = input(f"{Fore.RED}>>> {Fore.YELLOW}").upper()
        prefix = adjust_prefix(prefix)
        
        # Give example, then ask user for Y or N
        print(f"{Fore.LIGHTBLUE_EX}Example prefix would be {Fore.GREEN}{prefix}{example_file.upper()}")
        print(f"{Fore.LIGHTBLUE_EX}Would you like to continue? (Y/N)")
        while True:
            answer = readchar().upper()
            if answer == "Y":
                repeat_loop = False
                print(f"{Fore.YELLOW}{answer}")
                break
            # If N, repeat loop
            elif answer == "N":
                repeat_loop = True
                print(answer)
                break
        if repeat_loop: continue
        return prefix
    
def adjust_prefix(prefix):
    # Adjust user input to make sure it starts with IMAGE_ and ends with _
    if not prefix.startswith("IMAGE_"):
        prefix = "IMAGE_" + prefix
    if not prefix.endswith("_"):
        prefix += "_"
    return prefix

if __name__ == "__main__":
    try:
        main()
        print(f"{Fore.LIGHTMAGENTA_EX}Complete (press any button to continue)")
        readchar()
    except KeyboardInterrupt:
        print(f"\n{Fore.LIGHTMAGENTA_EX}Processed ended early by user (ENTER to exit)")
