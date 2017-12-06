'''
#File containing primary solvers for DEM
#Calculate if particles collide. Return list of particles which contacts
 the current particle
'''
import numpy as np
def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)

def Kutta_eqn_NSL(func,current_particle,f_total,t_i,y_i,h):
    k1 = h*func(current_particle,f_total,t_i,y_i)
    k2 = h*func(current_particle,f_total,t_i+h/2,y_i+k1/2)
    k3 = h*func(current_particle,f_total,t_i+h/2,y_i+k2/2)
    k4 = h*func(current_particle,f_total,t_i+h,y_i+k3)
    k = k1+2*k2+2*k3+k4
    return k
def Kutta_step_NSL(func,current_particle,f_total,t,y,h):
    return  y + (1/6)*Kutta_eqn_NSL(func,current_particle,f_total,t,y,h)

def Runge_Kutta_vector_NSL(func,current_particle,f_total,y_init_vec,start_time_pseudo,end_time_pseudo,num_steps):
    h = (end_time_pseudo-start_time_pseudo)/num_steps
    y = np.matrix(np.zeros((num_steps,4))) #4 because 2 dim position and velocity
    t_0 = start_time_pseudo
    y[0,:]=y_init_vec
    for i in range(1,num_steps):
        t_i = t_0+i*h
        y[i,:] = Kutta_step_NSL(func,current_particle,f_total,t_i,y[i-1,:],h)
    return y[i,:]
def collision(particle_list,particles_pre,particle_i_index):
    collision_list = [] #list for particle indices
    particle_i = particles_pre[particle_i_index]
    for p in range(len(particle_list)):
        PTC = particles_pre[p] # Particle To Check against
        if p != particle_i_index:#only check with other particles
            #Check for collision
            if distance(particle_i.xp,particle_i.yp,PTC.xp,PTC.yp) < particle_i.rad+PTC.rad:
                #collision occurs
                collision_list.append(p)
                #print("Particle "+str(particle_i_index)+" is hit with "+str(p))
            else:
                #no collision
                pass
        else: # Dont do anything if we are examining the particle itself
            pass
    return collision_list

#Now to calculate contact forces
def contact_force(current_particle,collided_list,particles,particles_pre,spring_constant,damping_coeff):
    # current particle, index of particles with which it sharts  contact, all particles
    r_i = np.array([[current_particle.xp],[current_particle.yp]]) #lagrangian position vector of main particle
    v_i = np.array([[current_particle.xv],[current_particle.yv]])
    f_total = np.zeros((2,1)) # initialize total contact forces
    #Calculate contact force for each particle in contact list
    for p in range(len(collided_list)):
        #print("we are being hit with particle ",collided_list[p])
        part_j = particles_pre[p]
        r_j = np.array([[part_j.xp],[part_j.yp]])
        v_j = np.array([[part_j.xv],[part_j.yv]])
        norm = (r_i-r_j)/np.abs(r_i-r_j)
        delta = (current_particle.rad+part_j.rad)-np.dot((r_i-r_j).transpose(),norm)
        nu = -np.dot((v_i-v_j).transpose(),norm)
        f_n = spring_constant*delta+damping_coeff*nu
        f_contact_ij = f_n*norm
        f_total += f_contact_ij
    #print(f_total)
    return f_total
#Lennard-Jones Force

#Newtons Second law
def secondLawFunc(current_particle,f_total,t,y):
    z = np.zeros((1,4))
    z[0,0] = y[:,1]
    z[0,1] = f_total[0]/current_particle.m
    z[0,2] = y[:,3]
    z[0,3] = f_total[1]/current_particle.m
    return z
def NSL(current_particle,f_total,grav_const,start_time,end_time):
    RK_init = np.zeros((1,4))
    RK_init = np.array([[current_particle.xp,current_particle.xv,current_particle.yp,current_particle.yv]])    #initialized values
    new_rv = Runge_Kutta_vector_NSL(secondLawFunc,current_particle,f_total,RK_init,start_time,end_time,10)
    current_particle.updateRK(new_rv)
    return 0
