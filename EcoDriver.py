# by clivej

import Tkinter as tk
from random import *
from math import *

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Acceleration:
	def __init__(self, hold, callback):
		self.trackVar = tk.DoubleVar()
		self.min = 2
		self.max = -2
		self.hold = hold
		self.holdMax = hold
		self.holdMin = hold
		self.callback = callback
		self.maxed = True
		self.mined = True

	def get(self):
		return self.trackVar.get()

	def set(self, value):
		self.holdMax = self.holdMax - 1
		self.holdMin = self.holdMin - 1 
		if self.holdMax == 0:
			self.holdMax = self.hold
			self.max = -2
		if self.holdMin == 0:
			self.holdMin = self.hold
			self.min = 2

		if value > self.max:
			self.max = value
			self.holdMax = self.hold
			self.maxed = True
		else:
			self.maxed = False

		if value < self.min:
			self.min = value
			self.holdMin = self.hold
			self.mined = True
		else:
			self.mined = False		

		self.trackVar.set(value)
		self.callback(value)

	def getTrackVar(self):
		return self.trackVar

	def newMax(self):
		return self.maxed		

	def newMin(self):
		return self.mined

class AccelerationInstrument:
	def __init__(self, parent, name, bg):
		self.acceleration = Acceleration(10, self.trackLine)

		self.pane = tk.Frame(parent)
		self.pane.pack(side=tk.LEFT)
	
		self.scale = tk.Scale(self.pane,
			variable=self.acceleration.getTrackVar(), from_=2, to=-2,
			tickinterval=0.25, orient="vertical", command=self.trackLine,
			length=600, resolution=0.001, showvalue=0
		)
		self.scale.pack(side=tk.LEFT)

		self.cvsWidth = 20
		self.canvas = tk.Canvas(self.pane, background=bg, width=self.cvsWidth) 
		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

		self.canvas.create_text(10, 10, text=name)

		self.canvas.create_line(0, 300, self.cvsWidth,300)
		self.canvas.create_line(0, self.yScaled(2), self.cvsWidth, self.yScaled(2))
		self.canvas.create_line(0, self.yScaled(-2), self.cvsWidth, self.yScaled(-2))
		self.lnMax = self.canvas.create_line(0, 300, self.cvsWidth,300, fill="red")
		self.lnMin = self.canvas.create_line(0, 300, self.cvsWidth,300, fill="blue")

	def yScaled(self, scaleValue):
		return -142.0 * scaleValue + 300

	def trackLine(self, scaleValue):
		if self.acceleration.newMax():
			y = self.yScaled(self.acceleration.get())
			self.canvas.delete(self.lnMax)
			self.lnMax = self.canvas.create_line(0, y, self.cvsWidth, y, fill="red", width=3)
		if self.acceleration.newMin():
			y = self.yScaled(self.acceleration.get())
			self.canvas.delete(self.lnMin)
			self.lnMin = self.canvas.create_line(0, y, self.cvsWidth, y, fill="blue", width=3)

	def randomise(self, a, b):
		self.acceleration.set(uniform(a,b))

class AngleInstrument:
	def __init__(self, parent, name, bg):
		cvsWidth = 200
		cvsHeight = 200
		offset = 10
		self.diameter = cvsHeight-offset
		self.radius = self.diameter/2

		self.angle = 0.0

		self.canvas = tk.Canvas(parent, background=bg, width=cvsWidth, height=cvsHeight) 
		self.canvas.pack(side=tk.TOP)

		self.canvas.create_text(offset, offset, text=name)

		self.canvas.create_oval(offset, offset, self.diameter, self.diameter)
		self.origin = Point(offset + (cvsWidth-2*offset)/2, offset + (cvsHeight-2*offset)/2)
		self.canvas.create_oval(self.origin.x-2, self.origin.y-2, self.origin.x+2, self.origin.y+2, fill="black")

		for n in range(0, 360, 5):
			self.tick(n, not n % 90)

		self.pointer = None
		self.set(0)

	def set(self, value):
		self.angle = value
		self.setPointer(value)

	def waggle(self):
		self.set(self.angle + uniform(-1,1))

	def pointAtAngle(self, degrees, distance):
		radians = degrees*pi/180
		return Point(self.origin.x + sin(radians)*distance, self.origin.y - cos(radians)*distance)

	def lineAtAngle(self, degrees, length, colour):
		p = self.pointAtAngle(degrees, length)
		lineId = self.canvas.create_line(self.origin.x, self.origin.y, p.x, p.y, fill=colour)
		return lineId

	def tick(self, degrees, label=False):
		if label:
			length = 16
		else:
			length = 4
		inner = self.pointAtAngle(degrees, self.radius-length/2)
		outer = self.pointAtAngle(degrees, self.radius+length/2)
		if label:
			tickLabel = self.canvas.create_text(inner.x, inner.y, text=degrees, font="Verdana, 9")
		tickId = self.canvas.create_line(inner.x, inner.y, outer.x, outer.y)
		return tickId		

	def setPointer(self, degrees):
		self.canvas.delete(self.pointer)
		self.pointer = self.lineAtAngle(degrees, 85, "red")


