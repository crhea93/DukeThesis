#Discrete Element Method Main Code
from randomField import create_map
from PrimaryCalculations import collision,contact_force,NSL
from copy import deepcopy
from plotting import plot_part,plot_part_save_inc
import matplotlib.pyplot as plt
import pylab
#Call particle map randomized field
# For now we will call a new field everytime we run while we have small fields
#--------------ParameterList-------------------#
num_particles = 20
x_min = -10
x_max = 10
y_min = -10
y_max = 10
start_time = 0
end_time = 2
n_time_steps = 500
spring_constant = 1
damping_coeff = 0.1
g = 6.67408*10**(-11) # gravitational constant
figname = 'images/particle_field'
#----------------------------------------------#

print("We are generating random field of particles")
particles = create_map(x_min,x_max,y_min,y_max,num_particles)
particles_pre = deepcopy(particles)
print("The field has been generated")

fig,ax = plt.subplots(1,1)
#Iterate through time
inc_t = (end_time-start_time)/n_time_steps #step time
t_prev = 0 #initiate time step
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
         #list of all particles that have collided with current particle
        collided_list = collision(particles,particles_pre,part)
        #calculate contact forces
        f_total = contact_force(current_particle,collided_list,particles,particles_pre,spring_constant,damping_coeff)
        #Solve newtons second law for updated position
        NSL(current_particle,f_total,g,t_prev,t_curr)
    particles_pre = deepcopy(particles)
    t_prev = t_curr #update previous time
    #plot figure
    plot_part_save_inc(particles,figname,t)
    plt.clf()
    print('-------------------------------------------')
