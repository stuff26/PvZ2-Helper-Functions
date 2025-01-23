import json
from colorama import Fore, init
from readchar import readchar
from os import path
init()


def main():
    # Ask for file to change
    file_to_edit = ask_for_file()
    
    # Open file
    with open(file_to_edit, "r", encoding="utf-8") as file:
        worldmap_contents = json.loads(file.read())
    print(f"{Fore.GREEN}{file_to_edit}{Fore.LIGHTBLUE_EX} opened")
    
    # Ask for how much to change
    change_x = ask_for_num("X")
    change_y = ask_for_num("Y", repeat=True)
    
    # Change coordinates
    worldmap_contents = change_coordinates(change_x, "x", worldmap_contents)
    worldmap_contents = change_coordinates(change_y, "y", worldmap_contents)
    print(f"{Fore.LIGHTBLUE_EX}Coordinates updated")
    
    # Ask user if they want to overwrite changes to save to new file
    option = ask_for_action(file_to_edit)
    
    # If 1 is answered, overwrite to new file
    if option == "1":
        file_to_edit = ask_for_writeto_file()
        
    # Write to file
    with open(file_to_edit, "w", encoding="utf-8") as file:
        json.dump(worldmap_contents, file, indent=4)
        
    # Inform user process is done
    print(f"{Fore.GREEN}{file_to_edit}{Fore.LIGHTBLUE_EX} updated")
    
def ask_for_file():
    print(f"{Fore.LIGHTBLUE_EX}Enter the file you want to edit, or just press ENTER to check {Fore.GREEN}worldmap.json")
    while 1:
        done = True
        # User input
        file_to_edit = input(f"{Fore.RED}>>> {Fore.YELLOW}")
        # If nothing is inputted, default to worldmap.json
        if file_to_edit == "":
            file_to_edit = "worldmap.json"
        # If no ending is added, add .json to it
        elif not "." in file_to_edit:
            file_to_edit += ".json"
        # If file is not valid JSON, ask user for input again
        try:
            with open(file_to_edit, "r", encoding="utf-8") as file:
                dummy = json.loads(file.read())
                if not dummy["objects"][0]["objclass"] == "WorldData":
                    raise KeyError
        except json.decoder.JSONDecodeError:
            print(f"{Fore.GREEN}{file_to_edit} {Fore.MAGENTA}is not a valid JSON, input again")
            continue
        except TypeError:
            print(f"{Fore.GREEN}{file_to_edit} {Fore.MAGENTA}is not a world map file, input again")
            continue
        except FileNotFoundError:
            print(f"{Fore.GREEN}{file_to_edit} {Fore.MAGENTA}not found, input again")
            continue
        except KeyError:
            print(f"{Fore.GREEN}{file_to_edit} {Fore.MAGENTA}is not a world map file, input again")
            continue
        # If a file that isn't a JSON file is inputted, double check with user
        if "." in file_to_edit and not file_to_edit.endswith(".json"):
            print(f"{Fore.GREEN}{file_to_edit} {Fore.LIGHTBLUE_EX}is not a JSON file, continue anyway? {Fore.MAGENTA}(Y/N)")
            while 1:
                user_input = input(f"{Fore.RED}>>> {Fore.YELLOW}").upper()
                if user_input == "Y":
                    break
                elif user_input == "N":
                    done = False
                    print(f"{Fore.LIGHTBLUE_EX}Enter the file you want to edit, or just press ENTER to check {Fore.GREEN}worldmap.json")
                    break
                else:
                    print(f"{Fore.MAGENTA}Enter only Y or N")
                    continue
        if done: break
    return file_to_edit

def ask_for_num(type, repeat=False):
    print(f"{Fore.LIGHTBLUE_EX}How much do you want to increase the {type} coordinate?")
    if not repeat: print("(Enter negative numbers to decrease the coordinate)")
    while 1:
        try:
            user_input = float(input(f"{Fore.RED}>>> {Fore.YELLOW}"))
        except ValueError:
            print(f"{Fore.MAGENTA}Enter only a number")
            continue
        break
    return user_input

def change_coordinates(change_amount, coordinate_type, worldmap_contents):
    for map_piece in worldmap_contents["objects"][0]["objdata"]["m_mapPieces"]:
        coordinate = float(map_piece["m_position"][coordinate_type])
        map_piece["m_position"][coordinate_type] = change_amount + coordinate
    for map_piece in worldmap_contents["objects"][0]["objdata"]["m_eventList"]:
        coordinate = float(map_piece["m_position"][coordinate_type])
        map_piece["m_position"][coordinate_type] = change_amount + coordinate
    return worldmap_contents


def ask_for_action(file_to_edit):
    print(f"{Fore.LIGHTBLUE_EX}What would you like to do with the new map data?")
    print(f"{Fore.LIGHTMAGENTA_EX}[1]: {Fore.LIGHTGREEN_EX}Overwrite to new file")
    print(f"{Fore.LIGHTMAGENTA_EX}[2]: {Fore.LIGHTGREEN_EX}Overwrite {file_to_edit}")
    while 1:
        answer = readchar()
        if answer == "1" or answer == "2":
            print(answer)
            break
    return answer

def ask_for_writeto_file():
    print(f"{Fore.LIGHTBLUE_EX}What file name do you want?")
    while 1:
        done = True
        file_to_write_to = input(f"{Fore.RED}>>> {Fore.YELLOW}")
        if not "." in file_to_write_to:
            file_to_write_to += ".json"
        if path.exists(file_to_write_to):
            print(f"{Fore.GREEN}{file_to_write_to} {Fore.LIGHTBLUE_EX}already exists, would you like to overwrite it? {Fore.LIGHTMAGENTA_EX}(Y/N)")
            while 1:
                answer = readchar().upper()
                if answer == "Y":
                    break
                elif answer == "N":
                    print(f"{Fore.LIGHTBLUE_EX}What file name do you want?")
                    done = False
                    break
        if done: break
    return file_to_write_to
    
if __name__ == "__main__":
    try:
        main()
        print(f"{Fore.LIGHTMAGENTA_EX}Complete (press any button to continue)")
        readchar()
    except KeyboardInterrupt:
        print(f"\n{Fore.LIGHTMAGENTA_EX}Processed ended early by user (ENTER to exit)")
        input()
