#!/usr/bin/python
# -*- coding: utf-8 -*-
from pychartdir import *
#饼状图
def piecharts1(filename):
	# The data for the pie chart
	data = [35, 30, 25, 7, 6, 5, 4, 3, 2, 1,12]
	# The labels for the pie chart
	labels = ["中国", "澳大利亚", "美国", "德国", "日本", "新加坡", "韩国", "马拉西亚", "印度", "加拿大","新西兰"]
	#图片大小和背景颜色
	c = PieChart(560, 270, goldColor(), -1, 1)
	#默认字体
	c.setDefaultFonts("simsun.ttc")
	#标题和背景颜色
	c.addTitle("这里是标题", "simsun.ttc", 15).setBackground(metalColor(0xff9999))
	#饼状图的圆心坐标和半径
	c.setPieSize(280, 135, 110)
	#设置3D深度
	c.set3D(20)

	c.setLabelLayout(SideLayout)
	# Set the label box background color the same as the sector color, with glass effect, and with 5
	# pixels rounded corners
	t = c.setLabelStyle()
	t.setBackground(SameAsMainColor, Transparent, glassEffect())
	t.setRoundedCorners(5)
	# Set the border color of the sector the same color as the fill color. Set the line color of the
	# join line to black (0x0)
	c.setLineColor(SameAsMainColor, 0x000000)
	c.setStartAngle(135)

	# Set the pie data and the pie labels
	c.setData(data, labels)
	# Output the chart
	c.makeChart(filename)
#饼状图
def piecharts2(filename):
	data = [35, 30, 25, 7, 6, 5, 4, 3, 2, 1,12]
	labels = ["中国", "澳大利亚", "美国", "德国", "日本", "新加坡", "韩国", "马拉西亚", "印度", "加拿大","新西兰"]
	c = PieChart(360, 300)
	c.setDefaultFonts("simsun.ttc")
	# Set the center of the pie at (180, 140) and the radius to 100 pixels
	c.setPieSize(180, 140, 100)
	# Add a title to the pie chart
	c.addTitle("这里是标题", "simsun.ttc", 15)
	c.set3D()
	c.setData(data, labels)
	# Explode the 1st sector (index = 0)
	c.setExplode(0)
	c.makeChart(filename)
#饼状图
def piecharts3(filename):
	data = [28, 45, 5, 1, 12]
	labels = ["Excellent", "Good", "Bad", "Very Bad", "Neutral"]
	icons = ["laugh.png", "smile.png", "sad.png", "angry.png", "nocomment.png"]
	c = PieChart(560, 300, silverColor(), 0x000000, 1)
	c.setRoundedFrame()
	c.setPieSize(280, 150, 120)
	# Add a title box with title written in CDML, on a sky blue (A0C8FF) background with glass effect
	c.addTitle(
	    "<*block,valign=absmiddle*><*img=doc.png*> Customer Survey: <*font=timesi.ttf,color=000000*>" \
	    "Do you like our <*font,color=dd0000*>Hyper<*super*>TM<*/font*> molecules?", "timesbi.ttf", 15,
	    0x000080).setBackground(0xa0c8ff, 0x000000, glassEffect())
	# Add a logo to the chart written in CDML as the bottom title aligned to the bottom right
	c.addTitle2(BottomRight,
	    "<*block,valign=absmiddle*><*img=molecule.png*> <*block*><*color=FF*>" \
	    "<*font=timesbi.ttf,size=12*>Molecular Engineering\n<*font=arial.ttf,size=10*>Creating " \
	    "better molecules")
	# Set the pie data and the pie labels
	c.setData(data, labels)
	c.set3D()
	c.setLabelLayout(SideLayout)
	c.setLabelStyle().setBackground(Transparent)
	c.addExtraField(icons)
	c.setLabelFormat("<*block,valign=absmiddle*><*img={field0}*> {label} ({percent|0}%)")
	c.setExplodeGroup(2, 3)
	c.setStartAngle(135)
	c.makeChart(filename)
