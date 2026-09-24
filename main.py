import os
import importlib

scripts = {
    "Script 1 - Resource Collection": "resource_collector",
    "Script 2 - Attack Overlay": "overlay_attack",
    "Script 3 - Auto Skip": "pre_attack_resources",
    "Exit": None
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear()
    print("=== Script Launcher ===\n")
    for i, name in enumerate(scripts.keys(), start=1):
        print(f"{i}. {name}")

def run_selected_script(choice):
    selected = list(scripts.items())[choice - 1]
    name, module_name = selected
    if module_name:
        print(f"\nRunning: script.{module_name}...\n")
        try:
            mod = importlib.import_module(f"scripts.{module_name}")
            if hasattr(mod, "main"):
                mod.main()
            else:
                print(f"Module '{module_name}' does not have a main() function.")
        except Exception as e:
            print(f"Error running script.{module_name}: {e}")
    else:
        print("Exiting.")
        exit(0)

def main():
    while True:
        show_menu()
        try:
            choice = int(input("\nEnter choice number: "))
            if 1 <= choice <= len(scripts):
                run_selected_script(choice)
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Enter a number.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()