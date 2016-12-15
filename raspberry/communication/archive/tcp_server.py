import socketserver
import subprocess

def getIP():
	return subprocess.check_output("/sbin/ifconfig").split(b'\n')[1].split()[1][5:]

class MyTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):	
		self.data = self.request.recv(256).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		# just send back the same data, but upper-cased
		self.request.sendall(self.data.upper())

def runServer():
	HOST, PORT = getIP(), 5005

	# Create the server, binding to localhost on port 9999
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
