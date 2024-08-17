
import logging
import sys
import time
from threading import Event
import socket
import struct
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper
import argparse
import droneCV2
import numpy as np
import cv2
import serial
import os
import pickle

with open("cameraMatrix.pkl", "rb") as file:
     cMatrix = pickle.load(file)
with open("distortionMatrix.pkl", "rb") as file:
     dMatrix = pickle.load(file)

from paho.mqtt import client as mqtt_client

"""MQTT"""
broker = 'broker.emqx.io'
port = 1883
topic = 'python/mqtt'
client_id = 'python-mqtt-600'
username = 'emqx'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        #set connecting client ID
        client = mqtt_client.Client(client_id = client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60

    def on_disconnect(client, userdata, rc):
        logging.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    
def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()





count = 0
imgsArraySize = 5

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)

#position_estimate = [0,0,0]
droneXPos = 0
droneYPos = 0
droneZPos = 0
droneRoll = 0
dronePitch = 0
droneYaw = 0
DEFAULT_HEIGHT = 0.5 #meters
BOX_LIMIT = 0.5
droneCurrentDegree = 0
distanceToSite = 0.5
tvecThreshold = 0.0025
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

imgdata = None
data_buffer = bytearray()

def rx_bytes(size):
    data = bytearray()
    while len(data) < size:
        packet_chunk = client_socket.recv(size-len(data))
        if not packet_chunk:
            raise ConnectionError("Socket connection lost")
        data.extend(packet_chunk)
    return data

def log_pos_callback(timestamp, data, logconf):

    global droneXPos, droneYPos, droneZPos
    droneXPos = data['stateEstimate.x']
    droneYPos = data['stateEstimate.y']
    droneZPos = data['stateEstimate.z']

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
    #print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    global droneRoll, dronePitch, droneYaw
    droneRoll = data['stabilizer.roll']
    dronePitch = data['stabilizer.pitch']
    droneYaw = data['stabilizer.yaw']

#add logging config to the logging framework of the cf
def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    #logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(5)
    logconf.stop()




'''
#RTL concept
#Go up 0.2 meters, go down 0.1 meters, go left 0.1 meters, go right 0.2 meters
d = {"up":0.2, "down":0.1}
for key, value in d.items():
    if key == "up":
        mc.down(value)
'''

def returnToLaunch():
    #will run this after dropping down and releasing latch
    time.sleep(2)
    print("Up 0.3 meters")
    #mc.up(.3) #drone dropped to .2m to drop latch (not fully landed)
    time.sleep(2)
    print("Turn right 180 degrees")
    #mc.turn_right(180)
    time.sleep(2)
    print("Forward 0.5 meters")
    #mc.forward(.5)
    #Adjust meters as needed
    time.sleep(2)
    print("Stopped")
    #mc.stop()


#Had to split them up because well do one at a time while checking the frame in between
def centerArucoHorizontal(horizontalOffset):
    #get values from get_offset_from_center in droneCV
    isCenteredX = False
    #check horiz offsets
    if horizontalOffset > 0:
        #to the left, move right
        print("Move right 0.1")
    elif horizontalOffset < 0:
        #to the right, move left
        print("Move left 0.1")
    else:
        print("Centered horizontally")
        isCenteredX = True
    return isCenteredX
    
def centerArucoVertical(verticalOffset):
    isCenteredY = False
    #check vert offsets
    if verticalOffset > 0:
        #below center, move up
        print("move up 0.1")
    elif verticalOffset < 0:
        #above center, move down
        print("move down 0.1 meters")
        #mc.down(0.1)
    else:
        print("Centered vertically")
        isCenteredY = True
    return isCenteredY


def correctHeightOffset():
    if droneZPos > 0.5:
        #higher than marker
        offset = droneZPos - 0.5
        print("Move down", str(offset))
    if droneZPos < 0.5:
        #lower than marker
        offset = 0.5 - droneZPos
        print("Move up", str(offset))
        #mc.up(offset)
        
def markerTooClose(frame, mc, tr, br, bl, tl):
    #droneZPos
    #this is wrong, tr has two values
    frameHeight = frame.shape[0]
    if tr < 20 or tl < 20 or br > frameHeight - 20 or bl > frameHeight - 20:
        #if any of the corners are reaching the edge of frame, its too close and move back
        mc.back(0.1)


