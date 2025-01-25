from PIL import Image
import os
import json
from colorama import Fore, init
from readchar import readchar
import universal_functions as uf
init()

should_give_safe_error = True
SCALE = 0.78125 # What to multiply dimensions from media by
IMAGE_PREFIX = "IMAGE_" # Image prefix to add to front of new image IDs
def main():
    print(f"{Fore.LIGHTBLUE_EX}Enter the XFL you want to edit")
    filepath = uf.ask_for_directory(is_file=False, look_for_files=("data.json", "library"))
    
    file_list = os.listdir(os.path.join(filepath, "library/media"))
    for file in file_list.copy():
        if not file.endswith(".png") and not uf.if_is_image_file(os.path.join(filepath, "library/media", file)):
            file_list.remove(file)
            continue
        index = file_list.index(file)
        file_list[index] = file.replace(".png", "") # Remove .png ending

    # Get contents of data.json
    datajson = uf.obtain_json_file_contents(os.path.join(filepath, "data.json"), silent=True)
    
    # Ask for prefix to include
    prefix = ask_for_prefix(file_list[0])
        
    # Clear image dictionary
    datajson["image"] = {}
    # Go through each image, take dimensions, calculate, and add to data.json
    library_path = os.path.join(filepath, "library/media")
    for file in file_list:
        # Open image
        try: image = Image.open(os.path.join(library_path, f"{file}.png"))
        except: continue
        
        # Calculate new image sizes
        width = int(image.width * SCALE)
        height = int(image.height * SCALE)
        
        # Make ID
        image_id = prefix + file.upper()
        
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
        datajson["image"][file] = image_info
        print(f"{Fore.LIGHTBLUE_EX}Added {Fore.GREEN}{file}")

    # Add new stuff to data.json
    uf.write_to_file(datajson, os.path.join(filepath, "data.json"), is_json=True)

def ask_for_prefix(example_file):
    while True:
        # User prompt
        print(f"{Fore.LIGHTBLUE_EX}What prefix do you want, or enter nothing to take the prefix of what is already in {Fore.GREEN}data.json")
        prefix = uf.better_user_input(ask_directory=False).upper()
        prefix = adjust_prefix(prefix)
        
        # Give example, then ask user for Y or N
        print(f"{Fore.LIGHTBLUE_EX}Example prefix would be {Fore.GREEN}{prefix}{example_file.upper()}")
        print(f"{Fore.LIGHTBLUE_EX}Would you like to continue? (Y/N)")
        while True:
            answer = readchar().upper()
            if answer in ("Y", "N"):
                print(answer)
                if answer == "Y":
                    return prefix
                break
    
def adjust_prefix(prefix):
    # Adjust user input to make sure it starts with IMAGE_ and ends with _
    if not prefix.startswith(IMAGE_PREFIX):
        prefix = IMAGE_PREFIX + prefix
    if not prefix.endswith("_"):
        prefix += "_"
    return prefix

if __name__ == "__main__":
    if not should_give_safe_error:
        main()
        input()
        
    else:
        try:
            main()
            input("Complete")
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            input()