#直方图
def barlabel1(filename):
	data = [35, 30, 25, 7, 6, 5, 4, 3, 2, 1,12]
	labels = ["中国", "澳大利亚", "美国", "德国", "日本", "新加坡", "韩国", "马拉西亚", "印度", "加拿大","新西兰"]
	# Create a XYChart object of size 600 x 360 pixels
	c = XYChart(600, 360)
	# Set the plotarea at (70, 20) and of size 500 x 300 pixels, with transparent background and border
	# and light grey (0xcccccc) horizontal grid lines
	c.setPlotArea(70, 20, 500, 300, Transparent, -1, Transparent, 0xcccccc)
	# Set the x and y axis stems to transparent and the label font to 12pt Arial
	c.xAxis().setColors(Transparent)
	c.yAxis().setColors(Transparent)
	c.xAxis().setLabelStyle("simsun.ttc", 12)
	c.yAxis().setLabelStyle("simsun.ttc", 12)
	# Add a blue (0x6699bb) bar chart layer using the given data
	layer = c.addBarLayer(data, 0x6699bb)
	# Use bar gradient lighting with the light intensity from 0.8 to 1.3
	layer.setBorderColor(Transparent, barLighting(0.8, 1.3))
	# Set rounded corners for bars
	layer.setRoundedCorners()
	# Display labela on top of bars using 12pt Arial font
	layer.setAggregateLabelStyle("Arial", 12)
	# Set the labels on the x axis.
	c.xAxis().setLabels(labels)
	# For the automatic y-axis labels, set the minimum spacing to 40 pixels.
	c.yAxis().setTickDensity(40)
	# Add a title to the y axis using dark grey (0x555555) 14pt Arial Bold font
	c.yAxis().setTitle("这里是数量", "simsun.ttc", 14, 0x555555)
	# Output the chart
	c.makeChart(filename)
def barlabel2(filename):
	data = [35, 30, 25, 7, 6, 5, 4, 3, 2, 1,12]
	labels = ["中国", "澳大利亚", "美国", "德国", "日本", "新加坡", "韩国", "马拉西亚", "印度", "加拿大","新西兰"]
	# The colors for the bars
	colors = [0x5588bb, 0x66bbbb, 0xaa6644, 0x99bb55, 0xee9944, 0x444466, 0xbb5555]
	# Create a XYChart object of size 600 x 360 pixels
	c = XYChart(600, 360)
	# Set the plotarea at (70, 20) and of size 500 x 300 pixels, with transparent background and border
	# and light grey (0xcccccc) horizontal grid lines
	c.setPlotArea(70, 20, 500, 300, Transparent, -1, Transparent, 0xcccccc)
	# Set the x and y axis stems to transparent and the label font to 12pt Arial
	c.xAxis().setColors(Transparent)
	c.yAxis().setColors(Transparent)
	c.xAxis().setLabelStyle("simsun.ttc", 12)
	c.yAxis().setLabelStyle("simsun.ttc", 12)
	# Add a multi-color bar chart layer using the given data
	layer = c.addBarLayer3(data, colors)
	# Use bar gradient lighting with the light intensity from 0.8 to 1.15
	layer.setBorderColor(Transparent, barLighting(0.8, 1.15))
	# Set rounded corners for bars
	layer.setRoundedCorners()
	# Set the labels on the x axis.
	c.xAxis().setLabels(labels)
	# For the automatic y-axis labels, set the minimum spacing to 40 pixels.
	c.yAxis().setTickDensity(40)
	# Add a title to the y axis using dark grey (0x555555) 14pt Arial font
	c.yAxis().setTitle("这里是纵坐标", "simsun.ttc", 14, 0x555555)
	# Output the chart
	c.makeChart(filename)
def barlabel3(filename):
	data = [35, 30, 25, 7, 6, 5, 4, 3, 2, 1,12]
	labels = ["中国", "澳大利亚", "美国", "德国", "日本", "新加坡", "韩国", "马拉西亚", "印度", "加拿大","新西兰"]
	colors = [0xcc0000, 0x66aaee, 0xeebb22, 0xcccccc, 0xcc88ff]
	c = XYChart(600, 380)
	c.setColors(whiteOnBlackPalette)
	c.setBackground(c.linearGradientColor(0, 0, 0, c.getHeight(), 0x0000cc, 0x000044))
	c.setRoundedFrame(0xffffff, 30, 0, 30, 0)
	title = c.addTitle("测试", "simsun.ttc", 18)
	title.setMargin2(0, 0, 6, 6)
	c.addLine(20, title.getHeight(), c.getWidth() - 21, title.getHeight(), 0xffffff)
	c.setPlotArea(70, 80, 480, 240, -1, -1, Transparent, 0xffffff)
	c.swapXY()
	c.addBarLayer3(data, colors).setBorderColor(Transparent, barLighting(0.75, 2.0))
	c.xAxis().setLabels(labels)
	c.syncYAxis()
	c.yAxis().setTitle("纵坐标", "simsun.ttc", 10)
	c.yAxis().setColors(Transparent)
	c.yAxis2().setColors(Transparent)
	c.xAxis().setTickColor(Transparent)
	c.xAxis().setLabelStyle("simsun.ttc", 8)
	c.yAxis().setLabelStyle("simsun.ttc", 8)
	c.yAxis2().setLabelStyle("simsun.ttc", 8)
	c.packPlotArea(30, title.getHeight() + 25, c.getWidth() - 50, c.getHeight() - 25)
	c.makeChart(filename)
barlabel3("barlabel3.png")