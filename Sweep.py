'''
Primary Program for FEM-DEM coupling
Ensure that all files print to PrimaryFiles directory
Inputs:
Mesh
Initial Pressure Value

Mui = viscosity of invading Fluid
Mud = viscosity of defending Fluid
'''
from Input.Sweep import *


# BASIC IMPORTS
import numpy as np
import os
import sys
from subprocess import call
from shutil import copyfile
from lammps import lammps
import time
# MODULES NEEDED TO INPUT
from pythonCode.Cohesion.VelToLammps import Interpolate
from pythonCode.Cohesion.Viscosity import visc_avg
from pythonCode.Cohesion.SaturationInterp import sat_int
from pythonCode.MOOSE.InitSatPorCircle import InitCircle,InitConst
from pythonCode.LAMMPS.DataToTxt import write_to_txt
from pythonCode.Cohesion.MooseRenameOutput import Moose_append_timestep,Moose_append_init,MooseRenamePorosity
from pythonCode.Cohesion.PorosityReconfigLammpsOutput import reconfig,reconfigInit
from pythonCode.MOOSE.Readmesh import count_FEMesh



def Setup(Sim_name,MooseFileDir,LammpsFileDir,ParticlesFile,Porosity_Filecpp,Mesh,mui):
    if os.path.exists("/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name)!= True:
        os.mkdir("/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name)
    os.chdir("/home/crhea/Dropbox/Thesis/PrimaryFiles/SweepSimulations/")
    copyfile("/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Porosity_Filecpp+".cpp","/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/"+Porosity_Filecpp+".cpp")
    copyfile("/home/crhea/Dropbox/Thesis/PrimaryFiles/SweepSimulations/"+ParticlesFile,"/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/"+ParticlesFile)
    os.chdir("/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/")
    if os.path.exists(LammpsFileDir)!=True:
        os.mkdir(LammpsFileDir)
        os.mkdir(LammpsFileDir+"/Pos")
        os.mkdir(MooseFileDir)



def runSim(Sim_name,MooseFileDir,LammpsFileDir,Porosity_Filecpp,PorosityFileMOOSE,Mesh,MooseFile,LammpsFile,ParticlesFile,In_Press,Num_times,Num_parts,Diameter,Poros,Mui,Mud,Domain,Ann_rad,Dom_rad,NN,Init=True):
    os.chdir("/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/")
    #Calculate element and node numbers for finite element mesh
    print(Mesh)
    num_nodes,num_elem = count_FEMesh(Mesh);
    print(Sim_name)
    lmp = lammps()
    #---------------------------INITIALIZATION---------------------------------#
    Update_Lammps_Init(Sim_name,LammpsFileDir,LammpsFile,ParticlesFile,Diameter,Domain)
    Update_Porosity(Sim_name,LammpsFileDir,Porosity_Filecpp,Mesh,Num_parts,Diameter/2.0,num_nodes,num_elem,Ann_rad,Dom_rad,NN)
    print("Reconfig Input file for the C++ file")
    reconfigInit(Sim_name,LammpsFileDir,ParticlesFile,Num_parts)
    os.system('g++ -o porosity porosity.cpp')
    os.system('./porosity')
    copyfile("Porosity.txt","Porosity_old.txt")
    Init_FF(Sim_name,MooseFileDir,MooseFile,Mesh,PorosityFileMOOSE,In_Press,Mui)
    # -------------- DONE WITH INITIALIZATION ----------------------#
    call('mpiexec -n 1 /home/crhea/Dropbox/Thesis/bat/bat-opt -i '+ MooseFile,shell=True)
    Moose_append_init(MooseFileDir+"/","MOOSEOutput.e")
    #Setup MOOSE for subsequent runs
    Update_Moose_after_Init(Sim_name,Mesh,MooseFile,PorosityFileMOOSE)
    for timestep in range(Num_times):
        # Run LAMMPS
        #call('lammps < LAMMPS/inputfiles/in.primary',shell=True)
        # Update Velocity and Viscosity Fields in LAMMPS
        print("----------Beginning Interpolating----------")
        Interpolate(ParticlesFile,Num_parts,"velocitiesX.csv","velocitiesY.csv",MooseFileDir+"/MOOSEOutput.e","VelForLammps")
        visc_avg("MOOSEValues_sat_updated.txt",ParticlesFile,Mui,Mud,Num_parts,"Viscosity")
        sat_int("MOOSEValues_sat_updated.txt",ParticlesFile,Num_parts,"SaturationInterpolated")
        print("----------Ending Interpolating----------")

        # RUN LAMMPS
        if timestep == 0:
            print("----------LAMMPS RUN "+str(timestep)+ " Beginning----------")
            lmp.file(LammpsFile+"_init")
            #lmp.close()
            print("----------LAMMPS RUN "+str(timestep)+ " Ending----------")
        else:
            print("----------LAMMPS RUN "+str(timestep)+ " Beginning----------")
            lmp.command("clear")
            #lmp = lammps()
            lmp.file(LammpsFile)
            #lmp.close()
            print("----------LAMMPS RUN "+str(timestep)+ " Ending----------")

        #Update csv files for particle positions
        write_to_txt("/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/"+LammpsFileDir+"/pos_lammps_out.txt",number_particles,LammpsFileDir+"/Pos/pos_",timestep)
        # ---------------------- POROSITY UPDATE ----------------------#
        if Poros == True: #Only run porosity update if desired
            Update_Porosity(Sim_name,LammpsFileDir,Porosity_Filecpp,Mesh,Num_parts,Diameter/2.0,num_nodes,num_elem,Ann_rad,Dom_rad,NN)
            print("Reconfig Input file for the C++ file")
            reconfig(Sim_name,LammpsFileDir,"/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/"+LammpsFileDir+"/pos_lammps_out.txt",Num_parts)
            os.system('g++ -o porosity porosity.cpp')
            start = time.time()
            os.system('./porosity')
            end = time.time()
            print("Total Time for porosity calculations "+str(end-start))
        else:
            pass
        # ---------------------------- LAMMPS UPDATE ---------------------#
        Update_Lammps(Sim_name,LammpsFileDir,LammpsFile)
        # -------------------------- MOOSE -------------------------------#
        Update_MOOSE(Sim_name,MooseFile,PorosityFileMOOSE,time)
        print("----------MOOSE RUN "+str(timestep+1)+ " Beginning----------")
        call('mpiexec -n 1 /home/crhea/Dropbox/Thesis/bat/bat-opt -i '+ MooseFile,shell=True)
        MooseRenamePorosity(Sim_name)
        print("----------MOOSE RUN "+str(timestep+1)+ " Ending----------")
        Moose_append_timestep(MooseFileDir+"/","MOOSEOutput.e",timestep)




def main():
    viscosities = [250.0,500.0,1000.0]
    for i in range(len(viscosities)):
        Name_of_Simu = Name_of_Sim+"_"+str(viscosities[i])
        Setup(Name_of_Simu,MOOSEFILEDIR,LAMMPSFILEDIR,ParticlesInput,PorosityFilecpp,mesh,viscosities[i])
        runSim(Name_of_Simu,MOOSEFILEDIR,LAMMPSFILEDIR,PorosityFilecpp,PorosityFileforMOOSE,mesh,MooseFile,LammpsFile,ParticlesInput,initial_press,number_times,number_particles,particle_diameter,Porosity_Boolean,viscosities[i],mud,Domain,annulus_radius,domain_radius,NN_number)




main()
