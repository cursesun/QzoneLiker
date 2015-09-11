import MySQLdb

global conn,cur

def executesql(sql):
    try:
        aa=cur.execute(sql)
	info = cur.fetchmany(aa)
	return result
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return None

try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('qzone1')
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#˵˵����top20
sql1='select count(*) count,name,qq from qz_emotion group by qq order by count desc limit 0,20'

#��������top20
sql2='select sum(comment_num) num,name,qq from qz_emotion group by qq order by num desc limit 0,20'

#˵˵����top20��˵˵������
sql3='select * from (select sum(comment_num) c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by e_num desc limit 0,20) as a order by a.r desc'

#��������top20��˵˵������
sql4='select * from (select sum(comment_num) c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by c_num desc limit 0,20) as a order by a.r desc'

#û���κ����Ƶ������top20������
sql5='select * from (select sum(comment_num) as c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by r desc limit 0,20) as a'

#˵˵����1000���ϵ�������top20
sql6='select * from (select sum(comment_num) as c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by r desc) as a where a.e_num>1000'

#�ҵĺ���������˵˵��top20
sql7='select count(id) count,comment_qq,comment_name from qz_comment where comment_qq in (select qq from qz_friend where who='2421181819') group by comment_qq order by count desc limit 0,20'

#�ҵĶ��Ⱥ�����˵˵��top20
sql8='select count(id) count,comment_qq,comment_name from qz_comment group by comment_qq order by count desc limit 0,20'

#�����ͳ��
sql9='select count(id) count,date_format(create_time,'%y') sdate from qz_emotion group by sdate order by sdate desc'

#����ͳ��
sql10='select count(id) count,date_format(create_time,'%m') sdate from qz_emotion group by sdate order by sdate desc'

#������ͳ��
sql11='select count(id) count,date_format(create_time,'%y-%m') sdate from qz_emotion group by sdate order by sdate desc'

#����ͳ��
sql12='select count(id) count,date_format(create_time,'%d') sdate from qz_emotion group by sdate order by sdate desc'

#��Сʱͳ��
sql13='select count(id) count,date_format(create_time,'%H') sdate from qz_emotion group by sdate order by sdate desc'

