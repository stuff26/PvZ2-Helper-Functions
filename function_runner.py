try:
    import sys
    from colorama import init, Fore
    init()
    import json
    import importlib
    from readchar import readchar
    import os
    import time
except Exception as e:
    print(f"ERROR: {e}")
    input()

is_function_compiler = False

def main():
    # Grab configurations for functions
    with open(open_in_exe("function_config.json"), "r", encoding="utf-8") as file:
        functions = json.loads(file.read())
    
    # Introduction
    print(f"{Fore.YELLOW}PvZ2 Helper Functions by stuff26")
    print(f"Version {Fore.GREEN}1.0")
    print(f"{Fore.YELLOW}Intended for usage with files for Sen 4.0 by Haruma")
    
    available_functions = {}
    function_num = 1
    # Print out each available function
    for function_title in functions:
        new_section(function_title)
        for function in functions[function_title]:
            available_functions[str(function_num)] = function["function_name"]
            display_option(function, function_num)
            function_num += 1
    display_dashed_line()
    
    # Ask for input
    while True:
        user_input = input(f"{Fore.RED}>>> {Fore.YELLOW}")
        # If option is not available
        if user_input not in available_functions.keys():
            print(f"{Fore.MAGENTA}Please select a valid option")
            continue
        # If all checks pass, break from loop
        break
    
    # Run function
    for x in available_functions:
        if user_input == x:
            function_name = available_functions[x]
            break
        
    if not is_function_compiler: sys.path.append("./scripts")
    # Turn function into object
    function_module = importlib.import_module(function_name)
    # Grab function
    function_to_call = getattr(function_module, "main")
    print(f"{Fore.LIGHTBLUE_EX}Executing {Fore.GREEN}{function_name}{Fore.LIGHTBLUE_EX}...")
    display_dashed_line()
    print()
    
    # Call function
    while True:
        try:
            pre_time = time.time()
            function_to_call()
            function_time = time.time() - pre_time
            break
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            display_dashed_line()
            print()
            print(f"{Fore.LIGHTBLUE_EX}Would you like to do retry this function (Y/N)")
            while True:
                answer = readchar().upper()
                if answer == "Y":
                    print(f"{Fore.YELLOW}{answer}")
                    display_dashed_line()
                    print()
                    continue
                elif answer == "N":
                    break
    
    # Exit
    display_dashed_line()
    print(f"\n{Fore.LIGHTMAGENTA_EX}Process completed in {round(function_time, 4)} seconds")
    print("(press any button to continue)")
    readchar()
    
    
def open_in_exe(relative_path):
    #Get the absolute path to the resource, whether running as a script or as a bundled executable.
    if hasattr(sys, '_MEIPASS'):  # Running as a PyInstaller bundle
        base_path = sys._MEIPASS
    else:  # Running as a script
        base_path = os.path.abspath(".")
        is_function_compiler = False
    return os.path.join(base_path, relative_path)
    
def display_option(option_details, function_num):
    name = option_details["name"]
    details = option_details["details"]
    function_input = option_details["input"]
    function_output = option_details["output"]
    print(f"{Fore.LIGHTMAGENTA_EX}[{function_num}]: {Fore.LIGHTGREEN_EX}{name}")
    print(f"{Fore.GREEN}- Function:  {Fore.LIGHTBLUE_EX}{details}")
    print(f"{Fore.GREEN}- Input:     {Fore.LIGHTBLUE_EX}{function_input}")
    print(f"{Fore.GREEN}- Output:    {Fore.LIGHTBLUE_EX}{function_output}\n")
    
def new_section(name):
    display_dashed_line()
    print(f"> {Fore.YELLOW}{name}")
    display_dashed_line()
    print()
    
def display_dashed_line():
    print(f"{Fore.RED}----------------")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Processed ended early by user (press any key to exit)")
        readchar()
    except Exception as e:
        print(f"\n{Fore.MAGENTA}ERROR: {e}")
        readchar()