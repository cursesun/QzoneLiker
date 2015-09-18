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

HttpClient_Ist = HttpClient()

NDLoginUrl="http://jwgl.jxau.edu.cn/user/checklogin"
Referer="http://jwc.jxau.edu.cn/"
logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b	%Y %H:%M:%S')
def	getReValue(html, rex, er, ex):
	v =	re.search(rex, html)
	if v is	None:
		print er
		if ex:
			raise Exception, er
		return ''
	return v.group(1)
class Login(HttpClient):
	def __init__(self,username,password):
		data = (
			('UserName', username),
			('PassWord', password)
		)
		rsp = HttpClient_Ist.Post(NDLoginUrl, data, Referer)
		#logging.info(rsp)
		self.guid=getReValue(rsp, r'(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})', 'Fail to get guid', 0)
		print "guid is ",self.guid
def getacademy():
	if len(guid)!=36:
		print "guid error",guid
		os._exit(0)
	url="http://jwgl.jxau.edu.cn/Common/BaseData/GetTreeListForCetCj/"+guid
	data = (
		('method', "POST"),
		('treeroot', "treeroot"),
		('parentid', "treeroot")
	)
	academys=[]
	try:
		html = HttpClient_Ist.Post(url, data, Referer)
		logging.info(html)
		data=json.loads(html)
		if data!=None and len(data)>0:
			for i in range(0,len(data)):
				node=data[i]
				#print node["id"],node["text"]
				academys.append((node["id"],node["text"]))
		else:
			print "academy data is none"
	except Exception,e:
		print "error",e
		logging.debug("===========html json========="+e)
	return academys
def getdata(node,parentid):
	if len(guid)!=36:
		print "guid error",guid
		os._exit(0)
	url="http://jwgl.jxau.edu.cn/Common/BaseData/GetTreeListForCetCj/"+guid
	data = (
		('method', "POST"),
		('node', node),
		('parentid', parentid)
	)
	datas=[]
	try:
		html = HttpClient_Ist.Post(url, data, Referer)
		#logging.info(html)
		data=json.loads(html)
		if data!=None and len(data)>0:
			for i in range(0,len(data)):
				node=data[i]
				#print node["id"],node["text"]
				datas.append((node["id"],node["text"]))
		else:
			print "datas is none"
	except Exception,e:
		print "error",e
		logging.debug("===========html json========="+e)
	return datas
def getstudents(bjdm,dir1="ASC",limit="100",sort="Xjzt",start=0):
	if len(guid)!=36:
		print "guid error",guid
		os._exit(0)
	url="http://jwgl.jxau.edu.cn/XueJiManage/XueJiManage/GetXueJiList/"+guid
	data = (
		('bjdm', bjdm),
		('dir', dir1),
		('limit', limit),
		('sort', sort),
		('start', start)
	)
	students=[]
	try:
		html = HttpClient_Ist.Post(url, data, Referer)
		logging.info(html)
		data=json.loads(html)
		totalCount=data["totalCount"]
		if totalCount>0:
			datas=data["Data"]
			if datas!=None and len(datas)>0:
				for i in range(0,len(datas)):
					node=datas[i]
					sno=node["Xh"]
					name=node["Xm"]
					sex=node["Xb"]
					birth=node["Csny"]
					address=node["HomeAddress"]
					if address==None or address=="":
						address=node["Jg"]
					academy=node["Yxmc"]
					major=node["Zymc"]
					classname=node["Bjmc"]
					classno=node["Bjdm"]
					print sno,name,sex,birth,address,academy,major,classname,classno
					students.append((sno,name,sex,birth,address,academy,major,classname,classno))
			else:
				print "students is none"
	except Exception,e:
		print "error",e
		logging.debug("===========html json========="+e)
	return students
def savestudents(values):
	try:
		count=cur.executemany('insert ignore into student(`sno`,`name`,`sex`,`birth`,`address`,`academy`,`major`,`classname`,`classno`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',values)
		conn.commit()
		return count
	except MySQLdb.Error,e:
		print e
	return 0
# -----------------
# 主程序
# -----------------
if __name__	== "__main__":
	global conn,cur
	try:
		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
		cur=conn.cursor()
		conn.select_db('ndstudents')
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

	global username,password,guid
	username=""#学号
	password=""#密码
	errtime=0
	while True:
		try:
			ndLogin	= Login(username, password)
			if len(ndLogin.guid)==36:
				break;
		except Exception, e:
			print str(e)
			errtime=errtime+1
			if errtime>10:
				os._exit(0)
	guid=ndLogin.guid
	academys=getacademy()
	if academys!=None and len(academys)>0:
		for i in range(0,len(academys)):
			print "=========academys no ",i,academys[i][1],"data"
			majors=getdata(academys[i][0],academys[i][0])#4
			if majors!=None and len(majors)>0:
				for j in range(0,len(majors)):
					print "==============majors no ",j,majors[j][1],"data"
					classes=getdata(majors[j][0],majors[j][0])#8
					if classes!=None and len(classes)>0:
						for k in range(0,len(classes)):
							print "=====================classes no ",k,classes[k][1],"data"
							students=getstudents(classes[k][0])
							if students!=None and len(students)>0:
								savestudents(students)
							print "=====================classes no ",k,classes[k][1],"data over====================="
					print "==============majors no ",j,majors[j][1],"data over=============="
			print "=========academys no ",i,academys[i][1],"data over========="

'''
create database ndstudents;
CREATE TABLE `student` (
  `sno` varchar(20) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `sex` varchar(2) DEFAULT NULL,
  `birth` varchar(15) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `academy` varchar(100) DEFAULT NULL,
  `major` varchar(100) DEFAULT NULL,
  `classname` varchar(100) DEFAULT NULL,
  `classno` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''