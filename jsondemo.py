#coding=utf-8
import MySQLdb
global conn,cur
def saveemotion(values):
    try:
        cur.executemany('insert into qz_emotion(`qq`,`tid`,`content`,`create_time`,`like_num`) values(%s,%s,%s,%s,%s)',values)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
def savecomment(values):
    try:
        cur.executemany('insert into em_comment(`qq`,`name`,`content`,`create_time`) values(%s,%s,%s,%s)',values)
	conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('qzone')
    values=[]
    for i in range(0,10):
        values.append(("2421181819","7b4d5090b19bc4552b0c0200","hehe","2012-9-23 12:23:32",i))
    saveemotion(values)
    values1=[]
    for j in range(0,10):
        values1.append(("2421181819","张三",i,"2012-9-23 12:23:32"))
    savecomment(values1)
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])



