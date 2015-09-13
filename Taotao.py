# -*- coding: utf-8	-*-
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
from HttpClient	import HttpClient

reload(sys)
sys.setdefaultencoding("utf-8")

# CONFIGURATION	FIELD
checkFrequency = 1
#check every k seconds
# STOP EDITING HERE
HttpClient_Ist = HttpClient()
UIN	= 0
skey = ''
Referer	= 'http://user.qzone.qq.com/'
QzoneLoginUrl =	'http://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=http%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&pt_qzone_sig=1&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=http%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html'

initTime = time.time()
#logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b	%Y %H:%M:%S')

def	getAbstime():
	return int(time.time())
	
def	date_to_millis(d):
	return int(time.mktime(d.timetuple())) * 1000

def	getReValue(html, rex, er, ex):
	v =	re.search(rex, html)

	if v is	None:
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
	def	__init__(self, vpath, qq=0):
		global UIN,	Referer, skey
		self.VPath = vpath	# QRCode保存路径
		AdminQQ	= int(qq)
		print "正在获取登陆页面"
		self.setCookie('_qz_referrer','qzone.qq.com','qq.com')
		self.Get(QzoneLoginUrl,'http://qzone.qq.com/')
		StarTime = date_to_millis(datetime.datetime.utcnow())
		T =	0
		while True:
			T =	T +	1
			self.Download('http://ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&daid=5',self.VPath)
			os.startfile('v.jpg')
			LoginSig = self.getCookie('pt_login_sig')
			print '[{0}] Get QRCode	Picture	Success.'.format(T)			 
			while True:
				html = self.Get('http://ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-{0}&js_ver=10131&js_type=1&login_sig={1}&pt_uistyle=32&aid=549000912&daid=5&pt_qzone_sig=1'.format(date_to_millis(datetime.datetime.utcnow()) -	StarTime, LoginSig), QzoneLoginUrl)
				ret	= html.split("'")
				if ret[1] == '65' or ret[1]	== '0':	 # 65: QRCode 失效,	0: 验证成功, 66: 未失效, 67: 验证中
					break
				time.sleep(2)
			if ret[1] == '0' or	T >	self.MaxTryTime:
				break

		if ret[1] != '0':
			return
		print "二维码已扫描，正在登陆"
		
		# 删除QRCode文件
		if os.path.exists(self.VPath):
			os.remove(self.VPath)

		# 记录登陆账号的昵称
		tmpUserName	= ret[11]

		self.Get(ret[5])
		UIN	= getReValue(ret[5], r'uin=([0-9]+?)&',	'Fail to get QQ	number', 1)
		Referer	= Referer+str(UIN)
		skey = self.getCookie('skey')

# -----------------
# 计算g_tk
# -----------------	  
def	utf8_unicode(c):			
	if len(c)==1:								  
		return ord(c)
	elif len(c)==2:
		n =	(ord(c[0]) & 0x3f) << 6				 
		n += ord(c[1]) & 0x3f			   
		return n		
	elif len(c)==3:
		n =	(ord(c[0]) & 0x1f) << 12
		n += (ord(c[1])	& 0x3f)	<< 6
		n += ord(c[2]) & 0x3f
		return n
	else:				 
		n =	(ord(c[0]) & 0x0f) << 18
		n += (ord(c[1])	& 0x3f)	<< 12
		n += (ord(c[2])	& 0x3f)	<< 6
		n += ord(c[3]) & 0x3f
		return n

def	getGTK(skey):
	hash = 5381
	for	i in range(0,len(skey)):
		hash +=	(hash << 5)	+ utf8_unicode(skey[i])
	return hash	& 0x7fffffff

