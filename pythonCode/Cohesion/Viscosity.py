'''
Transform Saturation into Viscosity
INPUTS:
SaturationFile - File generated from moose that is a field of the saturaiton VALUES
ParticleField - File of particle positions
mu1 - Viscosity of Defending FLUID (correlated to saturation value)
mu2 - Viscoisty of Invading Fluid
num_part - number of particles in simulation
'''
from scipy.interpolate import griddata
import numpy as np
def visc_avg(SaturationFile,ParticleField,mu1,mu2,num_part,output):
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
    Sat_interp = griddata((sat_data[:,0] , sat_data[:,1]), sat_data[:,2], (x_lammps, y_lammps), method="cubic", fill_value=0.0)

    # CALCULATE viscosity using a weighted average
    for i in range(num_part):
        viscosity[i] = Sat_interp[i]*mu1+(1-Sat_interp[i])*mu2

    # Print to output file
    out = open(output+".txt","w")
    for i in range(len(viscosity)):
        out.write(str(x_lammps[i].item(0))+" "+str(y_lammps[i].item(0))+" "+str(viscosity[i].item(0))+'\n')
    out.close()
    out.close()
