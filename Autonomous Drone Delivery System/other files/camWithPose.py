#Testing drone camera with opencv pose estimation and aruco detection

#import serial
import imutils
import argparse
import time
import socket,os,struct, time
import numpy as np
import cv2
import sys
import pickle
from imutils.video import VideoStream

"""COMPUTER VISION ALGORITHM"""

#Drone cam matrices
with open("cameraMatrix.pkl", "rb") as file:
    cMatrix = pickle.load(file)
with open("distortionMatrix.pkl", "rb") as file:
    dMatrix = pickle.load(file)

#Load arduino board
#arduino = serial.Serial('/dev/cu.usbmodem101', 9600)
#reset servo position to 0
#arduino.write(str(0).encode("utf-8"))

ap = argparse.ArgumentParser()
ap.add_argument("-t","--type",type=str,default="DICT_ARUCO_ORIGINAL",help="type of aruco tag to detect")
args = vars(ap.parse_args())

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

#VARIABLES
frameCenterColor = (0,255,0)
#offset values
downOff = 0
upOff = 0
leftOff = 0
rightOff = 0
horizontalFix = 0
verticalFix = 0
horizontalFixText = ""
verticalFixText = ""
landedText = ""

"""DRONE CAM CODE"""

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

imgdata = None
data_buffer = bytearray()

def rx_bytes(size):
    data = bytearray()
    while len(data) < size:
        data.extend(client_socket.recv(size-len(data)))
    return data


###FUNCTIONS TO MAKE

def arucoFound():
    pass

def get_offset_from_center():
    #values that this returns will be given to centerAruco function in autoFlight.py
    pass

start = time.time()
count = 0

while(1):
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
            frame = decoded
          
            ##Computer vision algorithm real
            (corners, ids, rejected) = arucoDetector.detectMarkers(frame)
            Xframe = frame.shape[1]
            Yframe = frame.shape[0]
            #draw frame lines intersecting the middle
            #cv2.line(frame, (0,Yframe//2), (Xframe,Yframe//2), (255,255,255), 2) #X axis
            #cv2.line(frame, (Xframe//2,0), (Xframe//2,Yframe), (255,255,255), 2) #X axis
            frameCenter = (Xframe//2, Yframe//2)
            cv2.circle(frame, frameCenter, 4, frameCenterColor, -1)
            print(f"Offsets ( Up: {upOff}, Down: {downOff}, Right: {rightOff}, Left: {leftOff})")

            if len(corners) > 0:
                ids = ids.flatten()
                for (markerCorner, markerId) in zip(corners, ids):
                    corners = markerCorner.reshape((4,2))

                    marker_size = 0.01
                    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                                    [marker_size / 2, marker_size / 2, 0],
                                    [marker_size / 2, -marker_size / 2, 0],
                                    [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
                    ret, rvec, tvec = cv2.solvePnP(marker_points, corners, cMatrix, dMatrix)
                    if ret:
                        cv2.drawFrameAxes(frame, cMatrix, dMatrix, rvec, tvec, 0.01 * 0.5)
                    if tvec[0] >= -0.01 and tvec[2] <= 0.047:
                        print("landed, release latch")

            #print("****decoded**** = ", decoded)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            #print(decoded.shape)
cv2.destroyAllWindows()

