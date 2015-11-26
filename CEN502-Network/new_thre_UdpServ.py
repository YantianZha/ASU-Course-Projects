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
        ack = (1, "Server will remove the file names of the client!")
        sent = self.sock.sendto(pickle.dumps(ack), address)

    def udp_processing(self, flag, file_name, address): 
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
        while True: 
	    recv_data, address = self.sock.recvfrom(1024)
            flag, file_name = pickle.loads(recv_data)
            print "file_name:", file_name

	    if flag != 2:
		t = thread.start_new_thread(self.udp_processing, (flag, file_name, address,))
#		t.start()
	    else:
		print "UDP server closing..."
		t.exit()

if __name__ == "__main__": 
    s = udp_serv() 
    s.run()


