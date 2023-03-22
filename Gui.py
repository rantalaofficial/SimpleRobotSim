import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Robot import Robot
from Box import Box

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ROBOT_LOCATION = [SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.70]
GROUND_HEIGHT = SCREEN_HEIGHT * 0.9
ARM_LENGTH = SCREEN_HEIGHT * 0.4
ROBOT_BASE_WIDTH = SCREEN_WIDTH * 0.05
robot = Robot(ARM_LENGTH, ARM_LENGTH, ROBOT_LOCATION[0], ROBOT_LOCATION[1], GROUND_HEIGHT)

box = Box([400, 100], 100, "", GROUND_HEIGHT)

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.timer = QTimer()
        self.timer.setInterval(int(1000 / 60))  # 60 fps
        self.timer.timeout.connect(self.updateCanvas)
        self.timer.start()

        self.UI()
        
    def UI(self):
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.move(15, 15)

        self.label = QLabel("Robot speed: " + str(self.slider.value()), self)
        self.label.move(35, 40)
        self.label.resize(200, 50)

        self.toggleButton = QPushButton("Grabber: OFF", self)
        self.toggleButton.setCheckable(True)
        self.toggleButton.move(20, 100)
        self.toggleButton.resize(120, 50)
        self.toggleButton.clicked.connect(self.toggleButtonClicked)

        self.clearButton = QPushButton("Clear trajectory", self)
        self.clearButton.move(20, 160)
        self.clearButton.resize(120, 50)
        self.clearButton.clicked.connect(self.clearButtonClicked)

        self.slider.valueChanged.connect(self.updateLabel)

        
        self.setWindowTitle("Robot")
        self.setGeometry(100, 100, 800, 800)
        self.show()

    def clearButtonClicked(self):
        robot.clearTrajectory()

    def updateLabel(self):
        sliderValue = self.slider.value()
        robot.waypointDistance = sliderValue / 10
        self.label.setText("Robot speed: " + str(sliderValue))

    def toggleButtonClicked(self):
        if self.toggleButton.isChecked():
            self.toggleButton.setText("Grabber: ON")
            self.toggleButton.setStyleSheet("background-color: green")
            box.grab(robot.getGrabberCoords())
        else:
            self.toggleButton.setText("Grabber: OFF")
            self.toggleButton.setStyleSheet("background-color: None")
            box.ungrab()
    def paintEvent(self, event):
        painter = QPainter(self)
        
        robot.gotoWaypoint()
        self.lines = robot.getArmCoords()

        rectBounds = box.getRect()
        box.grabberMoving(robot.getGrabberCoords())
        box.gravity()
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        painter.drawRect(rectBounds[0], rectBounds[1], rectBounds[2], rectBounds[3])

        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        painter.drawRect(0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        painter.drawRect(ROBOT_LOCATION[0] - ROBOT_BASE_WIDTH / 2, ROBOT_LOCATION[1], ROBOT_BASE_WIDTH, GROUND_HEIGHT - ROBOT_LOCATION[1])


        i = 1
        for line in self.lines:
            painter.setPen(QPen(Qt.black, 20 / i, Qt.SolidLine))
            painter.drawLine(line[0], line[1], line[2], line[3])
            painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            painter.drawEllipse(line[0] - 12.5, line[1] - 12.5, 25, 25)
            painter.drawEllipse(line[2] - 12.5, line[3] - 12.5, 25, 25)

            i += 1
        

        i = 1
        for waypoint in robot.waypoints:
            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            painter.drawEllipse(waypoint[0], waypoint[1], 5, 5)
            i += 1


    def mousePressEvent(self, event):
        robot.addWaypoint([event.x(), event.y()])

    def mouseMoveEvent(self, event):
        self.targetCoords = [event.x(), event.y()]

    def updateCanvas(self):
        self.update()
        


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()

        self.setCentralWidget(self.canvas)

        self.setGeometry(100, 100, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowTitle('Robot Simulator')

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())