def printLogs():
    #print important drone information
    print("***************************************************************\n")
    print(f"Drone X Position: {droneXPos}\nDrone Y Position: {droneYPos}\nDrone Z Position: {droneZPos}\nDrone Roll: {droneRoll}\nDrone Pitch: {dronePitch}\nDrone Yaw: {droneYaw}\n")
    print("***************************************************************\n")

def return_frame():
    #ONE FRAME
    packetInfoRaw = rx_bytes(4)
    [length, routing, function] = struct.unpack('<HBB', packetInfoRaw)
    imgHeader = rx_bytes(length - 2)
    [magic, width, height, depth, format, size] = struct.unpack('<BHHBBI', imgHeader)
    if magic == 0xBC:
        img_stream = bytearray()
        #print("Magic is good")
        #print("Resolution is {}x{} with depth of {} byte(s)".format(width, height, depth))
        #print("Image format is {}".format(format))
        #print("Image size is {} bytes".format(size))
        while len(img_stream) < size:
            packet_info_raw = rx_bytes(4)
            length, dst, src = struct.unpack('<HBB', packet_info_raw)
            chunk = rx_bytes(length - 2)
            img_stream.extend(chunk)
                    # mean_time_per_image = (time.time() - start) / count
                    # print("Mean time per image: {:.2f}s".format(mean_time_per_image))

    if format == 0:
                        # Assuming this is a raw Bayer image
        bayer_img = np.frombuffer(img_stream, dtype=np.uint8)
        bayer_img.shape = (244, 324)  # Adjust this if needed
        color_img = cv2.cvtColor(bayer_img, cv2.COLOR_BayerBG2BGRA)
        cv2.waitKey(1)
    elif format == 1:
                        
        nparr = np.frombuffer(img_stream, np.uint8)
        decoded = cv2.cvtColor(nparr, cv2.COLOR_BayerBG2BGRA)
        decoded = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)
        #decoded = cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB) #this might not be necessary
        
    else:
        print("Frame not received")
        
    frame = decoded

    return frame

"""
*main difference between mc.forward() and mc.start_forward() etc. is that mc.forward and mc.back wont continue
the code until the distance has been reached
mc.start_...() will not stop until the mc.stop() is given, which is done automatically when the mc instance is exited
"""


