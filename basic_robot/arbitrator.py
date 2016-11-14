from bbcon import BBCON

class Arbitrator:
    def __init__(self):
        self.bbcon = None

    def choose_action(self):
        behaviors = self.bbcon.active_behaviors

        # TODO: Choose which behavior wins, assign motor_recs and halt_req to variables below
        motor_rec = None
        halt_req = None

        return motor_rec, halt_req
