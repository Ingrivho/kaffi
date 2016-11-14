import behavior as

class Patrol(Behavior):

    def __init__(self, bbcon, sensobs, priority,active_flag = False, halt_request = False):
        Behavior.__init__(self, bbcon, sensobs, priority,active_flag = False, halt_request = False)

    def consider_activation(self):
        if self.bbcon.arbitrator.last_behavior == 3:
            self._activate()

    def consider_deactivation(self):
        if self.bbcon.arbitrator.last_behavior == 1:
            self._deactivate()

    def get_match_degree(self):
        sensor = self.sensobs[0]
        if sum(sensor) > 1.5 and max(sensor) - min(sensor) < 0.25:
            self.match_degree = 0
            return self.match_degree
        elif sum(sensor) > 1.5 and max(sensor) - min(sensor) < 0.25:
            line_pos = self._get_line_pos()
            if line_pos == -1:
                self.match_degree = 0
                return self.match_degree
            self.match_degree = abs(line_pos - 2.5)/2.5
        else:
            self.match_degree = 1.0
            return self.match_degree

    def _get_line_pos(self):
        sensor = self.sensobs[0]
        left = None
        right = None
        for i in range(sensor):
            if sensor[i] < 0.2:
                left = i
                break
        for o in range(sensor):
            if sensor[sensor.__len__() - 1 - o] < 0.2:
                right = o
                break

        if left != None and right != right:
            return (left + right) / 2
        else:
            return -1

    def sense_and_act(self):
        line_pos = self._get_line_pos()
        if line_pos < 2.5:
            self.motor_recommendations = ["turn_direction('left'," + str(abs(line_pos - 2.5)/2.5) +", 0.1)"]
        elif line_pos > 2.5:
            self.motor_recommendations = ["turn_direction('right'," + str(abs(line_pos - 2.5) / 2.5) + ", 0.1)"]
        else:
            self.motor_recommendations = ["go_direction('forward', 1.0, 0.1"]