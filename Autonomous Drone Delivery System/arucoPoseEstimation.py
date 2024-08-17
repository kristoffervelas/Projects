#import serial
import imutils
import argparse
import time
import cv2
import sys
from imutils.video import VideoStream
import pickle
import numpy as np

#Load arduino board
#arduino = serial.Serial('/dev/cu.usbmodem101', 9600)


#Drone cam matrices
with open("cameraMatrix.pkl", "rb") as file:
    cMatrix = pickle.load(file)
with open("distortionMatrix.pkl", "rb") as file:
    dMatrix = pickle.load(file)


ap = argparse.ArgumentParser()
ap.add_argument("-t","--type",type=str,default="DICT_ARUCO_ORIGINAL",help="type of aruco tag to detect")
args = vars(ap.parse_args())

ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)


# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
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

#reset servo position to 0
#arduino.write(str(0).encode("utf-8"))

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=1000)
    (corners, ids, rejected) = arucoDetector.detectMarkers(frame)
    Xframe = frame.shape[1]
    Yframe = frame.shape[0]



#    if ids != None:
#        ret = cv2.aruco.estimatePoseSingleMarkers(corners, 10)
#        cv2.aruco.drawDetectedMarkers(frame, corners)
        
    #draw frame lines intersecting the middle
    cv2.line(frame, (0,Yframe//2), (Xframe,Yframe//2), (255,255,255), 2) #X axis
    cv2.line(frame, (Xframe//2,0), (Xframe//2,Yframe), (255,255,255), 2) #X axis

    frameCenter = (Xframe//2,Yframe//2)
    cv2.circle(frame, frameCenter, 4, frameCenterColor, -1)

    cv2.putText(frame, f"OFFSETS ( Up: {upOff}, Down: {downOff}, Right: {rightOff}, Left: {leftOff})", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    cv2.putText(frame, horizontalFixText, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    cv2.putText(frame, verticalFixText, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0))
    cv2.putText(frame, landedText, (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
    if len(corners) > 0:
        ids = ids.flatten()
        for (markerCorner, markerId) in zip(corners, ids):
            corners = markerCorner.reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # draw the bounding box of the ArUCo detection
            cv2.line(frame, topLeft, topRight, (0, 255, 255), 2)
            cv2.line(frame, topRight, bottomRight, (255, 0, 255), 2)
            cv2.line(frame, bottomRight, bottomLeft, (255, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (255, 255, 255), 2)
        
            # compute and draw the center (x, y)-coordinates of the
            # ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
            # draw the ArUco marker ID on the frame
            cv2.putText(frame, str(markerId),
            	(topLeft[0], topLeft[1] - 15),
            	cv2.FONT_HERSHEY_SIMPLEX,
            	0.5, (0, 255, 0), 2)

            
            marker_size = 0.01
            marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                            [marker_size / 2, marker_size / 2, 0],
                            [marker_size / 2, -marker_size / 2, 0],
                            [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)

            ret, rvec, tvec = cv2.solvePnP(marker_points, corners, cMatrix, dMatrix)
            #if ret:
            #    cv2.drawFrameAxes(frame, cMatrix, dMatrix, rvec, tvec, 0.01 * 0.5)
            print("rvec:", str(rvec), " tvec:", str(tvec))
                
            trX = topRight[0]
            trY = topRight[1]
            tlX = topLeft[0]
            tlY = topLeft[1]
            brX = bottomRight[0]
            brY = bottomRight[1]
            blX = bottomLeft[0]
            blY = bottomLeft[1]

            #Determine if aruco is in withing center
            if tlX < frameCenter[0] and tlY < frameCenter[1] and trX > frameCenter[0] and trY < frameCenter[1] and blX < frameCenter[0] and blY > frameCenter[1] and brX > frameCenter[0] and brY > frameCenter[1]:
                 frameCenterColor = (0,0,255)
                 cv2.putText(frame, "Marker boundaries in center", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
            else:
                 frameCenterColor = (0,255,0)

            #if to the right of center
            if tlX > frameCenter[0] and blX > frameCenter[0]:
                 rightOff = blX-frameCenter[0] if blX>tlX else tlX-frameCenter[0]
                 #print(f"offset to the right {offsetValue} units...")
                 horizontalFixText=f"Move left {rightOff} units..."
            else:
                 rightOff = 0
            #if to the left of center
            if trX < frameCenter[0] and brX < frameCenter[0]:
                 leftOff = frameCenter[0]-trX if brX>trX else frameCenter[0]-brX
                 #print(f"offset to the left {offsetValue} units...")
                 horizontalFixText=f"Move right {leftOff} units..."
            else:
                 leftOff = 0
            #if below center
            if trY > frameCenter[1] and tlY > frameCenter[1]:
                 downOff = trY-frameCenter[1] if trY>tlY else tlY-frameCenter[1]
                 #print(f"offset down {offsetValue} units...")
                 verticalFixText = f"Move up {downOff} units..."
            else:
                 downOff = 0
            #if above center
            if brY < frameCenter[1] and blY < frameCenter[1]:
                 upOff = frameCenter[1]-blY if brY>blY else frameCenter[1]-brY
                 #print(f"offset upwards {offsetValue} units...")
                 verticalFixText=f"Move down {upOff} units..."
            else:
                 upOff = 0

            if tvec[0] >= -0.01 and tvec[2] <= 0.047:
                 landedText = "Landed, releasing latch..."
                 #arduino.write(str(180).encode("utf-8"))
                 #time.sleep(2)
                 #arduino.write(str(0).encode("utf-8"))
            else:
                 landedText = ""

            tvecTotal = 0
            for t in tvec:
                tvecTotal+=t
            print("Tvec ave: ", str(tvecTotal/3))



    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop() 



