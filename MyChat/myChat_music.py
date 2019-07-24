#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itchat
import uniout

HELP_MSG = u'''\
欢迎使用微信网易云音乐
帮助： 显示帮助
关闭： 关闭歌曲
歌名： 按照引导播放音乐\
'''

@itchat.msg_register(itchat.content.TEXT)
def music_player(msg):

    print('msg', msg)
    if msg['ToUserName'] != 'filehelper': return
    if msg['Text'] == u'关闭':
        # close_music()
        itchat.send(u'音乐已关闭', 'filehelper')
    if msg['Text'] == u'帮助':
        itchat.send(u'帮助信息', 'filehelper')
    else:
        # itchat.send(interact_select_song(msg['Text']), 'filehelper')
        itchat.send(u'谢谢','filehelper')
 
itchat.auto_login(True)
itchat.send(HELP_MSG, 'filehelper') 
itchat.run()