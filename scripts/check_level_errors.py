import json
import os
from colorama import Fore, init
import universal_functions as uf
init()


NEEDED_FILES = ("LEVELMODULES.json", "PLANTTYPES.json", "GRIDITEMTYPES.json", "ZOMBIETYPES.json")

OBJECT_CHECKING_GUIDE = uf.obtain_json_file_contents(uf.open_in_exe("check_level_errors_guide.json"))

# If a module definition is in one of these lists, then treat it as the module before it
MODULE_DERIVATIVES = {
    (
    "DinoStageProperties", "LunarStageProperties", "SportzballStageProperties",
     "JoustStageProperties", "FutureStageProperties", "DarkStageProperties",
     "CarnivalStageProperties", "EgyptStageProperties", "WestStageProperties",
     "ModernStageProperties", "LostCityStageProperties", "PirateStageProperties",
     "BeachStageProperties", "IceAgeStageProperties", "EightiesStageProperties",
     "FrontLawnStageProperties", "HeroesStageProperties"

     ): "StageModuleProperties",

     ("LevelOfTheDayModuleProperties"): "LevelEscalationModuleProperties",
     ("BeghouledSeedBankProperties"): "SeedBankProperties",
     ("ZombossRiftBattleModuleProperties"): "ZombossBattleModuleProperties",
     ("SpiderRainZombieSpawnerProps", "ParachuteRainZombieSpawnerProps"): "ZombieRainSpawnerProps"
}

HAS_FOUND_ERROR = False

def main():

    print(f"{Fore.LIGHTBLUE_EX}Enter the level file you want to scan")
    level = uf.get_json_file_contents()
    #level = uf.obtain_json_file_contents(r"C:\Users\zacha\Documents\Coding Stuff\Scripts\Script_Compiled\BEACH3.json")["objects"]
    print(f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}packages {Fore.LIGHTBLUE_EX}file you want to scan")
    packages_dir = uf.ask_for_directory(look_for_files=NEEDED_FILES, is_file=False, is_case_sensitive=False)
    #packages_dir = r"C:\Users\zacha\Documents\main.675.com.ea.game.pvz2_aub.obb.bundle\packages"

    # Set up a list of all the data from the packages dir and level that is needed
    file_dict = {
        "modules": get_aliases("levelmodules.json", packages_dir),
        "zombie_aliases": get_aliases("zombietypes.json", packages_dir),
        "plant_aliases": get_aliases("planttypes.json", packages_dir),
        "grid_aliases": get_aliases("griditemtypes.json", packages_dir),
        "zombie_types": get_aliases("zombietypes.json", packages_dir, is_typename=True),
        "plant_types": get_aliases("planttypes.json", packages_dir, is_typename=True),
        "grid_types": get_aliases("griditemtypes.json", packages_dir, is_typename=True),
        "level": get_aliases(level_data=level, is_level=True)
    }

    # Loop through every object in the level
    for level_object in level:
        if not isinstance(level_object, dict): # Fail safe to make sure all objects are dictionaries
            continue

        # Get type of object this is, if it is nothing (like {}), skip it
        definition = level_object.get("objclass", "")
        if not definition: 
            continue
        elif definition not in OBJECT_CHECKING_GUIDE:
            for key in MODULE_DERIVATIVES:
                if definition in key:
                    definition = MODULE_DERIVATIVES[key]
                    break
            else: # If not found in module derivatives, skip it
                continue
        
        # Get the objdata of the level and the guide from that objclass
        objdata = level_object["objdata"]
        guide = OBJECT_CHECKING_GUIDE[definition]

        # Loop through every key in objdata
        for param in objdata:
            try:
                if param not in guide: # Skip ones that are not included in the guide
                    continue

                data = objdata[param] # Get the param data

                # If the data is meant to be a list of values, loop through them
                if guide[param].get("is_nested_list", False):
                    for list_data in data:
                        for list_data2 in list_data:
                            if check_for_missing_alias(guide, param, list_data2, file_dict, level_object):
                                pass
                elif guide[param].get("is_list", False):
                    for list_data in data:
                        if check_for_missing_alias(guide, param, list_data, file_dict, level_object):
                            pass
                # Otherwise, check the individual param
                else:
                    if check_for_missing_alias(guide, param, data, file_dict, level_object):
                        pass
            except Exception as e:
                print(f"Errors when reading {definition}: {e}")
    global HAS_FOUND_ERROR
    if not HAS_FOUND_ERROR:
        print(f"{Fore.LIGHTBLUE_EX}No errors found")

# Checks through the data given to see if there is something missing
def check_for_missing_alias(guide:dict, param:str, data:str, file_dict:dict, level_object:dict):
    reference_name = guide[param]["reference"]
    reference = file_dict[reference_name]

    if guide[param].get("param_to_check", False):
        param_to_check = guide[param]["param_to_check"]
        data = data[param_to_check]
    
    if guide[param].get("is_at_sign", False):
        data, reference_name = split_at_sign(data)
        if reference_name:
            reference = file_dict[reference_name]

    global HAS_FOUND_ERROR
    if not reference_name:
        print(f"{data} has an invalid reference name")
        if not HAS_FOUND_ERROR: HAS_FOUND_ERROR = False
        return False
        
    elif data not in reference:
        print(f"Could not find {data} in {reference_name}")
        if not HAS_FOUND_ERROR: HAS_FOUND_ERROR = False
        return False
    else:
        return True


def split_at_sign(data):
    data = data[5:] # Remove RTID(
    data = data[0:len(data)-1] # remove ending )

    name, location = data.split("@")
    location_to_reference_dict = {
        "LevelModules": "modules",
        "PlantTypes": "plant_aliases",
        "ZombieTypes": "zombie_aliases",
        "GridItemTypes": "grid_aliases",
        ".": "level",
        "CurrentLevel": "level",
    }
    reference = location_to_reference_dict.get(location, False)
    return name, reference


# Get list of aliases or typenames from a file's objects
def get_aliases(file_name="", dir="", is_typename=False, level_data="", is_level=False) -> list:
    if not is_level:
        contents = uf.obtain_json_file_contents(os.path.join(dir, file_name))
    else:
        contents = {"objects": level_data}
    
    alias_list = set()
    for object in contents["objects"]:
        if not isinstance(object, dict):
            continue
        if is_typename:
            alias_list.add(object.get("objdata", dict()).get("TypeName", ""))
        else:
            alias_list.update(object.get("aliases", []))
    try: alias_list.remove("")
    except KeyError: pass

    return alias_list

if __name__ == "__main__":
    main()