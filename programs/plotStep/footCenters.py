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
p0.open("/python/gui0:i")
p1.open("/python/gui1:i")
p2.open("/python/ch0:i")
p3.open("/python/ch1:i")
# Connect output and input ports
yarp.Network.connect("/leftFootprint/gui1:o", "/python/gui1:i") # Left foot
yarp.Network.connect("/rightFootprint/gui0:o", "/python/gui0:i") # Right foot
yarp.Network.connect("/jr3/ch0:o", "/python/ch0:i") # Right foot sensor
yarp.Network.connect("/jr3/ch1:o", "/python/ch1:i") # Left foot sensor

# Read the data from de port
data0 = yarp.Bottle() # right foot position
data1 = yarp.Bottle() # left foot position
data2 = yarp.Bottle() # jr3 right
data3 = yarp.Bottle() # jr3 left


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
    p0.read(data0) # right foot postion
    p1.read(data1) # left foot position
    p2.read(data2) # jr3 right
    p3.read(data3) # jr3 left

    dl = data1.get(1).asDouble()*1000
    hl = data1.get(0).asDouble()*1000
    dr = -data0.get(1).asDouble()*1000
    hr = data0.get(0).asDouble()*1000

    # jr3 right
    fx2 = data2.get(0).asDouble()
    fy2 = data2.get(1).asDouble()
    fz2 = data2.get(2).asDouble()
    mx2 = data2.get(3).asDouble()
    my2 = data2.get(4).asDouble()
    mz2 = data2.get(5).asDouble()
    # jr3 left
    fx3 = data3.get(0).asDouble()
    fy3 = data3.get(1).asDouble()
    fz3 = data3.get(2).asDouble()
    mx3 = data3.get(3).asDouble()
    my3 = data3.get(4).asDouble()
    mz3 = data3.get(5).asDouble()

    def RightFoot():
    	# Big semicircle
    	ang = np.linspace(2*PI,PI,180)
    	x0 = dr + 70*np.cos(ang)
    	y0 = hr + 70*np.sin(ang)

    	# Straightline
    	x1 = np.ones(121) * (dr-70)
    	y1 = hr + np.linspace(1,121,121) - 1

    	# Little circle
    	ang2 = np.linspace(PI,14.25*PI/180,180)
    	x2 = dr - 15 + 55*np.cos(ang2)
    	y2 = hr + 120 + 55*np.sin(ang2)

    	# Inclined line
    	x3 = np.linspace(dr - 15 + 55*np.cos(14.25*PI/180), dr + 70*np.cos(2*PI), 100)
    	y3 = np.linspace(hr + 120 + 55*np.sin(14.25*PI/180), hr + 70*np.sin(2*PI), 100)

   	x_sole = np.concatenate([x0,x1,x2,x3])
    	y_sole = np.concatenate([y0,y1,y2,y3])
    	plt.plot(x_sole,y_sole,'k')

        return;

    def LeftFoot():
    	# Big semicircle
    	ang = np.linspace(2*PI,PI,180)
    	x0 = dl + 70*np.cos(ang)
    	y0 = hl + 70*np.sin(ang)

    	# Straightline
    	x1 = np.ones(121) * (dl-70)
    	y1 = hl + np.linspace(1,121,121) - 1

    	# Little circle
    	ang2 = np.linspace(PI,14.25*PI/180,180)
    	x2 = dl - 15 + 55*np.cos(ang2)
    	y2 = hl + 120 + 55*np.sin(ang2)

    	# Inclined line
    	x3 = np.linspace(dl - 15 + 55*np.cos(14.25*PI/180), dl + 70*np.cos(2*PI), 100)
    	y3 = np.linspace(hl + 120 + 55*np.sin(14.25*PI/180), hl + 70*np.sin(2*PI), 100)

    	x_sole = np.concatenate([-x0,-x1,-x2,-x3])
    	y_sole = np.concatenate([y0,y1,y2,y3])
    	plt.plot(x_sole,y_sole,'k')

    	return;

    # Foot print
    if fz2 <= -200:
    	RightFoot()

    if fz3 <= -200:
    	LeftFoot()

    x_left_foot = data1.get(0).asDouble()*1000
    y_left_foot = data1.get(1).asDouble()*1000

    x_right_foot = data0.get(0).asDouble()*1000
    y_right_foot = data0.get(1).asDouble()*1000


    
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


