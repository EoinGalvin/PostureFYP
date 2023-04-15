import cv2
import time
from cvzone.FaceMeshModule import FaceMeshDetector


def getMidpoint(p1, p2):
    midPoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    return midPoint


def Average(lst):
    return sum(lst) / len(lst)


def calculate():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = FaceMeshDetector(maxFaces=1)
    focalLengths = []
    heights = []

    time_end = time.time() + 5
    while time.time() < time_end:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            face = faces[0]
            pointLeft = face[145]
            pointRight = face[374]

            centreOfEyes = getMidpoint(pointLeft, pointRight)

            heights.append(centreOfEyes[1])
            pixelWidth, _ = detector.findDistance(pointLeft, pointRight)
            realWidth = 6.3

            # Finding the Focal Length
            userDistance = 50
            f = (pixelWidth * userDistance) / realWidth
            focalLengths.append(f)

        # cv2.imshow("Determine Focal Length", img)
        cv2.waitKey(1)
    return Average(focalLengths), Average(heights)
