'''
Input File for Front with Capillary and Viscous Forces
'''
#Name_of_Sim = 'Central_Square'
Name_of_Sim = 'SweepSimulations/Test'
MOOSEFILEDIR = 'MOOSEFILES'
LAMMPSFILEDIR = 'LAMMPSFILES'
# FILES FOR INPUT
mesh = '/home/crhea/Dropbox/Thesis/Mesh/Central_Square'
MooseFile = '/home/crhea/Dropbox/Thesis/bat/input/Radial.i'
LammpsFile = '/home/crhea/Dropbox/Thesis/LAMMPS/inputfiles/in.central_square'
ParticlesInput = 'lammps_circle_hydrostatic.lj'
PorosityFilecpp = 'porosity'
PorosityFileforMOOSE = 'Porosity'
# VALUES FOR INPUT
initial_press = 0.0+10**(-5)
number_particles = 9960
number_times = 2000
particle_diameter = 0.01
Porosity_Boolean = True
#mui = 0.8 #Viscosity of invading Fluid
mui = 80.0
mud = 0.5 #Viscosity of defending Fluid
Domain = [-0.6,0.6,-0.6,0.6] #Rectangle
#Values for Porosity calculations
annulus_radius = 0.02 #Radius of small anulus
domain_radius = 1.8 #Radius of domain
NN_number = 100 #Number of nearest neighbors

# FUNCTIONS FOR UPDATING (ONLY EVER NEED TO CHANGE THE LINES)
from pythonCode.MOOSE.InitSatPorCircle import InitConst,InitCircle
from pythonCode.Cohesion.ChangeFiles import change_input


def Init_FF(Sim_name,MooseFileDir,MooseFile,Mesh,Porosity_File,Init_Press):
    WorkingDirectory = '/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'
    Meshchange = 'file = '+Mesh+'.e'
    outputinitSatPress = "MOOSEValues"
    InitConst(Mesh+".e",outputinitSatPress,Init_Press)
    SatInitName = 'dataFile = '+WorkingDirectory+'MOOSEValues_sat_init.txt'
    PressInitName = 'dataFile = '+WorkingDirectory+'MOOSEValues_press_init.txt'
    PorosityInitName = 'dataFile = '+WorkingDirectory+Porosity_File+'.txt'
    PorosityInitNameOld = 'dataFile = '+WorkingDirectory+Porosity_File+'.txt'
    XvelName = '    output ='+WorkingDirectory+'velocitiesX'
    YvelName = '    output = '+WorkingDirectory+'velocitiesY'
    Sat_Out = '     output = '+WorkingDirectory+'MOOSEValues_sat_updated'
    Press_Out = '     output = '+WorkingDirectory+'MOOSEValues_press_updated'
    OutputName = 'file_base = '+WorkingDirectory+MooseFileDir+'/MOOSEOutput'
    lines_to_change = [3,110,115,120,125,146,151,156,161,184]
    new_lines = [Meshchange,SatInitName,PressInitName,PorosityInitName,PorosityInitNameOld,XvelName,YvelName,Sat_Out,Press_Out,OutputName]
    change_input(MooseFile,lines_to_change,new_lines)


# CHANGE FLUID FLOW MOOSE INPUT FILE
def Update_Moose_after_Init(Sim_name,Mesh,MooseFile,Porosity_File):
    WorkingDirectory = '/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'
    SatInitName = 'dataFile = '+WorkingDirectory+'MOOSEValues_sat_updated.txt'
    PressInitName = 'dataFile = '+WorkingDirectory+'MOOSEValues_press_updated.txt'
    PorosityInitName = 'dataFile = '+WorkingDirectory+Porosity_File+'.txt'
    PorosityInitNameOld = 'dataFile = '+WorkingDirectory+Porosity_File+'.txt'
    lines_to_change = [110,115,120,125]
    new_lines = [SatInitName,PressInitName,PorosityInitName,PorosityInitNameOld]
    change_input(MooseFile,lines_to_change,new_lines)

def Update_MOOSE(Sim_name,MooseFile,Porosity_File,time_Step):
    WorkingDirectory = '/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'
    PorosityInitName = 'dataFile = '+WorkingDirectory+Porosity_File+'.txt'
    PorosityInitNameOld = 'dataFile = '+WorkingDirectory+Porosity_File+'_old.txt'
    #OutputName = 'file_base = PrimaryFiles/'+Sim_name+'/MOOSEFILES/MOOSEOutput'+str(time_Step)
    lines_to_change = [120,125]#,237]
    new_lines = [PorosityInitName,PorosityInitNameOld]#,OutputName]
    change_input(MooseFile,lines_to_change,new_lines)

