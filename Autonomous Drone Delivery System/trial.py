import collections
import collections.abc
import dronekit_sitl
collections.MutableMapping = collections.abc.MutableMapping
from dronekit import connect, LocationGlobalRelative, VehicleMode
import time
import socket
import math

sitl = dronekit_sitl.start_default()
conn = sitl.connection_string()
drone = connect(conn, wait_ready=True)
#drone = connect("127.0.0.1:14550", wait_ready=True)
print("Autopilot Firmware version: %s" % drone.version)
print("Global Location: %s" % drone.location.global_frame)
print("Global Location (relative altitude): %s" % drone.location.global_relative_frame)
print("Local Location: %s" % drone.location.local_frame)
print("Attitude: %s" % drone.attitude) #roll, pitch, yaw
print("Velocity: %s" % drone.velocity)
print("Last Heartbeat: %s" % drone.last_heartbeat)
print("Is Armable?: %s" % drone.is_armable)
print("System status: %s" % drone.system_status.state)
print("Mode: %s" % drone.mode.name)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not drone.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    drone.mode = VehicleMode("STABILIZE")
    drone.armed = True

    # Confirm vehicle armed before attempting to take off
    while not drone.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    drone.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", drone.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if drone.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

arm_and_takeoff(20)





