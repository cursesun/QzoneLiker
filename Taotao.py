# -*- coding: utf-8 -*-
import re
import random
import json
import os
import sys
import datetime
import time
import threading
import urllib
import MySQLdb
import logging
from HttpClient import HttpClient

reload(sys)
sys.setdefaultencoding("utf-8")

# CONFIGURATION FIELD
checkFrequency = 10
#check every k seconds
# STOP EDITING HERE
HttpClient_Ist = HttpClient()
UIN = 0
skey = ''
Referer = 'http://user.qzone.qq.com/'
QzoneLoginUrl = 'http://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=http%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&pt_qzone_sig=1&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=http%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html'

initTime = time.time()
logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

def getAbstime():
    return int(time.time())
    
def date_to_millis(d):
    return int(time.mktime(d.timetuple())) * 1000

def getReValue(html, rex, er, ex):
    v = re.search(rex, html)

    if v is None:
        print er

        if ex:
            raise Exception, er
        return ''

    return v.group(1)
    
# -----------------
# 登陆
# -----------------
class Login(HttpClient):
    MaxTryTime = 5

    def __init__(self, vpath, qq=0):
        global UIN, Referer, skey
        self.VPath = vpath  # QRCode保存路径
        AdminQQ = int(qq)
        print "正在获取登陆页面"
        self.setCookie('_qz_referrer','qzone.qq.com','qq.com')
        self.Get(QzoneLoginUrl,'http://qzone.qq.com/')
        StarTime = date_to_millis(datetime.datetime.utcnow())
        T = 0
        while True:
            T = T + 1
            self.Download('http://ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&daid=5', self.VPath)
            LoginSig = self.getCookie('pt_login_sig')
            print '[{0}] Get QRCode Picture Success.'.format(T)          
            while True:
                html = self.Get('http://ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-{0}&js_ver=10131&js_type=1&login_sig={1}&pt_uistyle=32&aid=549000912&daid=5&pt_qzone_sig=1'.format(date_to_millis(datetime.datetime.utcnow()) - StarTime, LoginSig), QzoneLoginUrl)
                ret = html.split("'")
                if ret[1] == '65' or ret[1] == '0':  # 65: QRCode 失效, 0: 验证成功, 66: 未失效, 67: 验证中
                    break
                time.sleep(2)
            if ret[1] == '0' or T > self.MaxTryTime:
                break

        if ret[1] != '0':
            return
        print "二维码已扫描，正在登陆"
        
        # 删除QRCode文件
        if os.path.exists(self.VPath):
            os.remove(self.VPath)

        # 记录登陆账号的昵称
        tmpUserName = ret[11]

        self.Get(ret[5])
        UIN = getReValue(ret[5], r'uin=([0-9]+?)&', 'Fail to get QQ number', 1)
        Referer = Referer+str(UIN)
        skey = self.getCookie('skey')

# -----------------
# 计算g_tk
# -----------------  
def utf8_unicode(c):            
    if len(c)==1:                                 
        return ord(c)
    elif len(c)==2:
        n = (ord(c[0]) & 0x3f) << 6              
        n += ord(c[1]) & 0x3f              
        return n        
    elif len(c)==3:
        n = (ord(c[0]) & 0x1f) << 12
        n += (ord(c[1]) & 0x3f) << 6
        n += ord(c[2]) & 0x3f
        return n
    else:                
        n = (ord(c[0]) & 0x0f) << 18
        n += (ord(c[1]) & 0x3f) << 12
        n += (ord(c[2]) & 0x3f) << 6
        n += ord(c[3]) & 0x3f
        return n

def getGTK(skey):
    hash = 5381
    for i in range(0,len(skey)):
        hash += (hash << 5) + utf8_unicode(skey[i])
    return hash & 0x7fffffff

def saveemotion(values):
    try:
        cur.executemany('insert into qz_emotion(`qq`,`tid`,`content`,`create_time`,`comment_num`) values(%s,%s,%s,%s,%s)',values)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def savecomment(values):
    try:
        cur.executemany('insert into em_comment(`qq`,`tid`,`name`,`content`,`create_time`) values(%s,%s,%s,%s,%s)',values)
	conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def TaotHandler(qq,uin,pos,num):
    refer="http://cnc.qzs.qq.com/qzone/app/mood_v6/html/index.html"
    html = HttpClient_Ist.Get('http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={0}&inCharset=utf-8&outCharset=utf-8&hostUin={1}&notice=0&sort=0&pos={2}&num={3}&cgi_host=http%3A%2F%2Ftaotao.qq.com%2Fcgi-bin%2Femotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={4}'.format(uin,qq,pos,num,str(getGTK(skey))), refer)
    html=html.replace('_Callback(','')
    html=html.replace(');','')
    data=json.loads(html)
    emotions=[]
    comments=[]
    #这里要判断是否存在msglist，不存在则不再执行
    for i in range(0,len(data['msglist'])):
        if data['msglist'][i]==None:
	    break
	content=data['msglist'][i]['content']
	create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['msglist'][i]['created_time']))
	cmtnum=data['msglist'][i]['cmtnum']
	tid=str(data['msglist'][i]['tid'])
	emotions.append((qq,tid,content,create_time,cmtnum))
	if int(cmtnum)>0:
	    commentlist=data['msglist'][i]['commentlist']
            for j in range(0,len(commentlist)):
	        if commentlist[j]==None:
	            break;
	        c_qq=str(commentlist[j]['uin'])
	        c_content=str(commentlist[j]['content'])
	        c_createTime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(commentlist[j]['create_time'])))
	        c_name=str(commentlist[j]['name'])
	        comments.append((c_qq,tid,c_name,c_content,c_createTime))
	        logging.info(c_qq+tid+c_name+c_content+c_createTime+str(len(comments)))
    if len(emotions)>0:
        saveemotion(emotions)
    if len(comments)>0:
        savecomment(comments)
    print "qq:",uni,"pos:",pos,"...save emotion count is ",len(emotions)," comment count is ",len(comments)
    logging.info("qq:"+str(uni)+"pos:"+str(pos)+" over..")
    
# -----------------
# 主程序
# -----------------
if __name__ == "__main__":
    vpath = './v.jpg'
    qq = 2421181819
    friend=814180665
    num=20
    if len(sys.argv) > 1:
        vpath = sys.argv[1]
    if len(sys.argv) > 2:
        qq = sys.argv[2]

    try:
        qqLogin = Login(vpath, qq)
    except Exception, e:
        print str(e)
        os._exit()
    try:
        global conn,cur
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('qzone')
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    errtime=0
    count=0
    while True:
        try:
            if errtime > 5:
                break
            TaotHandler(qq,friend,count,num)
            time.sleep(checkFrequency)
            errtime = 0
	    count=count+20
        except Exception, e:
            print e
            errtime = errtime + 1
