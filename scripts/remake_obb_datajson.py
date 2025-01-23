import json
import os
from colorama import init, Fore
from readchar import readchar
import universal_functions as uf
init()

def main():
    # Open data.json
    try:
        data_directory = "data.json"
        data = uf.obtain_json_file_contents(data_directory, silent=True)
        if isinstance(data, type(None)): raise FileNotFoundError
        file_list = os.listdir("packet")
    except FileNotFoundError:
        print(f"{Fore.LIGHTBLUE_EX}Enter the {Fore.GREEN}data.json {Fore.LIGHTBLUE_EX}you want to edit (drag the file here)")
        data, data_directory = uf.get_json_file_contents(return_directory=True)
        print(f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}packet {Fore.LIGHTBLUE_EX}folder you want to run through")
        while True:
            packet_dir = uf.better_user_input(ask_directory=True)
            if not os.path.exists(packet_dir):
                print(f"{Fore.LIGHTMAGENTA_EX}ERROR: directory does not exist, input again")
                continue
            elif not os.path.isdir(packet_dir):
                print(f"{Fore.LIGHTMAGENTA_EX}ERROR: directory is not a folder, input again")
                continue
            file_list = os.listdir(packet_dir)
            break
    
    # Empty packet
    data["packet"].clear()
    
    # Check if file ends with .scg, then add to data
    for file_name in file_list:
        if file_name.endswith(".scg"):
            data["packet"].append(file_name[:-4]) # Remove file ending

    # Open data.json to overwrite it
    uf.write_to_file(data, data_directory, is_json=True)
        
if __name__ == "__main__":
    should_give_safe_error = True
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
