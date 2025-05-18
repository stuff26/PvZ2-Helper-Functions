import os
import json
from colorama import init, Fore
init()
import universal_functions as uf
import itertools
import xmltodict
import re
from readchar import readchar
from copy import deepcopy


FILE_TYPE_TO_CHECK = ("label", "sprite")
DEFAULT_ERROR_FILE = "errors.txt"
should_give_safe_error = False

FULL_ERROR_MESSAGE = ""
def main():
    print(f"{Fore.LIGHTBLUE_EX}Enter the {Fore.GREEN}XFL {Fore.LIGHTBLUE_EX}or individual symbol you want to scan")
    user_input_path = uf.ask_for_directory(accept_any=True, look_for_files=("DOMDocument.xml",))
    print(f"{Fore.LIGHTBLUE_EX}Processing...\n")
    
    # If individual symbol is given
    if os.path.isfile(user_input_path):
        file_contents = uf.open_xml_file(user_input_path)
        layer_list = file_contents["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"]
        symbol = os.path.basename(os.path.normpath(user_input_path))
        check_symbol(layer_list, symbol, is_file=True)
        
    # If XFL is given
    else:
        # Get list of symbols
        symbol_list = get_symbol_list(os.path.join(user_input_path, "DOMDocument.xml"))
        
        # Loop through each symbol
        for symbol in symbol_list:
            symbol_path = os.path.join(user_input_path, "library", symbol)
            file_contents = uf.open_xml_file(symbol_path)
        
            # Get list of layers from data
            layer_list = file_contents["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]
            if layer_list == None: # Ignore if no layers are found
                continue
            layer_list = layer_list.get("DOMLayer", {})
            if isinstance(layer_list, dict):
                layer_list = [layer_list]
            check_symbol(layer_list, symbol)
    
    # Print error
    global FULL_ERROR_MESSAGE
    if FULL_ERROR_MESSAGE == "":
        print(f"{Fore.LIGHTBLUE_EX}No errors found")
        return
    print(FULL_ERROR_MESSAGE)
    
def get_symbol_list(DOMDocument_dir):
    # Get DOMDocument
    DOMDocument = uf.open_xml_file(DOMDocument_dir)["DOMDocument"]
    
    # Get list of label and sprite symbols
    symbol_list = []
    for symbol in DOMDocument["symbols"]["Include"]:
        symbol_name = symbol.get("@href", False) # Get full symbol name
        
        if symbol_name:
            symbol_list.append(symbol_name)
            
    # Return
    return symbol_list

def check_symbol(layer_list, symbol, is_file=False):
        global FULL_ERROR_MESSAGE
        symbol_errors = ""
        
        # Loop through each layer
        for layer in layer_list:
            # Set up dictionary of errors
            total_errors = {
                "has_multiple_symbols_in_keyframe": [],
                "has_tweens": [],
                "multiple_image_layers": {},
                "improper_emptied_frames": [],
                "symbol_or_bitmap_in_wrong_type": {},
            }
            try:
                if isinstance(layer.get("frames", {}).get("DOMFrame", False), dict): # Ignore layers with only one key frame
                    layer["frames"]["DOMFrame"] = [layer["frames"]["DOMFrame"]]
                if layer.get("@layerType", False) == "folder": # Ignore folders
                    continue
            except TypeError: # Fail safe
                continue
            layer_name = layer.get("@name", "unknown")
            
            total_errors["has_multiple_symbols_in_keyframe"] = check_multiple_symbols_in_keyframe(layer)
            total_errors["has_tweens"] = check_tweens(layer)
            
            # If mulitple symbols, skip remaining checks to avoid errors
            if total_errors["has_multiple_symbols_in_keyframe"] == None:
                total_errors["multiple_image_layers"] = check_multiple_image_layers(layer)
                total_errors["improper_emptied_frames"] = check_emptied_frames(layer)
                if not is_file:
                    total_errors["symbol_or_bitmap_in_wrong_type"] = check_mismatch_symbol_or_bitmap(layer, symbol)
            
            error_message = get_error_message(total_errors, layer_name)
            if error_message:
                symbol_errors += error_message
            
            
        if symbol_errors != "":
            symbol_errors = f"\n\n{Fore.LIGHTBLUE_EX}Found errors in symbol {Fore.GREEN}{symbol}\n\n" + symbol_errors
            FULL_ERROR_MESSAGE += symbol_errors
    
def get_error_message(total_errors, layer_name):
    errors = []
    temp_message = ""
    add_message = lambda message : errors.append(message)
    
    # Check multiple image layers
    if total_errors["has_multiple_symbols_in_keyframe"] != None:
        temp_message = f"\t\t{Fore.LIGHTBLUE_EX}Found multiple symbols/bitmaps in single frames on range of frames\n\t\t\t{Fore.YELLOW}{total_errors['has_multiple_symbols_in_keyframe']}"
        add_message(temp_message)
    if total_errors["has_tweens"] != []:
        temp_message = f"\t\tFound frames with unconverted tweens\n\t\t\t{Fore.YELLOW}{total_errors['has_tweens']}"
        add_message(temp_message)
        
    else:
        if total_errors["multiple_image_layers"] != None:
            temp_message = f"\t\t{Fore.LIGHTBLUE_EX}Found multiple different symbols used\n\t\tIntended image symbol: {Fore.GREEN}{total_errors['multiple_image_layers']['intended_image_name']}"
            for error in total_errors["multiple_image_layers"]["found_errors"]:
                temp_message += f"\n\t\t\t{Fore.LIGHTBLUE_EX}Found {Fore.GREEN}{error} {Fore.LIGHTBLUE_EX}on range of frames: {Fore.YELLOW}{total_errors['multiple_image_layers']['found_errors'][error]}"
            add_message(temp_message)
            
        if total_errors["improper_emptied_frames"] != []:
            if errors != []: temp_message = "\n"
            temp_message += f"\t\t{Fore.LIGHTBLUE_EX}Found keyframes with gaps of empty keyframes on range of frames, separate these frames into another layer\n\t\t\t{Fore.YELLOW}{total_errors['improper_emptied_frames']}"
            add_message(temp_message)
        
        
    if errors:
        message = f"\t{Fore.LIGHTBLUE_EX}Layer {Fore.GREEN}{layer_name} {Fore.LIGHTBLUE_EX}has an error\n"
        for different_error in errors:
            message += different_error
        message += "\n"
        return message
    return None

def check_multiple_symbols_in_keyframe(layer):
    # Setup
    frame_list = frame_list = layer["frames"]["DOMFrame"]
    errors_list = []
    
    for frame in frame_list:
        frame_num = int(frame["@index"]) + 1
        elements = frame.get("elements", False)
        if not elements:
            continue # If empty keyframe, ignore
        
        elements_key_list = list(elements.keys())
        if "DOMSymbolInstance" in elements_key_list and "DOMBitmapInstance" in elements_key_list:
            errors_list.append(frame_num) # If bitmap and symbol found
            continue
        
        check_if_list = lambda key_to_check : isinstance(elements.get(key_to_check, False), list)
        if check_if_list("DOMSymbolInstance"): # If multiple symbols found
            errors_list.append(frame_num)
            continue
        if check_if_list("DOMBitmapInstance"): # If multiple bitmaps found
            errors_list.append(frame_num)
            continue
    
    
    # Process any errors found
    if errors_list != []:
        errors_list = to_ranges(errors_list)
        return errors_list
    else:
        return None
        
        
        
def check_multiple_image_layers(layer):
            
        # Get list of frames
        frame_list = layer["frames"]["DOMFrame"]
        
        # Set up to go through frame
        first = True
        errors_list = {
            "intended_image_name": "",
            "found_errors": {},
        }
        intended_image_name = ""
        
        # Loop through each frame
        for frame in frame_list:
            # Get image name and frame number
            image_name = frame.get("elements", None)
            if image_name == None:
                continue
            try:
                image_name = image_name["DOMSymbolInstance"]["@libraryItemName"]
            except KeyError:
                return None
            frame_num = int(frame["@index"]) + 1
            
            # If first, save intended image name
            if first:
                intended_image_name = image_name
                errors_list["intended_image_name"] = intended_image_name
                first = False
                continue
            
            # If not, check if image name is same as intended_image_name
            elif image_name != intended_image_name:
                if image_name not in errors_list["found_errors"]:
                    errors_list["found_errors"][image_name] = []
                errors_list["found_errors"][image_name].append(frame_num)
            
        # Process any errors found
        if errors_list["found_errors"] != {}:
            for error in errors_list["found_errors"]:
                errors_list["found_errors"][error] = to_ranges(errors_list["found_errors"][error])
            return errors_list
        else:
            return None
        
        
def check_emptied_frames(layer):
    # Setup
    new_layer = deepcopy(layer)
    frame_list = new_layer["frames"]["DOMFrame"]
    found_errors = []
    
    # Lambda functions
    check_elements = lambda frame : frame.get("elements", False)
    remove_instance = lambda frame : frame_list.pop(frame_list.index(frame))
    
    # Find first instance of a key frame
    for frame in frame_list:
        # Remove instance of frame
        remove_instance(frame)
        
        # If a keyframe is found, update status and break from loop
        if check_elements(frame):
            break
    
    # Find any potential keyframes
    for frame in frame_list.copy():
        # Remove instance of frame
        remove_instance(frame)
        
        # If last keyframe is found, update status and break from loop
        if not check_elements(frame):
            break
    
    # Find any keyframes
    for frame in frame_list.copy():
        # Remove instance of frame and get current index
        current_index = frame_list.index(frame)
        remove_instance(frame)
        
        # If any more keyframes are found, update status and add to errors
        if check_elements(frame):
            frame_num = int(frame["@index"]) + 1
            found_errors.append(frame_num)
            
    found_errors = to_ranges(found_errors)
    return found_errors

def check_mismatch_symbol_or_bitmap(layer, symbol):
    
    # Check if image
    is_image = False
    if symbol.startswith("image/"):
        is_image = True
    
    errors = {
        "is_image": is_image,
        "has_more_than_one_frame": False,
        "has_symbol": False,
        }
    frame_list = layer["frames"]["DOMFrame"]
    if isinstance(frame_list, list):
        errors["has_more_than_one_frame"] = True
    else:
        frame_list = [frame_list]
    


    for frame in frame_list:
        if frame and frame["elements"] and "DOMSymbolInstance" in frame["elements"]:
            errors["has_symbol"] = True
            
    return errors


def check_tweens(layer):
    frame_list = layer["frames"]["DOMFrame"]

    found_errors = []
    for frame in frame_list:
        if frame.get("@tweenType", False):
            found_errors.append(int(frame["@index"]) + 1)
    
    #found_errors = to_ranges(found_errors)
    return found_errors
            

# Convert range of different values to 
def to_ranges(iterable):
    return list(to_ranges2(iterable))

def to_ranges2(iterable):
    iterable = sorted(set(iterable))
    for key, group in itertools.groupby(enumerate(iterable),
                                        lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]
    return iterable

if __name__ == "__main__":
    main()
    input(f"{Fore.LIGHTMAGENTA_EX}Complete")

