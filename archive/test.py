import serial
ser = serial.Serial('/dev/ttyUSB0', 115200)
ser.write(chr(207));
ser.write(chr(201));
ser.write(chr(90)); 