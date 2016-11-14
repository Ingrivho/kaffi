from abc import abstractmethod
from camera import Camera
from PIL import Image
from imager2 import Imager
import time

class Sensob(object):
	def __init__(self, sensor):
		self.sensor = sensor
		self.value = 0

	@abstractmethod
	def update(self):
		self.value = self.sensor.update()

	def reset(self):
		self.sensor.reset()

# Finds the average center of a color on image taken
class CameraSensob(Sensob):
	def __init__(self, sensor):
		super(CameraSensob, self).__init__(sensor)

	def analyze_picture(self, image):
		x, y = image.size
		center, step = x/2, 1

		l = list()
		for i in range(0, x, step):
			for j in range(0, y, step):
				r,g,b = image.getpixel((i,j))
				if (r<100 and g > 120 and b < 100): # GREEN
					l.append(i)

		# print("float value: ", float(len(l)/(x*y)))
		if (float(len(l)/(x*y)) >= 0.004):
			# print("offset:", (sum(l)/len(l)/center)-1)
			return ((sum(l)/len(l)/center)-1, float(len(l)/(x*y)))
		return (0, 0)

	def update(self):
		image = self.sensor.update()
		if False: # True = save image
			img = Imager(image=image)
			img.dump_image("img.jpeg")
		self.value = self.analyze_picture(image)

# Checks if sensor finds dark spots
class ReflectanceSensob(Sensob):
	def __init__(self, sensor):
		super(ReflectanceSensob, self).__init__(sensor)

	def calculate_input(self):
		ir_values = self.sensor.update()
		for v in ir_values:
			print(v)
			if v <0.1:
				return 1
		return 0

	def update(self):
		self.value = self.calculate_input()

# Sets the value to distance to wall
class UltrasonicSensob(Sensob):
	def __init__(self, sensor):
		super(UltrasonicSensob, self).__init__(sensor)

	def update(self):
		self.value = self.sensor.update()