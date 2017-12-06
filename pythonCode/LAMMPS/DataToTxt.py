#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:08:30 2017

Python file to read data dump file created by LAMMPS and spit out txt file
with coordinate positions based on atom number.

This works by stepping through a directory that contains the files from lammps


arg1 -- path to lammps files (total path)
arg 2 -- number of particles
arg 3 -- output file
arg 4 -- filenumber to print out
@author: crhea
"""
import numpy as np
import os


#num_parts = 100
#outputfile = "particles_lammps"
import sys
def write_to_txt(datafile,num_parts,outputfile,filenumber):
    part_num = np.zeros((num_parts,1))
    x_coords = np.zeros((num_parts,1))
    y_coords = np.zeros((num_parts,1))
    x_vel = np.zeros((num_parts,1))
    y_vel = np.zeros((num_parts,1))
    mag_vel = np.zeros((num_parts,1))
    linenumber = 0
    count = 0;
    total_lines = sum(1 for line in open(datafile))
    for line in  open(datafile):
        if linenumber>8 and linenumber<num_parts+9:
            lineSplit = line.split(" ")
            part_num[count] = lineSplit[0]
            x_coords[count] = lineSplit[2]
            y_coords[count] = lineSplit[3]
            x_vel[count] = lineSplit[5]
            y_vel[count] = lineSplit[6]
            mag_vel[count] = np.sqrt(x_vel[count]**2+y_vel[count]**2)
            count += 1
        else:
             pass
        linenumber += 1


    '''out = open(outputfile+str(filenumber)+".txt","w")
    for i in range(num_parts):
        out.write(str(part_num[i].item(0))+" "+str(x_coords[i].item(0))+" "+str(y_coords[i].item())+'\n')
    out.close()
    '''
    out2 = open(outputfile+str(filenumber)+".csv","w")
    out2.write("Value"+ "," + "X" + "," + "Y"+"," + "X_vel"+"," + "Y_vel"+"," + "Mag_vel"+'\n')
    for i in range(num_parts):
        out2.write(str(part_num[i].item(0))+","+str(x_coords[i].item(0))+","+str(y_coords[i].item(0))+","+str(x_vel[i].item(0))+","+str(y_vel[i].item(0))+","+str(mag_vel[i].item(0))+'\n')
    out2.close()
