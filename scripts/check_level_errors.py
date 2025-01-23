import json
from sys import exit
import os
from colorama import Fore, init
from readchar import readchar
import universal_functions as uf
init()

should_give_safe_error = False
CHECKING_FILES = ["LEVELMODULES.json", "PLANTTYPES.json", "GRIDITEMTYPES.json", "ZOMBIETYPES.json", "CREATURETYPES.json"]

def main():
    # Get level JSON file
    print(f"{Fore.LIGHTBLUE_EX}Drag the file you want to scan here, or enter nothing to scan {Fore.LIGHTGREEN_EX}level.json")
    while True:
        scanning_level = uf.get_json_file_contents(default_directory="level.json")
        try:
            levelmodule_list = get_aliases(scanning_level)
            customgriditem_list = get_custom_alias(scanning_level, "griditem")
            customzombie_list = get_custom_alias(scanning_level, "zombie")
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            continue
        break
    
    # Get packages folder
    print(f"{Fore.LIGHTBLUE_EX}Drag the packages folder that you want to compare to here")
    while True:
        # Ask for folder
        base_path = uf.better_user_input(ask_directory=True)
        
        # Check if directory exists, then check if it is a folder
        if not os.path.exists(base_path):
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: directory does not exist")
            continue
        if not os.path.isdir(base_path):
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: directory is not a folder")
            continue
        
        # Get list of files in base_path
        existing_file_list = os.listdir(base_path)
        # Check if all necessary files are in folder
        should_repeat = False
        for file_name in CHECKING_FILES:
            if file_name not in existing_file_list:
                print(f"{Fore.LIGHTMAGENTA_EX}ERROR: could not find {Fore.GREEN}{file_name} {Fore.LIGHTMAGENTA_EX}in directory")
                should_repeat = True
                break
        if should_repeat: continue
        
        reading_file = ""
        try:
            reading_file = "LEVELMODULES.json"
            levelmodules_json = uf.obtain_json_file_contents(os.path.join(base_path, reading_file), silent=True)
            obbmodule_list = get_aliases(levelmodules_json)
            
            
            reading_file = "PLANTTYPES.json"
            planttypes_json = uf.obtain_json_file_contents(os.path.join(base_path, reading_file), silent=True)
            planttypes_list = get_typenames(planttypes_json)
            plantalias_list = get_aliases(planttypes_json)
            
            reading_file = "GRIDITEMTYPES.json"
            griditemtypes_json = uf.obtain_json_file_contents(os.path.join(base_path, reading_file), silent=True)
            griditemtypes_list = get_typenames(griditemtypes_json)
            griditemalias_list = get_aliases(griditemtypes_json)
            
            reading_file = "ZOMBIETYPES.json"
            zombietypes_json = uf.obtain_json_file_contents(os.path.join(base_path, reading_file), silent=True)
            zombietypes_list = get_typenames(zombietypes_json)
            zombiealias_list = get_aliases(zombietypes_json)
            
            reading_file = "CREATURETYPES.json"
            creaturetypes_json = uf.obtain_json_file_contents(os.path.join(base_path, reading_file), silent=True)
            dinotype_list = get_typenames(creaturetypes_json)
        except TypeError:
               print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {Fore.GREEN}{reading_file} {Fore.LIGHTMAGENTA_EX}could not be read, is possibly an invalid JSON")
               continue
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            continue
        break
    

    message = check_level(scanning_level, obbmodule_list, levelmodule_list, planttypes_list, plantalias_list, griditemtypes_list, griditemalias_list, customgriditem_list, zombietypes_list, zombiealias_list, customzombie_list, dinotype_list)
    print(f"{Fore.LIGHTMAGENTA_EX}{message}")
    print(f"{Fore.LIGHTBLUE_EX}\nLevel check complete")
    print("Do you want to save this message in a text file? (Y/N)")
    while True:
        answer = readchar().upper()
        if answer == "N":
            print(f"{Fore.YELLOW}{answer}")
            break
        if answer == "Y":
            print(f"{Fore.LIGHTBLUE_EX}What file name do you want to save it as, or enter nothing to write to {Fore.GREEN}level_errors.txt")
            file_to_write_to = input(f"{Fore.RED}>>> {Fore.YELLOW}")
            if file_to_write_to == "":
                file_to_write_to = "level_errors.txt"
            if "." not in file_to_write_to:
                file_to_write_to += ".txt"
                
            write_to_file(message, file_to_write_to)
                
            break
    

