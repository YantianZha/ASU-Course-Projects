import pickle

#a = 'AUGGCCAUAS'
#print a
#def getSubStrings(RNA, position):
#    return [RNA[i:i+3] for i in range(position, len(RNA) - 2, 3)]

#print getSubStrings(a, 0)
#print getSubStrings(a, 1)
#print getSubStrings(a, 2)

#print "a[::-1]", a[::-1]

#print "10%3:", 10%3
#mod_str = a[-(len(a)%3):]	#http://stackoverflow.com/questions/646644/how-to-get-last-items-of-a-list-in-python
#print "mod_str:", mod_str

#print "type(getSubStrings(a, 0))", type(getSubStrings(a, 0))
#getSubStrings(a, 0).append("new")
#print "getSubStrings(a, 0).append('s')", getSubStrings(a, 0)

##li = ['a', 'b', 'mpilgrim', 'z', 'example']
##li = ['AUG', 'GCC', 'AUA']
#li = getSubStrings(a, 0)
#li.append("new")  
#print "li:", li

#comp_str = getSubStrings(a, 0)
#comp_str.append(mod_str)
#print "comp_str:", comp_str


##li = getSubStrings(a, 0)
##print "li.extend('s')", li.extend('s')


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


def get_raw_msg(str_msg):
    """
    pickle msg will get a msg "S'...'"
    remove the "S'", and "'"
    """
    new_str_msg = str_msg[2:]
    new_str_msg = new_str_msg[:-3]
    print "new_str_msg[0]:", new_str_msg[0]
    print "new_str_msg[-1]", new_str_msg[-1]
    return new_str_msg


#################################
# test

test_str = 'AUGGCCAUAS'

print "getSubStrings(test_str, 0, 3)", getSubStrings(test_str, 0, 3)

print "get_raw_msg(pickle.dumps(test_str))", get_raw_msg(pickle.dumps(test_str))

dict1 = {0:2, 1:4}
print "dict1:", dict1

pick = pickle.dumps(dict1)
pick_p = pickle.dumps(pick)
print "pickle.dumps(dict1)", pick_p
depick_p = pickle.loads(pick_p)
depick = pickle.loads(depick_p)
print "depick", depick


#x = None
#print "pickle.dumps(x)", pickle.dumps(x)
#print "pickle.loads(x)", pickle.loads(x)
#print "len(pickle.dumps(x))", len(pickle.dumps(x))

