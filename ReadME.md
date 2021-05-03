
**Compiling**:-

The code can be directly complied through the command line/terminal, these are the commands

Server:-

python3 Udpchat.py -s 12345

Client:-

python3 Udpchat.py -c <nickname> 127.0.0.10 12345 1232


**Code**:-

I have written the code such that it reads the command line input for -s or -c and then calls the function server or client respectively. If there is wrong input in command line then program exits itself.

**Server**:-

If server is called the code checks for a port number on the command line and binds the server to that port number. Then the code checks for 3 different commands, which will be explained later. If none of those three commands are found then it takes the data sent by the client and adds it to the local client table, which is a list, and sends the table to all the active clients. The following three commands are checked: -

dereg : - if there is a dereg request, the server updates the client table and it changes the client who requested the dereg to offline in its local table and then sends the updated table to every online client.

reg : - if there is a reg request, the server updates the client able and it changes the client who requested the reg to online in its local table, then checks if it has any saved messages, which is a list, it sends the messages to the client, after which it deletes the messages from the saved messages list after which it sends the updated table to every online client.

saved\_m : - It also checks if the receiver is online and sends the sender a message that the receiver is online and an updated table to the sender. If a client sends a saved message request, it saves the port number of sender client, nick name of receiver client, the message to be sent, and the time stamp in a list.

The server prints out the data table everytime it gets updates and it also prints if it receives a saved message request and it prints when saves a message.


**Client** : -

If the client is called it takes the nickname, server ip, server port, client port from the command line. It binds the port to the cport input. The code first sends some data to the server and to register itself. The server sends a message that says you’re registered and then sends a client table. The client stores the table locally. The client then starts a select prodecure so as to listen to the incoming data to the port and take input from the user. The client then listens for the following commands : -

send : - the send command sends the client the message the sender wants to send and then waits for an ack if an ack is recevied it prints that the message has been received otherwise it tries to send the message to the server to save. If the server doesnot respond with an ACK the client exits the program. The client also checks if the receiver is online in its local table of clients in case the receiver is offline it directly sends the message to the server to be saved.

dereg : - the client sends the server dereg and then waits for the server to respond. It tries 5 times and if the server is unresponsive then it directly exits the program. In case the server sends an ack back it closes the UDP connection and frees the port number it was using. After the user can use reg command to register again to the server. The client cannot dereg or reg any other client then itself.

` `Any other input is treated as garbage and just prints “Wrong input” to the terminal.

I have implemented the code such that whenever there is a keyboard interrupt(ctrl +c) the client exits gracefully and also sends server a dereg request telling the server that it is going offline. The server also exits gracefully whenever there is a keyboard interrupt. I have assumed that the clients do not take nick names like reg, dereg and saved\_m and my code will exit if the client tries to take any of these nicknames. My code also exits if it detects that two different client wants the same nickname. The client that registers later will not be able to take the nickname. Everything is my code is case-sensitive including commands like reg, dereg, and send. If a client is typing something and a new message comes in, the message is displayed in the same line.


For screenshots of the program working look at ReadME.pdf 
