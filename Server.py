import socket
import threading

HEADER = 1024
PORT = 8080
SERVER = '192.168.1.248'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect!"

print("Server name " + socket.gethostname())
print("Socket ipv4 address " + SERVER)
print("Port number  = " + str(PORT))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Binds the server to the address specified
server.bind(ADDR)

MASTER = ()
SLAVES = []

#Handles connection between client and server
#runs for EACH CLIENT
def handle_client(connection, address):
	print(f"New connection {address} connected")
	
	if threading.activeCount() == 2:
		MASTER = (connection, address)
		connection.send('M'.encode(FORMAT))
	elif threading.activeCount() > 2:
		slave = (connection, address)
		SLAVES.append(slave)
		connection.send('S'.encode(FORMAT))
        
        
	connected = True
	while connected:
		#Blocking code until a message that conforms to the specifications are met
		#the parameter needs the number of bytes the message is going to take
		message_length = connection.recv(HEADER).decode(FORMAT)
		if message_length:
			message_length = int(message_length)
			message = connection.recv(message_length).decode(FORMAT)
			if(message == DISCONNECT_MESSAGE):
				connected = False
				print(f"{address} : Disconnecting")
		print(f"{address} {message}")
		connection.send("Message received".encode(FORMAT))
	connection.close()
	print(f"Active Connections {threading.activeCount() - 1}")

#Handles new connection
def start():
	server.listen()
	while True:
		#stores a socket object (connection) information (address)
		connection, address = server.accept()
		thread = threading.Thread(target = handle_client, args = (connection, address))
		thread.start()
		print(f"Active Connections {threading.activeCount() - 1}")

print("STARTING SERVER")
start()