def	saveemotion(values):
	try:
		cur.executemany('insert	into qz_emotion(`qq`,`name`,`tid`,`content`,`create_time`,`comment_num`,`source_name`) values(%s,%s,%s,%s,%s,%s,%s)',values)
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def	savecomment(values):
	try:
		cur.executemany('insert	into qz_comment(`qq`,`qq_name`,`comment_qq`,`tid`,`comment_name`,`content`,`create_time`) values(%s,%s,%s,%s,%s,%s,%s)',values)
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def	getallfriends(who):
	try:
		aa=cur.execute('select * from qz_friend	where who='+str(who))
		print "get ",who," friends count ",aa
		info = cur.fetchmany(aa)
		return info
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return None
def	getnotcheckedfriends(who):
	try:
		aa=cur.execute('select * from qz_friend	where flag=0 and who='+str(who))
		print "get ",who," friends count ",aa
		info = cur.fetchmany(aa)
		return info
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return None
def	getfriendsbyvisited(visited):
	try:
		aa=cur.execute('select * from qz_friend	where visited=%s',visited)
		info = cur.fetchmany(aa)
		return info
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return None
def	getfriendsbyneedinfo(who):
	try:
		aa=cur.execute('select * from qz_friend	where visited!=-1 and who=%s',who)
		info = cur.fetchmany(aa)
		return info
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return None
def	cannotvisit(uin):
	try:
		cur.execute('update	qz_friend set visited=-1 where qq='+str(uin))
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def	saveuserinfo(value):
	try:
		cur.execute('update	qz_friend set country=%s,province=%s,city=%s,address=%s,age=%s,sex=%s,birthyear=%s,birthday=%s,birth=%s,nickname=%s,visited=1 where	qq=%s',value)
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def	updateFlag(who):
	try:
		cur.execute('update	qz_friend set flag="1" where qq='+str(who))
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def	savefriend(value):
	try:
		cur.execute('insert	ignore into	qz_friend(`qq`,`who`,`name`,`sex`,`address`,`visited`) values(%s,%s,%s,%s,%s,%s)',value)
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def	savefriends(values):
	try:
		cur.executemany('insert	ignore into	qz_friend(`who`,`qq`,`name`) values(%s,%s,%s)',values)
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])	   
def	savechecked(value):
	try:
		cur.execute('insert ignore into qz_checked(`qq`,`name`) values(%s,%s)',value)
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def	getchecked(uin):
	try:
		count=cur.execute('select *	from qz_checked	where qq='+str(uin))
		return count
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return 1

def	GetUserInfo(uin):
	refer="http://user.qzone.qq.com/"+uin
	html = HttpClient_Ist.Get('http://user.qzone.qq.com/p/base.s8/cgi-bin/user/cgi_userinfo_get_all?uin={0}&vuin={1}&fupdate=1&rd=0.8255438883733334&g_tk={2}'.format(uin,QQ,str(getGTK(skey))), refer)
	html=html.replace('_Callback(','')
	html=html.replace(');','')
	code=0
	message=''
	try:
		data=json.loads(html)
		code=data['code']
		message=data['message']
		if data['data']!=None:
			country=data['data']['country']
		if country=='':
			country=data['data']['hco']
		province=data['data']['province']
		if province=='':
			province=data['data']['hp']
		city=data['data']['city']
		if city=='':
			city=data['data']['hc']
		address=country+province+city
		age=data['data']['age']
		sex=data['data']['sex']
		birthyear=data['data']['birthyear']
		birthday=data['data']['birthday']
		birth=str(birthyear)+"-"+str(birthday)
		nickname=data['data']['nickname']
		saveuserinfo((country,province,city,address,age,sex,birthyear,birthday,birth,nickname,uin))
		print "save",uin," userinfo	success"
	except Exception,e:
		print "=============save ",uin," userinfo fails",message
		if code==-99997:
			os._exit(0)
		#cannotvisit(uin)
	return

def	GetFriends(uin):
	if uin!=QQ:
		print "QQ not equals uin"
	return []
	message=''
	code=0
	try:
		refer="http://ctc.qzs.qq.com/qzone/v8/pages/friends/friend_index.html"
		html = HttpClient_Ist.Get('http://r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={0}&do=1&rd=0.8040608533192426&fupdate=1&clean=1&g_tk={1}'.format(uin,str(getGTK(skey))), refer)
		html=html.replace('_Callback(','')
		html=html.replace(');','')
		data=json.loads(html)
		friends=[]
		if data['data']!=None:
			if data['data']['items_list']>0:
				for	i in range(0,len(data['data']['items_list'])):
					f_qq=data['data']['items_list'][i]['uin']
					f_name=data['data']['items_list'][i]['name']
					friends.append((uin,f_qq,f_name))
		return friends
	except Exception,e:
		print "=============get	",uin,"	friends	fails",message,code
	return []
def	GetVisitor(who):
	refer="http://ctc.qzs.qq.com/qzone/v6/friend_manage/visitors.html"
	html = HttpClient_Ist.Get('http://g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_simple?uin={0}&mask=2&g_tk={1}&page=1&fupdate=1'.format(who,str(getGTK(skey))),	refer)
	html=html.replace('_Callback(','')
	html=html.replace(');','')
	data=json.loads(html)
	friends=[]
	if data['message']=='succ':
		if data['data']['count']>0:
			for	i in range(0,len(data['data']['items'])):
				uin=data['data']['items'][i]['uin']
				name=data['data']['items'][i]['name']
				visit_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['items'][i]['time']))
				friends.append((uin,who,name,'',''))
	return friends
