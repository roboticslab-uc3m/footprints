import yarp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

PI = np.pi

# Initialise YARP
yarp.Network.init()
# Create a port
p0 = yarp.Port()
p1 = yarp.Port()
p2 = yarp.Port()
p3 = yarp.Port()
# Open the port
p0.open("/gui0:i")
p1.open("/gui1:i")
p2.open("/gui2:i")
p3.open("/gui3:i")
# Connect output and input ports
yarp.Network.connect("/leftFootprint/state:o", "/gui0:i") # Left foot
yarp.Network.connect("/rightFootprint/state:o", "/gui1:i") # Right foot
yarp.Network.connect("/jr3/ch0:o", "/gui2:i") # Right foot sensor
yarp.Network.connect("/jr3/ch1:o", "/gui3:i") # Left foot sensor

# Read the data from de port
data0 = yarp.Bottle() #left foot
data1 = yarp.Bottle() #right foot
data2 = yarp.Bottle()
data3 = yarp.Bottle()


fig = plt.figure()

while 1:

    ax = fig.add_subplot(111)
    ax.grid()
    ax = fig.gca()
    ax.set_xlim([-500,500])
    ax.set_ylim([-500,500])
    ax.set_xlabel('y [mm]') # changed because of robot axes
    ax.set_ylabel('x [mm]') # changed because of robot axes

    

    # Reading YARP port
    print "Reading..."
    p0.read(data0)
    p1.read(data1)
    p2.read(data2)
    p3.read(data3)

    d = -data1.get(1).asDouble()*1000
    h = data1.get(0).asDouble()*1000
    d1 = data0.get(1).asDouble()*1000
    h1 = data1.get(0).asDouble()*1000

    fx2 = data2.get(0).asDouble()
    fy2 = data2.get(1).asDouble()
    fz2 = data2.get(2).asDouble()
    mx2 = data2.get(3).asDouble()
    my2 = data2.get(4).asDouble()
    mz2 = data2.get(5).asDouble()

    fx3 = data3.get(0).asDouble()
    fy3 = data3.get(1).asDouble()
    fz3 = data3.get(2).asDouble()
    mx3 = data3.get(3).asDouble()
    my3 = data3.get(4).asDouble()
    mz3 = data3.get(5).asDouble()

    def RightFoot():
    	# Big semicircle
    	ang = np.linspace(2*PI,PI,180)
    	x0 = d + 70*np.cos(ang)
    	y0 = h + 70*np.sin(ang)

    	# Straightline
    	x1 = np.ones(121) * (d-70)
    	y1 = h + np.linspace(1,121,121) - 1

    	# Little circle
    	ang2 = np.linspace(PI,14.25*PI/180,180)
    	x2 = d - 15 + 55*np.cos(ang2)
    	y2 = h + 120 + 55*np.sin(ang2)

    	# Inclined line
    	x3 = np.linspace(d - 15 + 55*np.cos(14.25*PI/180), d + 70*np.cos(2*PI), 100)
    	y3 = np.linspace(h + 120 + 55*np.sin(14.25*PI/180), h + 70*np.sin(2*PI), 100)

   	x_sole = np.concatenate([x0,x1,x2,x3])
    	y_sole = np.concatenate([y0,y1,y2,y3])
    	plt.plot(x_sole,y_sole,'k')

        return;

    def LeftFoot():
    	# Big semicircle
    	ang = np.linspace(2*PI,PI,180)
    	x0 = d1 + 70*np.cos(ang)
    	y0 = h1 + 70*np.sin(ang)

    	# Straightline
    	x1 = np.ones(121) * (d1-70)
    	y1 = h1 + np.linspace(1,121,121) - 1

    	# Little circle
    	ang2 = np.linspace(PI,14.25*PI/180,180)
    	x2 = d1 - 15 + 55*np.cos(ang2)
    	y2 = h1 + 120 + 55*np.sin(ang2)

    	# Inclined line
    	x3 = np.linspace(d1 - 15 + 55*np.cos(14.25*PI/180), d1 + 70*np.cos(2*PI), 100)
    	y3 = np.linspace(h1 + 120 + 55*np.sin(14.25*PI/180), h1 + 70*np.sin(2*PI), 100)

    	x_sole = np.concatenate([-x0,-x1,-x2,-x3])
    	y_sole = np.concatenate([y0,y1,y2,y3])
    	plt.plot(x_sole,y_sole,'k')

    	return;

    # Foot print
    if fz2 >= 100:
    	RightFoot()

    if fz3 >= 100:
    	LeftFoot()

    x_left_foot = data0.get(0).asDouble()*1000
    y_left_foot = data0.get(1).asDouble()*1000

    x_right_foot = data1.get(0).asDouble()*1000
    y_right_foot = data1.get(1).asDouble()*1000


    
    print "leftFoot center = [",-y_left_foot,",",x_left_foot,"] mm"
    print "rightFoot center = [",-y_right_foot,",",x_right_foot,"] mm\n"
    print fz2
    print fz3
    

    plt.plot(-y_left_foot,x_left_foot,'ro') # axes are changed because of robot axes
    plt.plot(-y_right_foot,x_right_foot,'bo')
    fig.show()
    

    #Sample time 1ms
    plt.pause(0.001) #delay in seconds
    fig.clf()

p.close()


