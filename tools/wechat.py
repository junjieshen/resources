#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from os import path
# Sending pictures and status to wechat
import itchat

@itchat.msg_register(itchat.content.TEXT)
def auto_reply(msg):
    #if msg['FromUserName'] != 'Elvis_S':
    #    print('Got message, but not for me')
    #    return
    if msg['Text'] == u'开始':
        itchat.send(u'不好意思，现在正忙，稍候给你回复。如果有重要的事情，请回复“重要”', msg['FromUserName'])
    if msg['Text'] == u'重要':
        itchat.send(u'你确定重要吗？要不要再考虑一下？如果真的很重要，请回复“很重要”', msg['FromUserName'])
    if msg['Text'] == u'很重要':
        itchat.send(u'再重要都没用！！', msg['FromUserName'])

itchat.auto_login(enableCmdQR=2, hotReload=True)

me = itchat.search_friends(wechatAccount='Elvis_S')
huan = itchat.search_friends(wechatAccount='harris_ch')
if not huan:
    print('no huan found')
#friends = itchat.get_friends(update=True)
itchat.run()
#itchat.logout()
