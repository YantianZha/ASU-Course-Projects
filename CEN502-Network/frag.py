#!/usr/bin/env python
#coding=utf-8

from __future__ import division
import pickle

"""
aaa = ('#' * 1024)
print len(aaa), type(aaa)

print "aaa:", aaa

# fragmentation
print "pickle.dumps(message):", pickle.dumps(aaa)
print "len(pickle.dumps(aaa)):", len(pickle.dumps(aaa))


bbb = pickle.dumps(aaa)

print "bbb:", bbb[:2]
# after pickly, bbb = aaa + 8
# header = 2 bytes
# data = 126 bytes
# total num of msgs are: len(msg)/126

print "len(str(2048)+aaa)", len(str(2048)+aaa)
print "len(pickle.dumps(2048))", len(pickle.dumps(2048))
print "pickle.dumps(str(2048)+aaa)", pickle.dumps(str(2048)+aaa)

print "len(pickle.dumps(str(2048)+aaa))", len(pickle.dumps(str(2048)+aaa))

num_fm_ts = "%04d" % 1
print "num_fm_ts", num_fm_ts

print "num_fm_ts + 30", int(num_fm_ts) + 30
"""


##############################

import math
from copy import deepcopy

str_ts = 'AUGGCCAUAS'

def decide_num_bts(string_a, total_bits):
    """
    Input: total_bits
    Assumes: x number bits, y length of data string
    Then: x + ceil[(total_bits-x)/y] = total_bits
    """

#    return math.ceil((len(string_a)/
    return 2

def find_missing(L):
    start, end = L[0], L[-1]
    return sorted(set(xrange(start, end + 1)).difference(L))

def getSubStrings(string_a, position, len_str):
    """
    Get a list of substrings with fixed length with the last one substring
    Input: position, starting point of creating the substring
           len_str, length of each substring except for the last one
    """
    # get the last substring 
    mod_str = string_a[-(len(string_a)%len_str):]

    # get a list of substrings with fixed length (except the last part)
    part_str = [string_a[i:i+len_str] for i in range(position, len(string_a) - (len_str-1), len_str)]
    
    # get complete string
    part_str.append(mod_str)

    return part_str

def cont_2_NumFm(num, t_bits):
    """
    Input: an number (23), total bits of output number
    Output: an number (0023)
    """
    num_id = "%010d" % num
    return num_id

def conv_list_str(L):
    # http://stackoverflow.com/questions/4481724/convert-a-list-of-characters-into-a-string
    return ''.join(L)

def det_seq_bts(string_a):
    """
    A string is 0101!120...
    then the seq bits are 0101 before '!'
    divide it creating a dictionary.
    """
    return string_a.index('!')

def get_seq(string_a):
    int_bts = det_seq_bts(string_a)
    return int(string_a[2:int_bts])		# string1[1:3], get string1[1]+string1[2]

def get_flag(string_a):
    return string_a[det_seq_bts(string_a)+1]		# S'0103!0...()

def get_data(string_a):
    return string_a[det_seq_bts(string_a)+2:]

def set_mss(len_data):
    def declen(n):
	"""
	Returns: number of bits of an oct number
	"""
	return len("%d"%n)
    return declen(len_data)

def msg_fragmt(str_msg):
    """
    Message fragmentation at client side.
    Spilit the message;
    Adds seq id;
    Adds frag at last bit (1, last fragment; 0 others)
    Input: string message
    Output: a list of fragmented messages
    """

#    print "msg_fragmt(str_msg)_DDDDD:", str_msg
    new_str_msg = []
    start = 0
    mss = 1000
    seq_bits = 4

#    print "str_msg:", str_msg

    frag_msg = getSubStrings(str_msg, start, mss)
#    print "frag_msg:", frag_msg
#    print "len(frag_msg):", len(frag_msg)

    # add seq id, flag, '!' 
    for id in range(len(frag_msg)):

#	print "id, frag_msg[id]", id, frag_msg[id]
	num_seq = cont_2_NumFm(id, seq_bits)

	if id < len(frag_msg)-1:
            new_fm = pickle.dumps(str(num_seq) + '!' + str(0) + frag_msg[id])
	    new_str_msg.append(new_fm)
#	    print "pickle.loads(new_fm):", pickle.loads(new_fm)

	elif id == len(frag_msg)-1:
	    new_fm = pickle.dumps(str(num_seq) + '!' + str(1) + frag_msg[id])
            new_str_msg.append(new_fm)
#	    print "pickle.loads(new_fm):", pickle.loads(new_fm)
    print "fragmentation of message:", new_str_msg
    return new_str_msg

def msg_reassemb(msg_seqs):
    """
    Input: a list of messages (seq, flag, data)
    Returns: the original complete string message
    """
    total_msg = []
    # get a list of tuple (seq, data, flag)
    for id in range(len(msg_seqs)):
	sub_str_msg = pickle.loads(msg_seqs[id])
	(seq, flag, data) = (get_seq(sub_str_msg), get_flag(sub_str_msg), get_data(sub_str_msg))
	total_msg.append((seq, flag, data))

    # http://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
    total_msg.sort(key=lambda tup: tup[1])

    if total_msg[-1][1] == '1':               # flag == 1
        total_msg.sort(key=lambda tup: tup[0])
	msg_seq = [int(i[0]) for i in total_msg]

	# find missing
	missing_msg = find_missing(msg_seq)

	if missing_msg:		# ask for resending
	    return false

	else:		
	    pure_msg = [seq[2] for seq in total_msg]
	    re_str_msg = conv_list_str(pure_msg)
	    print "reassemble of message:", re_str_msg
	    return re_str_msg 

    else:
	return 0

#################################
# test
"""
msg = "1234"
string_msg = pickle.dumps(msg)
print "string_msg:", string_msg

frag_ts_msg = pickle.dumps(str("%04d" % 103) + "!" + str(0) + string_msg)

#print det_seq_bts(string_msg)
#print "det_seq_bts: pickle.dumps(str(2048)+aaa)", det_seq_bts(pickle.dumps(str(2048) + '!' + aaa))

#print "get_seq(string_msg):", get_seq(string_msg)
#print "get_seq(pickle.dumps(str(2048) + '!' + aaa)):", get_seq(pickle.dumps(str(2048) + '!' + aaa))

#print "len(msg * 2):", len(msg * 2)
#print "set_mss(len(msg * 2))", set_mss(len(msg * 2))

#print "msg_fragmt(string_msg):", msg_fragmt(string_msg)


str_desm = pickle.loads(frag_ts_msg)
print "pickle.loads(frag_ts_msg):", str_desm
print "get_flag(str_desm):", get_flag(str_desm)

print "get_seq(str_desm):", get_seq(str_desm)

print "get_data(str_desm):", get_data(str_desm)

raw_data = pickle.loads(get_data(str_desm))
print "pickle.loads(get_data(str_desm)):", pickle.loads(get_data(str_desm))

msg_fragmt_ts = msg_fragmt(string_msg)

print "msg_fragmt_ts:", msg_fragmt_ts

print "msg_reassemb():", msg_reassemb(msg_fragmt_ts)

print "pickle.loads(msg_reassemb(msg_fragmt_ts)):", pickle.loads(msg_reassemb(msg_fragmt_ts))
"""
