import logging
import sys
import time
import argparse
from threading import Event
import socket,os,struct, time
import numpy as np
import cv2
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper
#from camWithPose import arucoFound
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)

position_estimate = [0,0,0]
DEFAULT_HEIGHT = .5 #meters
BOX_LIMIT = 0.5
droneCurrentDegree = 0

"""CAMERA CODE (not including the while(1) code segment)"""
# Args for setting IP/port of AI-deck. Default settings are for when
# AI-deck is in AP mode.
parser = argparse.ArgumentParser(description='Connect to AI-deck JPEG streamer example')
parser.add_argument("-n",  default="192.168.4.1", metavar="ip", help="AI-deck IP")
parser.add_argument("-p", type=int, default='5000', metavar="port", help="AI-deck port")
parser.add_argument('--save', action='store_true', help="Save streamed images")
args = parser.parse_args()

deck_port = args.p
deck_ip = args.n

print("Connecting to socket on {}:{}...".format(deck_ip, deck_port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((deck_ip, deck_port))
print("Socket connected")


start = time.time()
count = 0

imgdata = None
data_buffer = bytearray()

def rx_bytes(size):
  data = bytearray()
  while len(data) < size:
    data.extend(client_socket.recv(size-len(data)))
  return data

def getCameraFrame():
    
    """
    -returns the frame that the camera sees
    -CLEAN THIS UP BECAUSE THIS USES TIME TO ACCOMODATE FOR THE CONTINUOUS STREAMING,
    WE ONLY NEED ONE FRAME PER FUNCTION CALL
    """

    # First get the info
    packetInfoRaw = rx_bytes(4)
    #print(packetInfoRaw)
    [length, routing, function] = struct.unpack('<HBB', packetInfoRaw)
    #print("Length is {}".format(length))
    #print("Route is 0x{:02X}->0x{:02X}".format(routing & 0xF, routing >> 4))
    #print("Function is 0x{:02X}".format(function))

    imgHeader = rx_bytes(length - 2)
    #print(imgHeader)
    #print("Length of data is {}".format(len(imgHeader)))
    [magic, width, height, depth, format, size] = struct.unpack('<BHHBBI', imgHeader)

    if magic == 0xBC:
        #print("Magic is good")
        #print("Resolution is {}x{} with depth of {} byte(s)".format(width, height, depth))
        #print("Image format is {}".format(format))
        #print("Image size is {} bytes".format(size))

        # Now we start rx the image, this will be split up in packages of some size
        imgStream = bytearray()

        while len(imgStream) < size:
            packetInfoRaw = rx_bytes(4)
            [length, dst, src] = struct.unpack('<HBB', packetInfoRaw)
            #print("Chunk size is {} ({:02X}->{:02X})".format(length, src, dst))
            chunk = rx_bytes(length - 2)
            imgStream.extend(chunk)
     
        count = count + 1
        meanTimePerImage = (time.time()-start) / count
        print("{}".format(meanTimePerImage))
        print("{}".format(1/meanTimePerImage))
        #   print("****This is Format*****",format) 
        if format == 0:
            bayer_img = np.frombuffer(imgStream, dtype=np.uint8)   
            bayer_img.shape = (244, 324)
            color_img = cv2.cvtColor(bayer_img, cv2.COLOR_BayerBG2BGRA)
            cv2.imshow('Raw', bayer_img)
            cv2.imshow('Color', color_img)
            if args.save:
                cv2.imwrite(f"stream_out/raw/img_{count:06d}.png", bayer_img)
                cv2.imwrite(f"stream_out/debayer/img_{count:06d}.png", color_img)
            cv2.waitKey(1)
        else:
            with open("img.jpeg", "wb") as f:
                f.write(imgStream)
            nparr = np.frombuffer(imgStream, np.uint8)
            decoded = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED) #this is the image
            cv2.imshow('JPEG', decoded)
            cv2.waitKey(1)
            #print(decoded.shape)
            cv2.destoryAllWindows()
            return decoded



def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']
    position_estimate[2] = data['stateEstimate.z']

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


def takeoffAndSearch(scf):
    totalDegrees = 0
    degreeAmount = 3
    """
    - Go up DEFAULT_HEIGHT meters and wait 2 sec
    - Move forward .5 meters (this is where the aruco should be)
    - Keep turning until aruco is found
    - If turned 360 and still not found, meaning its probably too high or too low
        -get height offset and move accordingly
    - If found marker, move drone so marker is centered
    - If marker centered, go down .2m above ground and release latch
    """
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(2)
        mc.forward(.5)
        time.sleep(3)
        while not arucoFound():
            mc.turn_right(degreeAmount)
            totalDegrees+=degreeAmount
            droneCurrentDegree = totalDegrees
            time.sleep(0.3)
            if totalDegrees >= 360:
                correctHeightOffset(mc) #level drone to be in same height as marker
                continue

        #If found
        print("Aruco Detected")

        #mc.stop()

def centerAruco(mc):
    #get return values from camWithPose getting the offset of marker tothe center of frame
    #move drone to center it
    pass

def correctHeightOffset(mc):
    if position_estimate[2] > 0.5:
        #higher than marker
        offset = position_estimate[2] - 0.5
        mc.down(offset)
    if position_estimate[2] < 0.5:
        #lower than marker
        offset = 0.5 - position_estimate[2]
        mc.up(offset)
        

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
        logconf.add_variable('stateEstimate.z', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        simple_log_async(scf, lg_stab)

        logconf.start()
        
        ## DRONE COMMANDS
        
        #takeoff and find aruco
        takeoffAndSearch(scf)

        #if found, center aruco, go down, release latch

        #Go down to 0.2m above ground
        offsetToGoDown = position_estimate[2] - 0.2
        mc.down(offsetToGoDown)

        #once released, return to launch




        logconf.stop()

