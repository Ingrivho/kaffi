from arbitrator import Arbitrator

class BBCON:
    def __init__(self, behaviors, sensobs, motobs, arbitrator):
        self.behaviors = behaviors
        self.active_behaviors = []
        self.inactive_behaviors = []
        self.sensobs = sensobs
        self.motobs = motobs
        self.arbitrator = arbitrator

    def add_behavior(self, behavior):
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        if sensob not in self.sensobs:
            self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        if behavior in self.behaviors and behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        if behavior in self.behaviors and behavior not in self.inactive_behaviors:
            self.inactive_behaviors.append(behavior)

    def run_one_timestep(self):
        for sensob in self.sensobs:
            sensob.update()

        for behavior in self.behaviors:  # Or in self.active_behaviors?
            behavior.update()  # Must be run with sensob values as received through sensob.update() above

        motor_rec, halt_req = self.arbitrator.choose_action()
        for motob in self.motobs:
            motob.update(motor_rec)  # Remember: Each motob must be updated with its corresponding MRs, so this won't work
