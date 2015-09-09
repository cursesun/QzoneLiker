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
checkFrequency = 1
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
        cur.executemany('insert into qz_emotion(`qq`,`name`,`tid`,`content`,`create_time`,`comment_num`) values(%s,%s,%s,%s,%s,%s)',values)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def savecomment(values):
    try:
        cur.executemany('insert into qz_comment(`qq`,`qq_name`,`comment_qq`,`tid`,`comment_name`,`content`,`create_time`) values(%s,%s,%s,%s,%s,%s,%s)',values)
	conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def updateFlag(who):
    try:
        cur.execute('update qz_friend set flag="1" where qq='+str(who))
	conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def savefriend(value):
    try:
        cur.execute('insert into qz_friend(`qq`,`who`,`name`,`sex`,`address`,`online`) values(%s,%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE online=0',value)
	conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def getfriends(who):
    try:
        aa=cur.execute('select * from qz_friend where flag=0 and who='+str(who))
	print "get ",who," friends count ",aa
	info = cur.fetchmany(aa)
	return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return None
def savechecked(value):
    try:
        cur.execute('insert into qz_checked(`qq`,`name`) values(%s,%s)',value)
	conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def getchecked(qq):
    try:
        count=cur.execute('select * from qz_checked where qq='+str(qq))
	return count
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return 1

def GetVisitor(who):
    refer="http://ctc.qzs.qq.com/qzone/v6/friend_manage/visitors.html"
    html = HttpClient_Ist.Get('http://g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_simple?uin={0}&mask=2&g_tk={1}&page=1&fupdate=1'.format(who,str(getGTK(skey))), refer)
    html=html.replace('_Callback(','')
    html=html.replace(');','')
    data=json.loads(html)
    friends=[]
    if data['message']=='succ':
        if data['data']['count']>0:
            for i in range(0,len(data['data']['items'])):
	        uin=data['data']['items'][i]['uin']
		name=data['data']['items'][i]['name']
		online=data['data']['items'][i]['online']
		visit_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['items'][i]['time']))
		friends.append((uin,who,name,'','',online))
    return friends

def TaotHandler(uin,pos,num):
    refer="http://cnc.qzs.qq.com/qzone/app/mood_v6/html/index.html"
    html = HttpClient_Ist.Get('http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={0}&inCharset=utf-8&outCharset=utf-8&hostUin={1}&notice=0&sort=0&pos={2}&num={3}&cgi_host=http%3A%2F%2Ftaotao.qq.com%2Fcgi-bin%2Femotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={4}'.format(uin,qq,pos,num,str(getGTK(skey))), refer)
    html=html.replace('_Callback(','')
    html=html.replace(');','')
    if 'msglist' not in html:
        raise StandardError("msglist not found")
    if 'msglist' in html:
        data=json.loads(html)
        emotions=[]
        comments=[]
        for i in range(0,len(data['msglist'])):
            if data['msglist'][i]==None:
	        break
	    content=data['msglist'][i]['content']
	    create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['msglist'][i]['created_time']))
	    cmtnum=data['msglist'][i]['cmtnum']
	    tid=str(data['msglist'][i]['tid'])
	    name=data['msglist'][i]['name']
	    emotions.append((uin,name,tid,content,create_time,cmtnum))
	    if int(cmtnum)>0:
	        commentlist=data['msglist'][i]['commentlist']
                for j in range(0,len(commentlist)):
	            if commentlist[j]==None:
	                break;
	            c_qq=str(commentlist[j]['uin'])
	            c_content=str(commentlist[j]['content'])
	            c_createTime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(commentlist[j]['create_time'])))
	            c_name=str(commentlist[j]['name'])
	            comments.append((uin,name,c_qq,tid,c_name,c_content,c_createTime))
	            #logging.info(c_qq+tid+c_name+c_content+c_createTime+str(len(comments)))
		    if len(c_qq)>12:
		        logging.info(commentlist[j])
		    else:
		        savefriend((c_qq,uin,c_name,'','','0'))
        if len(emotions)>0:
            saveemotion(emotions)
        if len(comments)>0:
            savecomment(comments)
        print "qq:",uin,"pos:",pos,"...save emotion count is ",len(emotions)," comment count is ",len(comments)
        logging.info("qq:"+str(uin)+"pos:"+str(pos)+" over..")
def begin(friend,list=None):
    if list==None:
        list=getfriends(friend)
    while list!=None and len(list)>0:
        count=len(list)
        for f in list:
	    count=count-1
            errtime=0
	    begin=0
	    if getchecked(f[1])==0:
	        print "begin get ",f[1]," emotion ",count
                while True:
                    try:
                        if errtime > 1:
                            break
                        TaotHandler(f[1],begin,num)
                        #time.sleep(checkFrequency)
                        errtime = 0
	                begin=begin+20
                    except Exception, e:
                        print e
                        errtime = errtime + 1
		updateFlag(f[1])
		savechecked((f[1],f[2]))
                print "over get ",f[1]," emotion "
	    else:
	        print f[1]," has been checked"
        list=getfriends(friend)
# -----------------
# 主程序
# -----------------
if __name__ == "__main__":
    global qq,num
    vpath = './v.jpg'
    qq= 2421181819
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
    friend="2421181819"
    #begin(friend,[('0',friend,'naweixians')])
    begin(friend)