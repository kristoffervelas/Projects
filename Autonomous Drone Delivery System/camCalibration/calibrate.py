import cv2
import glob
import numpy as np
import pickle



def retrieve_matrices():
    FRAME_SIZE = (244, 324)
    CHESSBOARD_SIZE = (6, 8)

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


retrieve_matrices()

