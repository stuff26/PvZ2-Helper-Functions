import json
import copy
from readchar import readchar
import sys
import os
from colorama import init, Fore
import universal_functions as uf
init()


default_templates_file = "templates_base.json"
default_templates_copy_file = "template_copies.json"
def main():
    # Ask user for option on what to do
    user_option = opener_prompt()
    print(f"{Fore.YELLOW}{user_option}")
    
    # If chosen to make a template base
    if user_option == "2":
        templates_base_name = "templates_base.json"
        templates_base_contents = uf.obtain_json_file_contents(uf.open_in_exe(templates_base_name, is_main=(__name__=="__main__")), silent=False)
        uf.write_to_file(templates_base_contents, default_templates_file, is_json=True)
        print(f"{Fore.LIGHTBLUE_EX}Created {Fore.GREEN}{default_templates_file} {Fore.LIGHTBLUE_EX}in same directory as this executible, read through to know how to use it \nRerun this when you want to make the templates")
        return
    
    # Otherwise, continue with the code
    template_types = ("zombies", "griditems",)
    
    # Ask for file to copy from
    print(f"{Fore.LIGHTBLUE_EX}Enter the templates file you want to duplicate, or enter nothing to read {Fore.GREEN}{default_templates_file}")
    while True:
        templates, templates_dir = uf.get_json_file_contents(default_directory=default_templates_file, return_directory=True, silent=False)
        for template_type in template_types:
            if template_type not in templates:
                print(f"{Fore.LIGHTMAGENTA_EX}ERROR: File is not a template base file")
                break
        else: break # If went through without errors
            
    
    # Ask for amount of templates
    amount_of_templates = ask_for_amount_of_templates()
    
    # Duplicate templates
    for template_type in template_types:
        templates[template_type] = copy_templates(templates, template_type, amount_of_templates)
    
    # Prompt user to write to what file then write to it
    print(f"{Fore.LIGHTBLUE_EX}Successfully duplicated templates")
    print(f"{Fore.LIGHTBLUE_EX}Where do you wish to write the new templates to, or enter nothing to write to {Fore.GREEN}{default_templates_copy_file}")
    
    while True:
        file_to_write_to = uf.better_user_input(ask_directory=True)
        if file_to_write_to == "":
            file_to_write_to = default_templates_copy_file
        if "." not in file_to_write_to:
            file_to_write_to += ".json"
            
        try:
            uf.write_to_file(templates, file_to_write_to, is_json=True, parent_dir=templates_dir)
            break
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
            continue
    print(f"{Fore.LIGHTBLUE_EX}Wrote templates to {Fore.GREEN}{file_to_write_to}")
    
def opener_prompt():
    # Introduction
    print(f"{Fore.LIGHTBLUE_EX}Select an option:")
    print(f"{Fore.LIGHTMAGENTA_EX}[1]: {Fore.LIGHTGREEN_EX}Make copies using an existing templates file")
    print(f"{Fore.LIGHTMAGENTA_EX}[2]: {Fore.LIGHTGREEN_EX}Make templates file base")
    print(f"{Fore.LIGHTBLUE_EX}(select 2 if you want to know how to use this function)")
    
    # Return user answer
    while True:
        answer = readchar().upper()
        if answer == "1":
            return "1"
        if answer == "2":
            return "2"

def ask_for_copying_file(default_templates_file, template_types):
    print(f"{Fore.LIGHTBLUE_EX}What file do you want to copy from, or enter nothing to copy from {Fore.GREEN}{default_templates_file}")
    while True:
        file_contents = uf.get_json_file_contents(default_directory=default_templates_file)
        for template_type in template_types:
            if template_type not in file_contents.keys():
                print(f"{Fore.LIGHTMAGENTA_EX}File is not a template file, enter directory again")
                continue
        return file_contents
    
def ask_for_amount_of_templates():
    print(f"{Fore.LIGHTBLUE_EX}How many templates do you want?")
    while True:
        try:
            answer = int(input(f"{Fore.RED}>>> {Fore.YELLOW}"))
            print()
            return answer
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}:")
        
def copy_templates(templates, copying_type, amount_to_copy):
    temp_templates = []
    # Go through each template in wanted type
    for template in templates[copying_type]:
        # Make a copy of each template with specified number
        for template_num in range(1, amount_to_copy+1):
            temp_template = copy.deepcopy(template)
            
            # Make new aliases
            temp_template["aliases"] = [
                alias.replace("*", f"{template_num}") for alias in temp_template["aliases"]
            ]
            
            # Replace typename
            temp_template["objdata"]["TypeName"] = temp_template["objdata"]["TypeName"].replace("*", f"{template_num}")
            
            # Replace props name
            props_name, props_tag = uf.get_name_and_tag(temp_template["objdata"]["Properties"], "both")
            props_name = props_name.replace("*", f"{template_num}")
            temp_template["objdata"]["Properties"] = f"RTID({props_name}@{props_tag})"
            
            # Remove comments
            for x in copy.deepcopy(temp_template):
                if x.startswith("#comment"):
                    temp_template.pop(x)
            
            # Add to new templates list
            temp_templates.append(temp_template)
            
        print(f"{Fore.LIGHTBLUE_EX}Added {template['objdata']['TypeName']}")
        
    print(f"{Fore.LIGHTBLUE_EX}Finished adding {copying_type}\n")
            
    # Return new templates
    return temp_templates

def ask_file_to_write_to(default_template_copy_file):
    print(f"{Fore.LIGHTBLUE_EX}What file do you want to write to, or enter nothing to write to {Fore.GREEN}{default_template_copy_file}")
    while True:
        file_to_write_to = input(f"{Fore.RED}>>> {Fore.YELLOW}")
        
        if not file_to_write_to:
            return default_template_copy_file
        
        # Add .json ending if not specified in user input
        if "." not in file_to_write_to:
            file_to_write_to += ".json"
            
        # Prompt user if file already exists
        break_out_of_loop = True
        if os.path.exists(file_to_write_to):
            print(f"{Fore.GREEN}{file_to_write_to} {Fore.LIGHTBLUE_EX}already exists, do you want to overwrite it?")
            while True:
                answer = readchar().upper()
                if answer == "Y":
                    break
                if answer == "N":
                    break_out_of_loop = False
                    print(f"{Fore.LIGHTBLUE_EX}What file do you want to write to, or enter nothing to write to {Fore.GREEN}{default_template_copy_file}")
                    break
        if break_out_of_loop: return file_to_write_to
    
if __name__ == "__main__":
    try:
        main()
        print(f"{Fore.LIGHTMAGENTA_EX}Complete (press any key to continue)")
        readchar()
    except Exception as e:
        print(f"{Fore.LIGHTMAGENTA_EX}ERROR: {e}")
        readchar()