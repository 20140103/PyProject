#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itchat, time
import uniout
import re
from itchat.content import *

# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
# def text_reply(msg):
#     msg.user.send('%s: %s' % (msg.type, msg.text))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    strmsg = unicode(msg)
    print('msg',strmsg)
    print('msg', strmsg.find(u'智慧大保健实战冲锋队'))
    # if msg.find(u'智慧大保健实战冲锋队'):
    #     print u'这个群又开始说话了'
    #if msg.isAt:
    #msg.user.send(u'@%s\u2005I received: %s' % (
    #    msg.actualNickName, u'说话的人好帅'))

itchat.auto_login(True)
itchat.run(True)
# msg = u'asdfsadfasdfasdfasdfasfasdf智慧大保健实战冲锋队'
# print('msg', msg.find(u'智慧大保健实战冲锋队'))