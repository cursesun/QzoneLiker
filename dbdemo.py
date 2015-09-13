#coding=utf-8
import MySQLdb
global conn,cur
def getdepth(uin):
    try:
        cur.execute('select depth from qz_friend where depth=0 and qq='+str(uin))
        result=cur.fetchone()
        return result
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return (-1,)
try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('qzone2')
	depth=getdepth('2421181819')
    print depth
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
