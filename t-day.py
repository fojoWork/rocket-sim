import time
import os


def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

def loading_screen():
  whitespace = 10
  for i in range(10):
    print("[" + "#"*i, "-"*whitespace + "]", end="\r")
    whitespace -= 1
    time.sleep(0.5)
  print("[############]\n --Launched--")

LBS_TO_KG = 0.453592
LBS_FORCE_TO_NEWTONS = 4.44822
MILES_TO_METERS = 1609.34
DEFAULT_THRUST_LBS = 20000.0
DEFAULT_ISP = 300.0
DEFAULT_TARGET_DISTANCE_MILES = 10.0

clear_screen()
inputted_thrust = input("Please enter your desired pounds of thrust <lbs>: ").strip()
inputted_isp = input("What do you want your ISP value to be?: ").strip()
inputted_set_distance = input("What should the set distance be? <miles> If you would like to not set distance, leave blank <Default is 10 miles>: ").strip()

INPUTTED_THRUST_LBS = float(inputted_thrust) if inputted_thrust else DEFAULT_THRUST_LBS
INPUTTED_ISP = float(inputted_isp) if inputted_isp else DEFAULT_ISP
TARGET_DISTANCE_MILES = float(inputted_set_distance) if inputted_set_distance else DEFAULT_TARGET_DISTANCE_MILES

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

running = False


while True:
    clear_screen()
    print("="*33)
    print(f"Current Inputted Thrust: {INPUTTED_THRUST_LBS}lbs")
    print(f"Current ISP: {INPUTTED_ISP}")
    print(f"Current target distance: {TARGET_DISTANCE_MILES}")
    print("-"*5, "Launch rocket?", "-"*5)
    print("="*33)
    
    do_launch = input("\n")
    
    if 'y' in do_launch.lower() or 'yes' in do_launch.lower():
      loading_screen()
      running = True
      time.sleep(2)
      break

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
        velocity += acceleration * delta_time
        alt += velocity * delta_time

    current_time += delta_time

    fuel_pct = (fuel_mass / INITIAL_FUEL) * 100 # fuel percentage

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
