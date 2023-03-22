class Box:
    def __init__(self, location, size, color, ground_height):
        self.location = location
        self.size = size
        self.color = color
        self.ground_height = ground_height
        self.vertical_speed = 0

        self.grabbedPosition = False

    def gravity(self):
        if self.grabbedPosition:
            return
        if self.location[1] + self.size / 2 + self.vertical_speed < self.ground_height:
            self.location[1] += self.vertical_speed
            self.vertical_speed += 1
        else:
            self.location[1] = self.ground_height - self.size / 2
            self.vertical_speed = 0

    def getRect(self):
        return [int(self.location[0] - self.size / 2), int(self.location[1] - self.size / 2), int(self.size), int(self.size)]

    def grab(self, grabberLocation):
        if (grabberLocation[0] - self.size / 2 < self.location[0] < grabberLocation[0] + self.size / 2) and (
                grabberLocation[1] - self.size / 2 < self.location[1] < grabberLocation[1] + self.size / 2):
            self.grabbedPosition = [self.location[0] - grabberLocation[0], self.location[1] - grabberLocation[1]]
        else:
            self.grabbeedPosition = False

    def ungrab(self):
        self.grabbedPosition = False

    def grabberMoving(self, grabberLocation):
        if self.grabbedPosition:
            self.location = [grabberLocation[0] + self.grabbedPosition[0], grabberLocation[1] + self.grabbedPosition[1]]
