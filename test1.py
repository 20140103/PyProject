#!/usr/bin/env python
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Twt'


print 'hello'
a = [1,2,3,4]
for value in a:
    if value % 2 == 0:
        print value

#print add(19,9)



#function define
def add(a,b):
    return a + b

print add(19,1)

# f(x) = x!
def fact(n):
    if n == 1:
        return 1
    return n * fact(n - 1)

print '5! = '
print  fact(5)

print 'hello world'
'''
i = 0
while(1):
    i+=1
    if i>100 :
        break
    print i
'''

'''
for i in range(10):
    print  i
while(1):
    age = int(raw_input('age:'))

    if age == 100:
        break
    print 'age = ', age
    print 'age = %s' % age
'''

name = ['张三','aa','asad']

print name
print name[0]
print name[-1]
print name[1:]
import os
print [d for d in os.listdir('.')] # os.listdir可以列出文件和目录
#['.emacs.d', '.ssh', '.Trash', 'Adlm', 'Applications', 'Desktop', 'Documents', 'Downloads', 'Library', 'Movies', 'Music', 'Pictures', 'Public', 'VirtualBox VMs', 'Workspace', 'XCode']



g = (x * x for x in range(10))

for n in g:
    print n

def fib(max):
    n,a,b = 0,0,1
    while n < max:
        yield b
        a,b = b,a+b
        n += 1
k = fib(6)
for i in k:
    print i

