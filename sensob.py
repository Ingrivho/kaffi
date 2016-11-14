class Sensob:
    def __init__(self, sensor):
        self.sensor = sensor
        self.value = None
        self.update()

    def update(self):
        """
        The main method for a sensob is update, which should force the sensob to fetch the relevant sensor value(s)
        and convert them into the pre-processed sensob value. This should only need to be done once each timestep.
        So even if several behaviors share the same sensob, S, there should be no need for S to update more than
        once each timestep.
        """
        self.sensor.update()
        self.value = self.sensor.get_value()

    def get_value(self):
        return self.value

    def reset(self):
        self.sensor.reset()

