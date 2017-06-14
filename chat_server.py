import sys, socket, select

### CONFIGURATION ###

HOST = ""
RECV_BUFFER = 4096
PORT = 8000
MAXUSERCOUNT = 10

### END CONFIGURATION ###

SOCKET_LIST = []

def server_broadcast(arg_server_socket, arg_socket, arg_message):
	
	for _socket in SOCKET_LIST:
		
		if _socket != arg_server_socket and _socket != arg_socket:
			
			try:
			
				_socket.send(arg_message)
		
			except:
				
				_socket.close()
				if _socket in SOCKET_LIST:
					
					SOCKET_LIST.remove(_socket)

def server_chatserver():
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(MAXUSERCOUNT)
	SOCKET_LIST.append(server_socket)
	print("[INFO] Server started on port %s" % (PORT))
	
	while 1:
		
		_readable, _writeable, _error = select.select(SOCKET_LIST,[],[],0)
		
		for _socket in _readable:
			
			# New connection
			if _socket == server_socket:
				
				_sockfd, _addr = server_socket.accept()
				SOCKET_LIST.append(_sockfd)
				print("[CONNECTION] Client connected. Details: %s:%s" % (_addr[0], _addr[1]))
				server_broadcast(server_socket, _sockfd, "[SERVER] %s:%s entered the chatroom!\n" % (_addr[0], _addr[1]))
				
			# New message	
			else:
				
				try:
					
					_data = _socket.recv(RECV_BUFFER)
					if _data:
						
						server_broadcast(server_socket, _socket, "\r" + "[%s] %s" % (str(_socket.getpeername()), _data))
						
					else:
					
						if _socket in SOCKET_LIST:
							
							SOCKET_LIST.remove(_socket)
						
						server_broadcast(server_socket, _socket, "[SERVER] %s:%s has gone offline!\n" % (_addr[0], _addr[1]))
					
				except:
					
					server_broadcast(server_socket, _socket, "[SERVER] %s:%s has gone offline!\n" % (_addr[0], _addr[1]))
				
	server_socket.close()
	
if __name__ == "__main__":
	
	sys.exit(server_chatserver())