from colorama import init, Fore
init()
import universal_functions as uf
from os import path

OLD_TO_NEW_LIST = {
    "n": "name",
    "l": "lastest_level",
    "c": "coins",
    "spr": "sprouts",
    "g": "gems",
    "t": "gauntlets",
    "m": "mints",
    "pf": "penny_pursuit_fuel",
    "pt": "penny_pursuit_perk_progression",
    "p": "plants",
    "kz": "zombie_almanac",
    "wmed": "world_completion_data",
    "gf": "gamefeatures",
    "ne": "narrative_ids_seen",
    "dri": "endless_data",
    "cos": "costume_ids",
    "pr": "powerups",
    "tyi": "current_tresure_yeti_data",
    "gpi": "zen_garden_data",
    "upsi": "bought_flower_pot_ids",
    "pli": "boosted_plants",
    "izg": "start_in_zen_garden",
    "ap": "completed_minigames",
    "plis": "plant_level_data"
}

def main():
    # Obtain pp.dat json contents
    print(f"{Fore.LIGHTBLUE_EX}Enter the pp.dat file you want to convert")
    ppdat, ppdat_dir = uf.get_json_file_contents(return_directory=True)

    convert_to_original = "#1" in ppdat
    if convert_to_original:
        global OLD_TO_NEW_LIST
        OLD_TO_NEW_LIST = reverse_keys_and_values(OLD_TO_NEW_LIST)

    # Loop through every savefile
    try:
        for savefile in ppdat["objects"]:

            # Create new savefile dict
            new_savefile = dict()

            # Loop through each key
            for key in savefile["objdata"]:

                # If there is no key available to be translated, add to new dictionary as it is
                if not key in OLD_TO_NEW_LIST:
                    new_savefile[key] = savefile["objdata"][key]
                
                # Convert to new key
                else:
                    new_savefile[OLD_TO_NEW_LIST[key]] = savefile["objdata"][key]
            savefile["objdata"] = new_savefile
    except KeyError:
        print(f"{Fore.LIGHTMAGENTA_EX}ERROR: found error trying to read file, input file might not be a pp.dat file")
        return

    
    if not convert_to_original:
        ppdat["#1"] = "This is a cleaned up name version of a pp.dat by helper functions made by stuff26"
        ppdat["#2"] = "Please convert this to a proper pp.dat before inserting this into the game"
        ppdat["version"] = ppdat.pop("version")
        ppdat["objects"] = ppdat.pop("objects")
    else:
        ppdat.pop("#1")
        if "#2" in ppdat: ppdat.pop("#2")

    uf.write_to_file(ppdat, path.join(uf.back_a_directory(ppdat_dir)), "pp_new.json", is_json=True)

def reverse_keys_and_values(input_dict: dict) -> dict: 
    key_list = list(input_dict.keys())
    value_list = list(input_dict.values())
    new_dict = {}
    for i in range(0, len(key_list)):
        new_dict[value_list[i]] = key_list[i]
    
    return new_dict



if __name__ == "__main__":
    main()
    input("Complete")