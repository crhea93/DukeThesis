'''
This script reads in the elemental velocity data from MOOSE and interpolates the
data onto the particle fields
Arguements in the following order:
1 - Particle Field File
2 - Number of Particles
3 - Velocity X Field
4 - Velocity Y Field
5 - output file name
'''
import sys
import numpy as np
from scipy.interpolate import griddata
import netCDF4

def Interpolate(Pfield,num_particles,Velx,Vely,exodus_file,output):
    #Read in particle field
    lines_PF = sum(1 for line in open(Pfield))
    particles_x = np.zeros((num_particles,1))
    particles_y = np.zeros((num_particles,1))
    part_num = np.zeros((num_particles,1))
    linenumber = 0
    count = 0
    total_lines = sum(1 for line in open(Pfield))
    for line in  open(Pfield):
        if linenumber>9 and linenumber<9+total_lines:
            lineSplit = line.split(" ")
            part_num[count] = lineSplit[0]
            particles_x[count] = lineSplit[4]
            particles_y[count] = lineSplit[5]
            count += 1
        else:
             pass
        linenumber += 1
    #Read in velocities

     #exodus_file = '/home/crhea/Dropbox/Thesis/PrimaryFiles/Front/MOOSEFILES/MOOSEOutput10.e'
    nc = netCDF4.Dataset(exodus_file)
    xvel = nc.variables['vals_elem_var1eb1'][1]
    yvel = nc.variables['vals_elem_var2eb1'][1]

    #Read in element locations
    lines_vel = sum(1 for line in open(Velx))
    velx_pos = np.zeros((lines_vel-1,6)) # x1,y1,x2,y2,x3,y3
    vely_pos = np.zeros((lines_vel-1,6))
    velx = np.zeros((lines_vel-1,1))
    vely = np.zeros((lines_vel-1,1))
    countx = 0
    linenumberx = 0
    for linex in  open(Velx):
        if linenumberx>0:
            lineSplitx = linex.split(",")
            velx_pos[countx,0] = float(lineSplitx[0])
            velx_pos[countx,1] = float(lineSplitx[1])
            velx_pos[countx,2] = float(lineSplitx[2])
            velx_pos[countx,3] = float(lineSplitx[3])
            velx_pos[countx,4] = float(lineSplitx[4])
            velx_pos[countx,5] = float(lineSplitx[5])
            #if -10**(-10)<float(lineSplitx[6]) and float(lineSplitx[6])<10**(10):
            #    velx[countx] = 0.0
            #else:
            #    velx[countx] = float(lineSplitx[6])
            #print(lineSplitx[5])
            velx[countx] = xvel[countx]
            countx += 1
        else:
             pass
        linenumberx += 1

    county = 0
    linenumbery = 0
    for liney in  open(Vely):
        if linenumbery>0:
            lineSplity = liney.split(",")
            vely_pos[county,0] = float(lineSplity[0])
            vely_pos[county,1] = float(lineSplity[1])
            vely_pos[county,2] = float(lineSplity[2])
            vely_pos[county,3] = float(lineSplity[3])
            vely_pos[county,4] = float(lineSplity[4])
            vely_pos[county,5] = float(lineSplity[5])
            #if -10**(-10)<float(lineSplity[6]) and float(lineSplity[6])<10**(-10):
            #    vely[county] = 0.0
            #else:
            #    vely[county] = float(lineSplity[6])
            vely[county] = yvel[county]
            county += 1
        else:
             pass
        linenumbery += 1


    #Calculate velocities at center point
    center_velx = np.zeros((lines_vel-1,3)) #x,y,val
    center_vely = np.zeros((lines_vel-1,3))
    for i in range(lines_vel-1):
        center_velx[i,0] = (velx_pos[i,0]+velx_pos[i,2]+velx_pos[i,4])/3.0
        center_vely[i,0] = (vely_pos[i,0]+vely_pos[i,2]+vely_pos[i,4])/3.0
        center_velx[i,1] = (velx_pos[i,1]+velx_pos[i,3]+velx_pos[i,5])/3.0
        center_vely[i,1] = (vely_pos[i,1]+vely_pos[i,3]+vely_pos[i,5])/3.0
        center_velx[i,2] = velx[i]
        center_vely[i,2] = vely[i]



    #print(center_velx[:,2])
    #print(center_vely[:,2])
    #print(particles_x)
    #print(particles_y)
    #Interpolate
    Interpx = griddata((center_velx[:, 0], center_velx[:, 1]), center_velx[:, 2], (particles_x, particles_y), method="cubic", fill_value=0.0)
    Interpy = griddata((center_vely[:, 0], center_vely[:, 1]), center_vely[:, 2], (particles_x, particles_y), method="cubic", fill_value=0.0)
    #print(Interpx)
    #Print to new file
    out = open(output+"X.txt","w")
    outy = open(output+"Y.txt","w")
    for i in range(len(Interpx)):
        out.write(str(particles_x[i].item(0))+" "+str(particles_y[i].item(0))+" "+str(Interpx[i].item(0))+'\n')
        outy.write(str(particles_x[i].item(0))+" "+str(particles_y[i].item(0))+" "+str(Interpy[i].item(0))+'\n')
    out.close()
    outy.close()

#def main():
#    Interpolate(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5])
#main()
