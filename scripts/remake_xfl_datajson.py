from PIL import Image, UnidentifiedImageError
import os
from colorama import Fore, init
from readchar import readchar
import universal_functions as uf
init()

IMAGE_PREFIX = "IMAGE_" # Image prefix to add to front of new image IDs
def main():
    print(f"{Fore.LIGHTBLUE_EX}Enter the XFL you want to edit")
    filepath:str = uf.ask_for_directory(is_file=False, look_for_files=("data.json", "library", "DOMDocument.xml",), is_case_sensitive=False)
    
    DOMDocument:dict = uf.open_xml_file(os.path.join(filepath, "DOMDocument.xml"))["DOMDocument"]
    file_list = list()
    for file_dict in DOMDocument["media"]["DOMBitmapItem"]:
        file_list.append(file_dict.get("@href"))
        
    
    for file in file_list.copy():
        if not file.lower().startswith("media/"):
            file_list.remove(file)
            continue
        index = file_list.index(file)
        file_list[index] = file.lower().replace(".png", "") # Remove .png ending

    # Get contents of data.json
    datajson:dict = uf.obtain_json_file_contents(os.path.join(filepath, "data.json"), silent=True)
    scale:float = 1200 / int(datajson["resolution"])
    
    # Ask for prefix to include
    prefix:str = ask_for_prefix(file_list[0])
        
    # Clear image dictionary
    datajson["image"] = {}
    # Go through each image, take dimensions, calculate, and add to data.json
    library_path:str = os.path.join(filepath, "library")
    for file in file_list:
        # Open image
        file_name = f"{file}.png"
        try:
            image = Image.open(os.path.join(library_path, file_name))
        # If file does not exist in media folder
        except FileNotFoundError:
            print(f"{Fore.LIGHTMAGENTA_EX}Could not find {file_name}, will not be added to data.json")
            continue
        # If file can't be read by pillow
        except UnidentifiedImageError:
            print(f"{Fore.LIGHTMAGENTA_EX}{file_name} is not an image file, will not be added to data.json")
            continue
        
        # Calculate new image sizes
        width = int(image.width * scale)
        height = int(image.height * scale)
        
        # Make ID
        file = file.replace("media/", "")
        image_id = prefix + file.upper()
        
        # Create new image info
        image_info = {
            "id": image_id,
            "dimension": {
                "width": width,
                "height": height,
            },
            "additional": None,
        }
        # Add to datajson + give message
        datajson["image"][file] = image_info
        print(f"{Fore.LIGHTBLUE_EX}Added {Fore.GREEN}{file}")

    # Add new stuff to data.json
    uf.write_to_file(datajson, os.path.join(filepath, "data.json"), is_json=True)

def ask_for_prefix(example_file:str) -> str:
    while True:
        # User prompt
        print(f"{Fore.LIGHTBLUE_EX}What prefix do you want, or enter nothing to take the prefix of what is already in {Fore.GREEN}data.json")
        prefix = uf.better_user_input(ask_directory=False).upper()
        prefix = adjust_prefix(prefix)
        
        # Give example, then ask user for Y or N
        print(f"{Fore.LIGHTBLUE_EX}Example prefix would be {Fore.GREEN}{prefix}{example_file.upper().replace('MEDIA/', '')}")
        print(f"{Fore.LIGHTBLUE_EX}Would you like to continue? (Y/N)")
        while True:
            answer = readchar().upper()
            if answer in ("Y", "N"):
                print(answer)
                if answer == "Y":
                    return prefix
                break
    
def adjust_prefix(prefix:str) -> str:
    # Adjust user input to make sure it starts with IMAGE_ and ends with _
    if not prefix.startswith(IMAGE_PREFIX):
        prefix = IMAGE_PREFIX + prefix
    if not prefix.endswith("_"):
        prefix += "_"
    return prefix

if __name__ == "__main__":
    main()
    input("Complete")

