'''
File to create square of particles for lammps
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


def square_lattice(x_min,x_max,y_min,y_max,x_parts,y_parts,num_particles,output):
    particles = []
    x = np.linspace(x_min,x_max,x_parts)
    y = np.linspace(y_min,y_max,y_parts)
    for i in range(len(x)):
        for j in range(len(y)):
            new_particle = particle()
            new_particle.assign(x[j],0,y[i],0)
            particles.append(new_particle)

    f = open(output,"w")
    f.write("LAMMPS Data File for updated particles")
    f.write('\n')
    f.write(str(num_particles)+" atoms")
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
    for i in range(num_particles):
        f.write(str(i+1)+" 1 1 1 "+str(particles[i].xp)+" "+str(particles[i].yp)+ " 0 0 0 0"+'\n')

square_lattice(-0.495,0.495,-0.495,0.495,100,100,10000-1,'/home/crhea/Dropbox/Thesis/lammps_square_10000.lj')
