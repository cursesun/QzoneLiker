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

#说说总数top20
sql1='select count(*) count,name,qq from qz_emotion group by qq order by count desc limit 0,20'

#评论总数top20
sql2='select sum(comment_num) num,name,qq from qz_emotion group by qq order by num desc limit 0,20'

#说说数量top20的说说评论率
sql3='select * from (select sum(comment_num) c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by e_num desc limit 0,20) as a order by a.r desc'

#评论数量top20的说说评论率
sql4='select * from (select sum(comment_num) c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by c_num desc limit 0,20) as a order by a.r desc'

#没有任何限制的情况下top20评论率
sql5='select * from (select sum(comment_num) as c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by r desc limit 0,20) as a'

#说说数量1000以上的评论率top20
sql6='select * from (select sum(comment_num) as c_num,count(id) e_num,sum(comment_num)/count(id) r,name,qq from qz_emotion group by qq order by r desc) as a where a.e_num>1000'

#我的好友里评论说说数top20
sql7='select count(id) count,comment_qq,comment_name from qz_comment where comment_qq in (select qq from qz_friend where who='2421181819') group by comment_qq order by count desc limit 0,20'

#我的二度好友里说说数top20
sql8='select count(id) count,comment_qq,comment_name from qz_comment group by comment_qq order by count desc limit 0,20'

#按年份统计
sql9='select count(id) count,date_format(create_time,'%y') sdate from qz_emotion group by sdate order by sdate desc'

#按月统计
sql10='select count(id) count,date_format(create_time,'%m') sdate from qz_emotion group by sdate order by sdate desc'

#按年月统计
sql11='select count(id) count,date_format(create_time,'%y-%m') sdate from qz_emotion group by sdate order by sdate desc'

#按日统计
sql12='select count(id) count,date_format(create_time,'%d') sdate from qz_emotion group by sdate order by sdate desc'

#按小时统计
sql13='select count(id) count,date_format(create_time,'%H') sdate from qz_emotion group by sdate order by sdate desc'

