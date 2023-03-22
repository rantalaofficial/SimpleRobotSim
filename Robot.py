import math
import random

class Robot:
    def __init__(self, arm1Length, arm2Length, robotBasePositionX, robotBasePositionY, groundHeight):
        self.arm1Length = arm1Length
        self.arm2Length = arm2Length
        self.robotBasePosition = [robotBasePositionX, robotBasePositionY]
        self.groundHeight = groundHeight

        self.angles = [-math.pi / 2, math.pi / 2]

        self.waypoints = []
        self.waypointDistance = 10

    def clearTrajectory(self):
        self.waypoints = []

    def atTargetAngles(self):
        return abs(self.angles[0] - self.targetAngles[0]) < 0.01 and abs(self.angles[1] - self.targetAngles[1]) < 0.01
    
    def addWaypoint(self, waypoint):
        if (len(self.waypoints) > 0):
            lastWaypoint = self.waypoints[len(self.waypoints) - 1]
        else:
            lastWaypoint = self.getArmCoords()[1][2:4]

        errorLocation = [waypoint[0] - lastWaypoint[0], waypoint[1] - lastWaypoint[1]]

        distance = max(0.1, math.sqrt(errorLocation[0] ** 2 + errorLocation[1] ** 2))
        waypointAmount = math.ceil(distance / self.waypointDistance)
        for i in range(0, waypointAmount + 1):
            newWaypoint = [lastWaypoint[0] + errorLocation[0] * i / waypointAmount, lastWaypoint[1] + errorLocation[1] * i / waypointAmount]

            waypointDistanceToRobotBase = math.sqrt((newWaypoint[0] - self.robotBasePosition[0]) ** 2 + (newWaypoint[1] - self.robotBasePosition[1]) ** 2)
            if waypointDistanceToRobotBase < self.arm1Length + self.arm2Length:
                self.waypoints.append([lastWaypoint[0] + errorLocation[0] * i / waypointAmount, lastWaypoint[1] + errorLocation[1] * i / waypointAmount])

    def gotoWaypoint(self):
        if len(self.waypoints) > 0:
            self.gotoLocation(self.waypoints[0])
            if self.atTargetAngles():
                self.waypoints.pop(0)

    def angleDifference(self, angle1, angle2):
        angleDifference = angle1 - angle2
        if angleDifference > math.pi:
            angleDifference -= 2 * math.pi
        if angleDifference < -math.pi:
            angleDifference += 2 * math.pi
        return angleDifference


    def angleDifference(self, angle1, angle2):
        diff = (angle2 - angle1 + math.pi) % (2 * math.pi) - math.pi
        return diff if diff < -math.pi else diff

    def gotoLocation(self, targetCoords):
        self.targetAngles = self.inverseKinematics(targetCoords)

        angle1Error = self.targetAngles[0] - self.angles[0]
        angle2Error = self.targetAngles[1] - self.angles[1]

        self.angles[0] += angle1Error 
        self.angles[1] += angle2Error 

        return self.atTargetAngles()

    def getArmCoords(self):
        arm1EndCoords = self.angle1forwardKinematics(self.angles[0])
        arm2EndCoords = self.angle2forwardKinematics(self.angles[0], self.angles[1])

        return [
            [self.robotBasePosition[0], self.robotBasePosition[1], arm1EndCoords[0], arm1EndCoords[1]],
            [arm1EndCoords[0], arm1EndCoords[1], arm2EndCoords[0], arm2EndCoords[1]],
        ]

    def getGrabberCoords(self):
        arm2EndCoords = self.angle2forwardKinematics(self.angles[0], self.angles[1])
        return [arm2EndCoords[0], arm2EndCoords[1]]

    def inverseKinematics(self, targetCoords):
        x = (targetCoords[0] - self.robotBasePosition[0])
        y = min(self.groundHeight - self.robotBasePosition[1], targetCoords[1] - self.robotBasePosition[1])

        r = math.sqrt(x**2 + y**2)
        if r > self.arm1Length + self.arm2Length:
            return self.angles

        l1 = self.arm1Length
        l2 = self.arm2Length
        theta2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2))
        if math.sin(theta2) != 0:
            theta1_1 = math.atan2(y, x) - math.atan2(l2*math.sin(theta2), l1 + l2*math.cos(theta2))
            theta1_2 = math.atan2(y, x) - math.atan2(-l2*math.sin(theta2), l1 + l2*math.cos(theta2))
        else:
            theta1_1 = math.atan2(y-l2*math.sin(theta2), x-l1-l2*math.cos(theta2))
            theta1_2 = None

        if (x < 0 and theta1_2 is not None):
            return theta1_2, -theta2

        return theta1_1, theta2

    def angle1forwardKinematics(self, angle1):
        x = self.robotBasePosition[0] + self.arm1Length * math.cos(angle1)
        y = self.robotBasePosition[1] + self.arm1Length * math.sin(angle1)
        return x, y

    def angle2forwardKinematics(self, angle1, angle2):
        x = self.robotBasePosition[0] + self.arm1Length * math.cos(angle1) + self.arm2Length * math.cos(angle1 + angle2)
        y = self.robotBasePosition[1] + self.arm1Length * math.sin(angle1) + self.arm2Length * math.sin(angle1 + angle2)
        return x, y



