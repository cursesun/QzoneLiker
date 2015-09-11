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
def showresult(info,file):
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
if __name__ == "__main__":
    global conn,cur
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='moshu521',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('qzone1')
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    #count,name 先是数量，然后是标签
    sql1="select count(id) count,date_format(create_time,'%y') sdate from qz_emotion group by sdate order by sdate"
    info=executesql(sql1)
    if info!=None and len(info)>0:
        showresult2(info,"ok"+str(id(info)))
    else:
        print "no data"


#Custom Scatter Symbols