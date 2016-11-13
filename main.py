from zumo_button import ZumoButton
from camera import Camera
from reflectance_sensors import ReflectanceSensors
from ultrasonic import Ultrasonic
from led import Led
from sensobs import *
from behaviour import *
from arbitrator import Arbitrator
from motob import Motob
from bbcon import Bbcon

def main():
	print("Press the button")
	Led().light_on()
	ZumoButton().wait_for_press()
	Led().light_off()
	print("Button pressed")

	# Sensors
	camera_sensor = Camera(img_width=200, img_height=25)
	reflectance_sensor = ReflectanceSensors()
	ultrasonic_sensor = Ultrasonic()

	# Other
	led = Led()
	led.light_off()

	# Sensobs
	camera_sensob = CameraSensob(camera_sensor)
	reflectance_sensob = ReflectanceSensob(reflectance_sensor)
	ultrasonic_sensob = Sensob(ultrasonic_sensor)

	# Motobs
	motob = Motob()

	# Controller
	bbcon = Bbcon()

	# Behaviors
	moveForward_behavior = MoveForward(None, 1, bbcon)
	avoidCollision_behavior = AvoidCollision(ultrasonic_sensob, 4, bbcon)
	followColor_behavior = FollowColor(camera_sensob, 6, bbcon)
	pauseAtLines_behavior = PauseAtLines(reflectance_sensob, 8, bbcon)
	stopCloseColor_behavior = StopCloseColor(camera_sensob, 10, bbcon)

	# Add all sensobs to controller
	bbcon.add_sensob(camera_sensob)
	bbcon.add_sensob(reflectance_sensob)
	bbcon.add_sensob(ultrasonic_sensob)

	# Add all Behaviors to controller
	bbcon.add_behavior(avoidCollision_behavior)
	bbcon.add_behavior(moveForward_behavior)
	bbcon.add_behavior(followColor_behavior)
	bbcon.add_behavior(pauseAtLines_behavior)
	bbcon.add_behavior(stopCloseColor_behavior)

	bbcon.activate_all_behaviors()
	# Add all motobs to controller
	bbcon.add_motob(motob)

	print("starting")

	try:
		while bbcon.active:
			bbcon.run_one_timestep()

	except:
		print("Failed")
		motob.stop()
		print(sys.exc_info()[0])

main()