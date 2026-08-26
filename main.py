import time
import os
import json
from enum import IntEnum
import sys


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def loading_screen():
    whitespace = 50
    for i in range(50):
        print("  [" + "#" * i, "-" * whitespace + "]", end="\r")
        whitespace -= 1
        time.sleep(0.1)
    print("\r[" + "#"*50 + "]\n --Launched--")

# Reads presets file and then prompts user by letting them select or create a custom preset. Guess we arent using Enums :-(
def read_presets():
    try:
        with open('presets.json', 'r') as file:
            data = json.load(file)
    except Exception:
        data = {}

    if 'ships' in data:
        ships_val = data['ships']
        if isinstance(ships_val, dict):
            presets = ships_val
        elif isinstance(ships_val, list) and len(ships_val) > 0 and isinstance(ships_val[0], dict):
            presets = ships_val[0]
        else:
            presets = {}
    else:
        data = {"ships": data}
        presets = data["ships"]

    names = list(presets.keys())

    print("Please choose from a preset, or enter 0 to delete / 1 for custom values.")
    print("0. Delete a preset")
    print("1. Custom (enter values manually)")
    
    # Start preset listing at 2 so 0 and 1 remain distinct
    for i, name in enumerate(names, start=2):
        print(f"{i}. {name}")
    print(f"{len(names) + 2}. Exit (Quit Process)")

    while True:
        choice = input("\nEnter selection number: ").strip()
        if not choice:
            print("No selection made — using defaults.")
            return DEFAULT_THRUST_LBS, DEFAULT_ISP, DEFAULT_TARGET_DISTANCE_MILES

        try:
            idx = int(choice)
        except ValueError:
            print("Invalid selection. Please enter a valid number.")
            continue

        # Option 0: Delete
        if idx == 0:
            if not names:
                print("No presets available to delete.")
                continue

            user_input = input("Enter the number of the rocket to delete: ").strip()
            try:
                selected_num = int(user_input)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            # Preset numbers start at 2, so index in names list is selected_num - 2
            selected_index = selected_num - 2
            if 0 <= selected_index < len(names):
                selected_for_death = names[selected_index]
                protected_presets = ["Andromeda-7", "Artemis 3", "Soyuz 2"]
                
                if selected_for_death in protected_presets:
                    print(f"Cannot delete protected preset: {selected_for_death}")
                    return read_presets()

                presets.pop(selected_for_death, None)
                try:
                    with open('presets.json', 'w') as file:
                        json.dump(data, file, indent=2)
                    print(f"Successfully deleted preset: {selected_for_death}")
                except Exception as e:
                    print(f"Error saving changes: {e}")
                return read_presets()
            else:
                print("Invalid preset number for deletion.")
                continue

        # Option 1: Custom Preset
        if idx == 1:
            inputted_preset_name = input("Please enter your new preset name: ").strip()
            inputted_thrust = input("Please enter your desired pounds of thrust <lbs>: ").strip()
            inputted_isp = input("What do you want your ISP value to be?: ").strip()
            inputted_set_distance = input("What should the set distance be? <miles> [Default: 10]: ").strip(" ,")
            inputted_fuel_amount = input("Please enter your rocket's fuel amount in lbs: ").strip()
            inputted_dry_mass = input("Please input your dry mass in lbs: ").strip()

            INPUTTED_THRUST_LBS = float(inputted_thrust) if inputted_thrust else DEFAULT_THRUST_LBS
            INPUTTED_ISP = float(inputted_isp) if inputted_isp else DEFAULT_ISP
            TARGET_DISTANCE_MILES = float(inputted_set_distance) if inputted_set_distance else DEFAULT_TARGET_DISTANCE_MILES
            INPUTTED_FUEL_AMOUNT = float(inputted_fuel_amount) if inputted_fuel_amount else 5000
            INPUTTED_DRY_MASS = float(inputted_dry_mass) if inputted_dry_mass else 1000

            data['ships'][inputted_preset_name] = [
                {
                    "thrust": INPUTTED_THRUST_LBS,
                    "isp": INPUTTED_ISP,
                    "fuel": INPUTTED_FUEL_AMOUNT,
                    "dry_mass": INPUTTED_DRY_MASS,
                    "distance": TARGET_DISTANCE_MILES
                }
            ]

            try:
                with open('presets.json', 'w') as file:
                    json.dump(data, file, indent=2)
            except Exception as e:
                print(f"Error saving preset: {e}")

            print(f"Created and selected: {inputted_preset_name}")
            return INPUTTED_THRUST_LBS, INPUTTED_ISP, TARGET_DISTANCE_MILES

        # Options 2 to len(names) + 1: Existing Presets
        if 2 <= idx <= len(names) + 1:
            preset_name = names[idx - 2]
            preset_entry = presets.get(preset_name)
            
            if not preset_entry:
                print("Preset data missing, try another selection.")
                continue

            vals = preset_entry[0] if isinstance(preset_entry, list) else preset_entry
            INPUTTED_THRUST_LBS = float(vals.get('thrust', DEFAULT_THRUST_LBS))
            INPUTTED_ISP = float(vals.get('isp', DEFAULT_ISP))
            TARGET_DISTANCE_MILES = float(vals.get('distance', DEFAULT_TARGET_DISTANCE_MILES))

            print(f"You selected: {preset_name}")
            return INPUTTED_THRUST_LBS, INPUTTED_ISP, TARGET_DISTANCE_MILES

        # Exit Option
        if idx == len(names) + 2:
            sys.exit()

        print("Invalid selection. Try again.")