# CHANGE LAMMPS INPUT FILE
def Update_Lammps_Init(Sim_name,LammpsFileDir,LammpsFile,ParticlesInput,Diameter,DomainVals):
    DiameterData = 'variable        Diam equal '+str(Diameter)
    InitData = 'read_data       '+ParticlesInput
    Dump = 'dump pos 	all custom 1 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+LammpsFileDir+'/pos_lammps_out.txt id type x y z vx vy vz'
    Restart = 'restart		1 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+LammpsFileDir+'/restart1 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+LammpsFileDir+'/restart2'
    Fix1 = 'fix		1 all viscous/field 50.0 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsX.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsY.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/Viscosity.txt'
    Hookean = 'pair_style 	hooke/cap ${kn} ${kt} ${gamma_n} ${gamma_t} ${coeffFric} 0  10.0 10.0 0.78 0.99 50.0 '+'/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/SaturationInterpolated.txt'
    if len(Domain) == 4: #Rectangle
        DomainSet = 'region		box block '+str(DomainVals[0])+' '+str(DomainVals[1]) + ' '+str(DomainVals[2])+' '+str(DomainVals[3])+' -3 3 units box'
        lines_to_change = [2,29,30,41,42,43,46]
    else:
        #cirlce
        pass
    new_line_lammps = [DiameterData,InitData,DomainSet,Dump,Restart,Hookean,Fix1]
    change_input(LammpsFile+"_init",lines_to_change,new_line_lammps)


def Update_Lammps(Sim_name,LammpsFileDir,LammpsFile):
    RestartRead = 'read_restart  	/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+LammpsFileDir+'/restart1'
    Dump = 'dump pos 	all custom 1 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+LammpsFileDir+'/pos_lammps_out.txt id type x y z vx vy vz'
    Restart = 'restart		1 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+LammpsFileDir+'/restart1 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+LammpsFileDir+'/restart2'
    Fix1 = 'fix		1 all viscous/field 50.0 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsX.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsY.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/Viscosity.txt'
    Hookean = 'pair_style 	hooke/cap ${kn} ${kt} ${gamma_n} ${gamma_t} ${coeffFric} 0  10.0 10.0 0.78 0.99 50.0 '+'/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/SaturationInterpolated.txt'
    lines_to_change = [1,34,35,40,44]
    new_line_lammps2 = [RestartRead,Dump,Restart,Hookean,Fix1]
    change_input(LammpsFile,lines_to_change,new_line_lammps2)


def Update_Porosity(Sim_name,LammpsFileDir,Porosity_file,Mesh,nparticles,radius,nnodes,nelements,ann_r,dom_r,NN):
    input_path = "string input_path = \"/home/crhea/Dropbox/Thesis/Mesh/\";"
    input_path_lammps_Data = "string input_path_lammps_Data = \"/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/"+LammpsFileDir+"/\";"
    output_path = "string output_path = \"/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/\";"
    mesh_to_read = "string mesh_to_read = \""+Mesh+"_nodes\";"
    mesh_connectivity = "string mesh_connectivity = \""+Mesh+"_connectivity\";"
    file_name = "string file_name = \"lammps_pos_out_simple\";"
    output = "string outputname = \"Porosity\";"
    domain_radius = 'double domain_radius = '+str(dom_r)+';'
    annulus_radius = 'double annulus_radius = '+str(ann_r)+';'
    nnodes = 'int nnodes ='+str(nnodes)+';'
    number_cell_elements = 'int number_cell_elements = '+str(nelements)+';'
    num_of_NN = 'int num_of_NN = '+str(NN)+';'
    num_partic_lines = 'int nparticles = '+str(nparticles)+';'
    rad = 'double particle_rad = '+str(radius)+';'
    lines_to_change =  [638,639,640,641,642,643,644,645,646,647,649,651,653,654]
    new_lines = [input_path,input_path_lammps_Data,output_path,mesh_to_read,mesh_connectivity,file_name,output,domain_radius,annulus_radius,num_partic_lines,nnodes,number_cell_elements,num_of_NN,rad]
    change_input('/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/'+Porosity_file+'.cpp',lines_to_change,new_lines)
