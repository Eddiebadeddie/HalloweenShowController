import socket
import threading
import BaseClient

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

MASTER = None
SLAVES = {}

def Interpret(connection, address, message):
    if(message == DISCONNECT_MESSAGE):
        return False
    
    #Checks to see if the message is a command
    if (len(message.split(":"))) == 1:
        return True
    
    #IP_ADDRESS:FOO AB C
    #Send IP address of device first
    #Send function name afterwards
    #Number of variables after
    address = message.split(":")[0]
    SLAVES[address].send(message.encode(FORMAT))
    return True

#Handles connection between client and server
#runs for EACH CLIENT
def handle_client(connection, address):
	print(f"New connection {address} connected")
	
	if threading.activeCount() == 2:
		MASTER = BaseClient.Client(connection, address)
		if MASTER.messageCount == 0:
			MASTER.connection.send('M'.encode(FORMAT))
			MASTER.messageCount += 1
	elif threading.activeCount() > 2:
		SLAVES[address] = connection
		#Sends an identifying address for the device that just joined
		MASTER.connection.send(f"{address}".encode(FORMAT))
		connection.send('S'.encode(FORMAT))
        
        
	connected = True
	while connected:
		#Blocking code until a message that conforms to the specifications are met
		#the parameter needs the number of bytes the message is going to take
		message_length = connection.recv(HEADER).decode(FORMAT)
		if message_length:
			message_length = int(message_length)
			message = connection.recv(message_length).decode(FORMAT)
			connected = Interpret(connection, address, message)
		print(f"{address} {message}")
		connection.send("Message received".encode(FORMAT))
	connection.close()

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
