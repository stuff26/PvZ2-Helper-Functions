import json
import os
from sys import exit
import universal_functions as uf
from colorama import Fore, init
from readchar import readchar
init()


should_give_safe_error = False
FILE_LIST = ("PLANTTYPES.json", "PLANTPROPERTIES.json", "PLANTLEVELS.json", "PLANTALMANACDATA.json", "PROPERTYSHEETS.json",)

def main():
    print(f"{Fore.LIGHTBLUE_EX}Drag the {Fore.GREEN}packages {Fore.LIGHTBLUE_EX}folder you want to organize the plant files of here")
    input_directory = uf.ask_for_directory(is_file=False, look_for_files=FILE_LIST)
    
    # Get files
    def open_file(file):
        file_path = os.path.join(input_directory, file)
        return uf.obtain_json_file_contents(file_path, silent=True)
    
    planttypes_contents = open_file("PLANTTYPES.json")
    plantprops_contents = open_file("PLANTPROPERTIES.json")
    plantlevels_contents = open_file("PLANTLEVELS.json")
    plantalmanacdata_contents = open_file("PLANTALMANACDATA.json")
    propertysheets_contents = open_file("PROPERTYSHEETS.json")
    
    # Make backups for later
    plantfile_backups = {
        "PLANTTYPES_BACKUP.json": planttypes_contents.copy(),
        "PLANTPROPERTIES_BACKUP.json": plantprops_contents.copy(),
        "PLANTLEVELS_BACKUP.json": plantlevels_contents.copy(),
        "PLANTALMANACDATA_BACKUP.json": plantalmanacdata_contents.copy()
        }
        
    # Find list of plant typenames
    plant_list = []
    for object_inst in propertysheets_contents["objects"]:
        if object_inst["objclass"] == "GamePropertySheet":
            plant_list = object_inst["objdata"]["PlantTypeOrder"]
            break
        
    planttypes_contents["objects"] = organize_planttypes(planttypes_contents["objects"], plant_list)

    # Make dictionary of plant types with corresponding props
    plant_types_and_props = {}
    for plant_type in planttypes_contents["objects"]:
        try:
            typename = plant_type["objdata"]["TypeName"]
            props = uf.get_name_and_tag(plant_type["objdata"]["Properties"], "name")
            plant_types_and_props[typename] = props
        except: continue
    
    # Organize plant props
    plantprops_contents["objects"] = organize_plantprops(plantprops_contents["objects"], plant_types_and_props)

    # Organize plant levels
    plantlevels_contents["objects"] = organize_plantlevels(plantlevels_contents["objects"], plant_list)
    
    # Organize plant almanac data
    plantalmanacdata_contents["objects"] = organize_plantalmanacdata(plantalmanacdata_contents["objects"], plant_list)

    # Write results to file
    file_writeto_dict = {
        "PLANTTYPES.json": planttypes_contents,
        "PLANTPROPERTIES.json": plantprops_contents,
        "PLANTLEVELS.json": plantlevels_contents,
        "PLANTALMANACDATA.json": plantalmanacdata_contents
        }
    for file_name in file_writeto_dict:
        uf.write_to_file(file_writeto_dict[file_name], os.path.join(input_directory, file_name), is_json=True)
        
    # Write backups
    for file_name in plantfile_backups:
        uf.write_to_file(plantfile_backups[file_name], os.path.join(os.path.normpath(input_directory + os.sep + os.pardir), file_name), is_json=True)
        
    print(f"{Fore.LIGHTBLUE_EX}All plant files successfully organized. Backup files are written in the parent folder of {Fore.GREEN}packages")

def organize_planttypes(planttypes_contents, plant_list):
    # Make new list of plant types according to order in property sheets
    new_planttypes_list = []
    # Loop through list of plant typenames
    for plantname in plant_list:
        # Loop through list of plant types
        for planttype in planttypes_contents:
            # If names match, add to new_planttypes_list and remove from old one
            if plantname == planttype["objdata"]["TypeName"]:
                new_planttypes_list.append(planttype)
                planttypes_contents.remove(planttype)
                break
    
    # Readd remaining plant types
    first = True
    for internal_planttype in planttypes_contents:
        if first:
            to_add = {"#": "PLANT TYPES NOT IN PROPERTYSHEETS START HERE"}
            to_add.update(internal_planttype)
            internal_planttype = to_add
            first = False
        new_planttypes_list.append(internal_planttype)
    
    # Return new planttypes
    return new_planttypes_list

def organize_plantprops(plantprops_list, plant_types_and_props):
    # Organize plant props
    new_plantprops_list = []
    # Loop through dictionary
    for X in plant_types_and_props:
        # Loop through props list
        for plantprop in plantprops_list:
            # If props name and alias of props are same, add to new list
            try:
                if plant_types_and_props[X] in plantprop["aliases"]:
                    new_plantprops_list.append(plantprop)
                    plantprops_list.remove(plantprop)
                    break
            except: pass

    # Add unused props, don't add anim rig props
    animrig_list = []
    for plantprop in plantprops_list:
        if plantprop.get("objclass", False) == "PlantAnimRigPropertySheet":
            animrig_list.append(plantprop)
        else:
            new_plantprops_list.append(plantprop)

    # Add animrig to list depending on where it is called for
    for plantprop in new_plantprops_list:
        # Get animrig name
        try:
            plant_animrig = uf.get_name_and_tag(plantprop["objdata"]["AnimRigProps"], "name")
            # Loop through animrig data to find match
            for animrig in animrig_list:
                if plant_animrig in animrig["aliases"]:
                    plantprop_index = new_plantprops_list.index(plantprop)
                    new_plantprops_list.insert(plantprop_index+1, animrig)
                    animrig_list.remove(animrig)
            
        except: pass

    # Add template to top of plant props if it exists
    for plantprop in new_plantprops_list:
        if "PlantPropertySheetTemplate" in plantprop["aliases"]:
            to_add = [plantprop]
            new_plantprops_list.remove(plantprop)
            to_add.extend(new_plantprops_list)
            new_plantprops_list = to_add
            break
    
    # Return
    return new_plantprops_list

def organize_plantlevels(plantlevels_list, plant_list):
    new_plantlevels_list = []
    for plantname in plant_list:
        for plantlevel in plantlevels_list:
            if plantname == plantlevel.get("objdata", {}).get("Typename", False) or plantname == plantlevel.get("objdata", {}).get("TypeName", False):
                new_plantlevels_list.append(plantlevel)
                plantlevels_list.remove(plantlevel)
                
    # Add remaining levels
    to_remove = plantlevels_list.copy()
    for plantlevel in to_remove:
        new_plantlevels_list.append(plantlevel)
        plantlevels_list.remove(plantlevel)
    
    # Return
    return new_plantlevels_list

def organize_plantalmanacdata(plantalmanac_list, plant_list):
    new_plantalmanac_list = []
    to_remove = plantalmanac_list.copy()
    for plantname in plant_list:
        for plantalmanac in to_remove:
            if plantname == plantalmanac.get("objdata", {}).get("TypeName", False):
                new_plantalmanac_list.append(plantalmanac)
                plantalmanac_list.remove(plantalmanac)
    # Add remaining almanac data
    to_remove = plantalmanac_list.copy()
    for plantalmanac in to_remove:
        new_plantalmanac_list.append(plantalmanac)
        plantalmanac_list.remove(plantalmanac)
    
    # Return
    return new_plantalmanac_list
    

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