# Returns list of all alias names in files
def get_aliases(contents):
    alias_list = []
    
    # Go through each module and store the alias
    for module in contents["objects"]:
        if "aliases" in module.keys():
            aliases_temp = module["aliases"]
            for alias in aliases_temp:
                alias_list.append(alias)
    return alias_list

# Returns list of all alias names in files
def get_typenames(contents):
    typename_list = []
    
    # Go through each module and store the alias
    for x in contents["objects"]:
        if "objdata" in x.keys():
            typename_list.append(x["objdata"]["TypeName"])
    return typename_list

def get_custom_alias(contents, scanning_type):
    alias_list = []
    
    # Go through each module and store the alias
    if scanning_type == "zombie":
        for module in contents["objects"]:
            if "aliases" in module.keys() and module["objclass"] == "ZombieType":
                aliases_temp = module["aliases"]
                for alias in aliases_temp:
                    alias_list.append(alias)
    elif scanning_type == "griditem":
        for module in contents["objects"]:
            if "aliases" in module.keys() and module["objclass"] == "GridItemType":
                aliases_temp = module["aliases"]
                for alias in aliases_temp:
                    alias_list.append(alias)
    return alias_list

def check_level(level_content, obbmodule_list, levelmodule_list, planttypes_list, plantalias_list, griditemtypes_list, griditemalias_list, customgriditem_list, zombietypes_list, zombiealias_list, customzombie_list, dinotype_list):
    # Check initial modules
    module_list = []
    
    # Get list of initial modules
    for module in level_content["objects"][0]["objdata"]["Modules"]:
        module_list.append(get_name_and_tag(module))
        
    # Check modules
    message = check_modules(level_content, obbmodule_list, levelmodule_list, module_list)
    message += check_seedbank(level_content, planttypes_list, plantalias_list)
    message += check_initialmodules(level_content, planttypes_list, griditemtypes_list, zombietypes_list)
    message += check_zombiewaves(level_content, zombietypes_list, zombiealias_list, customzombie_list)
    message += check_othermodules(level_content, obbmodule_list, levelmodule_list, planttypes_list, plantalias_list, griditemtypes_list, griditemalias_list, customgriditem_list, zombietypes_list, zombiealias_list, customzombie_list, dinotype_list)
    return message
    
def check_modules(level_content, obbmodule_list, levelmodule_list, module_list):
    message = ""
    # Check stage module
    stagemodule_name, stagemodule_tag = get_name_and_tag(level_content["objects"][0]["objdata"]["StageModule"])
    if stagemodule_tag == "LevelModules":
        if not stagemodule_name in obbmodule_list:
            message += f"\n{stagemodule_name}@{stagemodule_tag} not found in obb modules"
    elif stagemodule_tag == "CurrentLevel" or stagemodule_tag == ".":
        if not stagemodule_name in levelmodule_list:
            message += f"\n{stagemodule_name}@{stagemodule_tag} not found in level modules"
    else:
        message += f"\n{stagemodule_name}@{stagemodule_tag} tag is not valid"
        
    # Check each initial module
    for x in module_list:
        # If ends in @LevelModules, check obb module list
        if x[1] == "LevelModules":
            if not x[0] in obbmodule_list:
                message += f"\n{x[0]}@{x[1]} not found in obb modules"
        elif x[1] == "CurrentLevel" or x[1] == ".":
            if not x[0] in levelmodule_list:
                message += f"\n{x[0]}@{x[1]} not found in level modules"
        else:
            message += f"\n{x[0]}@{x[1]} tag is not valid"
            
        
    # Check wave modules
    for module in level_content["objects"]:
        if "objclass" in module.keys():
            if module["objclass"] == "WaveManagerProperties":
                waves = module["objdata"]["Waves"]
                for x in waves:
                    for y in x:
                        wavemodule_name, wavemodule_tag = get_name_and_tag(y)
                        accept = ["LevelModules", ".", "CurrentLevel"]
                        if wavemodule_tag == "LevelModules" and not wavemodule_name in obbmodule_list:
                            message += f"\n{wavemodule_name}@{wavemodule_tag} in wave modules not found in obb modules"
                        elif (wavemodule_tag == "CurrentLevel" or wavemodule_tag == ".") and not wavemodule_name in levelmodule_list:
                            message += f"\n{wavemodule_name}@{wavemodule_tag} in wave modules not found in level's modules"
                        elif not wavemodule_tag in accept:
                            message += f"\n{wavemodule_name}@{wavemodule_tag} has invalid tag"
    return message
        
