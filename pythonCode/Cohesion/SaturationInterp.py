'''Interpolate saturation values onto particle positions'''
from scipy.interpolate import griddata
import numpy as np
def sat_int(SaturationFile,ParticleField,num_part,output):
    total_lines_Sat = sum(1 for line in open(SaturationFile))
    sat_data = np.zeros((total_lines_Sat,3))
    viscosity = np.zeros((num_part,1))
    x_lammps = np.zeros((num_part,1))
    y_lammps = np.zeros((num_part,1))
    # READ IN MOOSE DATA
    linecount = 0
    for line in open(SaturationFile):
        lineSplit = line.split(" ")
        sat_data[linecount,0] = lineSplit[0]
        sat_data[linecount,1] = lineSplit[1]
        sat_data[linecount,1] = lineSplit[2]
        linecount += 1
    # Now read in LAMMPS DATA
    linenumber = 0
    count = 0
    total_lines = sum(1 for line in open(ParticleField))
    for line in  open(ParticleField):
        if linenumber>9 and linenumber<9+total_lines:
            lineSplit = line.split(" ")
            x_lammps[count] = lineSplit[4]
            y_lammps[count] = lineSplit[5]
            count += 1
        else:
             pass
        linenumber += 1


    # CALCULATE Saturation at the particle points through interpolation
    Sat_interp = griddata((sat_data[:,0] , sat_data[:,1]), sat_data[:,2], (x_lammps, y_lammps), method="cubic", fill_value=0.1)
    Sat_interp += 0.0001


    # Print to output file
    out = open(output+".txt","w")
    for i in range(len(viscosity)):
        out.write(str(x_lammps[i].item(0))+" "+str(y_lammps[i].item(0))+" "+str(Sat_interp[i].item(0))+'\n')
    out.close()
    out.close()
