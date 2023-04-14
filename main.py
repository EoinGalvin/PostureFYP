import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from win11toast import notify
import time
from configparser import ConfigParser
import tkinter as tk
from user import User
from notifications import Notifications

config = ConfigParser()


def getMidpoint(p1, p2):
    midPoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    return midPoint


def getSlope(p1, p2):
    rise = (p2[1] - p1[1])
    run = (p2[0] - p1[0])
    return rise, run


def eligibleNotificationChecker(value, message):
    if value >= 100:
        notify(message)
        return True
    else:
        return False


def Average(lst):
    return sum(lst) / len(lst)


def calculateFocal():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
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


def runConfig():
    focalLength, webcamHeight = calculateFocal()

    config.read('config.ini')
    config.set('main', 'FOCAL_LENGTH', str(round(focalLength)))
    config.set('main', 'WEBCAM_Y_POS', str(round(webcamHeight) / 480))

    with open('config.ini', 'w') as f:
        config.write(f)

    configQuestionLabel.destroy()
    label.destroy()
    label2.destroy()
    yesNoButtonFrame.destroy()

    focalLengthLabel = tk.Label(window,
                                text="The focal length of your current webcam is: " + str(round(focalLength)),
                                font=('Arial', '14'))
    focalLengthLabel.pack()
    webcamYPosLabel = tk.Label(window,
                               text="The theoretical y position of your Webcam is : " + str(round(webcamHeight) / 480),
                               font=('Arial', '14'))
    webcamYPosLabel.pack()

    runButton = tk.Button(window, text="Run Program", font=('Arial', '14'), command=runMain)
    runButton.pack()


def runMain():
    window.destroy()
    config.read('config.ini')
    focalLength = int(config.get('main', 'FOCAL_LENGTH'))
    webcamYPos = float(config.get('main', 'WEBCAM_Y_POS'))

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = FaceMeshDetector(maxFaces=1)

    user = User()
    notifications = Notifications(user)

    realDistanceBetweenEyes = 6.3

    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=True)

        if faces:
            face = faces[0]
            leftEye = face[145]
            rightEye = face[374]

            centreOfEyes = getMidpoint(leftEye, rightEye)
            pixelToRealRatio = detector.findDistance(leftEye, rightEye)[0] / realDistanceBetweenEyes
            webcamLevelApproximation = img.shape[0] * webcamYPos
            pixelDistanceBetweenEyes = detector.findDistance(leftEye, rightEye)

            user.setHeight(webcamLevelApproximation, centreOfEyes, pixelToRealRatio)
            user.setDistance(pixelDistanceBetweenEyes, realDistanceBetweenEyes, focalLength)
            user.setCentreYOffset(leftEye, rightEye, img, pixelToRealRatio)
            user.setEyeAngle(leftEye, rightEye)

            user.displayUserInformation(img)

            notifications.heightTrackerHigh()
            notifications.heightTrackerLow()

            notifications.distanceTrackerClose()
            notifications.distanceTrackerFar()

            notifications.centreOffsetTracker()
            notifications.eyeAngleTracker()

        # cv2.imshow("Display User Data", img)
        cv2.waitKey(1)


window = tk.Tk()
window.geometry("600x600")
window.title("PostureChecker")

configQuestionLabel = tk.Label(window,
                               text="Do you wish to complete a configuration phase?",
                               font=('Arial', '14'))
configQuestionLabel.pack()

label = tk.Label(window,
                 text="If yes is selected, the configuration will start instantly.",
                 font=('Arial', '14'))
label.pack()

label2 = tk.Label(window,
                  text="Please sit directly in-front of the webcam, 50 cm away",
                  font=('Arial', '14'))
label2.pack()

yesNoButtonFrame = tk.Frame(window)
yesNoButtonFrame.columnconfigure(0, weight=1)

yesButton = tk.Button(yesNoButtonFrame, text="Yes", font=('Arial', '14'), command=runConfig)
yesButton.grid(row=0, column=0)

noButton = tk.Button(yesNoButtonFrame, text="No", font=('Arial', '14'), command=runMain)
noButton.grid(row=0, column=1)

yesNoButtonFrame.pack()

window.mainloop()
