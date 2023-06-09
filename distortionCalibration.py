# This code is a modification of Nicolai Nielsen's calibration code,modified to suit this project and put into a
# single file to integrate accordingly. Nicolai Youtube Video: https://www.youtube.com/watch?v=_-BTKiamRTg Nicolai
# Github Repository: https://github.com/niconielsen32

import numpy as np
import cv2 as cv
import glob
import pickle
import os
from win11toast import notify

def calibrateDistortion(webcamIndex):

    if os.path.isdir('images') == False:
        print("creating image folder")
        os.mkdir('images')

    cap = cv.VideoCapture(webcamIndex, cv.CAP_DSHOW)

    num = 0

    while cap.isOpened():

        succes, img = cap.read()

        k = cv.waitKey(5)

        if k == 27:
            break
        elif k == ord('s'):  # wait for 's' key to save and exit
            cv.imwrite('images/img' + str(num) + '.png', img)
            print("image saved!")
            num += 1

        cv.imshow('Img', img)

    # Release and destroy all windows before termination
    cap.release()

    cv.destroyAllWindows()

    # ############### FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

    chessboardSize = (7, 7)
    frameSize = (640, 480)

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

    size_of_chessboard_squares_mm = 20
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    if len(os.listdir('images')) != 0:
        images = glob.glob('images/*.png')

        for image in images:

            img = cv.imread(image)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

                # Draw and display the corners
                cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
                cv.imshow('img', img)
                cv.waitKey(1000)

        cv.destroyAllWindows()

        # ############# CALIBRATION #######################################################

        ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

        # Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
        pickle.dump((cameraMatrix, dist), open("calibration.pkl", "wb"))
        pickle.dump(cameraMatrix, open("cameraMatrix.pkl", "wb"))
        pickle.dump(dist, open("dist.pkl", "wb"))
    else:
        notify("No images")
