import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from configparser import ConfigParser
import tkinter as tk
import threading

from user import User
from notifications import Notifications
from calculateFocalandHeight import calculate

config = ConfigParser()


def mainThreadRunner():
    runningThread = threading.Thread(target=runMain)
    runningThread.start()


def calibrationThreadRunner():
    runCalibrationThread = threading.Thread(target=runCalibration)
    runCalibrationThread.start()


def getMidpoint(p1, p2):
    midPoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    return midPoint


def saveConfig(heightMax, heightMin, distanceMax, distanceMin, cOffsetMax, eyeAngleMax):
    try:
        config.read('config.ini')
        config.set('ergonomics', 'HEIGHT_MAX', heightMax)
        config.set('ergonomics', 'HEIGHT_MIN', heightMin)
        config.set('ergonomics', 'DISTANCE_MAX', distanceMax)
        config.set('ergonomics', 'DISTANCE_MIN', distanceMin)
        config.set('ergonomics', 'C_OFFSET_MAX', cOffsetMax)
        config.set('ergonomics', 'EYE_ANGLE_MAX', eyeAngleMax)
    except IOError:
        print("failed to save configuration.")

    with open('config.ini', 'w') as f:
        config.write(f)


def runMain():
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

        img, faces = detector.findFaceMesh(img, draw=False)

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


runningThread = threading.Thread(target=runMain)


def runCalibration():
    focalLength, webcamHeight = calculate()

    config.read('config.ini')
    config.set('main', 'FOCAL_LENGTH', str(round(focalLength)))
    config.set('main', 'WEBCAM_Y_POS', str(round(webcamHeight) / 480))

    with open('config.ini', 'w') as f:
        config.write(f)

    calibrationWindowConfirmation = tk.Tk()
    calibrationWindowConfirmation.geometry("500x80")
    calibrationWindowConfirmation.title("Calibration Confirmation")
    focalLengthLabel = tk.Label(calibrationWindowConfirmation,
                                text="The focal length of your current webcam is: " + str(round(focalLength)),
                                font=('Arial', '14'))
    focalLengthLabel.pack()
    webcamYPosLabel = tk.Label(calibrationWindowConfirmation,
                               text="The theoretical y position of your Webcam is : " + str(
                                   round(webcamHeight / 480, 3)),
                               font=('Arial', '14'))
    webcamYPosLabel.pack()

    calibrationWindowConfirmation.mainloop()


runCalibrationThread = threading.Thread(target=runCalibration)

window = tk.Tk()
window.configure(background="white")
window.geometry("466x346")
window.title("PostureChecker")

# ---------------------------------------------------------------------

calibrationFrame = tk.Frame(window, background="white", highlightbackground="black", highlightthickness=2)

pleaseWaitLabel = tk.Label(calibrationFrame,
                           text="Calibrate Webcam",
                           font=('Arial', '14'),
                           background="white")
pleaseWaitLabel.pack()

instructionsLabel1 = tk.Label(calibrationFrame,
                              text="Please position yourself directly in-front of the camera,",
                              font=('Arial', '14'),
                              background="white")
instructionsLabel1.pack()

instructionsLabel2 = tk.Label(calibrationFrame,
                              text="50cm away for the duration of the configuration.",
                              font=('Arial', '14'),
                              background="white")
instructionsLabel2.pack()

calibrateButton = tk.Button(calibrationFrame, text="Calibrate", font=('Arial', '14'),
                            command=lambda: calibrationThreadRunner())
calibrateButton.pack()

calibrationFrame.place(x=0, y=219)
# ---------------------------------------------------------------------
configurationFrame = tk.Frame(window, width=220, height=220, background="white", highlightbackground="black",
                              highlightthickness=2)

heightMinFrame = tk.Frame(configurationFrame)
heightMinLabel = tk.Label(heightMinFrame, text="Min Height:", background="white")
heightMinLabel.grid(row=0, column=0)
heightMinEntry = tk.Entry(heightMinFrame)
heightMinEntry.grid(row=0, column=1)

heightMaxFrame = tk.Frame(configurationFrame)
heightMaxLabel = tk.Label(heightMaxFrame, text="Max Height:", background="white")
heightMaxLabel.grid(row=0, column=0)
heightMaxEntry = tk.Entry(heightMaxFrame)
heightMaxEntry.grid(row=0, column=1)

distanceMinFrame = tk.Frame(configurationFrame)
distanceMinLabel = tk.Label(distanceMinFrame, text="Min Distance:", background="white")
distanceMinLabel.grid(row=0, column=0)
distanceMinEntry = tk.Entry(distanceMinFrame)
distanceMinEntry.grid(row=0, column=1)

distanceMaxFrame = tk.Frame(configurationFrame)
distanceMaxLabel = tk.Label(distanceMaxFrame, text="Max Distance:", background="white")
distanceMaxLabel.grid(row=0, column=0)
distanceMaxEntry = tk.Entry(distanceMaxFrame)
distanceMaxEntry.grid(row=0, column=1)

cOffsetMaxFrame = tk.Frame(configurationFrame)
cOffsetMaxLabel = tk.Label(cOffsetMaxFrame, text="Max C-Offset:", background="white")
cOffsetMaxLabel.grid(row=0, column=0)
cOffsetMaxEntry = tk.Entry(cOffsetMaxFrame)
cOffsetMaxEntry.grid(row=0, column=1)

eyeAngleMaxFrame = tk.Frame(configurationFrame)
eyeAngleMaxLabel = tk.Label(eyeAngleMaxFrame, text="Max Eye Angle:", background="white")
eyeAngleMaxLabel.grid(row=0, column=0)
eyeAngleMaxEntry = tk.Entry(eyeAngleMaxFrame)
eyeAngleMaxEntry.grid(row=0, column=1)

try:
    config.read('config.ini')
    heightMaxEntry.insert(10, config.get('ergonomics', 'HEIGHT_MAX'))
    heightMinEntry.insert(10, config.get('ergonomics', 'HEIGHT_MIN'))
    distanceMaxEntry.insert(10, config.get('ergonomics', 'DISTANCE_MAX'))
    distanceMinEntry.insert(10, config.get('ergonomics', 'DISTANCE_MIN'))
    cOffsetMaxEntry.insert(10, config.get('ergonomics', 'C_OFFSET_MAX'))
    eyeAngleMaxEntry.insert(10, config.get('ergonomics', 'EYE_ANGLE_MAX'))
except IOError:
    print("failed to read configuration file.")
submitButton = tk.Button(configurationFrame, text="Submit Configuration", command=lambda: saveConfig(
    heightMaxEntry.get(),
    heightMinEntry.get(),
    distanceMaxEntry.get(),
    distanceMinEntry.get(),
    cOffsetMaxEntry.get(),
    eyeAngleMaxEntry.get()
))
submitButton.place(x=87, y=180)

heightMaxFrame.place(x=16, y=0)
heightMinFrame.place(x=18, y=30)
distanceMaxFrame.place(x=7, y=60)
distanceMinFrame.place(x=9, y=90)
cOffsetMaxFrame.place(x=7, y=120)
eyeAngleMaxFrame.place(x=0, y=150)

configurationFrame.place(x=0, y=0)
# ----------------------------------------------------------------------

runProgramButton = tk.Button(window, text="Run Program",
                             font=('Arial', '14'), command=lambda: mainThreadRunner())

runProgramButton.place(x=280, y=90)

window.mainloop()