LBS_TO_KG = 0.453592
LBS_FORCE_TO_NEWTONS = 4.44822
MILES_TO_METERS = 1609.34
DEFAULT_THRUST_LBS = 20000.0
DEFAULT_ISP = 300.0
DEFAULT_TARGET_DISTANCE_MILES = 10.0


# get_user_inputs merged into read_presets


def prompt_launch(INPUTTED_THRUST_LBS, INPUTTED_ISP, TARGET_DISTANCE_MILES):
    while True:
        clear_screen()
        print("=" * 33)
        print(f"Current Inputted Thrust: {INPUTTED_THRUST_LBS}lbs")
        print(f"Current ISP: {INPUTTED_ISP}")
        print(f"Current target distance: {TARGET_DISTANCE_MILES}")
        print("-" * 5, "Launch rocket?", "-" * 5)
        print("=" * 33)

        do_launch = input("\n ~$: ")

        if 'y' in do_launch.lower() or 'yes' in do_launch.lower():
            loading_screen()
            time.sleep(2)
            return True
        else:
            clear_screen()
            read_presets()


def run_simulation(INPUTTED_THRUST_LBS, INPUTTED_ISP, TARGET_DISTANCE_MILES):
    GRAVITY = 9.80665
    DRY_MASS = 1000 * LBS_TO_KG
    INITIAL_FUEL = 5000 * LBS_TO_KG
    fuel_mass = INITIAL_FUEL
    thrust_n = INPUTTED_THRUST_LBS * LBS_FORCE_TO_NEWTONS
    target_distance_m = TARGET_DISTANCE_MILES * MILES_TO_METERS
    mass_flow_rate = thrust_n / (INPUTTED_ISP * GRAVITY)

    alt = 0.0
    velocity = 0.0
    current_time = 0.0
    delta_time = 0.05

    running = True

    while running:
        clear_screen()
        total_mass = DRY_MASS + fuel_mass

        if fuel_mass > 0:
            current_thrust = thrust_n
            fuel_mass -= mass_flow_rate * delta_time
            if fuel_mass < 0:
                fuel_mass = 0.0
            engine_status = "ACTIVE"
        else:
            current_thrust = 0.0
            engine_status = "MECO (CUTOFF)"

        net_force = current_thrust - (total_mass * GRAVITY)
        acceleration = net_force / total_mass

        if alt <= 0.0 and acceleration < 0.0:
            acceleration = 0.0
            velocity = 0.0
            alt = 0.0
        else:
            velocity += (acceleration * delta_time) ** 2
            alt += velocity * delta_time

        current_time += delta_time

        fuel_pct = (fuel_mass / INITIAL_FUEL) * 100

        print(
            "================ TELEMETRY DASHBOARD ================\n"
            f"Mission Elapsed Time : T+{current_time:06.2f}s\n"
            f"Engine Status        : {engine_status}\n"
            f"Altitude             : {alt:10.2f} m ({(alt / MILES_TO_METERS):.2f} mi)\n"
            f"Velocity             : {velocity:10.2f} m/s\n"
            f"Acceleration         : {acceleration:10.2f} m/s²\n"
            f"Propellant Remaining : {fuel_mass:8.1f} kg ({fuel_pct:5.1f}%)\n"
            f"Vehicle Total Mass   : {total_mass:8.1f} kg\n"
            "=====================================================",
            flush=True,
        )

        if target_distance_m and alt >= target_distance_m:
            print(f"\n ALERT [!] - Target distance reached: {TARGET_DISTANCE_MILES:.2f} miles achieved")
            running = False

        if alt < 0.0 and current_time > 1.0:
            print(f"\n ALERT [!] - Rocket has touched down.", flush=True)
            running = False

        time.sleep(0.05)

# Assembles all main code blocks into functions for modularity
def main():
    clear_screen()
    INPUTTED_THRUST_LBS, INPUTTED_ISP, TARGET_DISTANCE_MILES = read_presets()
    prompt_launch(INPUTTED_THRUST_LBS, INPUTTED_ISP, TARGET_DISTANCE_MILES)
    run_simulation(INPUTTED_THRUST_LBS, INPUTTED_ISP, TARGET_DISTANCE_MILES)


if __name__ == '__main__':
    main()
