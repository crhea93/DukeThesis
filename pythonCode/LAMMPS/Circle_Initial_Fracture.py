'''
File to create square of particles for lammps
This creates a square lattice with an inclusion for an initial crack.
This is done by creating a square lattice and then simply subtracting the particles
that are inside the inclusion.
'''

import numpy as np

class particle:
    def __init__(self):
        self.xp = 0 # x coordinate
        self.xv = 0 # x velocity
        self.yp = 0 # y coordinate
        self.yv = 0 # y velocity
        self.rad = 0.01# particle radius
        self.m = 0 # mass
    def assign(self,xpos,xvel,ypos,yvel):
        self.xp = xpos
        self.xv = xvel
        self.yp = ypos
        self.yv = yvel
        self.rad = 0.01
        self.m = 1

def particle_in(x_minin,x_maxin,y_minin,y_maxin,particle):
    inside = False
    if (x_minin<=particle.xp<=x_maxin) and (y_minin<=particle.yp<=y_maxin):
        inside = True
    else:
        pass
    return inside
def particle_outside_inner(inner_rad,particle,particle_rad):
    outside = False
    if (inner_rad<=np.sqrt(particle.xp**2+particle.yp**2)-particle_rad):
        outside = True
#        print(particle.xp )
 #       print(particle.yp)
    else:
        pass
    return outside

def particle_within(outer_rad,particle,particle_rad):
    inside = False
    if (np.sqrt(particle.xp**2+particle.yp**2)+particle_rad<=outer_rad):
        inside = True
    else:
        pass
    return inside

def square_lattice(x_min,x_max,y_min,y_max,x_parts,y_parts,num_particles,outer_Rad,inner_rad,part_rad,output):
    particles = []
    x = np.linspace(x_min,x_max,x_parts)
    y = np.linspace(y_min,y_max,y_parts)
    num_particles_in = 0
    for i in range(len(x)):
        for j in range(len(y)):
            new_particle = particle()
            new_particle.assign(x[i],0,y[j],0)
            #Check if particle is in inclusion
            if particle_outside_inner(inner_rad,new_particle,part_rad) == False:
                pass
            elif particle_within(outer_Rad,new_particle,part_rad) == False:
                pass
            else:
                particles.append(new_particle)
                num_particles_in += 1
    f2 = open('/home/crhea/Documents/DukeThesis/test.csv','w')
    f2.write("ID,X,Y \n")
    f = open(output,"w")
    f.write("LAMMPS Data File for updated particles")
    f.write('\n')
    f.write(str(num_particles_in)+" atoms")
    f.write('\n')
    f.write('\n')
    f.write('1 atom types')
    f.write('\n')
    f.write(str(x_min-0.1)+" "+str(x_max+0.1)+" xlo xhi")
    f.write('\n')
    f.write(str(y_min-0.1)+" "+str(y_max+0.1)+" "+" ylo yhi")
    f.write('\n')
    f.write('-0.5 0.5 zlo zhi')
    f.write('\n')
    f.write('\n')
    f.write('Atoms')
    f.write('\n')
    f.write('\n')
    #write Positions
    print(num_particles_in)
    for i in range(num_particles_in):
        f.write(str(i+1)+" 1 1 1 "+str(particles[i].xp)+" "+str(particles[i].yp)+ " 0 0 0 0"+'\n')
        f2.write(str(i+1)+","+str(particles[i].xp)+","+str(particles[i].yp)+'\n')

square_lattice(-0.49,0.49,-0.49,0.49,100,100,10000,0.5,0.05,0.005,'/home/crhea/Documents/DukeThesis/ParticleFiles/lammps_circle_100x100_T.lj')
