#coding=utf-8
import MySQLdb
global conn,cur
def getfriends():
    try:
		aa=cur.execute('select `who`,`qq`,`name`,`visited`,`depth` from qz_friend where depth=4 limit 160000,10000')
		info = cur.fetchmany(aa)
		return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return (-1,)

def saveuserinfo(values):
	try:
		cur.executemany('insert ignore into qz_emotion(`who`,`qq`,`name`,`visited`,`depth`) values(%s,%s,%s,%s,%s)',values)
		conn.commit()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return (-1,)
try:
	conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
	cur=conn.cursor()
	conn.select_db('qzone2')
	result=getfriends()
	print len(result)
	saveuserinfo(result)
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])