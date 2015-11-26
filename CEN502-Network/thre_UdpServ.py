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
import threading 

class udp_serv:
    """
    UDP server class. Served as a directory server.
    """

    def __init__(self): 
	print "Please input your host ip:"
	self.host = raw_input('--> ')
#        self.host = ''
	self.port = 10000
	self.server = 0
        self.backlog = 5
        self.size = 1024
        self.threads = []

    def open_socket(self): 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.server.bind((self.host,self.port)) 

    def run(self): 
        self.open_socket() 
        input = [self.server,sys.stdin] 
        running = 1 
        while running: 
            inputready,outputready,exceptready = select.select(input,[],[]) 

            for s in inputready: 

                if s == self.server: 
                    # handle the server socket 
                    c = Client(self.server.accept()) 
                    c.start() 
                    self.threads.append(c) 

                elif s == sys.stdin: 
                    # handle standard input 
                    junk = sys.stdin.readline() 
                    running = 0 

        # close all threads 

        self.sock.close() 
        for c in self.threads: 
            c.join()  

class Client(threading.Thread):
    """
    The client socket in UDP server
    """
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            recv_data, address = sock.recvfrom(4096)
            flag, file_name = pickle.loads(recv_data)
            print "file_name:", file_name

            if flag == 1:
                print "You chosen 1, directory will be updated!"
                u = srv_update(file_name, address)

            elif flag == 0:
                print "You chosen 0, IP of the host who has the file will be sent!"
                u = srv_backIP(file_name, address)

            else:
                self.client.close()
                running = 0
   
    def srv_update(self, file_name, address):
        """
        UDP server received a file name and update the directory
        """
        sub_file = []
        for id in range(len(file_name)):
            sub_file.append(file_name[id])
 #           print "sub_file:", sub_file
 #           file_addr.append({file_name, address})
            file_addr[sub_file[id]] = address    # dictionary
        print >>sys.stderr, 'received file: %s, from %s' % (file_name, address)

        # send acknowledgement
        ack = (1, "Server has received the file name!")
        sent = sock.sendto(pickle.dumps(ack), address)

    def srv_backIP(file_name, address):
        """
        Send the ip of the file the client wants
        """
        get_file = 0

        for file in file_addr.keys():
            if (file == file_name):
                message = (file, file_addr[file])
                sent = sock.sendto(pickle.dumps(message), address)
                #print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
                print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
                get_file = 1

        if get_file == 0:
            error = "There's no such a file."
            message = (error)
            sent = sock.sendto(pickle.dumps(message), address)
            print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)

if __name__ == "__main__": 
    s = udp_serv() 
    s.run()


