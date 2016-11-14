from basic_robot.motors import Motors


class Motob:
    def __init__(self):
        self.motor = Motors()
        self.value = ("S", 0) #a holder of the most recent motor recommendation sent to the motob

    def update(self, motor_recommendation):
        """receive a new motor recommendation, load it into the value slot, and operationalize it."""
        self.value = motor_recommendation
        self.operationalize()

    def operationalize(self):
        """convert a motor recommendation into one or more motor settings, which are sent to
the corresponding motor(s)"""
        command = self.value[0]
        speed = self.value[1]
        duration = 0.2

        if command == "L":
            self.motor.left(speed, duration)
        elif command == "R":
            self.motor.right(speed, duration)
        elif command == "F":
            self.motor.forward(speed, duration)
        elif command == "B":
            self.motor.backward(speed, duration)
        elif command == "S":
            self.motor.stop()
        elif command == "LF":
            self.motor.set_value((speed/2, speed), duration)
        elif command == "RF":
            self.motor.set_value((speed, speed/2), duration)
