#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import itchat

# itchat.auto_login()

# itchat.send('Hello, filehelper', toUserName='filehelper')

import itchat

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text

itchat.auto_login(hotReload=True)
itchat.run()