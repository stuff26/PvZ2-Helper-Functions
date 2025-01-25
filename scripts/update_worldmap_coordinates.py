import json
from colorama import Fore, init
from readchar import readchar
from os import path
import universal_functions as uf
init()

should_give_safe_error = True
def main():
    # Ask for file to change
    print(f"{Fore.LIGHTBLUE_EX}Enter the worldmap file you want to edit")
    worldmap_file, worldmap_file_dir = uf.get_json_file_contents(default_directory=0, return_directory=True, silent=False)
    
    # Ask for how much to change
    change_x = ask_for_num("X")
    change_y = ask_for_num("Y", repeat=True)
    
    # Change coordinates
    worldmap_file = change_coordinates(change_x, "x", worldmap_file)
    worldmap_file = change_coordinates(change_y, "y", worldmap_file)
    
    # Ask user if they want to overwrite changes to save to new file
    uf.write_to_file(worldmap_file, worldmap_file_dir, is_json=True)

def ask_for_num(type, repeat=False):
    print(f"{Fore.LIGHTBLUE_EX}How much do you want to increase the {type} coordinate?")
    if not repeat: print("(Enter negative numbers to decrease the coordinate)")
    while 1:
        try:
            user_input = float(uf.better_user_input())
        except ValueError:
            print(f"{Fore.MAGENTA}Enter only a number")
            continue
        return user_input

def change_coordinates(change_amount, coordinate_type, worldmap_contents):
    for map_piece in worldmap_contents["objects"][0]["objdata"]["m_mapPieces"]:
        coordinate = float(map_piece["m_position"][coordinate_type])
        map_piece["m_position"][coordinate_type] = change_amount + coordinate
    for map_piece in worldmap_contents["objects"][0]["objdata"]["m_eventList"]:
        coordinate = float(map_piece["m_position"][coordinate_type])
        map_piece["m_position"][coordinate_type] = change_amount + coordinate
    return worldmap_contents
    
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
