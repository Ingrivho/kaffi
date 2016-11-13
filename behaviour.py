from abc import abstractmethod
from PIL import Image
from random import randint

class Behaviour(object):
	def __init__(self, sensob, priority, bbcon):
		self.sensob = sensob
		self.priority = priority
		self.bbcon = bbcon

		self.motor_recommendation = 0
		self.match_degree = 0
		self.active_flag = True
		self.weight = 0

	def calculate_weight(self):
		self.weight = self.priority * self.match_degree

	@abstractmethod
	def set_match_degree(self):
		pass

	@abstractmethod
	def set_motor_recomendation(self):
		pass

	def consider_state(self):
		self.test()

	@abstractmethod
	def test(self):
		pass

	# If active update weight and recomendation, then consider new state for next run
	def update(self):
		self.set_motor_recomendation()
		self.set_match_degree()
		self.calculate_weight()
		self.consider_state()

# Robot moves forward
class MoveForward(Behaviour):
	def __init__(self, sensob, priority, bbcon):
		super(MoveForward, self).__init__(sensob, priority, bbcon)

	def set_match_degree(self):
		self.match_degree = 1.0

	def set_motor_recomendation(self):
		self.motor_recommendation = ('F', 8)

	def test(self):
		return True

# Follows a given color with camera
class FollowColor(Behaviour):
	def __init__(self, sensob, priority, bbcon):
		super(FollowColor, self).__init__(sensob, priority, bbcon)

	def set_match_degree(self):
		if self.sensob.value[0] == 0:
			self.match_degree = 0.0
		else:
			self.match_degree = 1.0

	def set_motor_recomendation(self):
		if abs(self.sensob.value[0]) <= 0.1:
			self.motor_recommendation = ('F', 8)
		elif self.sensob.value[0] > 0.3:
			# kjøre til høyre (R, 1)
			self.motor_recommendation = ('R', 2)
		elif self.sensob.value[0] < -0.3:
			# kjøre til venstre (L, 1)
			self.motor_recommendation = ('L', 2)

	def test(self):
		return True

# Stops the robot when very close to target
class StopCloseColor(Behaviour):
	def __init__(self, sensob, priority, bbcon):
		super(StopCloseColor, self).__init__(sensob, priority, bbcon)
		
	def set_match_degree(self):
		if self.sensob.value[1] >= 0.8:
			self.match_degree = 1.0
		else:
			self.match_degree = 0.0

	def set_motor_recomendation(self):
		if self.sensob.value[1] >= 0.8:
			self.motor_recommendation = ('S', 1)
			self.bbcon.halt_request()

	def test(self):
		return True

# Robot takes a break when black lines under it
class PauseAtLines(Behaviour):
	def __init__(self, sensob, priority, bbcon):
		super(PauseAtLines, self).__init__(sensob, priority, bbcon)
		self.n = 0

	def set_match_degree(self):
		self.match_degree = self.sensob.value

	def set_motor_recomendation(self):
		if self.sensob.value == 1:
			self.motor_recommendation = ('S', 32)

	def test(self):
		if self.sensob.value == 1 and self.active_flag:
			self.active_flag = False

		elif not self.active_flag:
			self.bbcon.deactivate_behavior(self)
			self.active_flag = True
		else:
			if not self in self.bbcon.active_behaviors:
				self.bbcon.activate_behavior(self)


# Makes sure the robot will not crash
class AvoidCollision(Behaviour):
	def __init__(self, sensob, priority,  bbcon):
		super(AvoidCollision, self).__init__(sensob, priority, bbcon)

	def set_match_degree(self):
		if self.sensob.value <= 15.0:
			self.match_degree = 1.0
		else:
			self.match_degree = 0

	def set_motor_recomendation(self):
		if self.sensob.value <= 15.0:
			self.motor_recommendation = ('LL', 8)

	def test(self):
		return True