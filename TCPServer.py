#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverPort = 7001
serverSocket.bind((socket.gethostname(), serverPort)) #associate the server port number with this socket
serverSocket.listen(1) #wait and listen for some client to knock on the door

while True:

	#Establish the connection
	print 'The server is ready to serve...'
	connectionSocket, addr = serverSocket.accept() #the server creates a new socket dedicated to the particular client
	try:
		message = connectionSocket.recv(1024) #receives message from client
		print '-------the message is------- ', message
		filename = message.split()[1]
		print '-------the filename is------ ', filename 
		f = open(filename[1:]) #get rid of '/' in the front of the filename
		outputdata = f.read()
		#Send one HTTP header line into socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n") #sends a 200 OK header line
		#Send the content of the requested file to the client
		print '-------length is------ ', len(outputdata)
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i])
		connectionSocket.send("\r\n") 
		connectionSocket.close() 
		print 'File sending success'
	except IOError:
		#Send response message for file not found
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
		#Close client socket
		connectionSocket.close() 
serverSocket.close() #Close the server socket