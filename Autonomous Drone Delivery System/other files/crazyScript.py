import logging
import sys
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)

position_estimate = [0,0]
DEFAULT_HEIGHT = 0.1 #meters
BOX_LIMIT = 0.5

def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']

def param_deck_flow(_, value_str):
    value = int(value_str)
    print(value)
    if value:
        deck_attached_event.set()
        print('Deck is attached!')
    else:
        print('Deck is NOT attached!')


#Asynchronous logging

def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

#add logging config to the logging framework of the cf
def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(5)
    logconf.stop()


"""MOVEMENT COMMANDS"""
"""
mc.up(meters)
mc.down(meters)
mc.forward(meters)
mc.back(meters)
mc.turn_left(degrees)
mc.turn_right(degrees)
"""


#fly up, wait 3 secs, fly back down
def take_off_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(2)
        #mc.turn_right(180)
        #time.sleep(3)
        #mc.turn_right(180)
        #time.sleep(2)
        mc.stop()

#Go forward .2m, turn, and go back .2m
def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        mc.forward(0.2)
        time.sleep(1)
        mc.turn_left(180) #degrees
        time.sleep(1)
        mc.forward(0.2)
        time.sleep(1)
        mc.stop()

#move around inside box limit
def move_box_limit(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        while(1):
            #cf will start moving back and forth until crtl+c
            time.sleep(0.1)
            if position_estimate[0] > BOX_LIMIT:
                mc.start_back()
            elif position_estimate[0] < -BOX_LIMIT:
                mc.start_forward()
            time.sleep(1)

def bounce_box_limit(scf):
    body_x_cmd = 0.2
    body_y_cmd = 0.1
    max_vel = 0.2
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        while(1):
            if position_estimate[0] > BOX_LIMIT:
                body_x_cmd = -max_vel
            elif position_estimate[0] < -BOX_LIMIT:
                boxy_x_cmd = max_vel
            
            if position_estimate[1] > BOX_LIMIT:
                body_y_cmd = -max_vel
            elif position_estimate[1] < -BOX_LIMIT:
                body_y_cmd = max_vel\
                
            mc.start_linear_motion(body_x_cmd, body_y_cmd, 0)
            time.sleep(1)
            

"""
*main difference between mc.forward() and mc.start_forward() etc. is that mc.forward and mc.back wont continue
the code until the distance has been reached
mc.start_...() will not stop until the mc.stop() is given, which is done automatically when the mc instance is exited
"""


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    #loggings
    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        
        #logging while flying
        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        #simple_log_async(scf, lg_stab)

        #logconf.start()
        #take_off_simple(scf)
        take_off_simple(scf)
        #logconf.stop()

