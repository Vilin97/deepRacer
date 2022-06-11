from turtle import degrees
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

# Get waypoints from numpy file
waypoints = np.load("2022_june_open.npy")
# print(waypoints)
# Input 3 coords [[x1,y1],[x2,y2],[x3,y3]]
def circle_radius(coords):
    # Flatten the list and assign to variables
    x1, y1, x2, y2, x3, y3 = [i for sub in coords for i in sub]

    a = x1*(y2-y3) - y1*(x2-x3) + x2*y3 - x3*y2
    b = (x1**2+y1**2)*(y3-y2) + (x2**2+y2**2)*(y1-y3) + (x3**2+y3**2)*(y2-y1)
    c = (x1**2+y1**2)*(x2-x3) + (x2**2+y2**2)*(x3-x1) + (x3**2+y3**2)*(x1-x2)
    d = (x1**2+y1**2)*(x3*y2-x2*y3) + (x2**2+y2**2) * \
        (x1*y3-x3*y1) + (x3**2+y3**2)*(x2*y1-x1*y2)
    if abs(a) < 0.0001:
        r = 999
    else:
        r = abs((b**2+c**2-4*a*d) / abs(4*a**2)) ** 0.5
    return r

def plot_curve(i, waypoints):
    # plot curve around index i
    begin = (i-6)%len(waypoints)
    end = (i+7)%len(waypoints)
    xs = [w[2] for w in waypoints[begin: end]]
    ys = [w[3] for w in waypoints[begin: end]]
    plt.scatter(xs,ys)

def get_angle():
    num_waypoints = len(waypoints)
    min_radius = 999
    index = 999
    for (i,_) in enumerate(waypoints):
        waypoint1 = (waypoints[i][2], waypoints[i][3])
        waypoint2 = (waypoints[(i-2)%num_waypoints][2], waypoints[(i-2)%num_waypoints][3])
        waypoint3 = (waypoints[(i+2)%num_waypoints][2], waypoints[(i+2)%num_waypoints][3])
        r = circle_radius([waypoint1, waypoint2, waypoint3])
        if r < 0.8:
            plot_curve(i,waypoints)
        if r < min_radius:
            min_radius = r
            index = i

    print(f"smallest radius: {min_radius}. At index {index}.")
    L = 0.165 # axle length
    print(f"largest turning angle: {360/(2*np.pi)*np.arcsin(L/min_radius)}")


# PLotting waypoints with slopes
import math
# Get number of waypoints
num_waypoints = waypoints.shape[0]
# print("Number of waypoints = " + str(num_waypoints))
for i, point in enumerate(waypoints):
    prev_waypoint = (point[2], point[3])
    next_waypoint = tuple(waypoints[(i+1)%num_waypoints][2:4])
    dx = next_waypoint[0] - prev_waypoint[0]
    dy = next_waypoint[1] - prev_waypoint[1]
    if abs(dx) < 0.0001 and abs(dy) < 0.0001:
        continue
    if abs(dx) < abs(dy):
        slope_inv = dx/dy
        xs = [prev_waypoint[0]+slope_inv*i*0.001 for i in range(-100,100)]
        ys = [prev_waypoint[1]+i*0.001 for i in range(-100,100)]
        # plt.scatter(xs,ys,s=0.4)
        # plt.scatter(prev_waypoint[0],prev_waypoint[1],s=5)
    else:
        slope = dy/dx
        xs = [prev_waypoint[0]+i*0.001 for i in range(-100,100)]
        ys = [prev_waypoint[1]+slope*i*0.001 for i in range(-100,100)]
        # plt.scatter(xs,ys,s=0.4)
        # plt.scatter(prev_waypoint[0],prev_waypoint[1],s=5)
    desired_direction = math.atan2(dy,dx)
    degree = math.degrees(desired_direction)
    if degree < 0:
        degree = -degree
    plt.scatter(i,degree,s=8)
    if abs(dx) > 0.001:
        diff=abs(math.tan(desired_direction) - dy/dx)
        if diff > 0.01:
            print(diff)
    
# plt.plot(range(num_waypoints),directions)
plt.show()
    # print("Waypoint " + str(i) + ": " + str(waypoint))