if __name__ == '__main__':
    count = 0
    cflib.crtp.init_drivers()


    run() #mqtt

    #Load arduino board
    #arduino = serial.Serial('/dev/cu.usbmodem1301', 9600)

    #reset servo position to 0
    #arduino.write(str(180).encode("utf-8"))
    
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        
        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                        cb=param_deck_flow)
        time.sleep(1)

        if not deck_attached_event.wait(timeout=5):
            print('No flow deck detected!')
            sys.exit(1)

        #loggings
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stabilizer.yaw', 'float')
        scf.cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        #logging while flying
        logconf = LogConfig(name='Position', period_in_ms=10)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)
        #simple_log_async(scf, lg_stab)

        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
            #while loop is for continuous viewing of camera while processing for aruco
            print("starting flight")
            takeoffToAruco = True
            returnToLaunchSite = False
            logconf.start()
            lg_stab.start()
            while True:
                
                if takeoffToAruco:
                    #mc.forward(1.2)
                    #time.sleep(1)
                    print("Move forward 1.2")
                    takeoffToAruco = False

                if returnToLaunchSite:
                    print("Landing and release latch.")
                    #will be made True after released latch
                    #returnToLaunch()
                    #arduino.write(str(0).encode("utf-8"))
                    #time.sleep(2)
                    #arduino.write(str(180).encode("utf-8"))
                    #time.sleep(2)
                    returnToLaunchSite = False
                    break

            



                """CONTROL"""

                #starting process (takeoff)
                #this is where move forward will be
                


                
                packetInfoRaw = rx_bytes(4)
                [length, routing, function] = struct.unpack('<HBB', packetInfoRaw)
                imgHeader = rx_bytes(length - 2)
                [magic, width, height, depth, format, size] = struct.unpack('<BHHBBI', imgHeader)
                if magic == 0xBC:
                    img_stream = bytearray()
                    #print("Magic is good")
                    #print("Resolution is {}x{} with depth of {} byte(s)".format(width, height, depth))
                    #print("Image format is {}".format(format))
                    #print("Image size is {} bytes".format(size))
                    while len(img_stream) < size:
                        packet_info_raw = rx_bytes(4)
                        length, dst, src = struct.unpack('<HBB', packet_info_raw)
                        chunk = rx_bytes(length - 2)
                        img_stream.extend(chunk)
                                # mean_time_per_image = (time.time() - start) / count
                                # print("Mean time per image: {:.2f}s".format(mean_time_per_image))

                if format == 0:
                                    # Assuming this is a raw Bayer image
                    bayer_img = np.frombuffer(img_stream, dtype=np.uint8)
                    bayer_img.shape = (244, 324)  # Adjust this if needed
                    color_img = cv2.cvtColor(bayer_img, cv2.COLOR_BayerBG2BGRA)
                    cv2.waitKey(1)
                elif format == 1:
                                    
                    nparr = np.frombuffer(img_stream, np.uint8)
                    decoded = cv2.cvtColor(nparr, cv2.COLOR_BayerBG2BGRA)
                    decoded = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)
                    print("Returned frame")
                    #decoded = cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB) #this might not be necessary
                    
                else:
                    print("Frame not received")
                    
                frame = decoded
                print("frame returned")
                #print(frame.shape)
                #cv2.imshow('frame', frame)
                #cv2.destroyAllWindows()

                retVal = droneCV2.detect_aruco(frame)
                if retVal == None:
                    print("Aruco not detected")
                    mc.forward(0.01)
                else:
                    print("Aruco detected")
                    corners, tr, br, bl, tl, frameCenter = retVal
                    verticalOffset, horizontalOffset = droneCV2.get_offset_from_center(tr, br, bl, tl, frameCenter)
                    print(f"Frame center: {frameCenter}")
                    print(f"Vert: {verticalOffset}, Hori: {horizontalOffset}")
                    if verticalOffset == 0 and horizontalOffset == 0:
                        #centered, move forward till tvec is within threshold
                        #release latch, stop
                    
                        newFrame = cv2.resize(frame, (800, 600))
                        print("Centered (2)")
                        cv2.imshow('Centered Frame', newFrame)
                        cv2.waitKey(1)
                        newCorners = corners[0]
                        
                        tvec = droneCV2.poseEstimate(newCorners)
                        #if rvec and tv:
                        #    cv2.drawFrameAxes(frame, cMatrix, dMatrix, rvec, tvec, 0.01 * 0.5)
                        print("Distance to Marker: ", tvec)
                        cv2.destroyWindow('Centered Frame')
                        while (tvec > tvecThreshold):
                            frame = return_frame()
                            newFrame = cv2.resize(frame, (800, 600))
                            cv2.imshow('tvecTracking', newFrame)
                            cv2.waitKey(1)
                            retVal = droneCV2.detect_aruco(frame)
                            if retVal is not None:
                                corners, _, _, _, _, _, = retVal
                                if corners is not None:
                                    newCorners = corners[0]
                                    tvec = droneCV2.poseEstimate(newCorners)
                                    print("Tvec Average: ", tvec)
                                    #mc.forward(0.01)

                                
                                    
                            
                        cv2.destroyWindow('tvecTracking')
                        returnToLaunchSite = True
                        print("Releasing latch")
                        #return 
                        #Return to launch function
                        mc.stop()

                    else:
                        horiCentered = False
                        vertCentered = False
                        cv2.destroyAllWindows()
                        while (not horiCentered) and (not vertCentered):
                            
                            #keeps centering the aruco
                            horiCentered = centerArucoHorizontal(horizontalOffset)
                            vertCentered = centerArucoVertical(verticalOffset)
                            frame = return_frame()
                            #frame = cv2.circle(frame, frameCenter, 3, (0, 255, 0), 1)
                            newFrame = cv2.resize(frame, (800, 600))
                            cv2.imshow("frame", newFrame)
                            cv2.waitKey(1)
                            
                            
                            retval = droneCV2.detect_aruco(frame)
                            if retval == None:
                                print("Aruco not detected")
                                #maybe move back at this point to refind the aruco
                                mc.forward(0.01)
                            else:
                                corners, tr, br, bl, tl, frameCenter = retval
                                verticalOffset, horizontalOffset = droneCV2.get_offset_from_center(tr, br, bl, tl, frameCenter)
                                print(f"Offsets | Vertical: {verticalOffset}, Horizontal: {horizontalOffset}")
                           
                            #os.system('clear')





                #testRun(mc)
                
                
                #print important info
                printLogs()


        logconf.stop()
        lg_stab.stop()


                




client_socket.close()
cv2.destroyAllWindows()