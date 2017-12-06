'''
This program will initialize the saturation and pore-pressure variables
Currently it only allows for a circular region (10/15/17)
INPUTS:
1 - Mesh exodus file total path
2 - Output file local path
3 - Center X coordinate
4 - Center Y coordinate
5 - Radius of Circle
6 - Value of Pressure Initial
'''
import netCDF4
import numpy as np
import sys
def InitCircle(mesh,output,xCen,yCen,Rad,press_val):
    exodus_file = str(mesh)
    element_type = 'T3' #'Q4' or 'T3'
    nc = netCDF4.Dataset(exodus_file)
    x = nc.variables['coord'][0]
    y = nc.variables['coord'][1]

    sat_values = np.zeros((len(x),1))
    pore_values = np.zeros((len(x),1))

    max_sat = 1.00-10**(-5)
    current_value_sat = 0.0
    current_value_press = 0.0
    aux_dist = 0.0
    for i in range(len(x)):
        x_cur = x[i]
        y_cur = y[i]
        aux_dist = np.sqrt((x_cur-xCen)**2+(yCen-y_cur)**2)
        if aux_dist < Rad:
            current_value_sat = max_sat-max_sat*(aux_dist/Rad)
            current_value_press = press_val-press_val*(aux_dist/Rad)
        else:
            current_value_sat = 0.0
            current_value_press = 0.0

        sat_values[i] = current_value_sat
        pore_values[i] = current_value_press

    outSat = open(output+"_sat_init.txt","w")
    outPor = open(output+"_press_init.txt","w")
    for i in range(len(x)):
        x_cur = x[i]
        y_cur = y[i]
        outSat.write(str(x_cur)+" "+str(y_cur)+" "+str(sat_values[i].item(0))+'\n')
        outPor.write(str(x_cur)+" "+str(y_cur)+" "+str(pore_values[i].item(0))+'\n')





#------------------ CONSTANT FIELDS ------------------------------------#
def InitConst(mesh,output,press_val):
    exodus_file = str(mesh)
    element_type = 'T3' #'Q4' or 'T3'
    nc = netCDF4.Dataset(exodus_file)
    x = nc.variables['coord'][0]
    y = nc.variables['coord'][1]

    sat_values = np.zeros((len(x),1))
    pore_values = np.zeros((len(x),1))

    for i in range(len(x)):
        current_value_sat = 0.0+0.0001
        current_value_press = press_val

        sat_values[i] = current_value_sat
        pore_values[i] = current_value_press

    outSat = open(output+"_sat_init.txt","w")
    outPor = open(output+"_press_init.txt","w")
    for i in range(len(x)):
        x_cur = x[i]
        y_cur = y[i]
        outSat.write(str(x_cur)+" "+str(y_cur)+" "+str(sat_values[i].item(0))+'\n')
        outPor.write(str(x_cur)+" "+str(y_cur)+" "+str(pore_values[i].item(0))+'\n')




#def main():
#    Init(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
#main()
