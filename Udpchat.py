from socket import*
import sys
import select
import time

try: #incase the inputs on command line are wrong
	sorc = (sys.argv[1]) #checks for -s or -c on command line
	portornick = sys.argv[2] # takes port for -s and nick for -c
except IndexError or ValueError: #exit if wrong input
	exit()

def server(port):
	try:
		s = socket(AF_INET,SOCK_DGRAM)
		s.bind(("127.0.0.10", port))
		print("The server is up and running")
		tab = [] #Table for ip address nick etc.
		saved_messages = [] # to save messages for offline chat
		try: # for keyboard interrupt "crtl + c"
			while True:
				data, addr = s.recvfrom(4096) # receive data from clients
				#print(data)
				data_client = data.decode("utf-8")
				data_client = data_client.split() # making list of client sent data
				if data_client[0] == "dereg": # addressing de registration request
					try:
						if(data_client[1] == "reg"):
							find_index = tab.index(data_client[2]) # finding index of client
						else:
							find_index = tab.index(data_client[1]) # finding index of client
						tab[find_index + 3] = "offline" # marking client offline
						ack = "ACK" # send ACK to client
						s.sendto(ack.encode("utf-8"),addr)
						indices = [i for i, x in enumerate(tab) if x == "online"] # getting the indices of all the active client to send the updated table.	
						print(tab)
						for y in indices:
							address_for_all_clients = [tab[y-2],tab[y-1]] # gets all clients addresses to send updated table
							s.sendto(str(tab).encode("utf-8"),tuple(address_for_all_clients)) # sends updated table to all clients
					except ValueError: # incase client types wrong nickname
						pass	
				elif data_client[0] == "reg": # receive registration request
					if data_client[1] in tab:
						find_reg_index = tab.index(data_client[1]) # finding index of client looking to register
						tab[find_reg_index + 3] = "online" # marking client online
						ack = "You are registered" # send ACK to client
						if data_client[1] in saved_messages: # check if client has saved messages
								you_have = ">>>[You have messages]"
								ack = ack + "\n" + you_have #making ack for client
								list_of_indexes = [i for i in range(len(saved_messages)) if saved_messages[i] == data_client[1]] #getting index for client
								for j in list_of_indexes:# getting message for client along with time and sender
									nick_of_sender = tab[(tab.index(saved_messages[j-1]))-2] # getting nick of sender
									ack = ack + "\n>>>" + "[" + nick_of_sender + "]: <" + str(saved_messages[j+2]) + "> " + str(saved_messages[j+1])
								for k in range(len(list_of_indexes)): # removing all the messages that are sent
									del saved_messages[j-1-(4*k):j+3-(4*k)]	#the 4*k is used because, when one message is removed the list gets shifted by 4
						s.sendto(ack.encode("utf-8"),addr) 
						print("Messages for " + data_client[1] + " have been delivered")
						print("Messages for " + data_client[1] + " have been deleted from the server")
						indices = [i for i, x in enumerate(tab) if x == "online"] # getting the indices of all the active client to send the updated table.
						print(tab) # display updates table on the server
						for y in indices:
							address_for_all_clients = [tab[y-2],tab[y-1]] # gets all clients addresses to send updated table
							s.sendto(str(tab).encode("utf-8"),tuple(address_for_all_clients)) # sends updated table to all clients
					else:
						pass	
				elif data_client[0] == "save_m": # saved message request received
					index_of_offline_client = tab.index(data_client[1])# looking for index of the client in table
					if tab[index_of_offline_client + 3] == "online": # if the client is online then don't have to save message
						client_is_online = ">>>Client " + data_client[1] + " exists!!"
						s.sendto(client_is_online.encode("utf-8"),addr) # new table is sent to the client who thought the other client is offline
						s.sendto(str(tab).encode("utf-8"),addr)
					else:
						saved_messages.append(addr[1]) # saving the port number of client who sent the request to save message in list saved_messages
						saved_messages.append(data_client[1])# saving the name of the client to whom the message has to be sent
						store = ' '.join([str(data_client) for data_client in data_client[2:]])  # isolating the message string from the data
						#print(store)
						saved_messages.append(store)
						t = time.localtime()
						current_time = time.strftime("%H:%M:%S", t)
						saved_messages.append(current_time)# saving time when data was received
						print("Messages for " + data_client[1] + " has been saved in the server")
						ack = "Messages received by the server and saved" # send ACK to client
						s.sendto(ack.encode("utf-8"),addr) # sending ack to client
				
				else:
					if(data.decode("utf-8") in tab): #checks for duplicate nick
						message = bytes("Nick already taken".encode("utf-8"))
						s.sendto(message,addr) #sends to new client
						#print(message)
					else:
						message = bytes("Welcome, You are registered.".encode("utf-8"))
						#print(message)
						s.sendto(message,addr) #sends to new client	
						tab.append(data.decode("utf-8")) # appends new client to table
						tab.append(addr[0])
						tab.append(addr[1])
						tab.append("online")
						print(tab)
						indices = [i for i, x in enumerate(tab) if x == "online"] # getting the indices of all the active client to send the table.
						for y in indices:
							address_for_all_clients = [tab[y-2],tab[y-1]] # gets all clients addresses to send updated table
							s.sendto(str(tab).encode("utf-8"),tuple(address_for_all_clients)) # sends updated table to all clients
		except KeyboardInterrupt: #incase the user presses ctrl+c
			print("The server is down!!!")
			exit(0)
	except IndexError or ValueError:
		exit(0)
	
	
					
