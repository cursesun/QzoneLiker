#coding=utf-8
import MySQLdb
global conn,cur
def getfriendsbyvisited(visited):
    try:
        aa=cur.execute('select * from qz_friend where visited=%s limit 170,180',visited)
	info = cur.fetchmany(aa)
	return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return None
try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('qzone')
    temp=getfriendsbyvisited(-1)
    if temp!=None and len(temp)>0:
        for t in temp:
	    print t[0],t[1]
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])



