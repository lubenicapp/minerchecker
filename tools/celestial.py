from real_math import *
import time

class Celestial:

    def __init__(self, orbit):
        self.orbit = orbit
        self.distance = self.orbit[1][0]
        self.angle = self.orbit[1][1]
        self.x = self.orbit[0][0]
        self.y = self.orbit[0][1]
        self.rotation_speed = float(self.orbit[2])
        self.creation_time = self.orbit[3]

    def get_current_angle(self, ts = time.time()):
        if (self.distance == 0):
            return self.angle
        speedReal = toReal(self.rotation_speed)
        distanceReal = toReal(self.distance)
        radiansAngularSpeedInReal = div(speedReal, distanceReal)
        timeDiffReal = toReal(ts - self.creation_time)
        angleToAddRadianReal = mul(radiansAngularSpeedInReal, timeDiffReal)
        angleToAddDegree = realRadianToDegree(angleToAddRadianReal)
        return (angleToAddDegree + self.angle) % toReal(360)

    def current_cartesian_position(self, ts = time.time()):
        currentAngleReal = self.get_current_angle(ts)
        currentAngleRadians = realDegreeToRadian(currentAngleReal)
        angleCos = cos(currentAngleRadians)
        angleSin = sin(currentAngleRadians)
        distanceReal = toReal(self.distance)
        x = fromReal(round(mul(distanceReal, angleCos))) + self.x
        y = fromReal(round(mul(distanceReal, angleSin))) + self.y
        return [x, y]
