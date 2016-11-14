#! python3

from basic_robot.camera import Camera
from basic_robot.irproximity_sensor import IRProximitySensor
from basic_robot.reflectance_sensors import ReflectanceSensors
from basic_robot.ultrasonic import Ultrasonic
from basic_robot.zumo_button import ZumoButton
from arbitrator import Arbitrator
import behavior
from motob import Motob
from sensob import Sensob
import time
from basic_robot.motors import Motors


class BBCon:
    def __init__(self):
        #cam = Camera(img_width=300, img_height=200)
        #print(cam.update())

        self.arbitrator = Arbitrator(self) # the arbitrator object that will resolve actuator requests produced by the behaviors
        self.motob = Motob() # the single motor object used by the bbcon
        self.sensobs = {
            #"C": Sensob(Camera()),
            "I": Sensob(IRProximitySensor()),
            "R": Sensob(ReflectanceSensors()),
            #"U": Sensob(Ultrasonic())
        } # list of all sensory objects used by the bbcon
        self.behaviors = [
            #behavior.AvoidObstacleFront(self),
            behavior.AvoidObstacleSides(self),
            behavior.walkRandomly(self),
            behavior.walkStraight(self),
            behavior.detectVictory(self)
        ]  # list of all the behavior objects used by the bbcon
        self.active_behaviors = self.behaviors  # list of all the behaviors that are currently active
        self.motor_command = ("S", False)


        self.debug_motor = Motors()

    def activate_behavior(self):
        """"add an existing behavior onto the active-behaviors list"""

    def deactive_behavior(self):
        """remove an existing behavior from the active behaviors list"""

    def run_one_timestep(self):
        """
        constitutes the core BBCON
        activity. It should perform (at least) the following actions on each call:
        1. Update all sensobs - These updates will involve querying the relevant sensors for their values, along
        with any pre-processing of those values (as described below)
        2. Update all behaviors - These updates involve reading relevant sensob values and producing a motor
        recommendation.
        3. Invoke the arbitrator by calling arbitrator.choose action, which will choose a winning behavior and
        return that behavior's motor recommendations and halt request flag.
        4. Update the motobs based on these motor recommendations. The motobs will then update the settings
        of all motors.
        5. Wait - This pause (in code execution) will allow the motor settings to remain active for a short period
        of time, e.g., one half second, thus producing activity in the robot, such as moving forward or turning.
        6. Reset the sensobs - Each sensob may need to reset itself, or its associated sensor(s), in some way
        """
        print("new timestep", self.motor_command)


        for i in self.sensobs:
            self.sensobs[i].update()
        for i in range(len(self.active_behaviors)):
            behavior = self.active_behaviors[i]
            behavior.update()
            print(behavior.__class__.__name__ + ": " + str(behavior.weight), behavior.motor_recommendation)
        command = self.arbitrator.choose_action()
        print("Command:", command)
        self.motor_command = command
        self.motob.update(command[0])
        #time.sleep(0.1)
        for i in self.sensobs:
            self.sensobs[i].reset()

if __name__ == '__main__':
    bb = BBCon()
    print("ready to run first timestep")
    ZumoButton().wait_for_press()
    bb.motob = Motob()
    while True:
        bb.run_one_timestep()
