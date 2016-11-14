from motors import Motors

class Motob():
    def __init__(self):
        self.motor = Motors()
        self.action = None
        self.duration = None

    def update(self, motor_recommendation):
        if motor_recommendation is None:
            return
        self.action, self.duration = motor_recommendation
        self.operationalize(self.action, self.duration)

    def operationalize(self, action, duration):
        if action == 'F':
            self.motor.set_value((0.2, 0.2), duration)
        elif action == 'B':
            self.motor.set_value((-0.2, -0.2), duration)
        elif action == 'L':
            self.motor.set_value((-0.4, 0.4), duration)
        elif action == 'R':
            self.motor.set_value((0.4, -0.4), duration)
        elif action == 'S':
            self.motor.stop()
        elif action == 'LL':
            self.motor.set_value((-0.6, 0.6), duration)

    def stop(self):
        self.motor.stop()
