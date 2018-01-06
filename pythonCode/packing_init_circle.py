'''
Run lammps file to create initial packing fraction
'''
from lammps import lammps
import os
import numpy as np


def reformat(inputfile,outputfile,num_particles):
    outfile = open(outputfile+'.lj',"w")
    outfile.write("LAMMPS Data File for updated particles")
    outfile.write('\n')
    outfile.write(str(num_particles)+" atoms")
    outfile.write('\n')
    outfile.write('\n')
    outfile.write('1 atom types')
    outfile.write('\n')
    outfile.write(str(-1.0)+" "+str(1.0)+" xlo xhi")
    outfile.write('\n')
    outfile.write(str(-1.0)+" "+str(1.0)+" "+" ylo yhi")
    outfile.write('\n')
    outfile.write('-0.5 0.5 zlo zhi')
    outfile.write('\n')
    outfile.write('\n')
    outfile.write('Atoms')
    outfile.write('\n')
    outfile.write('\n')

    count = 0
    count2 = 0
    outfilecsv = open(outputfile+'.csv','w')
    outfilecsv.write("X,Y,ID, Mag_vel \n")
    for line in open(inputfile):
        if count>8 and count2<=num_particles:
            count2 += 1
            outfile.write(str(count2)+" 1 1 1 "+str(line.split(" ")[2])+" "+str(line.split(" ")[3])+ " 0 0 0 0"+'\n')
            outfilecsv.write(str(line.split(" ")[2])+","+str(line.split(" ")[3])+","+str(count2)+','+str(np.sqrt(float(line.split(" ")[5])**2+float(line.split(" ")[6])**2))+"\n")
        count += 1


def changeInput():
    pass

def main():
    lmp = lammps()
    os.chdir('/home/crhea/Documents/DukeThesis/')
    lmp.file('/home/crhea/Documents/DukeThesis/LAMMPS/inputfiles/in.Initialize_Packing_Circle')
    for i in range(100):
        reformat('/media/crhea/Data/HydroEquil/pos_lammps_out'+str(1000*i)+'.txt','/media/crhea/Data/HydroEquil/test'+str(i),7860)

main()
