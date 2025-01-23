import json
import os
import shutil
from colorama import init, Fore
from readchar import readchar
from PIL import Image
import universal_functions as uf
init()

default_texture_format = 147

def main():
    resourcegroup_type = ask_for_resourcegroup_type()
    resource_group, resources_1536, resources_other, texture_format, spritesheet_dirs, other_rsgfolder_dir = intro_user_prompt(resourcegroup_type)
    new_package_folder = f"./{resource_group}.package"
    
    
    # Make folder
    temp_path = os.path.join(new_package_folder, "resource/atlases")
    if not resourcegroup_type == "other":
        make_dir(temp_path)
        temp_path = os.path.join(new_package_folder, "resource/images")
        if resourcegroup_type == "image+anim": make_dir(temp_path)
    
    temp_path = os.path.join(new_package_folder, "resource/soundbanks")
    if resourcegroup_type == "other":
        make_dir(temp_path)
    
    if not resourcegroup_type == "other":
        # Make image data
        image_data = make_spritesheet_json(resources_1536)
    
    
        # Make image data file
        temp_path = os.path.join(new_package_folder, f"resource/atlases/{resource_group}.json")
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(image_data, file, indent=5)
        print(f"{Fore.GREEN}{resource_group}.json {Fore.LIGHTBLUE_EX}made")
        
        # Move image file to directory
        num = 0
        for spritesheet_dir in spritesheet_dirs:
            spritesheet_name = f"{resource_group}_{str(num).zfill(2)}.png"
            temp_path = os.path.join(new_package_folder, f"resource/atlases/{spritesheet_name}")
            shutil.copyfile(spritesheet_dir, temp_path)
            num += 1
        print(f"All spritesheets are moved to atlases")
    
    # Get PAM list
    otherresources_dict = None
    if resourcegroup_type != "image_only":
        otherresources_dict = get_otherresources_dict(resources_other, resourcegroup_type)
    
    # Made data.json
    datajson = make_datajson(texture_format, resource_group, otherresources_dict, resources_1536, resourcegroup_type)
    temp_path = os.path.join(new_package_folder, "data.json")
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(datajson, file, indent=5)
    print(f"{Fore.GREEN}data.json {Fore.LIGHTBLUE_EX}made")
    
    # Copy othe files to new directory
    if resourcegroup_type == "image+anim":
        temp_path_to_copy_to = os.path.join(new_package_folder, "resource/images")
        temp_path_to_copy_from = os.path.join(other_rsgfolder_dir, "res/IMAGES/768")
        shutil.rmtree(temp_path_to_copy_to, ignore_errors=True) # Clear folder
        shutil.copytree(temp_path_to_copy_from, temp_path_to_copy_to)
        print("Copied files in images")
    elif resourcegroup_type == "other":
        temp_path_to_copy_to = os.path.join(new_package_folder, "resource/soundbanks")
        temp_path_to_copy_from = os.path.join(other_rsgfolder_dir, "res/SOUNDBANKS")
        shutil.rmtree(temp_path_to_copy_to, ignore_errors=True)
        shutil.copytree(temp_path_to_copy_from, temp_path_to_copy_to)
        print("Copied files in soundbanks")
    
        
    print(f"{Fore.LIGHTBLUE_EX}Complete, wrote to {Fore.GREEN}{new_package_folder.replace('./', '')}{Fore.LIGHTBLUE_EX}. Ensure you pack with regular when packing with Sen")
        
        
        
def ask_for_resourcegroup_type():
    print(f"{Fore.LIGHTBLUE_EX}What type of resource group do you want to convert")
    print(f"{Fore.LIGHTMAGENTA_EX}[1] {Fore.LIGHTGREEN_EX}Image and Animation")
    print(f"{Fore.LIGHTMAGENTA_EX}[2] {Fore.LIGHTGREEN_EX}Image only")
    print(f"{Fore.LIGHTMAGENTA_EX}[3] {Fore.LIGHTGREEN_EX}Audio")
    while True:
        answer = readchar()
        if answer == "1":
            print(answer)
            return "image+anim"
        if answer == "2":
            print(answer)
            return "image_only"
        if answer =="3":
            print(answer)
            return "other"