def check_seedbank(level_content, planttypes_list, plantalias_list):
    message = ""
    # Find seedbank and check through
    for x in level_content["objects"]:
        if "objclass" in x.keys():
            # Check initial seedbank
            if x["objclass"] == "SeedBankProperties":
                # Save content
                seedbank_content = x
                
                # Check PresetPlant List
                try:
                    for x in seedbank_content["objdata"]["PresetPlantList"]:
                        if not x["PlantType"] in planttypes_list:
                            message += f"\n{x} in seedbank not found in plant types"
                except: pass
                # Check PlantIncludeList
                try:
                    for x in seedbank_content["objdata"]["PlantIncludeList"]:
                        if not x in planttypes_list:
                            message += f"\n{x} in seedbank not found in plant types"
                except: pass
                # Check PlantExcludeList
                try:
                    for x in seedbank_content["objdata"]["PlantExcludeList"]:
                        if not x in planttypes_list:
                            message += f"\n{x} in seedbank not found in plant types"
                except: pass
                        
            # Check initial conveyor belt
            elif x["objclass"] == "ConveyorSeedBankProperties":
                conveyorbelt_content = x
                for x in conveyorbelt_content["objdata"]["InitialPlantList"]:
                    if not x["PlantType"] in planttypes_list:
                        plant_name = x["PlantType"]
                        message += f"\n{plant_name} in conveyor belt not found in plant types"
                        
            # Check conveyor modifiers
            elif x["objclass"] == "ModifyConveyorWaveActionProps":
                conveyormodify_content = x["objdata"]
                
                for x in conveyormodify_content["Remove"]:
                    plant_name, plant_tag = get_name_and_tag(x["Type"])
                    if plant_tag == "PlantTypes":
                        if not plant_name in plantalias_list:
                            message += f"\n{plant_name} in conveyor modifier not found in plant types"
                    else:
                        message += f"\n{plant_name}@{plant_tag} has invalid tag"
                
                for x in conveyormodify_content["Add"]:
                    plant_name, plant_tag = get_name_and_tag(x["Type"])
                    if plant_tag == "PlantTypes":
                        if not plant_name in plantalias_list:
                            message += f"\n{plant_name} in conveyor modifier not found in plant types"
                    else:
                        message += f"\n{plant_name}@{plant_tag} has invalid tag"
    return message
        
        
def check_initialmodules(level_content, planttypes_list, griditemtypes_list, zombietypes_list):
    message = ""
    for module in level_content["objects"]:
        if "objclass" in module.keys():
            # Check GIs
            if module["objclass"] == "InitialGridItemProperties":
                for y in module["objdata"]["InitialGridItemPlacements"]:
                    if not y["TypeName"] in griditemtypes_list:
                        name = y["TypeName"]
                        module_name = module["aliases"][0]
                        message += f"\n{name} in {module_name} module not found in grid item types"
            # Check zombies
            elif module["objclass"] == "InitialZombieProperties":
                for y in module["objdata"]["InitialZombiePlacements"]:
                    if not y["TypeName"] in zombietypes_list:
                        name = y["TypeName"]
                        module_name = x["aliases"][0]
                        message += f"\n{name} in {module_name} module not found in zombie types"
            # Check plants
            elif module["objclass"] == "InitialPlantProperties":
                for y in module["objdata"]["InitialPlantPlacements"]:
                    if not y["TypeName"] in planttypes_list:
                        name = y["TypeName"]
                        module_name = x["aliases"][0]
                        message += f"\n{name} in {module_name} module not found in plant types"
            # Check SOS plants
            elif module["objclass"] == "ProtectThePlantChallengeProperties":
                for y in x["objdata"]["Plants"]:
                    if not y["PlantType"] in planttypes_list:
                        name = y["PlantType"]
                        module_name = x["aliases"][0]
                        message += f"\n{name} in {module_name} module not found in plant types"
    return message
        
