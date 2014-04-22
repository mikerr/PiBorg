#!/usr/bin/env python
# by clivej 

import EcoDriver as ed
import XLoBorg as xlo
from math import *

TIMED_ACTION_INTERVAL = 200 # milliseconds

# Define a procedure that is called after a given number of milliseconds
# This one simulates the XLoBorg by setting random numbers to the
# instruments on the display
#
def simulate():
	app.instAccelX.randomise(-1.5, 0.25)
	app.instAccelY.randomise(-1.5, 1.5)
	app.instAccelZ.randomise(0, 2)
	app.instAngleX.waggle()
	app.instAngleY.waggle()
	app.instAngleZ.waggle()
	app.setTimedActions(simulate, TIMED_ACTION_INTERVAL) # calls itself again (and again... (and...))

# Define a procedure that sets the instrument values to
# a set of test values. See if the display matches.
#
def fixedDisplay():
	x = 1.25
	y = 0.25
	z = -0.5
	app.instAccelX.acceleration.set(x)
	app.instAccelY.acceleration.set(y)
	app.instAccelZ.acceleration.set(z)
	pitch = 45
	yaw = 20
	roll = 270
	app.instAngleX.set(pitch)
	app.instAngleY.set(yaw)
	app.instAngleZ.set(roll)
	
def readXlo():
	ax, ay, az = xlo.ReadAccelerometer()
	
	app.instAccelX.acceleration.set(ax)
	app.instAccelY.acceleration.set(ay)
	app.instAccelZ.acceleration.set(az)

	# As these are raw values, things aren't really going to work.
	# I need the correction algorithms discussed on the PiBorg Forums.
	# In the meantime, this allows some visualisation.
	mx, my, mz = xlo.ReadCompassRaw()
	app.instAngleX.set(mx)
	app.instAngleY.set(my)
	app.instAngleZ.set(mz)
	
	app.setTimedActions(readXlo, TIMED_ACTION_INTERVAL) # call again
	

# Start the App! This is the first sectio of code that runs when we launch this
# script with python. It creates the app, sets the name of the procedure with the
# time actions we want and then runs the app's main loop. The main loop will call
# our timed actions every TIMED_ACTION_INTERVAL (milliseconds)
#
xlo.printFunction = xlo.NoPrint
xlo.Init()
app = ed.EcoDriverApp()
app.setTimedActions(readXlo, TIMED_ACTION_INTERVAL)
app.mainloop()

