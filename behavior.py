import time
import random
from sensob import Sensob
from basic_robot.camera import Camera
from PIL import Image, ImageSequence, ImageEnhance, ImageFilter, ImageOps


class Behavior:
    def __init__(self, bbcon):
        self.bbcon = bbcon
        self.sensobs = self.bbcon.sensobs
        self.motor_recommendation = ("S", 0.123) # a recommendation that this behavior provides to the arbitrator. In this assignment, we assume that ALL motobs (and there will only be one or a small few) are used by all behaviors
        self.active_flag = False  # boolean variable indicating that the behavior is currently active or inactive
        self.halt_request = False  # some behaviors can request the robot to completely halt activity (and thus end the run)
        self.priority = 0  # a static, pre-defined value indicating the importance of this behavior
        self.match_degree = 0  # a real number in the range [0, 1] indicating the degree to which current conditions warrant the performance of this behavior
        self.weight = self.priority * self.match_degree  # the product of the priority and the match degree, which the arbitrator uses as the basis for selecting the winning behavior for a timestep

    def consider_deactivation(self):
        """whenever a behavior is active, it should test whether it should deactivate"""
        pass

    def consider_activation(self):
        """whenever a behavior is inactive, it should test whether it should activate"""
        pass

    def update(self):
        if self.active_flag:
            self.match_degree = 0
            self.consider_deactivation()
            self.sense_and_act()
            self.weight = self.priority * self.match_degree
        else:
            self.consider_activation()
        """
        the main interface between the bbcon and the behavior

        The call to update will initiate calls to these other methods, since an update will involve the following
        activities:
        * Update the activity status - Each behavior will have its own tests for becoming active or inactive.
        Some behaviors may be active all of the time, so the tests are trivial, whereas other behaviors may be
        computationally expensive to run and thus the bbcon can spare resources if it shuts them off in cases
        where they are clearly not needed. For example, behaviors that require camera images, particularly
        images that are preprocessed by sensobs, are expensive. If all behaviors that use a particular camerabased
        sensob are inactive, then the expensive image-processing computations can be avoided for that
        period of inactivity. Hence, when a behavior becomes active or inactive, its sensobs should be informed
        of the status change so that they too may activate or deactivate. Of course, for sensobs that are used
        by two or more behaviors, some simple extra bookkeeping is required: if sensob S is used by both
        behaviors A and B, then S can only deactivate when both A and B are inactive.
        * Call sense and act
        * Update the behavior's weight - Use the match degree (calculated by sense and act) multiplied by the
        behavior's user-defined priority.
        """

    def sense_and_act(self):
        """
        the core computations performed by the behavior that use sensob readings to produce
        motor recommendations (and halt requests)

        The central computation of a behavior occurs in its sense and act method. The activity in this method
        will be highly specialized for each behavior but will typically involve gathering the values of its sensobs (and
        possibly checking for relevant posts on the bbcon). Using that information, the behavior will then determine
        motor recommendations, and possibly a halt request. It must also set the match degree slot to a real value
        in the range [0, 1].
        In some cases, a behavior may require instance variables that maintain some memory of previous states of
        the sensobs. For instance, a red-object tracking behavior might record the fraction of red in the previous
        camera image and then compare it to the fraction in the current image to determine the movement of the
        red object relative to the agent. Similarly, a line-following behavior may want to record a series of recent
        line readings to indicate whether the agent is successfully staying on the line or gradually losing touch with
        it
        """


"""
    AvoidObstacleFront skal bare undersøke hvor langt det er til
    det som er foran roboten og stoppe og svinge f.eks. 90 grader
    til venstre om det kommer for nære.
"""
class AvoidObstacleFront(Behavior):


    def __init__(self, bbcon):
        Behavior.__init__(self, bbcon)
        self.priority = 5 # ganske viktig så det burde ha høy prioritet?
        self.ultrasonic = self.sensobs["U"] # klassenavnet på sensoben må endres til det som Mathilde kaller den, her ultrasonic
        self.active_flag = True # antar at dette er en behavior som alltid er aktiv så lenge roboten er i bevegelse
        self.motor_recommendation = ("S", 0)

    def sense_and_act(self):
        frontDistance = self.ultrasonic.get_value() #frontDistance vil være avstanden som blir hentet fra ultrasonic-sensoren
        print("FrontDistance =", frontDistance)
        if frontDistance < 5 and frontDistance != 0:
            self.match_degree = 1
        else:
            self.match_degree = 0

"""
    AvoidObstacleSides bruker IRproximity-sensoren og svinger vekk
    fra vegger som kommer for nære på siden.
"""
class AvoidObstacleSides(Behavior):

    def __init__(self, bbcon):
        Behavior.__init__(self, bbcon)
        self.priority = 5
        self.IRproximity = self.sensobs["I"]
        self.active_flag = True

    def sense_and_act(self):
        rightSensorIndex = 0
        leftSensorIndex = 1
        speed = 0.5
        if self.IRproximity.get_value()[rightSensorIndex]:
            self.match_degree = 1
            self.motor_recommendation = ("R", speed)
        if self.IRproximity.get_value()[leftSensorIndex]:
            self.match_degree = 1
            self.motor_recommendation = ("L", speed)


class walkRandomly(Behavior):

    def __init__(self, bbcon):
        Behavior.__init__(self, bbcon)
        self.priority = 3
        self.active_flag = True
        self.startTime = time.time()

    def sense_and_act(self):
        currentTime = time.time()
        timeElapsed = currentTime - self.startTime
        directionList = ["RF", "LF"]
        if timeElapsed > 5:
            self.match_degree = 1
            speed = random.uniform(0.2, 0.6)
            direction = random.choice(directionList)
            self.motor_recommendation = (direction, speed)
            self.startTime = time.time()

class walkStraight(Behavior):

    def __init__(self, bbcon):
        Behavior.__init__(self, bbcon)
        self.priority = 2
        self.active_flag = True

    def sense_and_act(self):
        self.match_degree = 1
        self.motor_recommendation = ("F", 0.5)
    
"""
    turnAwayFromObstacle er for å snu vekk fra hindringer
    som fått Roar til å stoppe.
"""
class turnAwayFromObstacle(Behavior):

    def __init__(self, bbcon):
        Behavior.__init__(self, bbcon)
        self.priority = 6   # denne må ha høyere prioritet enn AvoidObstacleFront, ellers så vil den aldri bli brukt
        self.active_flag = True
        self.ultrasonic = self.sensobs["U"]

    def sense_and_act(self):
        frontDistance = self.ultrasonic.get_value
        if self.bbcon.motor_command[0] == ("S", 0) and frontDistance < 10:
            self.match_degree = 1
            self.motor_recommendation = ("L", 1)


class detectVictory(Behavior):

    def __init__(self, bbcon):
        Behavior.__init__(self, bbcon)
        self.priority = 5
        self.active_flag = True
        self.reflectance = self.sensobs["R"]
        self.cam = Sensob(Camera(img_width=1, img_height=1))

    def sense_and_act(self):
        # TODO: hente og tolke verdier fra reflectance-sensorene og stoppe om det er en linje
        reflectanceList = self.reflectance.get_value()
        if reflectanceList[0] < 0.5 or reflectanceList[-1] < 0.5:
            self.match_degree = 1
            self.motor_recommendation = ("S", 0)
            self.cam.update()
            #im = Image.open("image.png")
            #im_rgb = im.convert("RGB")
            #r, g, b = im_rgb.getpixel((0,0))
            #print(r, g, b)
            print(self.cam.value)