def intro_user_prompt(resourcegroup_type):
    # Ask for resource group name
    print(f"{Fore.LIGHTBLUE_EX}What is the name of the resource group you want to convert? (ex {Fore.GREEN}AlwaysLoaded{Fore.LIGHTBLUE_EX})")
    resource_group = input(f"{Fore.RED}>>> {Fore.YELLOW}")
    
    # Get 1536 details
    if resourcegroup_type != "other":
        print(f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}{resource_group}_1536.json {Fore.LIGHTBLUE_EX}(drag the file here)")
        resources_1536 = uf.get_json_file_contents()
        resources_1536 = get_spritesheet_info(resources_1536)
    else:
        resources_1536 = None
                
    # Get other res group folder
    if not resourcegroup_type == "image_only":
        if resourcegroup_type == "image+anim":
            print(f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}{resource_group}_Common.json")
        elif resourcegroup_type == "other":
            print(f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}{resource_group}.json")
        resources_other = uf.get_json_file_contents()
    else:
        resources_other = None
    
    # Get texture format
    if not resourcegroup_type == "other":
        print(f"{Fore.LIGHTBLUE_EX}Enter the texture format number of {Fore.GREEN}{resource_group} {Fore.LIGHTBLUE_EX}(or enter nothing to use {default_texture_format})")
        while True:
            try:
                texture_format = input(f"{Fore.RED}>>> {Fore.YELLOW}")
                if texture_format == "":
                    texture_format = default_texture_format
                else:
                    texture_format = int(texture_format)
                break
            except ValueError:
                print(f"{Fore.LIGHTMAGENTA_EX}Enter a number only")
                continue
    else:
        texture_format = None
    
    # Get 1536 spritesheet
    if not resourcegroup_type == "other":
        spritesheet_dirs = []
        for spritesheet_name in resources_1536:
            print(f"{Fore.LIGHTBLUE_EX}Input the directory for {Fore.GREEN}{spritesheet_name}")
            while True:
                directory_temp = uf.clean_directory(input(f"{Fore.RED}>>> {Fore.YELLOW}"))
                try:
                    # If file does not exist, raise error
                    if not os.path.exists(directory_temp):
                        raise FileNotFoundError
                    # If file is not an image file, raise error
                    elif not if_is_image_file(directory_temp):
                        raise SyntaxError
                    # Otherwise, continue
                    spritesheet_dirs.append(directory_temp)
                    break
                
                except FileNotFoundError:
                    print(f"{Fore.LIGHTMAGENTA_EX}ERROR: directory is not found or does not exist")
                except SyntaxError:
                    print(f"{Fore.LIGHTMAGENTA_EX}ERROR: file is not an image file")
                print(f"{Fore.LIGHTBLUE_EX}Enter the spritesheet directory again")
    else:
        spritesheet_dirs = None
        
    # Get res folder dir
    other_rsgfolder_dir = None
    if not resourcegroup_type == "image_only":
        if resourcegroup_type == "image+anim":
            print(f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}{resource_group}_Common.packet")
        elif resourcegroup_type == "other":
            print(f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}{resource_group}.packet")
        other_rsgfolder_dir = uf.clean_directory(input(f"{Fore.RED}>>> {Fore.YELLOW}"))
    
    return [resource_group, resources_1536, resources_other, texture_format, spritesheet_dirs, other_rsgfolder_dir]

# Convert 1536 resources to a dictionary that is easier to work with
def get_spritesheet_info(resources_1536):
    # Add each info for spritesheets
    spritesheet_info = {}
    for res in resources_1536["resources"].copy():
        if res.get("atlas", False):
            # Set up spritesheet info
            spritesheet_info[res["id"]] = {
                "width": res["width"],
                "height": res["height"],
                "path": "",
                "individual_sprites": []
                }
            # Make path
            path = res["path"]
            new_path = ""
            for indiv_path in path:
                new_path += indiv_path + "/"
            new_path = new_path.replace("1536_", "")[:-1] # Removes 1536_ and remove ending '/'
            spritesheet_info[res["id"]]["path"] = new_path
    
    # Add image info for spritesheets
    for res in resources_1536["resources"].copy():
        # Loop through spritesheet_info to find which parent to add to
        for spritesheet in spritesheet_info:
            if spritesheet == res.get("parent", False):
                spritesheet_info[spritesheet]["individual_sprites"].append(res)
                break

    # Return data once done
    return spritesheet_info

