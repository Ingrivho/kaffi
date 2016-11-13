from arbitrator import Arbitrator
from zumo_button import ZumoButton
from led import Led

class Bbcon():
    def __init__(self):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motobs = []
        self.arbitrator = Arbitrator();
        self.active = True

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        self.sensobs.append(sensob)

    def add_motob(self, motob):
        self.motobs.append(motob)

    def activate_behavior(self, behavior):
        if behavior in self.behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    def activate_all_behaviors(self):
        for b in self.behaviors:
            self.activate_behavior(b)

    def get_active_behaviors(self):
        return self.active_behaviors

    def halt_request(self):
        self.active = False
        for m in self.motobs:
            m.stop()
        Led().pulse(10, 0.1)

    def run_one_timestep(self):
        # Update all sensobs
        self.update_sensobs()

        # Update all behaviours
        self.update_behaviors()

        # Invoke the arbitrator
        recommendations = self.arbitrator.choose_action(self.active_behaviors)

        # Update all motobs based on the above
        print(recommendations)
        self.update_motors(recommendations)

        # Exits if button is pressed again
        if ZumoButton().check_if_pressed() == 0:
            self.halt_request()

        # Resets sensors
        self.reset_sensobs()

    def update_sensobs(self):
        for sensob in self.sensobs:
            sensob.update()

    def reset_sensobs(self):
        for sensob in self.sensobs:
            sensob.reset()

    def update_behaviors(self):
        for behavior in self.behaviors:
            behavior.update()

    def update_motors(self, recommendation):
        for motob in self.motobs:
            motob.update(recommendation)



