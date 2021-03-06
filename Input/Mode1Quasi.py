'''
Input File for Tube with Capillary and Viscous Forces as well as porosity
'''
Name_of_Sim = 'Mode1'
MOOSEFILEDIR = 'MOOSEFILES'
LAMMPSFILEDIR = 'LAMMPSFILES'
ResultsDir = '/media/crhea/Data/Mode1/'
# FILES FOR INPUT
#PorosityFileInit = 'constant_Ref1'
mesh = '/home/crhea/Documents/DukeThesis/Mesh/square_Ref1'
MooseFile = '/home/crhea/Documents/DukeThesis/bat/input/Mode1.i'
LammpsFile = '/home/crhea/Documents/DukeThesis/LAMMPS/inputfiles/in.square'
ParticlesInput = 'lammps_square_100x100_inc.lj'
PorosityFilecpp = 'porosity'
PorosityFileforMOOSE = 'Porosity'
# VALUES FOR INPUT
initial_press = 0.0+10**(-5)
number_particles = 8000
number_times = 100
particle_diameter = 0.01
Porosity_Boolean = True
mui = 0.8 #Viscosity of invading Fluid
mud = 0.5 #Viscosity of defending Fluid
Domain = [-0.5,0.5,-0.5,0.5]
#Values for Porosity calculations
annulus_radius = 0.05 #Radius of small anulus
domain_radius = 1.0 #Radius of domain
NN_number = 100 #Number of nearest neighbors


# FUNCTIONS FOR UPDATING (ONLY EVER NEED TO CHANGE THE LINES)
from pythonCode.MOOSE.InitSatPorCircle import InitConst
from pythonCode.Cohesion.ChangeFiles import change_input

def Init_FF(Sim_name,ResultsDir,MooseFileDir,MooseFile,Mesh,Porosity_File,Init_Press,mui):
    WorkingDirectory = ResultsDir+Sim_name+'/'
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
    InvadingFluidViscosity = 'water_viscosity = '+str(mui)
    lines_to_change = [3,79,110,115,120,125,146,151,156,161,184]
    new_lines = [Meshchange,InvadingFluidViscosity,SatInitName,PressInitName,PorosityInitName,PorosityInitNameOld,XvelName,YvelName,Sat_Out,Press_Out,OutputName]
    change_input(MooseFile,lines_to_change,new_lines)


# CHANGE FLUID FLOW MOOSE INPUT FILE
def Update_Moose_after_Init(Sim_name,ResultsDir,Mesh,MooseFile,Porosity_File):
    WorkingDirectory = ResultsDir+Sim_name+'/'
    SatInitName = 'dataFile = '+WorkingDirectory+'MOOSEValues_sat_updated.txt'
    PressInitName = 'dataFile = '+WorkingDirectory+'MOOSEValues_press_updated.txt'
    PorosityInitName = 'dataFile = '+WorkingDirectory+Porosity_File+'.txt'
    PorosityInitNameOld = 'dataFile = '+WorkingDirectory+Porosity_File+'_old.txt'
    lines_to_change = [110,115,120,125]
    new_lines = [SatInitName,PressInitName,PorosityInitName,PorosityInitNameOld]
    change_input(MooseFile,lines_to_change,new_lines)

def Update_MOOSE(Sim_name,ResultsDir,MooseFile,Porosity_File,time_Step):
    WorkingDirectory = ResultsDir+Sim_name+'/'
    PorosityInitName = 'dataFile = '+WorkingDirectory+Porosity_File+'.txt'
    PorosityInitNameOld = 'dataFile = '+WorkingDirectory+Porosity_File+'_old.txt'
    #OutputName = 'file_base = PrimaryFiles/'+Sim_name+'/MOOSEFILES/MOOSEOutput'+str(time_Step)
    lines_to_change = [120,125]#,237]
    new_lines = [PorosityInitName,PorosityInitNameOld]#,OutputName]
    change_input(MooseFile,lines_to_change,new_lines)

