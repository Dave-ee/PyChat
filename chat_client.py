import sys, socket, select

### CONFIGURATION ###

RECV_BUFFER = 4096

### END CONFIGURATION ###

SOCKET_LIST = []

def client_chatserver():

	if (len(sys.argv) < 3):
		
		print("Usage: %s <hostname> <port>" % (sys.argv[0]))
		sys.exit()
		
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.settimeout(2)
	
	try:
	
		client_socket.connect((HOST,PORT))
		
	except:
	
		print("[ERROR] Unable to connect!")
		sys.exit()
		
	print("[INFO] Connected to remote host. You can start sending messages.")
	sys.stdout.write("[YOU] "); sys.stdout.flush()
	
	while 1:
	
		SOCKET_LIST = [sys.stdin, client_socket]
		
		_readable, _writeable, _error = select.select(SOCKET_LIST,[],[])
		
		for _socket in _readable:
			
			if _socket == client_socket:
				
				# Incoming message from server
				_data = _socket.recv(RECV_BUFFER)
				if not _data:
					
					print("[INFO] Disconnected from remote host.")
					sys.exit()
					
				else:
					
					sys.stdout.write(_data)
					sys.stdout.write("[YOU] "); sys.stdout.flush()
					
			else:
			
				_message = sys.stdin.readline()
				client_socket.send(_message)
				sys.stdout.write("[YOU] "); sys.stdout.flush()
				
if __name__ == "__main__":

	sys.exit(client_chatserver())