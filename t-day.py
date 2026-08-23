import time
import threading as th

# We need threading so that we can perform snapshots for gathering Distance over Time data, 

inputted_thrust = float(input("Please enter your desired pounds of thrust <lbs>: "))
inputted_isp = float(input("What do you want your ISP value to be?: "))
inputted_set_distance = float(input("What should the set distance be? <miles>: "))

isp = inputted_isp
altitude = 0.0 #feet
time_ = 0.0
dot = inputted_set_distance * time_
speed = 17500.0
expected_time = inputted_set_distance / speed
fuel = 5000 #lbs
weight = fuel + 1000 #lbs
gravity = -9.8
thrust = inputted_thrust / (weight * gravity)
fuel_consumption = thrust / (inputted_isp * 9.8)
acceleration = (thrust / weight) - gravity
velocity = 0 + ((acceleration ** 2) * fuel_consumption)

def start_snapshot(current_altitude):  #time and current altitude
  start_time = time.time()
  return start_time, current_altitude

def end_snapshot(current_altitude):
  end_time = time.time()
  return end_time, current_altitude

start, start_distance = start_snapshot
end, end_distance = end_snapshot

is_launched = False

def launch():
  global is_launched
  is_launched = True

  starting_snapshot_thread = th.Thread(target=start_snapshot)
  starting_snapshot_thread.start()
  
  
while is_launched:
  #rocket logic
  altitude += thrust
  
  pass
  