def	TaotHandler(uin,pos,num):
	refer="http://cnc.qzs.qq.com/qzone/app/mood_v6/html/index.html"
	html = HttpClient_Ist.Get('http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={0}&inCharset=utf-8&outCharset=utf-8&hostUin={1}&notice=0&sort=0&pos={2}&num={3}&cgi_host=http%3A%2F%2Ftaotao.qq.com%2Fcgi-bin%2Femotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={4}'.format(uin,QQ,pos,num,str(getGTK(skey))), refer)
	html=html.replace('_Callback(','')
	html=html.replace(');','')
	try:
		data=json.loads(html)
		emotions=[]
		comments=[]
		for	i in range(0,len(data['msglist'])):
			if data['msglist'][i]==None:
				break
			content=data['msglist'][i]['content']
			create_time=time.strftime("%Y-%m-%d	%H:%M:%S", time.localtime(data['msglist'][i]['created_time']))
			cmtnum=data['msglist'][i]['cmtnum']
			tid=str(data['msglist'][i]['tid'])
			name=data['msglist'][i]['name']
			source_name=data['msglist'][i]['source_name']
			emotions.append((uin,name,tid,content,create_time,cmtnum,source_name))
			if int(cmtnum)>0:
				commentlist=data['msglist'][i]['commentlist']
				for	j in range(0,len(commentlist)):
					if commentlist[j]==None:
						break;
					c_qq=str(commentlist[j]['uin'])
					c_content=str(commentlist[j]['content'])
					c_createTime=str(time.strftime("%Y-%m-%d %H:%M:%S",	time.localtime(commentlist[j]['create_time'])))
					c_name=str(commentlist[j]['name'])
					comments.append((uin,name,c_qq,tid,c_name,c_content,c_createTime))
					#logging.info(c_qq+tid+c_name+c_content+c_createTime+str(len(comments)))
					if len(c_qq)<=12:
						savefriend((c_qq,uin,c_name,'','','0'))
						#logging.info("========c_qq=========="+commentlist[j])
		if len(emotions)>0:
			saveemotion(emotions)
		if len(comments)>0:
			savecomment(comments)
		print "qq:",uin,"pos:",pos,"...save	emotion	count is ",len(emotions)," comment count is	",len(comments)
	except Exception,e:
		#logging.info("===========html json========="+html)
		logging.info("===========html json========="+uin+e)
		raise StandardError(e)

#如果list不为None，则爬取list一个人的说说后再爬取他好友的说说，注意这里的root_qq最好要有很多说说
#如果list为None，则爬取friend的所有好友的说说
def	begin(root_qq,list=None):
	if list==None:
		list=getnotcheckedfriends(root_qq)
	while list!=None and len(list)>0:
		count=len(list)
		for	f in list:
			count=count-1
			errtime=0
			begin=0
			if getchecked(f[1])==0:
				print "===============begin	get	",f[1]," emotions index	is ",count
				while True:
					try:
						if errtime > 1:
							break
						TaotHandler(f[1],begin,20)	#爬取用户的说说，评论，以及好友
						#time.sleep(checkFrequency)
						errtime	= 0
						begin=begin+20
					except Exception, e:
						print e
						errtime	= errtime +	1
					updateFlag(f[1])#更新qz_friend，表示该用户已经爬取过
					savechecked((f[1],f[2]))#更新qz_checked，表示该用户已经爬取过
					print "===============over	get	",f[1]," emotions"
			else:
				print f[1]," has been checked"
				updateFlag(f[1])#更新qz_friend，表示该用户已经爬取过
			list=getnotcheckedfriends(root_qq)
def	getloginqqfriend():
	friends=GetFriends(QQ)
	if len(friends)>0:
		savefriends(friends)
def	fillfriendsinfo(uin):
	oldlist=[]
	temp=getfriendsbyneedinfo(uin)
	if temp!=None and len(temp)>0:
		print "get ",uin," friends info"
		for	t in temp:
			if t[1]	not	in oldlist:
				GetUserInfo(t[1])
				oldlist.append(t[1])
# -----------------
# 主程序
# -----------------
if __name__	== "__main__":
	global QQ,num,checked
	global conn,cur
	vpath =	'./v.jpg'
	QQ=	2421181819
	num=20
	checked=[]
	if len(sys.argv) > 1:
		vpath =	sys.argv[1]
	if len(sys.argv) > 2:
		QQ = sys.argv[2]
	try:
		qqLogin	= Login(vpath, QQ)
	except Exception, e:
		print str(e)
		os._exit()
	try:
		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
		cur=conn.cursor()
		conn.select_db('qzone')
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	
	roots=getallfriends(QQ)
	if len(roots)>0:
		ll=len(roots)
		for	root in	roots:
		   ll=ll-1
		   print root[1],"is root begin...",ll
		   begin(root[1])
		   updateFlag(root[1])
		   savechecked((f[1],f[2]))#更新qz_checked，表示该用户已经爬取过
		   print root[1],"is root over..."
		
	#root_qq="853912656"
	#begin(root_qq)
	#begin(root_qq,[('0',root_qq,'naweixians')])
	#getloginqqfriend()
	#fillfriendsinfo("742814483")