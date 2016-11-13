from operator import attrgetter

from motob import Motob


class Arbitrator():
	def __init__(self):
		pass

	def choose_action(self, behaviors):
		result = behaviors[0]
		for behavior in behaviors:
			# print (behavior, behavior.weight)
			if behavior.weight > result.weight:
				result = behavior
		# print("Doing: ", result)
		return result.motor_recommendation
