import cvzone
import numpy as np

def getMidpoint(p1, p2):
    midPoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    return midPoint

def getSlope(p1, p2):
    rise = (p2[1] - p1[1])
    run = (p2[0] - p1[0])
    return rise, run

class User:
    centreOffset = None
    distance = None
    height = None
    eyeAngle = None

    def setCentreYOffset(self, leftEye, rightEye, img, pixelToRealRatio):
        centreOfEyes = getMidpoint(leftEye, rightEye)
        centreOfImage = (img.shape[1] // 2, img.shape[0] // 2)
        centreOffsetPixels = abs(centreOfImage[0] - centreOfEyes[0])

        self.centreOffset = int(centreOffsetPixels / pixelToRealRatio)

    def setDistance(self, pixelDistanceBetweenEyes, realDistanceBetweenEyes, focalLength):
        self.distance = int((realDistanceBetweenEyes * focalLength) / pixelDistanceBetweenEyes[0])

    def setHeight(self, levelWithWebcamYCoord, centreOfEyes, pixelToRealRatio):
        heightOffsetInPixels = levelWithWebcamYCoord - centreOfEyes[1]

        self.height = int(heightOffsetInPixels / pixelToRealRatio)

    def setEyeAngle(self, leftEye, rightEye):
        rise, run = getSlope(leftEye, rightEye)
        self.eyeAngle = int(abs(np.rad2deg(np.arctan2(rise, run))))

    def displayUserInformation(self, img):
        cvzone.putTextRect(img, f'Eye Angle: {int(self.eyeAngle)} degree',
                           (50, 30),
                           scale=1.5)

        cvzone.putTextRect(img, f'Distance: {int(self.distance)}cm',
                           (50, 70),
                           scale=1.5)

        cvzone.putTextRect(img, f'Height: {int(self.height)}cm',
                           (50, 110),
                           scale=1.5)

        cvzone.putTextRect(img, f'C-offset: {int(self.centreOffset)}cm',
                           (50, 150),
                           scale=1.5)
