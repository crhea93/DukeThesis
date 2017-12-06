'''
Program to create input file for LAMMPS
INPUTS :
1 - number of particles
2 - x low
3 - x high
4 - y low
5 - y high
6 - Input File for Positions
7 - Input File for velocities
8 - Input File for Angular Velocities
'''

import numpy as np
def create_readin(num_part,xlo,xhi,ylo,yhi,input_file_pos,input_file_vel,output_file):
    pos = np.zeros((num_part,3))
    vel = np.zeros((num_part,3))
    omega = np.zeros((num_part,3))
    count = 0
    for line in open(input_file_pos):
        if count>8:
            lineSplit = line.split(" ")
            pos[count,0] = lineSplit[2]
            pos[count,1] = lineSplit[3]
        count+=1

    count = 0
    for line in open(input_file_vel):
        if count>8:
            lineSplit = line.split(" ")
            vel[count,0] = lineSplit[2]
            vel[count,1] = lineSplit[3]
            omega[count,0] = lineSplit[5]
            omega[count,1] = lineSplit[6]
        count+=1

    #Now lets write out HEADER
    f = open.(output_file)
    f.write("LAMMPS Data File for updated particles")
    f.write(str(num_part)+" atoms")
    f.write('\n')
    f.write('1 atom types')
    f.write(str(xlo)+" "+str(xhi)+" xlo xhi")
    f.write(str(ylo)+" "+str(yhi)+" "+" ylo yhi")
    f.write('\n')
    f.write('Atoms')
    f.write('\n')
    #write Positions
    for i in range(num_part):
        f.write(str(i)+" 1 1 1 "+str(pos[i,0])+" "+str(pos[i,1])+ " 0 0 0 0")
    f.write('\n')
    f.write("Velocities")
    f.write('\n')
    for i in range(num_part):
        f.write(str(i)+" "+str(vel[i,0])+" "+str(vel[i,1])+" 0")
