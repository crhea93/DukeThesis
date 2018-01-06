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
        self.rad = 0.05# particle radius
        self.m = 0 # mass
    def assign(self,xpos,xvel,ypos,yvel):
        self.xp = xpos
        self.xv = xvel
        self.yp = ypos
        self.yv = yvel
        self.rad = 0.05
        self.m = 1


def square_lattice(x_min,x_max,y_min,y_max,x_parts,y_parts,num_particles,output):
    particles = []
    x = np.linspace(x_min,x_max,x_parts)
    y = np.linspace(y_min,y_max,y_parts)
    for i in range(len(y)):
        for j in range(len(x)):
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

square_lattice(-4.95,4.95,-0.495,0.495,100,40,4000,'/home/crhea/Documents/DukeThesis/lammps_tube_4000.lj')
