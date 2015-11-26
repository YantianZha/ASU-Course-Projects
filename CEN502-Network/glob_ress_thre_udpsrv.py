#!/usr/bin/env python 
# -*- coding:UTF-8 -*-

"""
UDP server that matains a directory, supporting multithreading
Input: file_name(str),client_ip, flag (flag = 1, share, 0, download)
Output:client_ip
https://pymotw.com/2/socket/udp.html
http://blog.csdn.net/hu330459076/article/details/7868028
"""

import socket
import sys
import pickle

import select
import thread
import time

import frag

class udp_serv:
    """
    UDP server class. Served as a directory server.
    """

    def __init__(self): 
	print "Please input your host ip:"
	self.host = raw_input('--> ')
#        self.host = ''
	self.port = 10000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host,self.port))
	self.file_addr = {}
	self._thread_ = {}
	self.message = (0, 0, 0)

    def send_msg(self, message, address):
        str_msg = pickle.dumps(message)

        # message (string) fragmentation
        frag_msg = frag.msg_fragmt(str_msg)
    
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
                    sent = self.sock.sendto(msg, address)

                count += 1

            if count == 5:
                print "400(ERROR)"
                break

    def srv_update(self, file_name, address):
        """
        UDP server received a file name and update the directory
        """
        sub_file = []
        for id in range(len(file_name)):
            sub_file.append(file_name[id])
 #           print "sub_file:", sub_file
 #           file_addr.append({file_name, address})
            self.file_addr[sub_file[id]] = address    # dictionary

        # send acknowledgement
        ack = (1, "Server has received the file name!")
        sent = self.sock.sendto(pickle.dumps(ack), address)

    def srv_backIP(self, file_name, address):
        """
        Send the ip of the file the client wants
        """
        get_file = 0

        for file in self.file_addr.keys():
            if (file == file_name):
                message = (file, self.file_addr[file])
                sent = self.sock.sendto(pickle.dumps(message), address)
#		sent = self.send_msg(message, address)
                #print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
                print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
                get_file = 1

        if get_file == 0:
            error = "There's no such a file."
            message = (error)
            sent = self.sock.sendto(pickle.dumps(message), address)
            print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)

    def del_files(self, address):
	"""
	Input: IP of a client
	delete all its files stored in directory
	"""
	ip = address[0]

	print "Original directory is:", self.file_addr
	self.file_addr = {key:value for key, value in self.file_addr.items() if value[0] != ip}
	print "Directory after deleting is:", self.file_addr

        # send acknowledgement
	self.message[1] = 1
	print "self.message", self.message	
#        sent = self.sock.sendto(pickle.dumps(ack), address)
#	self.send_msg(ack)
	self.send_msg(self.message, address)


    def udp_processing(self, flag, ack, file_name, address): 
	    """
	    Main processing module
	    """
            if flag == 1:
                print "You chosen 1, directory will be updated!"
                u = self.srv_update(file_name, address)

            elif flag == 0:
                print "You chosen 0, IP of the host who has the file will be sent!"
                u = self.srv_backIP(file_name, address)

	    elif flag == 2:
		print "You chosen 2, all your files will be deleted from directory!"
		u = self.del_files(address)

    def run(self): 
 	raw_data = []
	recv_data = 0

        # set RTT
        rtt = 2
        count = 0
        alarm = time.time() + rtt

	enter = 0

        while True: ## Loop infinitely
            try:
	        if enter == 0:
                    print "Directory server starts receiving new messages:"
		    data, address = self.sock.recvfrom(1024)
		    raw_data.append(data)
	            recv_data = frag.msg_reassemb(raw_data)
		    enter = 1
	        else:
                    self.sock.settimeout(5)
                    try:
		        if recv_data == 0:
                            data, address = self.sock.recvfrom(1024)
	                    raw_data.append(data)
		            recv_data = frag.msg_reassemb(raw_data)
                        if recv_data:
                            print "200(OK)"
			    enter = 0         

	         	    # send ack to client
		            ack = 1
		            sent = self.sock.sendto(pickle.dumps(ack), address)

                            self.message = pickle.loads(recv_data)

			    print "self.message:", self.message

                            if self.message[0] != 2:
                                t = thread.start_new_thread(self.udp_processing, (self.message[0], self.message[1], self.message[2], address,))

                            else:
				t = thread.start_new_thread(self.udp_processing, (self.message[0], self.message[1], self.message[2], address,))
#				self._thread_[address] = t
#			        for th in self._thread_.keys():
#				    if th == address:
#                           	        print "UDP server closing..."
#                              	        self._thread_.exit()
				t.exit()
                    except socket.timeout:
		        data = "NO RESPONSE"
                        print "Failed to receive the complete file:"
		        print "400(ERROR)"
		        raw_data = []
		        enter = 0

	    except socket.timeout: 
		self.sock.settimeout(5)	

if __name__ == "__main__": 
    s = udp_serv() 
    s.run()