class EcoDriverApp(tk.Frame):
	def __init__(self, master=None):
		
		tk.Frame.__init__(self, master)
		self.pack()

		#------ constants for controlling layout ------
		btnWidth = 6
		
		btnPadx = "2m"
		btnPady = "1m"

		btnFrPadx =  "3m"
		btnFrPady =  "2m"      
		btnFrIpadx = "3m"
		btnFrIpady = "1m"

		# -------------- end constants ----------------

		### VERTICAL (tk.TOP/bottom) orientation inside baseFrame

		# title frame
		self.frTitle = tk.Frame(self, background="blue")
		self.frTitle.pack(side=tk.TOP)    
		tmpLbl = tk.Label(self.frTitle, text="XLoBorg Reader/Simulator")
		tmpLbl.pack(side=tk.LEFT)
		
		# mid frame - to contain all additional frames for main instrument panels
		self.frMid = tk.Frame(self)
		self.frMid.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES) # note tk.TOP side packing  

		# Instrument panels from tk.LEFT to right  
		# 1) The Accelerometer
		self.instAccelX = AccelerationInstrument(self.frMid, "X", "#FFC9C9")
		self.instAccelY = AccelerationInstrument(self.frMid, "Y", "#CFFFD6")
	 	self.instAccelZ = AccelerationInstrument(self.frMid, "Z", "#CFF0FF")

		# 2) The Magnetometer 
		self.frMag = tk.Frame(self.frMid, background="green", width=250) # h and w to become redundant later
		self.frMag.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

		self.instAngleX = AngleInstrument(self.frMag, "X", "#FFC9C9")
		self.instAngleY = AngleInstrument(self.frMag, "Y", "#CFFFD6")
		self.instAngleZ = AngleInstrument(self.frMag, "Z", "#CFF0FF")
	 	
 		# buttons frame to go at the bottom
		self.frBtns = tk.Frame(self)
		self.frBtns.pack(side=tk.TOP, ipadx=btnFrIpadx, ipady=btnFrIpady, padx=btnFrPadx, pady=btnFrPady)

		# add the buttons to the frBtns	
		self.btnClose = tk.Button(self.frBtns, command=self.btnCloseClick)
		self.btnClose.configure(text="Close")  
		self.btnClose.configure(width=btnWidth, padx=btnPadx, pady=btnPady)
		self.btnClose.pack()
		self.btnClose.bind("<Return>", self.btnCloseClick_a)

	# Sets a function (actions) that will be called after milliseconds have elapsed
	def setTimedActions(self, actions, milliseconds):
		self.delay = milliseconds
		self.after(milliseconds, actions)
			
	def btnCloseClick(self): 
		self.quit()     
						
	def btnCloseClick_a(self, event): 
		self.btnCloseClick() 

	def simulate(self):
		self.instAccelX.randomise(-0.5, 0.25)
		self.instAccelY.randomise(-1.5, 1.5)
		self.instAccelZ.randomise(0, 2)
		self.instAngleX.waggle()
		self.instAngleY.waggle()
		self.instAngleZ.waggle()
		self.setTimedActions(self.simulate, self.delay)

