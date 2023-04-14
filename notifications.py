from win11toast import notify

EYE_ANGLE_MAX = 8
DISTANCE_MAX = 74
DISTANCE_MIN = 40
HEIGHT_MAX = 2
HEIGHT_MIN = -3
C_OFFSET_MAX = 4


def eligibleNotificationChecker(value, message):
    if value >= 100:
        notify(message)
        return True
    else:
        return False


class Notifications:
    heightCountLow = 0
    heightCountHigh = 0

    distanceCountFar = 0
    distanceCountClose = 0

    cOffsetCount = 0
    eyeAngleOffsetCount = 0
    user = None

    def __init__(self, user):
        if user is not None:
            self.user = user

    def heightTrackerHigh(self):
        if self.user.height >= HEIGHT_MAX:
            self.heightCountHigh += 1
        else:
            self.heightCountHigh = 0

        if eligibleNotificationChecker(self.heightCountHigh, "You are sitting too high"):
            self.heightCountHigh = 0

    def heightTrackerLow(self):
        if self.user.height <= HEIGHT_MIN:
            self.heightCountLow += 1
        else:
            self.heightCountLow = 0

        if eligibleNotificationChecker(self.heightCountLow, "You are sitting too low"):
            self.heightCountLow = 0

    def distanceTrackerFar(self):
        if self.user.distance >= DISTANCE_MAX:
            self.distanceCountFar += 1
        else:
            self.distanceCountFar = 0

        if eligibleNotificationChecker(self.distanceCountFar, "You are too far from the monitor"):
            self.distanceCountFar = 0

    def distanceTrackerClose(self):
        if self.user.distance <= DISTANCE_MIN:
            self.distanceCountClose += 1
        else:
            self.distanceCountClose = 0

        if eligibleNotificationChecker(self.distanceCountClose, "You are too close to the monitor"):
            self.distanceCountClose = 0

    def centreOffsetTracker(self):
        if self.user.centreOffset >= C_OFFSET_MAX:
            self.cOffsetCount += 1
        else:
            self.cOffsetCount = 0

        if eligibleNotificationChecker(self.cOffsetCount, "You are not sitting directly in front of your monitor"):
            self.cOffsetCount = 0

    def eyeAngleTracker(self):
        if self.user.eyeAngle >= EYE_ANGLE_MAX:
            self.eyeAngleOffsetCount += 1
        else:
            self.eyeAngleOffsetCount = 0

        if eligibleNotificationChecker(self.eyeAngleOffsetCount, "Eye Angle Offset"):
            self.eyeAngleOffsetCount = 0
