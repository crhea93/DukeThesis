## RK Calculations for 1d Lennard Jones force
import numpy as np
def calculate_ypp(y_p,r_0,ep):
    print("y_p/r_0 is ",y_p/r_0)
    if np.sqrt(y_p**2+r_0**2)<1.e-1:
        return 0
    else:
        return 0
def LJF_1dfunc(current_particle,r_0,f_total,t,y):
    ep = 1.0
    x_p = y[:,0]
    x_v = y[:,1]
    y_p = y[:,2]
    y_v = y[:,3]
    z = np.zeros((1,4))
    z[0,0] = x_v #this wont update anything
    z[0,1] = 0 #this too wont update anything
    z[0,2] = y_v #only update y coordinates
    z[0,3] = f_total #Only updating y coordinates
    return z
def eulerstep(current_particle,r_0,f_total,t,y,h):
    return y+h*LJF_1dfunc(current_particle,r_0,f_total,t,y)
def EulerLFJ(current_particle,r_eq,f_total,start_time_pseudo,end_time_pseudo,num_steps=10):
    h = (end_time_pseudo-start_time_pseudo)/num_steps
    y = np.matrix(np.zeros((num_steps,4))) #4 because 2 dim position and velocity
    t_0 = start_time_pseudo
    y[0,:] = np.array([[current_particle.xp,current_particle.xv,current_particle.yp,current_particle.yv]])
    print(current_particle.yv)
    for i in range(1,num_steps):
        t_i = t_0+i*h
        y[i,:] = eulerstep(current_particle,r_eq,f_total,t_i,y[i-1,:],h)
    current_particle.updateEuler(y[i,:])
    return 0