def check_zombiewaves(level_content, zombietypes_list, zombiealias_list, customzombie_list):
    # Check all the waves for proper existing names
    message = ""
    
    already_found = []
    already_found_types = []
    for module in level_content["objects"]:
        if "objclass" in module.keys():
            # Check: normal waves, groundspawn, necromancy, storm, hamsterball spawn
            accept = ["SpawnZombiesJitteredWaveActionProps", "HamsterZombieSpawnerProps", "StormZombieSpawnerProps", "SpawnZombiesDelayedFromGridItemsProps", "SpawnZombiesFromGroundSpawnerProps", "SpawnZombiesFromGridItemSpawnerProps"]
            if module["objclass"] in accept:
                zombie_list = module["objdata"]["Zombies"]
                for x in zombie_list:
                    zombie_name, zombie_tag = get_name_and_tag(x["Type"])
                    
                    if zombie_tag == "ZombieTypes" and not zombie_name in zombiealias_list and not (zombie_name + "@" + zombie_tag) in already_found:
                        message += f"\n{zombie_name}@{zombie_tag} not found in zombie types"
                        already_found.append(zombie_name + "@" + zombie_tag)
                        already_found_types.append(zombie_name)
                        
                    elif (zombie_tag == "CurrentLevel" or zombie_tag == ".") and not zombie_name in customzombie_list and not (zombie_name + "@" + zombie_tag) in already_found:
                        message += f"\n{zombie_name}@{zombie_tag} not found in level"
                        already_found.append(zombie_name + "@" + zombie_tag)
                        already_found_types.append(zombie_name)
                        
                    elif not (zombie_tag == "ZombieTypes" or zombie_tag == "CurrentLevel" or zombie_tag == "."):
                        message += f"\n{zombie_name}@{zombie_tag} has invalid tag"
                        already_found.append(zombie_name + "@" + zombie_tag)
                        already_found_types.append(zombie_name)
                    
                    if "Row" in x.keys():
                        row_num = x["Row"]
                        try:
                            if int(row_num) < 1 or int(row_num) > 5:
                                message += f"\n{zombie_name}@{zombie_tag} is on {row_num}, which is invalid"
                        except:
                            message += f"\n{zombie_name}@{zombie_tag} is not on proper row number, is on {row_num}"
                        
            accept = ["ZombieRainSpawnerProps", "SpiderRainZombieSpawnerProps", "ParachuteRainZombieSpawnerProps"]
            if module["objclass"] in accept:
                zombie_name = module["objdata"]["SpiderZombieName"]
                if not zombie_name in zombietypes_list and not zombie_name in already_found_types:
                    message += f"\n{zombie_name} not found in zombie types"
                    already_found.append(zombie_name + "@ZombieTypes")
                    already_found_types.append(zombie_name)
            
            if module["objclass"] == "BeachStageEventZombieSpawnerProps":
                zombie_name = module["objdata"]["ZombieName"]
                if not zombie_name in zombietypes_list and not zombie_name in already_found_types:
                    message += f"\n{zombie_name} not found in zombie types"
                    already_found.append(zombie_name + "@ZombieTypes")
                    already_found_types.append(zombie_name)
            # Check escalation
            if module["objclass"] == "LevelEscalationModuleProperties":
                zombies_list = module["objdata"]["ZombiePool"]
                for x in zombies_list:
                    zombie_name, zombie_tag = get_name_and_tag(x)
                    if zombie_tag == "ZombieTypes" and not x in already_found and not zombie_name in zombietypes_list:
                        message += f"\n{zombie_name}@{zombie_tag} not found in zombie types"
                    elif not zombie_tag == "ZombieTypes":
                        message += f"\n{zombie_name}@{zombie_tag} has invalid tag"
    return message
        