# Returns true if file is an image file, otherwise return false
def if_is_image_file(directory):
    try:
        with Image.open(directory) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False

# Make directory if directory does not exist
def make_dir(directory):
    try:
        os.makedirs(directory)
    except: pass

# Make spritesheet JSON (ex AlwaysLoaded.json)
def make_spritesheet_json(resources_1536):
    # Set up spritesheet json
    spritesheet_json = {}
    for spritesheet_id in resources_1536:
        # Set up new spritesheet info
        spritesheet_json[spritesheet_id.replace("1536_", "")] = {
                                                "type": "Image",
                                                "path": resources_1536[spritesheet_id]["path"],
                                                "dimension": {
                                                    "width": resources_1536[spritesheet_id]["width"],
                                                    "height": resources_1536[spritesheet_id]["height"]
                                                },
                                                "data": {} # This will be added onto with the code below
                                            }
        
        for res in resources_1536[spritesheet_id]["individual_sprites"]:
            # Get IDs and coordinates
            sprite_id = res["id"]
            x_coord = res.get("ax", 0)
            y_coord = res.get("ay", 0)
            width_amount = res.get("aw", 0)
            height_amount = res.get("ah", 0)
            x_offset = res.get("x", 0)
            y_offset = res.get("y", 0)
            
            # Get path
            path_name = ""
            for path_part in res["path"]:
                path_name += f"{path_part}/"
            path_name = path_name[:-1].replace("1536/", "")
        
            # Make image_sprite data and add it
            toadd_image_sprite = {
                        "type": "Image",
                        "path": path_name,
                        "default": {
                            "ax": x_coord,
                            "ay": y_coord,
                            "aw": width_amount,
                            "ah": height_amount,
                            "x": x_offset,
                            "y": y_offset
                        }
                    }
            spritesheet_json[spritesheet_id.replace("1536_", "")]["data"][sprite_id] = toadd_image_sprite
        
    # Set up proper full dictionary then return it
    spritesheet_json = {
                            "type": "1536",
                            "packet": spritesheet_json
                            }
    return spritesheet_json

# Turn the other resource dictionary into a dictionary of every other file ID and their path so it's easier to work with, then return it
def get_otherresources_dict(resource_details, resourcegroup_type):
    # Make dictionary of each PAM id and path
    pam_list = {}
    for res in resource_details["resources"]:
        path = ""
        for path_part in res["path"]:
            path += f"{path_part}/"
        path = path[:-1].replace("/768", "") # Remove ending '/' and remove /768
        pam_list[res["id"]] = path
    return pam_list

# Make data.json and return it
def make_datajson(texture_format, resource_group, pam_list, resource_details, resourcegroup_type):
    # Check if resource group type is a texture group
    has_texture = True
    if resourcegroup_type == "other":
        has_texture = False
    
    # Add category
    category = None
    if resourcegroup_type != "other":
        category = {
		"resolution": [
            1536,
            768
		],
		"format": texture_format
	}
    
    # Make dictionary
    datajson = {
	"#expand_method": "simple",
	"version": 4,
	"texture_format_category": 0,
	"composite": has_texture,
	"category": category,
	"subgroup": {
		f"{resource_group}": {
			"category": {
				"common_type": has_texture,
				"locale": None,
				"compression": 3
			},
			"resource": { # Will be added onto with code below
			}
		}
	}
}
        
        # Add image data
    if resourcegroup_type != "other":
        datajson["subgroup"][resource_group]["resource"][resource_group] = {
				"type": "ImageData",
				"path": f"atlases/{resource_group}.json"
			}
        
        
    # Make list of PAMs
    if resourcegroup_type == "image+anim":
        for pam in pam_list:
            datajson["subgroup"][resource_group]["resource"][pam] = {
                                                                    "type": "PopAnim",
                                                                    "path": pam_list[pam]
            }
    elif resourcegroup_type == "other":
        for pam in pam_list:
            datajson["subgroup"][resource_group]["resource"][pam] = {
                                                                    "type": "SoundBank",
                                                                    "path": pam_list[pam]
            }
        
    # Return datajson
    return datajson
        


if __name__ == "__main__":
    should_give_safe_error = False
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