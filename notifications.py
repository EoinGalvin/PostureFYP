from win11toast import notify
from configparser import ConfigParser

config = ConfigParser()


def eligibleNotificationChecker(value, message):
    if value >= 150:
        notify(message)
        return True
    else:
        return False


class Notifications:
    HEIGHT_MAX = 2
    HEIGHT_MIN = -3
    DISTANCE_MAX = 74
    DISTANCE_MIN = 40
    C_OFFSET_MAX = 4
    EYE_ANGLE_MAX = 8

    heightCountLow = 0
    heightCountHigh = 0

    distanceCountFar = 0
    distanceCountClose = 0

    cOffsetCount = 0
    eyeAngleOffsetCount = 0
    user = None

    def __init__(self, user):
        try:
            config.read('config.ini')
            self.HEIGHT_MAX = int(config.get('ergonomics', 'HEIGHT_MAX'))
            self.HEIGHT_MIN = int(config.get('ergonomics', 'HEIGHT_MIN'))
            self.DISTANCE_MAX = int(config.get('ergonomics', 'DISTANCE_MAX'))
            self.DISTANCE_MAX = int(config.get('ergonomics', 'DISTANCE_MIN'))
            self.C_OFFSET_MAX = int(config.get('ergonomics', 'C_OFFSET_MAX'))
            self.EYE_ANGLE_MAX = int(config.get('ergonomics', 'EYE_ANGLE_MAX'))
        except IOError:
            print("failed to read configuration file.")

        if user is not None:
            self.user = user

    def heightTrackerHigh(self):
        if self.user.height >= self.HEIGHT_MAX:
            self.heightCountHigh += 1
        else:
            self.heightCountHigh = 0

        if eligibleNotificationChecker(self.heightCountHigh, "You are sitting too high"):
            self.heightCountHigh = 0

    def heightTrackerLow(self):
        if self.user.height <= self.HEIGHT_MIN:
            self.heightCountLow += 1
        else:
            self.heightCountLow = 0

        if eligibleNotificationChecker(self.heightCountLow, "You are sitting too low"):
            self.heightCountLow = 0

    def distanceTrackerFar(self):
        if self.user.distance >= self.DISTANCE_MAX:
            self.distanceCountFar += 1
        else:
            self.distanceCountFar = 0

        if eligibleNotificationChecker(self.distanceCountFar, "You are too far from the monitor"):
            self.distanceCountFar = 0

    def distanceTrackerClose(self):
        if self.user.distance <= self.DISTANCE_MIN:
            self.distanceCountClose += 1
        else:
            self.distanceCountClose = 0

        if eligibleNotificationChecker(self.distanceCountClose, "You are too close to the monitor"):
            self.distanceCountClose = 0

    def centreOffsetTracker(self):
        if self.user.centreOffset >= self.C_OFFSET_MAX:
            self.cOffsetCount += 1
        else:
            self.cOffsetCount = 0

        if eligibleNotificationChecker(self.cOffsetCount, "You are not sitting directly in front of your monitor"):
            self.cOffsetCount = 0

    def eyeAngleTracker(self):
        if self.user.eyeAngle >= self.EYE_ANGLE_MAX:
            self.eyeAngleOffsetCount += 1
        else:
            self.eyeAngleOffsetCount = 0

        if eligibleNotificationChecker(self.eyeAngleOffsetCount, "Eye Angle Offset"):
            self.eyeAngleOffsetCount = 0