def check_othermodules(level_content, obbmodule_list, levelmodule_list, planttypes_list, plantalias_list, griditemtypes_list, griditemalias_list, customgriditem_list, zombietypes_list, zombiealias_list, customzombie_list, dinotype_list):
    message = ""
    for module in level_content["objects"]:
        if "objclass" in module.keys():
            # Check potion spawn module
            if module["objclass"] == "ZombiePotionModuleProperties":
                gi_list = module["objdata"]["PotionTypes"]
                for x in gi_list:
                    if not x in griditemtypes_list:
                        message += f"\n{x} not found in grid item types"
            # Check Crazy Olaf module
            if module["objclass"] == "CrazyOlafTestProperties":
                try:
                    plant_list = module["objdata"]["PlantIncludelist"]
                    for x in plant_list:
                        if not x in planttypes_list:
                            message += f"\n{x} not found in plant types"
                except: pass
                try:
                    plant_list = module["objdata"]["PlantExcludelist"]
                    for x in plant_list:
                        if not x in planttypes_list:
                            message += f"\n{x} not found in plant types"
                except: pass
                try:
                    plant_list = module["objdata"]["PlantRequiredList"]
                    for x in plant_list:
                        if not x in planttypes_list:
                            message += f"\n{x} not found in plant types"
                except: pass
                del plant_list
                try:
                    dino_list = []
                    for x in module["objdata"]["CreatureList"]:
                        dino_list.append(x["CreatureTypeName"])
                    for x in dino_list:
                        if not x in dinotype_list:
                            message += f"\n{x} not found in creature types"
                except: pass
            # Check general zombie module for the 0.5 people that use it
            if module["objclass"] == "GeneralZombieModuleProperties":
                zombie_list = []
                for phase in module["objdata"]["Phases"]:
                    zombie_list.append(phase["ZombieType"])
                for x in zombie_list:
                    if not x in zombietypes_list:
                        message += f"\n{x} not found in zombie types"
            # Check FBC zomboss glaciar module
            if module["objclass"] == "GlacierModuleProperties":
                zombie_list = []
                for x in module["objdata"]["ZombieSpawnData"]:
                    for y in x["Entries"]:
                        if y["TypeName"]: zombie_list.append(y["TypeName"])
                for x in zombie_list:
                    if not x in zombietypes_list:
                        message += f"\n{x} not found in zombie types"
            # Check beghouled spawner
            if module["objclass"] == "BeghouledZombieSpawnerProperties":
                zombie_list = []
                for x in module["objdata"]["Stages"]:
                    for y in x["Types"]:
                        zombie_list.append(y["ZombieType"])
                for x in zombie_list:
                    if not x in zombietypes_list:
                        message += f"\n{x} not found in zombie types"
            # Check beghouled seedbank
            if module["objclass"] == "BeghouledSeedBankProperties":
                plant_list = []
                for x in module["objdata"]["PresetPlantList"]:
                    plant_list.append(x["PlantType"])
                for x in module["objdata"]["BeghouledUpgradeList"]:
                    plant_list.append(x)
                for x in plant_list:
                    if not x in planttypes_list:
                        message += f"\n{x} not found in plant types"
            # Check beghouled plants
            if module["objclass"] == "BeghouledPresetProperties":
                plant_list = []
                for x in module["objdata"]["InitialPlants"]:
                    plant_list.append(x)
                for x in module["objdata"]["UpgradeMap"]:
                    plant_list.append(x["BasePlant"])
                    plant_list.append(x["UpgradedPlant"])
                for x in plant_list:
                    if not x in planttypes_list:
                        message += f"\n{x} not found in plant types"
            # Check zomboss module
            if module["objclass"] == "ZombossBattleModuleProperties":
                zombie_name = module["objdata"]["ZombossMechType"]
                if not zombie_name in zombietypes_list:
                    message += f"\n{zombie_name} not found in zombie types"
            # Check vasebreaker module
            if module["objclass"] == "VaseBreakerPresetProperties":
                zombie_list = []
                plant_list = []
                for x in module["objdata"]["Vases"]:
                    if "ZombieTypeName" in x.keys():
                        zombie_list.append(x["ZombieTypeName"])
                    if "PlantTypeName" in x.keys():
                        plant_list.append(x["PlantTypeName"])
                for x in zombie_list:
                    if not x in zombietypes_list:
                        message += f"\n{x} not found in zombie types"
                for x in plant_list:
                    if not x in planttypes_list:
                        message += f"\n{x} not found in plant types"
            # Check endless vasebreaker module
            if module["objclass"] == "VaseBreakerEndlessProperties":
                zombie_list = []
                plant_list = []
                for stage in module["objdata"]["Stages"]:
                    for x in stage["PlantTypes"]:
                        plant_list.append(x["Type"])
                    try:
                        for x in stage["FixedZombieTypes"]:
                            zombie_list.append(x["Type"])
                    except: pass
                    try:
                        for x in stage["EscalatingZombieTypes"]:
                            zombie_list.append(x["Type"])
                    except: pass
                            
                for x in zombie_list:
                    if not x in zombietypes_list:
                        message += f"\n{x} not found in zombie types"
                for x in plant_list:
                    if not x in planttypes_list:
                        message += f"\n{x} not found in plant types"
            # Check defeat certain zombie challenge module
            if module["objclass"] == "DefeatZombiesOfTypeChallengeProps":
                zombie_list = []
                for x in module["objdata"]["TypesToKill"]["List"]:
                    zombie_list.append(x)
                for x in zombie_list:
                    if not x in zombietypes_list:
                        message += f"\n{x} not found in zombie types"
            # Check rift swap module
            if module["objclass"] == "LevelDifficultyScalingModuleProperties":
                zombie_list = []
                for swap in module["objdata"]["ZombieLevelSwaps"]:
                    for x in swap["Swaps"]:
                        zombie_name, zombie_tag = get_name_and_tag(x["From"])
                        if not (zombie_name + "@" + zombie_tag) in zombie_list:
                            zombie_list.append(zombie_name + "@" + zombie_tag)
                        for y in x["To"]:
                            zombie_name, zombie_tag = get_name_and_tag(y)
                            if not (zombie_name + "@" + zombie_tag) in zombie_list:
                                zombie_list.append(zombie_name + "@" + zombie_tag)
                for x in zombie_list:
                    if x.endswith("@ZombieTypes"):
                        if not (x.split("@"))[0] in zombiealias_list:
                            message += f"\n{x} not found in zombie types"
                    if x.endswith("@.") or x.endswith("@CurrentLevel"):
                        if not (x.split("@"))[0] in customzombie_list:
                            message += f"\n{x} not found in current level"
            # Check GI spawn module
            if module["objclass"] == "SpawnGravestonesWaveActionProps":
                gi_list = []
                for x in module["objdata"]["GravestonePool"]:
                    gi_list.append(get_name_and_tag(x["Type"])[0] + "@" + get_name_and_tag(x["Type"])[1])
                for x in gi_list:
                    if x.endswith("@GridItemTypes"):
                        if not x.split("@")[0] in griditemalias_list:
                            message += f"\n{x} not found in grid item types"
                    elif x.endswith("@.") or x.endswith("@CurrentLevel"):
                        if not x.split("@")[0] in customgriditem_list:
                            message += f"\n{x} not found in level"
                    else:
                        message += f"\n{x} has invalid tag"
            # Check portal spawn module
            if module["objclass"] == "SpawnModernPortalsWaveActionProps":
                suffix = module["objdata"]["PortalType"]
                if not "zombieportal_" + suffix in griditemtypes_list:
                    message += f"\nzombieportal_{suffix} not found in grid item types"
            # Check dino spawn
            if module["objclass"] == "DinoWaveActionProps":
                dino_name = "dino" + module["objdata"]["DinoType"]
                if not dino_name in dinotype_list:
                    message += f"\n{dino_name} not found in creature types"
            # Check endless wave setup
            if module["objclass"] == "DangerRoomJitteredWaveGenerator":
                zombie_list = []
                for x in module["objdata"]["ZombiePool"]:
                    zombie_name, zombie_tag = get_name_and_tag(x)
                    zombie_list.append(zombie_name + "@" + zombie_tag)
                for x in zombie_list:
                    if not x.split("@")[0] in zombiealias_list:
                        message += f"\n{x} not found in zombie types"
            # Check endless portal spawn
            if module["objclass"] == "DangerRoomModernDesigner":
                gi_list = []
                for x in module["objdata"]["PortalTypePool"]:
                    gi_list.append("zombieportal_" + x["Value"])
                for x in gi_list:
                    if not x in griditemtypes_list:
                        message += f"\n{x} not found in grid item types"
            # Check endless necromancy spawn
            if module["objclass"] == "DangerRoomDarkEventGenerator":
                try: name = module["objdata"]["GravestoneType"]
                except: pass
                if not name in griditemtypes_list:
                    message += f"\n{name} not found in grid item types"
                try: name = module["objdata"]["SunGravestoneType"]
                except: pass
                if not name in griditemtypes_list:
                    message += f"\n{name} not found in grid item types"
                try: name = module["objdata"]["PlantfoodGravestoneType"]
                except: pass
                if not name in griditemtypes_list:
                    message += f"\n{name} not found in grid item types"
                try: name = module["objdata"]["SpawnZombieType"]
                except: pass
                if not name in zombietypes_list:
                    message += f"\n{name} not found in zombie types"
            # Check endless low tide spawn
            if module["objclass"] == "DangerRoomBeachTideChanger":
                name = module["objdata"]["BasicLowTideZombieType"]
                if not name in zombietypes_list:
                    message += f"\n{name} not found in zombie types"
                zombie_list = []
                for x in module["objdata"]["SpecialLowTideZombieTypes"]:
                    zombie_list.append(x)
                for x in zombie_list:
                    if not x in zombietypes_list:
                        message += f"\n{x} not found in zombie types"
    return message
                


# I totally did not steal this from somewhere yes
def get_name_and_tag(s):
    """
        Get name and tag from a string with format "RTID(X@Y)"
    """
    return s.replace("RTID(", "").replace(")", "").replace("$", "").split("@")

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


        
        

