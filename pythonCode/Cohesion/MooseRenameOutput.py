'''
Renames moose output to be in the proper format for paraview to read as a
time series!
'''
import os
from shutil import copyfile
import netCDF4
def Moose_append_timestep(directory,filename,timestep):
    filename_no_ext = os.path.splitext(filename)[0]
    '''if timestep+1<10:
        timestamp = '00'+str(timestep+1)
    elif 10<=timestep+1<100:
        timestamp = '0'+str(timestep+1)
    else:
        timestamp = str(timestep+1)
    copyfile(directory+filename,directory+filename_no_ext+'.e-s.'+timestamp)
    '''
    nc = netCDF4.Dataset(directory+filename)

    por = nc.variables['vals_nod_var1'][1]
    pp = nc.variables['vals_nod_var3'][1]
    sat = nc.variables['vals_nod_var4'][1]
    x = nc.variables['coordx']
    y = nc.variables['coordy']

    fileout = open(directory+'MooseSimple'+str(timestep+1)+'.csv','w')
    fileout.write("X,Y,pp,sat,porosity \n")
    for i in range(len(x)):
        fileout.write(str(x[i])+","+str(y[i])+","+str(pp[i])+","+str(sat[i])+","+str(por[i])+'\n')

def Moose_append_init(directory,filename):
    filename_no_ext = os.path.splitext(filename)[0]
    #copyfile(directory+filename,directory+filename_no_ext+'.e-s.000')
    print(directory+filename)
    nc = netCDF4.Dataset(directory+filename)
    print(nc)
    por = nc.variables['vals_nod_var1'][1]#7
    pp = nc.variables['vals_nod_var3'][1]#//9
    sat = nc.variables['vals_nod_var4'][1]#10
    x = nc.variables['coordx']
    y = nc.variables['coordy']

    fileout = open(directory+'MooseSimple0.csv','w')
    fileout.write("X,Y,pp,sat,porosity \n")
    for i in range(len(x)):
        fileout.write(str(x[i])+","+str(y[i])+","+str(pp[i])+","+str(sat[i])+","+str(por[i])+'\n')

def MooseRenamePorosity(Sim_name,Resultsdir):
    copyfile(Resultsdir+Sim_name+'/Porosity.txt', Resultsdir+Sim_name+'/Porosity_old.txt')
