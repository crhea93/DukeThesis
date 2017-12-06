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

def square_lattice(x_min,x_max,y_min,y_max,x_min_inc,x_max_inc,y_min_inc,y_max_inc,x_parts,y_parts,output):
    particles = []
    x = np.linspace(x_min,x_max,x_parts)
    y = np.linspace(y_min,y_max,y_parts)
    particle_numbers_inlower = []
    num_particles_in = 0
    for i in range(len(x)):
        for j in range(len(y)):
            new_particle = particle()
            new_particle.assign(x[j],0,y[i],0)
            #Check if particle is in inclusion
            if particle_in(x_min_inc,x_max_inc,y_min_inc,y_max_inc,new_particle) == True:
                pass
            else:

                if x_max_inc<=new_particle.xp and y_min_inc<=new_particle.yp<=y_max_inc:
                    particle_numbers_inlower.append(new_particle)
                else:
                    particles.append(new_particle)
                num_particles_in += 1

    #print(len(particles))
    #Now to clear up the lower packing region
    weak_zone_keep = []
    #for i in range(len(particle_numbers_inlower)):
        #if i%100000==0:
        #    weak_zone_keep.append(particle_numbers_inlower[i])
        #else:
        #    pass

    particles_final = particles+weak_zone_keep
    print(len(particles_final))
    f = open(output,"w")
    f.write("LAMMPS Data File for updated particles")
    f.write('\n')
    f.write(str(len(particles_final))+" atoms")
    f.write('\n')
    f.write('\n')
    f.write('1 atom types')
    f.write('\n')
    f.write(str(-0.5)+" "+str(0.5)+" xlo xhi")
    f.write('\n')
    f.write(str(-0.5)+" "+str(0.5)+" "+" ylo yhi")
    f.write('\n')
    f.write('-0.5 0.5 zlo zhi')
    f.write('\n')
    f.write('\n')
    f.write('Atoms')
    f.write('\n')
    f.write('\n')
    #write Positions
    for i in range(len(particles_final)):
        f.write(str(i+1)+" 1 1 1 "+str(particles_final[i].xp)+" "+str(particles_final[i].yp)+ " 0 0 0 0"+'\n')

square_lattice(-0.495,0.495,-0.495,0.4955,-0.5,0.0,-0.1,0.1,100,100,'/home/crhea/Dropbox/Thesis/lammps_square_100x100_inc.lj')
