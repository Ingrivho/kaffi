class Arbitrator:
    def __init__(self, bbcon):
        self.bbcon = bbcon # The arbitrator may include an instance variable housing a pointer to the bbcon, such that the arbitrator can easily fetch all of the bbcon’s active behaviors

    def choose_action(self):
        """
        check all of the active behaviors and pick a winner

        This choice can either be very simple: pick the behavior with the highest weight; or it can include an element
        of stochasticity. In this latter case, the arbitrator makes a random, but biased, choice among the behaviors,
        with bias stemming from the behavior weights.

        Regardless of the selection strategy, choose action should return a tuple containing:
        1. motor recommendations (one per motob) to move the robot, and
        2. a boolean indicating whether or not the run should be halted.
        """
        behaviors = self.bbcon.active_behaviors

        motor_recommendation = None
        highest_weight = float("-inf")
        halt = False
        for behavior in behaviors:
            print("arb", behavior.__class__.__name__, behavior.weight, behavior.motor_recommendation)
            if behavior.weight > highest_weight:
                motor_recommendation = behavior.motor_recommendation
                halt = behavior.halt_request
                highest_weight = behavior.weight
        command = (motor_recommendation, halt)
        return command


