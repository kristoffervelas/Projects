import argparse
import time
import socket,os,struct, time
import numpy as np
import cv2
import glob
import pickle

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


start = time.time()
count = 0


def retrieve_matrices():
    FRAME_SIZE = (244, 324)
    CHESSBOARD_SIZE = (7, 7)

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((1, (CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1]), 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHESSBOARD_SIZE[0],0:CHESSBOARD_SIZE[1]].T.reshape(-1,2)
    
    size_of_chessboard_squares_mm = 50
    objp = objp * size_of_chessboard_squares_mm


    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob('calibration_imgs/*.png')

    for image in images:

        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        print(ret)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,1), criteria)
            imgpoints.append(corners2)

            cv2.drawChessboardCorners(img, CHESSBOARD_SIZE, corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(1000)

    ret, cameraMatrix, distortion_coefs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, FRAME_SIZE, None, None)
    print(cameraMatrix, " Shape: ", cameraMatrix.shape)
    print(distortion_coefs, " Shape: ", distortion_coefs.shape)
    with open('matrices/cameraMatrix.pkl', 'wb') as file:
        pickle.dump(cameraMatrix, file)
    with open('matrices/distortionMatrix.pkl', 'wb') as file:
        pickle.dump(distortion_coefs, file)

count2 = 0

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
          count2+=1
          nparr = np.frombuffer(imgStream, np.uint8)
          decoded = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED) #this is the image
          frame = decoded
          if count2 % 10 == 0:
            print("image being taken")
            cv2.imwrite(f"calibration_imgs/img{count2+1}.png", frame)
          if count2 == 100:
            break
          print("****decoded**** = ", decoded)
          cv2.imshow('JPEG', decoded)
          cv2.waitKey(1)

