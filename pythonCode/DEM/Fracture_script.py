#Discrete Element Method Main Code for fracture Mode I
from randomField import square_lattice
from LJF import EulerLFJ
from copy import deepcopy
from plotting import plot_part,plot_part_save_inc
import matplotlib.pyplot as plt
from pylab import *
# For now we will call a new field everytime we run while we have small fields
#--------------ParameterList-------------------#
num_particles = 25
x_min = 0
x_max = 4
y_min = 0
y_max = 4
start_time = 0
end_time = 1
n_time_steps = 2
r_equilibrium = 1.0 # Equilibrium distance between particles in lattice
figname = '../images/fracture_ModeI/time'
#----------------------------------------------#

print("We are generating random field of particles")
particles = square_lattice(x_min,x_max,y_min,y_max,num_particles)
f_total = 0
print("The field has been generated")
fig,ax = plt.subplots(1,1)
#Iterate through time
inc_t = (end_time-start_time)/n_time_steps #step time
t_prev = 0 #initiate time step
#plot_part(particles)
for t in range(n_time_steps):
    print("We are on time step ",t+1)
    if t != 0: #only if on second time step
        t_prev = start_time+inc_t*(t-1) #prev time
    t_curr = start_time+inc_t*t #current time
    #Iterate through particles
    for part in range(num_particles):
        if  part%10 == 0:
            print("We are on particle ",part)
        current_particle = particles[part]
        #Solve newtons second law for updated position
        EulerLFJ(current_particle,r_equilibrium,f_total,t_prev,t_curr)
    for i in range(len(particles)):
        print(particles[i].xp)
        print(particles[i].yp)
    t_prev = t_curr #update previous time
    #plot figure
    plot_part_save_inc(particles,figname,t,x_min,x_max,y_min,y_max)
    plt.clf()
    print('-------------------------------------------')
