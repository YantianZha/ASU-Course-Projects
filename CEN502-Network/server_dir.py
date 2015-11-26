#!/usr/bin/env python  
# -*- coding:UTF-8 -*- 

"""
UDP server that matains a directory 
Input: file_name(str),client_ip, flag (flag = 1, share, 0, download)
Output:client_ip
https://pymotw.com/2/socket/udp.html
http://blog.csdn.net/hu330459076/article/details/7868028
"""

#from socket import *
import socket
import sys
import pickle

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

file_addr = {}

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    #file_addr = []
    recv_data, address = sock.recvfrom(4096)
    flag, file_name = pickle.loads(recv_data)
    print "file_name:", file_name
    if flag == 1:
      sub_file = []
      for id in range(len(file_name)):
          sub_file.append(file_name[id])
	  print "sub_file:", sub_file 
      #file_addr.append({file_name, address})    
          file_addr[sub_file[id]] = address    # dictionary
      #print "file_addr", address
      #print >>sys.stderr, 'received %s bytes from %s' % (len(recv_data), address)
      #print >>sys.stderr, recv_data
      ack = (1, "Server has received the file name!")
      sent = sock.sendto(pickle.dumps(ack), address) 

 
    # add a test send the test messag
    print "file_addr[0]_UP", file_addr
    
    if flag ==0:
      get_file = 0
      print "file_name", file_name
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
          #print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
          print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)  




