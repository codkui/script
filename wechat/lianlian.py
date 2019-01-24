#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018 12 28 00 59
# Project: 心心
from __future__ import unicode_literals
import requests
import time
import json


from wxpy import *
from wechat_sender import listen
import _thread

lastId=0
goods=[]
xinxin=True
def getList():
    global xinxin
    nowT=int(round(time.time() * 1000))
    goodList=requests.get("https://api.lianlianlvyou.com/v1/wx/list?&i=wx3ed1ccc70f9740b4&timestamp="+str(nowT) )
    # print(goodList.text)
    datas=json.loads(goodList.text)
    # print(datas)
    relData=datas["data"]["list"]["data"]
    global goods
    global lastId
    for i in range(len(relData)) :
        if relData[i]["id"]>lastId :
            lastId=relData[i]["id"]
            url=getInfo(relData[i]["id"])
            goods.append({"id":relData[i]["id"],"title":relData[i]["title"],"url":url})
            print("获取到全新商品："+str(relData[i]["id"])+relData[i]["title"])
            xinxin.send('新商品上线：'+relData[i]["title"]+"   "+url)
            time.sleep(1)
    print(goods)

def getInfo(id):
    nowT=int(round(time.time() * 1000))
    res=requests.get("https://api.lianlianlvyou.com/v1/wx/product2?i=wx3ed1ccc70f9740b4&id="+str(id)+"&timestamp="+str(nowT))
    datas=json.loads(res.text)
    return datas["data"]["productHtmlUrl"]
def timeOut(a,b):
    while True:
        try:
            getList()
        except:
            print("抓取发生异常")
        
        time.sleep(60)
        




if __name__=='__main__':
    
    bot = Bot('bot.pkl')
    # global my_friend
    # global xinxin
    xinxin = bot.friends().search('心花开时雨亦晴')[0]
    bot.file_helper.send('通知机器人已上线')
    def keepLive(a,b):
        num=0
        while True:
            
            # if num%10==0: 
            bot.file_helper.send('通知机器人持续在线')
            # bot.file_helper.send('')
            # print("发送了保持消息")
            num+=1
            time.sleep(120)
    _thread.start_new_thread( keepLive, ("Thread-1", 2, ) )
    # tuling = Tuling(api_key='25cf318ad5fb4e11bfc6b192fe907c8d')
    # xiaoi = XiaoI('open_ZGhc0vg3Lk5G', 'FZvepGoKqzR1lYoMvLOH')
    
    # 使用小 i 机器人自动与指定好友聊天
    # @bot.register(my_friend)
    # def reply_my_friend(msg):
    #     xiaoi.do_reply(msg)
    # @bot.register(Friend)
    # def reply_test(msg):
    #     print(msg)
    #     # msg.reply('test')
    #     tuling.do_reply(msg)
    # def text_reply(msg):
    #     api_url = 'http://www.tuling123.com/openapi/api'
    #     apikey = '25cf318ad5fb4e11bfc6b192fe907c8d'
    #     data = {'key': apikey,'info': msg}
    #     req = requests.post(api_url, data=data).text
    #     replys = json.loads(req)['text']
    #     return replys
    print("开始抓取任务")
    _thread.start_new_thread( timeOut, ("Thread-1",3, ) )
    print("开始启动微信联系")
    listen(bot) # 只需改变最后一行代码
    time.sleep(10)
    
    # timeOut(my_friend)