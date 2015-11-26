#!/usr/bin/env python
#coding=utf-8

from shutil import *
from glob import glob

print 'BEFORE:', glob('ex_shutil_copy.*')
copyfile('ex_shutil_copy.py', 'ex_shutil_copy.copy')

print 'AFTER:', glob('ex_shutil_copy.*')



