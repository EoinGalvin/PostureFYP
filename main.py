import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import time
from configparser import ConfigParser
import tkinter as tk
import threading

from user import User
from notifications import Notifications
from configGUI import configGUI
from calculateFocalandHeight import calculate

config = ConfigParser()


def getMidpoint(p1, p2):
    midPoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    return midPoint


def runCalibration():
    configQuestionLabel.destroy()
    label.destroy()

    ButtonFrame.destroy()

    pleaseWaitLabel = tk.Label(window,
                               text="The configuration stage will begin in 5 seconds.",
                               font=('Arial', '14'))
    pleaseWaitLabel.pack()

    instructionsLabel1 = tk.Label(window,
                                  text="Please position yourself directly in-front of the camera,",
                                  font=('Arial', '14'))
    instructionsLabel1.pack()

    instructionsLabel2 = tk.Label(window,
                                  text="50cm away for the duration of the configuration.",
                                  font=('Arial', '14'))
    instructionsLabel2.pack()

    time.sleep(5)
    focalLength, webcamHeight = calculate()

    config.read('config.ini')
    config.set('main', 'FOCAL_LENGTH', str(round(focalLength)))
    config.set('main', 'WEBCAM_Y_POS', str(round(webcamHeight) / 480))

    with open('config.ini', 'w') as f:
        config.write(f)

    pleaseWaitLabel.destroy()
    instructionsLabel1.destroy()
    instructionsLabel2.destroy()

    focalLengthLabel = tk.Label(window,
                                text="The focal length of your current webcam is: " + str(round(focalLength)),
                                font=('Arial', '14'))
    focalLengthLabel.pack()
    webcamYPosLabel = tk.Label(window,
                               text="The theoretical y position of your Webcam is : " + str(
                                   round(webcamHeight / 480, 3)),
                               font=('Arial', '14'))
    webcamYPosLabel.pack()
    runningThread = threading.Thread(target=runMain)
    runButton = tk.Button(window, text="Run Program", font=('Arial', '14'), command=runningThread.start)
    runButton.pack()


def runMain():
    for widgets in window.winfo_children():
        widgets.destroy()

    endHelpLabel = tk.Label(window,
                            text="To pause the application press '^' ",
                            font=('Arial', '14'))
    endHelpLabel.pack()
    runningThread = threading.Thread(target=runMain)
    runButton2 = tk.Button(window, text="Run Program", font=('Arial', '14'), command=runningThread.start)
    runButton2.pack()

    config.read('config.ini')
    focalLength = int(config.get('main', 'FOCAL_LENGTH'))
    webcamYPos = float(config.get('main', 'WEBCAM_Y_POS'))

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 15)

    detector = FaceMeshDetector(maxFaces=1)

    user = User()
    notifications = Notifications(user)

    realDistanceBetweenEyes = 6.3

    while True:
        success, img = cap.read()
        if not success:
            break

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

        cv2.imshow("Display User Data", img)

        if cv2.waitKey(1) & 0xFF == ord('^'):
            break
    cap.release()
    cv2.destroyAllWindows()


window = tk.Tk()
window.geometry("600x200")
window.title("PostureChecker")

configQuestionLabel = tk.Label(window,
                               text="Do you wish to complete a Calibration?",
                               font=('Arial', '14'))
configQuestionLabel.pack()

label = tk.Label(window,
                 text="If yes, please sit directly in-front of the webcam, 50 cm away",
                 font=('Arial', '14'))
label.pack()

ButtonFrame = tk.Frame(window)
ButtonFrame.columnconfigure(0, weight=1)

calibrateThread = threading.Thread(target=runCalibration)
calibrateButton = tk.Button(ButtonFrame, text="Calibrate", font=('Arial', '14'), command=calibrateThread.start)
calibrateButton.grid(row=0, column=0)

configThread = threading.Thread(target=configGUI)
configButton = tk.Button(ButtonFrame, text="Configuration", font=('Arial', '14'), command=configThread.start)
configButton.grid(row=0, column=1)

runningThread = threading.Thread(target=runMain)
runProgramButton = tk.Button(ButtonFrame, text="Run Program", font=('Arial', '14'), command=runningThread.start)
runProgramButton.grid(row=0, column=2)

ButtonFrame.pack()

window.mainloop()
