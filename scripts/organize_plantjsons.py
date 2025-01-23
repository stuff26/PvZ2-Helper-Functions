import json
from os import path
from sys import exit
def main():
    # Get files
    planttypes_contents = open_file("PLANTTYPES.json")
    plantprops_contents = open_file("PLANTPROPERTIES.json")
    plantlevels_contents = open_file("PLANTLEVELS.json")
    plant_almanacdata_contents = open_file("PLANTALMANACDATA.json")
    propertysheets_contents = open_file("PROPERTYSHEETS.json")
        
    # Find list of plant typenames
    for object in propertysheets_contents["objects"]:
        if object["objclass"] == "GamePropertySheet":
            plant_list = object["objdata"]["PlantTypeOrder"]
            break

        
    # Make list of plant types and props
    planttypes_list = []
    for planttype in planttypes_contents["objects"]:
        planttypes_list.append(planttype)
    plantprops_list = []
    for plantprops in plantprops_contents["objects"]:
        plantprops_list.append(plantprops)

    # Make new list of plant types according to order in property sheets
    new_planttypes_list = []
    # Loop through list of plant typenames
    for plantname in plant_list:
        # Loop through list of plant types
        for planttype in planttypes_list:
            # If names match, add to new_planttypes_list and remove from old one
            if plantname == planttype["objdata"]["TypeName"]:
                new_planttypes_list.append(planttype)
                planttypes_list.remove(planttype)
                break
    
    # Readd remaining plant types
    first = True
    for internal_planttype in planttypes_list:
        if first:
            to_add = {"#": "PLANT TYPES NOT IN PROPERTYSHEETS START HERE"}
            to_add.update(internal_planttype)
            internal_planttype = to_add
            del to_add
            first = False
        new_planttypes_list.append(internal_planttype)
    del first

    # Make dictionary of plant types with corresponding props
    plant_types_and_props = {}
    for plant_type in new_planttypes_list:
        try:
            typename = plant_type["objdata"]["TypeName"]
            props = get_name(plant_type["objdata"]["Properties"])
            plant_types_and_props[typename] = props
        except: continue

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
        try:
            if plantprop["objclass"] == "PlantAnimRigPropertySheet":
                animrig_list.append(plantprop)
            else:
                new_plantprops_list.append(plantprop)
        except: pass

    # Add animrig to list depending on where it is called for
    for plantprop in new_plantprops_list:
        # Get animrig name
        try:
            plant_animrig = get_name(plantprop["objdata"]["AnimRigProps"])
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
            del to_add
            break

    # Organize plant levels
    plantlevels_list = plantlevels_contents["objects"]
    new_plantlevels_list = []
    for plantname in plant_list:
        for plantlevel in plantlevels_list:
            try:
                if plantname == plantlevel["objdata"]["Typename"]:
                    new_plantlevels_list.append(plantlevel)
                    plantlevels_list.remove(plantlevel)
            except:
                try:
                    if plantname == plantlevel["objdata"]["TypeName"]:
                        new_plantlevels_list.append(plantlevel)
                        plantlevels_list.remove(plantlevel)
                except: pass
    # Add remaining levels
    to_remove = plantlevels_list.copy()
    for plantlevel in to_remove:
        new_plantlevels_list.append(plantlevel)
        plantlevels_list.remove(plantlevel)
        
    # Organize plant almanac data
    plantalmanac_list = plant_almanacdata_contents["objects"]
    new_plantalmanac_list = []
    to_remove = plantalmanac_list.copy()
    for plantname in plant_list:
        for plantalmanac in to_remove:
            try:
                if plantname == plantalmanac["objdata"]["TypeName"]:
                    new_plantalmanac_list.append(plantalmanac)
                    plantalmanac_list.remove(plantalmanac)
            except: pass
    # Add remaining almanac data
    to_remove = plantalmanac_list.copy()
    for plantalmanac in to_remove:
        new_plantalmanac_list.append(plantalmanac)
        plantalmanac_list.remove(plantalmanac)


    # Write results to file
    with open("planttypes_results.json", "w", encoding="utf-8") as file:
        planttypes_contents["objects"] = new_planttypes_list
        json.dump(planttypes_contents, file, indent=4)
    with open("plantprops_results.json", "w", encoding="utf-8") as file:
        plantprops_contents["objects"] = new_plantprops_list
        json.dump(plantprops_contents, file, indent=4)
    with open("plantlevels_results.json", "w", encoding="utf-8") as file:
        plantlevels_contents["objects"] = new_plantlevels_list
        json.dump(plantlevels_contents, file, indent=4)
    with open("plantalmanacdata_results.json", "w", encoding="utf-8") as file:
        plant_almanacdata_contents["objects"] = new_plantalmanac_list
        json.dump(plant_almanacdata_contents, file, indent=4)
        
    print("Would you like to overwrite current packages with new files? (Please make a backup to be safe) (Y/N)")
    while 1:
        user_input = readchar().upper()
        if user_input == "Y":
            print("Y")
            with open("./packages/planttypes.json", "w", encoding="utf-8") as file:
                planttypes_contents["objects"] = new_planttypes_list
                json.dump(planttypes_contents, file, indent=4)
            with open("./packages/plantproperties.json", "w", encoding="utf-8") as file:
                plantprops_contents["objects"] = new_plantprops_list
                json.dump(plantprops_contents, file, indent=4)
            with open("./packages/plantlevels.json", "w", encoding="utf-8") as file:
                plantlevels_contents["objects"] = new_plantlevels_list
                json.dump(plantlevels_contents, file, indent=4)
            with open("./packages/plantalmanacdata.json", "w", encoding="utf-8") as file:
                plant_almanacdata_contents["objects"] = new_plantalmanac_list
                json.dump(plant_almanacdata_contents, file, indent=4)
                break
        if user_input == "N":
            print("N")
            break
    

# i am not a little theif
def get_name(s):
    """
        Get name and tag from a string with format "RTID(X@Y)"
    """
    return s.replace("RTID(", "").replace(")", "").replace("$", "").split("@")[0]
        
def open_file(file_name):
    try:
        with open(path.join("./packages", file_name), "r", encoding="utf-8") as file:
            return json.loads(file.read())
    except:
        print(f"{file_name} not found, ensure this is in the right directory and all rtons are converted to jsons")
        input()
        exit()

if __name__ == "__main__":
    main()
    print("Complete (press any key to continue)")
    readchar()
