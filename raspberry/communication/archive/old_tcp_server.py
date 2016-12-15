#!/usr/bin/env python

import subprocess
import socket

def getIP():
	return subprocess.check_output("/sbin/ifconfig").split(b'\n')[1].split()[1][5:]

TCP_IP = getIP()
print(TCP_IP)
#TCP_IP = socket.getfqdn()
#TCP_IP = socket.gethostname()  
#TCP_IP = '192.168.70.144'
TCP_PORT = 5005
BUFFER_SIZE = 50  # Normally 1024, but we want fast response
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
   
conn, addr = s.accept()
print ('Connection address:', addr)
while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	print ("received data:", data)
	conn.send(data)  # echo
conn.close()
