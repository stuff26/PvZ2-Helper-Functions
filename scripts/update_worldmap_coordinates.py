from colorama import Fore, init
import universal_functions as uf
init()

def main():
    # Ask for file to change
    print(f"{Fore.LIGHTBLUE_EX}Enter the worldmap file you want to edit")
    worldmap_file, worldmap_file_dir = uf.get_json_file_contents(default_directory=0, return_directory=True, silent=False)
    
    # Ask for how much to change
    change_x:float = ask_for_num("X")
    change_y:float = ask_for_num("Y", repeat=True)
    
    # Change coordinates
    change_coordinates(change_x, "x", worldmap_file)
    change_coordinates(change_y, "y", worldmap_file)
    
    # Overwrite file
    uf.write_to_file(worldmap_file, worldmap_file_dir, is_json=True)

def ask_for_num(type:str, repeat:bool=False) -> float:
    print(f"{Fore.LIGHTBLUE_EX}How much do you want to increase the {type} coordinate?")
    if not repeat: print("(Enter negative numbers to decrease the coordinate)")

    while True:
        try:
            user_input = float(uf.better_user_input())
        except ValueError:
            print(f"{Fore.MAGENTA}Enter only a number")
            continue
        return user_input

def change_coordinates(change_amount:float, coordinate_type:str, worldmap_contents:dict):
    for map_piece in worldmap_contents["objects"][0]["objdata"]["m_mapPieces"]:
        coordinate = float(map_piece["m_position"][coordinate_type])
        map_piece["m_position"][coordinate_type] = change_amount + coordinate
    for map_piece in worldmap_contents["objects"][0]["objdata"]["m_eventList"]:
        coordinate = float(map_piece["m_position"][coordinate_type])
        map_piece["m_position"][coordinate_type] = change_amount + coordinate
    
if __name__ == "__main__":
    main()
    input("Complete")
