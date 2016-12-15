import serial

class Communication:

	def __init__(self):
		self.newfile = open('test.bin', 'wb')
		self.ser = serial.Serial('/dev/ttyUSB0', 115200)

	def send(self, command):
		print(bytearray([command]))
		self.ser.write(bytearray([command]))
		self.newfile.write(bytearray([command]))
