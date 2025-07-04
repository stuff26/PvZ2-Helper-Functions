from os import path, makedirs
from copy import deepcopy
from colorama import Fore, init
import universal_functions as uf
init()

FILES_NEEDED = {"ZOMBIETYPES.json", "ZOMBIEPROPERTIES.json", "PROPERTYSHEETS.json"}
def main():
            
    
    # Get packages files
    print(f"{Fore.LIGHTBLUE_EX}Enter the desired {Fore.GREEN}packages {Fore.LIGHTBLUE_EX}directory to edit")
    packages_dir = uf.ask_for_directory(is_file=False, look_for_files=FILES_NEEDED, accept_any=False)
    file_contents = dict()
    for file in FILES_NEEDED:
        file_contents[file] = uf.obtain_json_file_contents(path.join(packages_dir, file), silent=False)["objects"]
    file_contents_backup = deepcopy(file_contents)
    
    # Get almanac order list
    zombie_almanac_order = None
    for property_object in file_contents["PROPERTYSHEETS.json"]:
        if property_object.get("objclass", None) == "GamePropertySheet" and property_object["objdata"].get("ZombieAlmanacOrder", False):
            zombie_almanac_order = property_object["objdata"]["ZombieAlmanacOrder"]
            break
    
    # Organize zombie types
    sorted_zombietypes_list = []
    dummy_zombietypes_list = file_contents["ZOMBIETYPES.json"].copy()
    for zombie_name in zombie_almanac_order:
        for zombie_type in dummy_zombietypes_list:
            try:
                if zombie_type["objdata"]["TypeName"] == zombie_name:
                    sorted_zombietypes_list.append(zombie_type)
                    file_contents["ZOMBIETYPES.json"].remove(zombie_type)
                    dummy_zombietypes_list.remove(zombie_type)
                    break
            except KeyError:
                continue

    sorted_zombietypes_list.extend(file_contents["ZOMBIETYPES.json"])
    file_contents["ZOMBIETYPES.json"] = sorted_zombietypes_list
    
    # Get list of typnames with props
    zombie_types_and_props = {}
    for zombietype in sorted_zombietypes_list:
        try:
            typename = zombietype["objdata"]["TypeName"]
            props_name = zombietype["objdata"]["Properties"]
            props_name = uf.get_name_and_tag(props_name, return_type="name")
            zombie_types_and_props[typename] = props_name
        except KeyError:
            continue

    
    # Organize props
    new_zombieprops_list = []
    dummy_zombieprops_list = file_contents["ZOMBIEPROPERTIES.json"].copy()
    for zombie_typename in zombie_types_and_props:
        for zombie_props in dummy_zombieprops_list:
            try:
                if zombie_types_and_props[zombie_typename] in zombie_props.get("aliases", []):
                    new_zombieprops_list.append(zombie_props)
                    file_contents["ZOMBIEPROPERTIES.json"].remove(zombie_props)
                    dummy_zombieprops_list.remove(zombie_props)
                    break
            except KeyError:
                continue
    new_zombieprops_list.extend(file_contents["ZOMBIEPROPERTIES.json"])
    file_contents["ZOMBIEPROPERTIES.json"] = new_zombieprops_list

    # Write to files
    except_list = {"PROPERTYSHEETS.json"}
    backup_dir = path.join(uf.back_a_directory(packages_dir), "packages_backup")
    makedirs(backup_dir, exist_ok=True) # Make backup folder
    for file in FILES_NEEDED:
        if file not in except_list:
            backupfile_dir = path.join(backup_dir, file)
            setup_to_write = lambda file : {"version": 1, "objects": file}

            uf.write_to_file(setup_to_write(file_contents_backup[file]), backupfile_dir, is_json=True)
            uf.write_to_file(setup_to_write(file_contents[file]), path.join(packages_dir, file), is_json=True)
    
if __name__ == "__main__":
    main()