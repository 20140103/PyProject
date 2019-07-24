#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %d	整数
# %f	浮点数
# %s	字符串
# %x	十六进制整数

print "hello world"
print r'''hello world ...1
        hello world  ...2
        '''
print True
print False
print True or False
print True and False
print not True
print not False

a = 1
b = 2

print 'a > b %s	' % (a > b)
print 'a < b %s ' % (a < b)
print 'a>=b %s' % (a >= b)
print 'a<=b %s' % (a <= b)
print 'a = %d b = %d' % (a , b)
print 'a+b = %d ' % (a+b)
print 'a-b = %d' % (a-b)
print 'a*b = %d' % (a*b)
print 'a/b = %d' % (a/b)
print r'a%b=' + '%d' % (a%b)

