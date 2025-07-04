import universal_functions as uf
import os
from colorama import Fore, init
init()

def main():
    # Ask for directory from user
    print(f"{Fore.LIGHTBLUE_EX}Enter the {Fore.GREEN}XFL {Fore.LIGHTBLUE_EX}you want to edit")
    input_path:str = uf.ask_for_directory(accept_any=True, look_for_files=("DOMDocument.xml",))

    # Ask how much to offset
    print(f"{Fore.LIGHTBLUE_EX}How much do you want to offset the X coordinate by? (or enter nothing to not move it)")
    x_offset:float = ask_for_number()
    print(f"{Fore.LIGHTBLUE_EX}How much do you want to offset the Y coordinate by?")
    y_offset:float = ask_for_number()

    # If nothing is provided, skip everything
    if x_offset == 0 and y_offset == 0: return

    # XFL is provided
    if not os.path.isfile(input_path):
        symbol_list:list = get_symbol_list(os.path.join(input_path, "DOMDocument.xml"))
        for symbol in symbol_list:
            symbol_path = os.path.join(input_path, "library", symbol)
            symbol_file = uf.open_xml_file(symbol_path)
            symbol_file = offset_anim(symbol_file, x_offset, y_offset)
            uf.write_to_file(symbol_file, symbol_path, is_xml=True)
    
    # Individual symbol is provided
    else:
        symbol_file = uf.open_xml_file(input_path)
        symbol_file = offset_anim(symbol_file, x_offset, y_offset)
        uf.write_to_file(symbol_file, input_path, is_xml=True)

# Asks the user how much to offset by
def ask_for_number() -> float:
    while True:
        # Input
        answer = uf.better_user_input()

        # If nothing is entered, default to 0
        if answer == "": 
            answer = 0

        else:
            # Attempt to convert answer into a float, give the user an error if the input is not a number
            try:
                answer = float(answer)
            except ValueError:
                print("Enter a number")
                continue
        # Return
        return answer

# Gets a list of symbols that are part of the xfl
def get_symbol_list(DOMDocument_dir:str) -> list[str]:
    # Get DOMDocument
    DOMDocument = uf.open_xml_file(DOMDocument_dir)["DOMDocument"]
    
    # Get list of label and sprite symbols
    symbol_list = []
    for symbol in DOMDocument["symbols"]["Include"]:
        symbol_name:str = symbol.get("@href", False) # Get full symbol name
        if symbol_name.startswith("label/") or symbol_name == "main_sprite.xml":
            symbol_list.append(symbol_name)
            
    # Return
    return symbol_list

# Change all the cordinates in the symbol
def offset_anim(symbol_file:dict, x_offset:float, y_offset:float) -> dict:
    # Get a list of layers and loop through it
    layer_list = uf.fix_layer_or_frame_list(symbol_file["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"],to_layer=True)
    for layer in layer_list:

        # Get a list of frames and loop through it
        frames = uf.fix_layer_or_frame_list(layer["frames"]["DOMFrame"], to_layer=True)
        for frame in frames:

            # Get a list of elements and loop through it
            elements = frame["elements"]
            if elements == None: continue
            for element_type in elements:

                element = uf.fix_layer_or_frame_list(elements[element_type], to_layer=True)
                for element2 in element:

                    # Change coordinates
                    x_cord = float(element2["matrix"]["Matrix"].get("@tx", 0))
                    element2["matrix"]["Matrix"]["@tx"] = str(x_cord + x_offset)
                    y_cord = float(element2["matrix"]["Matrix"].get("@ty", 0))
                    element2["matrix"]["Matrix"]["@ty"] = str(y_cord + y_offset)
    
    # Return
    return symbol_file



if __name__ == "__main__":
    main()
    input("Complete")