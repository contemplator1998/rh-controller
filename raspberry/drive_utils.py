from enum import IntEnum
import communication

class Drive_utils:
	
	class COMMANDS(IntEnum):
		set_angle = 201
		set_servo0 = 202
		set_servo1 = 203
		set_servo2 = 204
		set_servo3 = 205
		set_servo4 = 206
		set_servo5 = 207
		set_servo6 = 208
		set_servo7 = 209
		set_mode0 = 210
		set_mode1 = 211
		set_grasp0 = 212
		set_grasp1 = 213
		set_start_velosity = 214
		set_stop_velosity = 215
		set_repeat_start = 216
		set_repeat_stop = 217
		set_divisor_start = 218
		set_divisor_stop = 219
		set_max_angle = 220
		set_min_angle = 221
		set_position = 222

	def __init__(self):
		self.comm = communication.Communication()

	def configure(self, drive):
		motor_command = self.COMMANDS.set_servo0 + drive;
		self.comm.send(motor_command)
		print('Set start velocity: {0}'.format(50))
		print('Set stop velocity: {0}'.format(50))
		self.comm.send(self.COMMANDS.set_start_velosity)
		self.comm.send(50)
		self.comm.send(self.COMMANDS.set_stop_velosity)
		self.comm.send(50)
		

	def move(self, drive, angle):
		if drive < 0 or drive > 7:
			raise DriveIndexError("Drive index is out of range!")
		motor_command = self.COMMANDS.set_servo0 + drive;
		print('Moving {0} drive to {1}'.format(drive, angle))
		print('Using {0} command'.format(motor_command))
		self.comm.send(motor_command)
		self.comm.send(self.COMMANDS.set_angle)
		self.comm.send(angle)


x = Drive_utils()
x.configure(5)
x.move(5, 90)
x.move(4, 18)
x.move(3, 7)
x.move(2, 165)
x.move(1, 90)
x.move(0, 180)

