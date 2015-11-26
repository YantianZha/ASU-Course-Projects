#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
UDP client sending file name
https://pymotw.com/2/socket/udp.html
http://blog.csdn.net/hu330459076/article/details/7868028
"""


import socket
import sys
import pickle
import time

import frag
from down_up_http import download_file

class Client:
    """ 
    Client connected to center server, and http server of client's host
    """ 
    def __init__(self, flag):
	# Create a UDP socket
	self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	self.flag = flag
	ack = 1

    	print "Please input the center server address:"
	CtSrv_addr = raw_input('--> ')

	self.server_address = (CtSrv_addr, 10000)

	file_name = 0

        self.message = (self.flag, file_name, ack)

    def send_msg(self, message, address):
	print "message!!!!!:", message
        str_msg = pickle.dumps(message)

        # message (string) fragmentation
        frag_msg = frag.msg_fragmt(str_msg)	
	print "frag_msg!!!!!:", frag_msg

        # send
        for msg in frag_msg:
            sent = self.sock.sendto(msg, address)

        # set RTT
        rtt = 2
        count = 0
        alarm = time.time() + rtt
        #sock.settimeout(1)
        while True: ## Loop infinitely
            self.sock.settimeout(1)
            try:
                recv_message, server = self.sock.recvfrom(1024)
                if recv_message[1]:
                    print "200(OK)"
                    break
            except socket.timeout:
                print "resend the file name to share:"
                str_msg = pickle.dumps(message)

                # message (string) fragmentation
                frag_msg = frag.msg_fragmt(str_msg)

                # send
                for msg in frag_msg:
                    sent = self.sock.sendto(msg, address)

                count += 1

            if count == 5:
                print "400(ERROR)"
                break

    def ressem_recv(self):
        raw_data = []
        recv_data = 0

        # set RTT
        rtt = 2
        count = 0
        alarm = time.time() + rtt

        enter = 0

        while True: ## Loop infinitely
            if enter == 0:
                data, address = self.sock.recvfrom(1024)
                raw_data.append(data)
                recv_data = frag.msg_reassemb(raw_data)
                enter = 1
            else:
                self.sock.settimeout(5)
                try:
                    if recv_data == 0:
                        data, server = self.sock.recvfrom(1024)
                        raw_data.append(data)
                        recv_data = frag.msg_reassemb(raw_data)
                    if recv_data:
                        print "200(OK)"
		        enter = 0
	                return recv_data
			break

                except socket.timeout:
                    print "Failed to receive, exit anyway."
                    print "400(ERROR)"
                    raw_data = []
                    enter = 0
	 	    break

    def get_al_file_nms(self):
        file_name_upload = ()       # initialize an empty tuple
  	switch = 'y'
  	while switch == 'y':
            print "Please input the file_name that you want to share: name1, name2, ..."
            file_name = tuple(str(x.strip()) for x in raw_input().split(','))
            file_name_upload = file_name_upload + (file_name)
            print "If you want to add more file names to share, please press 'y', otherwise press ANY KEY:"
            switch = raw_input('--> ')
            if switch != 'y':
                break
        return file_name_upload

    def client_download(self):
	"""
	Returns: address of a host who has the file wanted
	"""
        print "Please input the file_name that you want to download:"
        file_name_download = raw_input('--> ')
        self.message = (self.message[0], self.message[1], file_name_download)

        print "trying to get the file:", self.message[1] # Send request
#        sent = self.sock.sendto(pickle.dumps(self.message), self.server_address) # serialize data into an array of bytes
        self.send_msg(self.message, self.server_address)

#        str_msg = pickle.dumps(message)

        # message (string) fragmentation
#        frag_msg = frag.msg_fragmt(str_msg)

        # send
#        for msg in frag_msg:
#            sent = self.sock.sendto(msg, self.server_address)

        # set RTT
        rtt = 2
        alarm = time.time() + rtt
        while True: ## Loop infinitely
            self.sock.settimeout(1)
            try:
                 # receive message
                 print >>sys.stderr, 'waiting to receive'
                 data, server = self.sock.recvfrom(1024)
                 data_deser = pickle.loads(data)     # deserialization
                 print >>sys.stderr, 'received "%s"' % data
                 print "data_deser:", data_deser
                 print "Start downloading the data!"
                 recv_data = download_file(data_deser[1], data_deser[0])
                 print "recv_data", recv_data
                 update_msg = (1, file_name_download)   # flag = 1 to share file name
                 sent = self.sock.sendto(pickle.dumps(update_msg), self.server_address) # serialize data into an array of bytes
                 break

            except socket.timeout:
                 # resend
                 print "resend the message:"
                 sent = self.sock.sendto(pickle.dumps(self.message), self.server_address) # serialize data into an array of bytes

    def client_upload(self):
	"""
	Client uploads one/some file(s), and gets the ack then.
	"""
        file_name_upload = self.get_al_file_nms()
        message = (1, 0, file_name_upload)
        print "The client will upload: ", file_name_upload

#        sent = self.sock.sendto(pickle.dumps(message), self.server_address)
	str_msg = pickle.dumps(message)

	# message (string) fragmentation
	frag_msg = frag.msg_fragmt(str_msg)
	
	# send
	for msg in frag_msg:
	    sent = self.sock.sendto(msg, self.server_address)

        # set RTT
        rtt = 2
        count = 0
        alarm = time.time() + rtt
        #sock.settimeout(1)
        while True: ## Loop infinitely
            self.sock.settimeout(1)
            try:
                data, server = self.sock.recvfrom(1024)
                if data:
                    print "200(OK)"
                    break
            except socket.timeout:
                print "resend the file name to share:"
      		str_msg = pickle.dumps(message)

        	# message (string) fragmentation
        	frag_msg = frag.msg_fragmt(str_msg)

        	# send
        	for msg in frag_msg:
            	    sent = self.sock.sendto(msg, self.server_address)

                count += 1

            if count == 5:
                print "400(ERROR)"
                break

    def client_exit(self):
	"""
	Client disconnects itself from center server,
	deletes file names stored in center server,
	and close the client socket
	"""
        print "The client is exiting, all its file in directory will be deleted."
        self.message = (2, self.message[1], self.message[2])
        sent = self.send_msg(self.message, self.server_address)

	count = 0

        while True: ## Loop infinitely
            self.sock.settimeout(5)
            try:
                self.message, self.server_address = self.ressem_recv()  # self.sock.recvfrom(1024)

		print "self.message, self.server_address:", self.message[1]
                if self.message[1]:
		    print "received message:", self.sock.settimeout(1)
       		    print >>sys.stderr, 'closing socket'
                    self.sock.close()
                    print "200(OK)"
                    break
            except socket.timeout:
                print "resend the exiting command:"
#                sent = self.sock.sendto(pickle.dumps(self.message), self.server_address)
                sent = self.send_msg(self.message, self.server_address)
                count += 1

            if count == 5:
                print >>sys.stderr, 'closing socket'
                self.sock.close()
                print "400(ERROR)"
                break
        
#        print >>sys.stderr, 'closing socket'
        self.sock.close()

    def run(self):
        """
	Main method of running the client
	"""
	try:
	    if (self.flag == 0):
	        t = self.client_download()
	    if (self.flag == 1):
		t = self.client_upload()
	    if (self.flag == 2):
		t = self.client_exit()

	finally:
	    print 0 

if __name__ == "__main__":
    while True:
	print "Press 0 if you want to download, 1 if you want to update, 2 if you want to exit:"
        flag = input('--> ')		# input gets int, raw_input gets string

        if (flag != 0) and (flag != 1) and (flag != 2):
	    print "flag:", flag
	    print "Please input again with the right option."
       	    pass 

        else:
	    s = Client(flag)
      	    s.run()

        if flag == 2:
            break