def client(nick):
	ip = (sys.argv[3]) # gets server ip
	sport = int(sys.argv[4]) # gets server port
	cport = int(sys.argv[5]) # gets client port
	#print(nick + " "+ip + " " + str(sport)+ " "+ str(cport))
	client_socket = socket(AF_INET,SOCK_DGRAM)
	client_socket.bind(("127.0.0.10", cport))
	client_socket.settimeout(0.5) # sets timeout
	empty = nick #nickname to be sent to server
	if nick == "reg" or nick == "dereg" or nick == "save_m":
		print("Please use a different nickname!!")
		exit()
	#print(nick)
	try:
		client_socket.sendto(empty.encode("utf-8"),(ip,sport)) # sends registration data to server
		data, addr = client_socket.recvfrom(4096) # receives data from server
	except timeout:
		print(">>>Server not available")
		exit()
	print(">>>" + data.decode("utf-8"))
	if(data.decode("utf-8") == "Nick already taken"):
		exit()
	msg = "" # empty string to send data
	data_table = ""
	random = 1 # Used to get >>> in front of the first Client updated print message. Really useless and not optimized.
	try: # for ctrl+c exception
		while True:
			readers,_,_ = select.select([sys.stdin, client_socket],[],[]) # select function to read all inputs simulatenously
			for reader in readers:
				#print(">>>",end='')
				if reader is client_socket: # listening for data
					data, addr = client_socket.recvfrom(4096)
					#print(">>> ", end='')
					if(random == 1):# again very useless and inefficient approach.
						if(addr[1] == sport): # updating table
							data_table = data.decode("utf-8")
							data_table = data_table.replace("[","") # removing garbage values
							data_table = data_table.replace("]","")
							data_table = data_table.replace(" ","")
							data_table = data_table.replace("'","")
							data_table = data_table.split(",") # making a list
							#print(data_table)
							print(">>>Client table Updated")
							print(">>>",end='')#>>> for new input
							sys.stdout.flush()
							random = 0
						else: # Theoretically this will never be executed, just here for show
							sender_address = data_table.index(str(addr[1])) # finding sender address and nick to print it out
							sender_nick = data_table[sender_address - 2]
							print("["+sender_nick+"]" + ": " + data.decode("utf-8"))
							print(">>>",end='')
							sys.stdout.flush()
						if addr[1] != sport and data.decode("utf-8") != "ACK": #new message is checked 
							ack = "ACK" # send ACK to client
							client_socket.sendto(ack.encode("utf-8"),addr)
					else:
						if(addr[1] == sport): # updating table
							data_table = data.decode("utf-8")
							data_table = data_table.replace("[","") # removing garbage values
							data_table = data_table.replace("]","")
							data_table = data_table.replace(" ","")
							data_table = data_table.replace("'","")
							data_table = data_table.split(",") # making a list
							#print(data_table)
							#print("1")
							print("Client table Updated")
							print(">>>",end='')#>>> for new input
							sys.stdout.flush()
						else:
							data_n = str(data) # converting bytes data to string for ACK message send by the user
							if data.decode("utf-8") != "ACK" or data_n == "b'ACK'": 
								sender_address = data_table.index(str(addr[1])) # finding sender address and nick to print it out
								sender_nick = data_table[sender_address - 2]
								print("["+sender_nick+"]" + ": " + data.decode("utf-8"))
								print(">>>",end='')
								sys.stdout.flush()
							else:
								pass
						data_n = str(data)
						if (bool(addr[1] != sport) & (bool(addr[1] != cport) | (bool(data.decode("utf-8") != "ACK") & bool(data_n == "b'ACK'")))): #new message is checked if it is ACK then there is no need to send ACK back. Also, other things to send ACK messages.
							ack = "ACK" # send ACK to client
							client_socket.sendto(ack.encode("utf-8"),addr)	#send ACK to client					
							
	
				else:
					#print(">>> ", end='')
					msg = input('>>>') # taking client input
					msg = msg.split() # making a list of input
					if msg[0] == "send": # checking for send in the input message
						new_msg = ' '.join([str(msg) for msg in msg[2:]]) # isolating the string to be sent
						try:
							#print(new_msg)
							port_of_nick = data_table.index(str(msg[1])) # finding the nick's port
							if data_table[port_of_nick + 3] == "online": #check if the client is online
								try: # try sending client data
									if(msg[1] == nick): #if send to himself
										#print(new_msg)
										print("[Message received by " + msg[1] + ".]")#No need to wait for ACK as sending something to yourself won't need ACK
										client_socket.sendto(new_msg.encode("utf-8"),(data_table[port_of_nick+1],int(data_table[port_of_nick+2]))) # send to oneself
										print(">>>",end='')
										sys.stdout.flush()
									else:
										client_socket.sendto(new_msg.encode("utf-8"),(data_table[port_of_nick+1],int(data_table[port_of_nick+2]))) # send to the client
										data, addr = client_socket.recvfrom(4096) # wait for ack
										print("[Message received by " + msg[1] + ".]") # print if ack recceived
										print(">>>",end='')
										sys.stdout.flush()
								except timeout: #if timeout in case client is not responsive
									print("No ACK from " + msg[1] + ", message sent to server.")
									new_msg = "save_m " + str(msg[1])+ " " + new_msg # send to server to save message if client is not responsive
									try:
										#print(new_msg)
										client_socket.sendto(new_msg.encode("utf-8"),(ip,sport)) #send to server
										data, addr = client_socket.recvfrom(4096) # wait for ack from server
										print(data.decode("utf-8")) # print ack from server
										print(">>>",end='')
										sys.stdout.flush()
									except timeout:#if server does not respond
										print(">>>Server not responding")
										print(">>>Exiting")
										exit()#exit if server is unresponsive
							elif data_table[port_of_nick + 3] == "offline": # if client is offline
								new_msg = "save_m " + str(msg[1]) + " " + new_msg #directly send msg to server
								try:
									#print(new_msg)
									client_socket.sendto(new_msg.encode("utf-8"),(ip,sport))
									data, addr = client_socket.recvfrom(4096)
									print("["+data.decode("utf-8")+"]") #print ack received from server
									print(">>>",end='')
									sys.stdout.flush()
								except timeout: #if server does not respond
									print(">>>Server not responding")
									print(">>>Exiting")
									exit()#  exit if server is unresponsive
						except ValueError: #incase there is a valueError like wrong nick etc.
							print("Invalid Input") 
							print(">>>",end='')
							sys.stdout.flush()
					elif msg[0] == "dereg":# if client trying to de register
						if msg[1] in nick.split(): # checking client is de regestering itself
							send_data = "dereg " + str(msg[1])
							for x in range(5):#try 5 times to dereg from server
								try: 
									client_socket.sendto(send_data.encode("utf-8"),(ip,sport)) # try contacting server
									data, addr = client_socket.recvfrom(4096)
									print("[You are offline. Bye.]")
									client_socket.close() #closing udp connection and get the port free 
									try:
										while True:
											new_data = input('>>>') # looking if client wants to register again
											new_data_list = new_data.split()
											if new_data_list[0] == "reg" and new_data_list[1] in nick.split(): # if client registers again then open connection again
												client(new_data) #call client again to register
											else:
												print(">>>Not a valid Input") #if the input is not reg then pass
												pass
										break
									except KeyboardInterrupt: # if ctrl+c is pressed
										print("You have exited.")
										exit()#exit
								except timeout: #if timeout then pass and keep running loop
									pass
							if(x == 4): # if server does not respond 5 times then exit
								print("[Server not responding]")
								print(">>>[Exiting]")
								exit()
						else: #if there is a false nick in dereg
							print("Incorrect Nick")		
							print(">>>",end='')
							sys.stdout.flush()
							
					else: # if there is a wrong or garbage input
						print("Wrong Input!!!")
						print(">>>",end='')
						sys.stdout.flush()		
							
	except KeyboardInterrupt: #if ctrl+c is pressed
		final_data = "dereg " + nick # if exiting tell server that going offline
		#print(final_data)
		client_socket.sendto(final_data.encode("utf-8"),(ip,sport)) # try contacting server before leaving
		print("You have exited.")
		exit(0)#exit
	
def main(): # main function
	try:
		if sorc == "-s":
			server(int(portornick)) # start server if command line specifies -s
		elif sorc == "-c":
			client(portornick)# start client if command line specifies -c
	except Exception: # exit if any exception is thrown
		exit()
		

if __name__ == "__main__": #call main function.
	main()
	
