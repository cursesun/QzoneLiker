#!/usr/bin/python
# -*- coding: utf-8 -*-
from pychartdir import *
import MySQLdb
def executesql(sql):
    try:
        aa=cur.execute(sql)
	result = cur.fetchmany(aa)
	return result
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return None
def showresult0(info,file):
    counts= [f[0] for f in info]
    names = [f[1] for f in info]
    width=len(counts)*40
    if len(counts)<10:
        width=len(counts)*100
    height=1000
    c = XYChart(width,height)		# img width height
    c.setPlotArea(60,40,width-100,height-100)	#x,y,width,height
    c.addBarLayer(counts)		#y
    c.xAxis().setLabels(names)		#x
    c.setDefaultFonts("simsun.ttc")	#font
    c.makeChart(file+".png")		#file

def showresult1(info,file):
    counts= [f[0] for f in info]
    names = [f[1] for f in info]
    width=len(counts)*40
    if len(counts)<10:
        width=len(counts)*100
    height=1000
    c = XYChart(width,height)
    c.setPlotArea(70, 20, width-100,height-100, Transparent, -1, Transparent, 0xcccccc)
    c.xAxis().setColors(Transparent)
    c.yAxis().setColors(Transparent)
    c.xAxis().setLabelStyle("arial.ttf", 12)
    c.yAxis().setLabelStyle("arial.ttf", 12)
    layer = c.addBarLayer(counts, 0x6699bb)
    layer.setBorderColor(Transparent, barLighting(0.8, 1.3))
    layer.setRoundedCorners()
    layer.setAggregateLabelStyle("Arial", 12)
    c.xAxis().setLabels(names)
    c.yAxis().setTickDensity(40)
    c.yAxis().setTitle("Y-Axis Title Placeholder", "arialbd.ttf", 14, 0x555555)
    c.makeChart(file+".png")
def showresult2(info,file):
    counts= [f[0] for f in info]
    names = [f[1] for f in info]
    width=len(counts)*40
    if len(counts)<10:
        width=len(counts)*100
    height=1000
    c = XYChart(width,height)
    colors = [0x5588bb, 0x66bbbb, 0xaa6644, 0x99bb55, 0xee9944, 0x444466, 0xbb5555]
    c.setPlotArea(70, 20, width-100,height-100, Transparent, -1, Transparent, 0xcccccc)
    c.xAxis().setColors(Transparent)
    c.yAxis().setColors(Transparent)
    c.xAxis().setLabelStyle("arial.ttf", 12)
    c.yAxis().setLabelStyle("arial.ttf", 12)
    layer = c.addBarLayer3(counts, colors)
    layer.setBorderColor(Transparent, barLighting(0.8, 1.15))
    layer.setRoundedCorners()
    c.xAxis().setLabels(names)
    c.yAxis().setTickDensity(40)
    c.yAxis().setTitle("Y-Axis Title Placeholder", "arial.ttf", 14, 0x555555)
    c.makeChart(file+".png")
def showresult3(info,file):
    counts= [f[0] for f in info]
    names = [f[1] for f in info]
    c = XYChart(1800,800)
    c.setPlotArea(30, 20, 1700, 700)
    c.addLineLayer(counts)
    c.xAxis().setLabels(names)
    c.xAxis().setLabelStep(3)
    c.makeChart(file+".png")
 
sql=[]
#Custom Scatter Symbols
#说说总数top20
sql.append("select count(*) count,name,qq from qz_emotion group by qq order by count desc limit 0,20")
#评论总数top20
sql.append("select sum(comment_num) num,name,qq from qz_emotion group by qq order by num desc limit 0,20")
#说说数量top20的说说评论率
sql.append("select * from (select sum(comment_num)/count(id) r,name,sum(comment_num) c_num,count(id) e_num,qq from qz_emotion group by qq order by e_num desc limit 0,20) as a order by a.r desc")
#评论数量top20的说说评论率
sql.append("select * from (select sum(comment_num)/count(id) r,name,sum(comment_num) c_num,count(id) e_num,qq from qz_emotion group by qq order by c_num desc limit 0,20) as a order by a.r desc")
#没有任何限制的情况下top20评论率
sql.append("select * from (select sum(comment_num)/count(id) r,name,sum(comment_num) as c_num,count(id) e_num,qq from qz_emotion group by qq order by r desc limit 0,20) as a")
#说说数量1000以上的评论率top20
sql.append("select * from (select sum(comment_num)/count(id) r,name,sum(comment_num) as c_num,count(id) e_num,qq from qz_emotion group by qq order by r desc) as a where a.e_num>1000")
#我的好友里评论说说数top20
sql.append("select count(id) count,comment_name,comment_qq from qz_comment where comment_qq in (select qq from qz_friend where who='2421181819') group by comment_qq order by count desc limit 0,20")
#我的二度好友里说说数top20
sql.append("select count(id) count,comment_name,comment_qq from qz_comment group by comment_qq order by count desc limit 0,20")
#按年份统计
sql.append("select count(id) count,date_format(create_time,'%y') sdate from qz_emotion group by sdate order by sdate")
#按月统计
sql.append("select count(id) count,date_format(create_time,'%m') sdate from qz_emotion group by sdate order by sdate")
#按年月统计
sql.append("select count(id) count,date_format(create_time,'%y-%m') sdate from qz_emotion group by sdate order by sdate")
#按日统计
sql.append("select count(id) count,date_format(create_time,'%d') sdate from qz_emotion group by sdate order by sdate")
#按小时统计
sql.append("select count(id) count,date_format(create_time,'%H') sdate from qz_emotion group by sdate order by sdate")

if __name__ == "__main__":
    global conn,cur
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('qzone1')
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    #count,name 先是数量，然后是标签
    for i in range(0,len(sql)):
	info=executesql(sql[i])
	if info!=None and len(info)>0:
	    showresult0(info,"showresult0"+str(id(sql[i])))
	    showresult1(info,"showresult1"+str(id(sql[i])))
	    showresult2(info,"showresult2"+str(id(sql[i])))
	    showresult3(info,"showresult3"+str(id(sql[i])))
        else:
            print "no data"