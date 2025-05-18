try:
    import sys
    from colorama import init, Fore
    init()
    from json import loads
    from importlib import import_module
    from readchar import readchar
    import os
    from time import time
except Exception as e:
    print(f"ERROR: {e}")
    input()


def main():
    # Grab configurations for functions
    with open(open_in_exe("function_config.json"), "r", encoding="utf-8") as file:
        functions = loads(file.read())
    
    # Introduction
    print(f"{Fore.YELLOW}PvZ2 Helper Functions by stuff26")
    print(f"Version {Fore.GREEN}{functions['version']}")
    print(f"{Fore.YELLOW}Intended for usage with files for Sen 4.0 by Haruma\n")
    
    available_functions = {}
    function_num = 1
    # Print out each available function
    for function_title in functions['functions']:
        new_section(function_title)
        for function in functions['functions'][function_title]:
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
    function_module = import_module(function_name)
    # Grab function
    function_to_call = getattr(function_module, "main")
    print(f"{Fore.LIGHTBLUE_EX}Executing {Fore.GREEN}{function_name}{Fore.LIGHTBLUE_EX}...")
    display_dashed_line()
    print()
    
    # Call function
    
    while True:
        try:
            pre_time = time()
            function_to_call()
            function_time = time() - pre_time
            
            display_dashed_line()
            print(f"\n{Fore.LIGHTMAGENTA_EX}Process completed in {round(function_time, 4)} seconds")
            print("(press any button to continue)")
            readchar()
            break

        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            display_dashed_line()
            print()
            print(f"{Fore.LIGHTBLUE_EX}Would you like to do retry this function (Y/N)")
            should_exit = False
            while True:
                answer = readchar().upper()
                if answer == "Y":
                    print(f"{Fore.YELLOW}{answer}")
                    display_dashed_line()
                    print()
                    should_exit = True
                    break
                elif answer == "N":
                    break
            if should_exit:
                display_dashed_line()
                print(f"\n{Fore.LIGHTMAGENTA_EX}Process completed")
                print("(press any button to continue)")
                readchar()
                break
    
    
def open_in_exe(relative_path):
    global is_function_compiler
    is_function_compiler = True
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
    print(f"{Fore.RED}---------------------")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Processed ended early by user (press any key to exit)")
        readchar()
    except Exception as e:
        print(f"\n{Fore.MAGENTA}ERROR: {e}")
        readchar()