# CHANGE LAMMPS INPUT FILE
def Update_Lammps_Init(Sim_name,ResultsDir,LammpsFileDir,LammpsFile,ParticlesInput,Diameter,DomainVals):
    DiameterData = 'variable        Diam equal '+str(Diameter)
    InitData = 'read_data       '+ParticlesInput
    Dump = 'dump pos 	all custom 1 '+ResultsDir+Sim_name+'/'+LammpsFileDir+'/pos_lammps_out.txt id type x y z vx vy vz'
    Restart = 'restart		1 '+ResultsDir+Sim_name+'/'+LammpsFileDir+'/restart1 '+ResultsDir+Sim_name+'/'+LammpsFileDir+'/restart2'
    Fix1 = 'fix		1 all viscous/field 100.0 '+ResultsDir+Sim_name+'/VelForLammpsX.txt '+ResultsDir+Sim_name+'/VelForLammpsY.txt '+ResultsDir+Sim_name+'/Viscosity.txt'
    Hookean = 'pair_style 	hooke/cap ${kn} ${kt} ${gamma_n} ${gamma_t} ${coeffFric} 0  10.0 10.0 0.78 0.99 50.0 '+ResultsDir+Sim_name+'/SaturationInterpolated.txt'
    if len(Domain) == 4: #Rectangle
        DomainSet = 'region		box block '+str(DomainVals[0])+' '+str(DomainVals[1]) + ' '+str(DomainVals[2])+' '+str(DomainVals[3])+' -3 3 units box'
        lines_to_change = [2,29,30,41,42,43,46]
    else:
        #cirlce
        pass
    new_line_lammps = [DiameterData,InitData,DomainSet,Dump,Restart,Hookean,Fix1]
    change_input(LammpsFile+"_init",lines_to_change,new_line_lammps)


def Update_Lammps(Sim_name,ResultsDir,LammpsFileDir,LammpsFile):
    RestartRead = 'read_restart  	'+ResultsDir+Sim_name+'/'+LammpsFileDir+'/restart1'
    Dump = 'dump pos 	all custom 1 '+ResultsDir+Sim_name+'/'+LammpsFileDir+'/pos_lammps_out.txt id type x y z vx vy vz'
    Restart = 'restart		1 '+ResultsDir+Sim_name+'/'+LammpsFileDir+'/restart1 '+ResultsDir+Sim_name+'/'+LammpsFileDir+'/restart2'
    Fix1 = 'fix		1 all viscous/field 100.0 '+ResultsDir+Sim_name+'/VelForLammpsX.txt '+ResultsDir+Sim_name+'/VelForLammpsY.txt '+ResultsDir+Sim_name+'/Viscosity.txt'
    Hookean = 'pair_style 	hooke/cap ${kn} ${kt} ${gamma_n} ${gamma_t} ${coeffFric} 0  10.0 10.0 0.78 0.99 50.0 '+ResultsDir+Sim_name+'/SaturationInterpolated.txt'
    lines_to_change = [1,34,35,40,44]
    new_line_lammps2 = [RestartRead,Dump,Restart,Hookean,Fix1]
    change_input(LammpsFile,lines_to_change,new_line_lammps2)


def Update_Porosity(Sim_name,ResultsDir,LammpsFileDir,Porosity_file,Mesh,nparticles,radius,nnodes,nelements,ann_r,dom_r,NN):
    input_path = "string input_path = \"/home/crhea/Documents/DukeThesis/Mesh/\";"
    input_path_lammps_Data = "string input_path_lammps_Data = \""+ResultsDir+Sim_name+"/"+LammpsFileDir+"/\";"
    output_path = "string output_path = \""+ResultsDir+Sim_name+"/\";"
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
    #lines_to_change =  [555,556,557,558,559,560,561,562,563,564,566,568,570,571] #parallel
    lines_to_change = [638,639,640,641,642,643,644,645,646,647,649,651,653,654]
    new_lines = [input_path,input_path_lammps_Data,output_path,mesh_to_read,mesh_connectivity,file_name,output,domain_radius,annulus_radius,num_partic_lines,nnodes,number_cell_elements,num_of_NN,rad]
    change_input(ResultsDir+Sim_name+'/'+Porosity_file+'.cpp',lines_to_change,new_lines)
