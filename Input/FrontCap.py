'''
Input File for Front with Capillary and Viscous Forces
'''
Name_of_Sim = 'FrontCap'
# FILES FOR INPUT
mesh = 'square_Ref1'
MooseFile = 'bat/input/Front.i'
LammpsFile = 'LAMMPS/inputfiles/in.front_cap'
ParticlesInput = 'PrimaryFiles/'+Name_of_Sim+'/lammps_front_100.lj'
PorosityFilecpp = 'porosity'
PorosityFileforMOOSE = 'Porosity'
# VALUES FOR INPUT
initial_press = 0.0+10**(-5)
number_particles = 100
number_times = 100
particle_diameter = 0.05
Porosity_Boolean = False #Update porosity or not
mui = 0.8 #Viscosity of invading Fluid
mud = 0.5 #Viscosity of defending Fluid
Domain = [-0.5,0.5,-0.5,0.5]
#Values for Porosity calculations
annulus_radius = 0.03 #Radius of small anulus
domain_radius = 1.0 #Radius of domain
NN_number = 20 #Number of nearest neighbors
# FUNCTIONS FOR UPDATING (ONLY EVER NEED TO CHANGE THE LINES)
from pythonCode.MOOSE.InitSatPorCircle import InitConst
from pythonCode.Cohesion.ChangeFiles import change_input

def Init_FF(Sim_name,MooseFile,Mesh,Porosity_File,Init_Press):
    Meshchange = 'file = Mesh/'+Mesh+'.e'
    outputinitSatPress = "PrimaryFiles/"+Sim_name+"/MOOSEValues"
    #InitConst("Mesh/"+Mesh+".e",outputinitSatPress,Init_Press)
    SatInitName = 'dataFile = PrimaryFiles/'+Sim_name+'/MOOSEValues_sat_init.txt'
    PressInitName = 'dataFile = PrimaryFiles/'+Sim_name+'/MOOSEValues_press_init.txt'
    PorosityInitName = 'dataFile = PrimaryFiles/'+Sim_name+'/'+Porosity_File+'.txt'
    XvelName = '    output = PrimaryFiles/'+Sim_name+'/velocitiesX'
    YvelName = '    output = PrimaryFiles/'+Sim_name+'/velocitiesY'
    Sat_Out = '     output = PrimaryFiles/'+Sim_name+'/MOOSEValues_sat_updated'
    Press_Out = '     output = PrimaryFiles/'+Sim_name+'/MOOSEValues_press_updated'
    OutputName = 'file_base = PrimaryFiles/'+Sim_name+'/MOOSEFILES/MOOSEOutput'

    lines_to_change = [3,168,173,178,199,204,209,214,237]
    new_lines = [Meshchange,SatInitName,PressInitName,PorosityInitName,XvelName,YvelName,Sat_Out,Press_Out,OutputName]
    change_input(MooseFile,lines_to_change,new_lines)


# CHANGE FLUID FLOW MOOSE INPUT FILE
def Update_Moose_after_Init(Sim_name,Mesh,MooseFile,Porosity_File):
    SatInitName = 'dataFile = PrimaryFiles/'+Sim_name+'/MOOSEValues_sat_updated.txt'
    PressInitName = 'dataFile = PrimaryFiles/'+Sim_name+'/MOOSEValues_press_updated.txt'
    PorosityInitName = 'dataFile = PrimaryFiles/'+Sim_name+'/'+Porosity_File+'.txt'
    lines_to_change = [168,173,178]
    new_lines = [SatInitName,PressInitName,PorosityInitName]
    change_input(MooseFile,lines_to_change,new_lines)

def Update_MOOSE(Sim_name,MooseFile,Porosity_File,time_Step):
    PorosityInitName = 'dataFile = PrimaryFiles/'+Sim_name+'/'+Porosity_File+'.txt'
    #OutputName = 'file_base = PrimaryFiles/'+Sim_name+'/MOOSEFILES/MOOSEOutput'+str(time_Step)
    lines_to_change = [178]#,237]
    new_lines = [PorosityInitName]#,OutputName]
    change_input(MooseFile,lines_to_change,new_lines)

# CHANGE LAMMPS INPUT FILE
def Update_Lammps_Init(Sim_name,LammpsFile,ParticlesInput,Diameter,DomainVals):
    DiameterData = 'variable        Diam equal '+str(Diameter)
    InitData = 'read_data       '+ParticlesInput
    Dump = 'dump pos 	all custom 100 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/LAMMPSFILES/pos_lammps_out.txt id type x y z vx vy vz'
    Restart = 'restart		100 PrimaryFiles/'+Sim_name+'/LAMMPSFILES/restart1 PrimaryFiles/'+Sim_name+'/LAMMPSFILES/restart2'
    Fix1 = 'fix		1 all viscous/field 0.5 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsX.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsY.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/Viscosity.txt'
    if len(Domain) == 4: #Rectangle
        DomainSet = 'region		box block '+str(DomainVals[0])+' '+str(DomainVals[1]) + ' '+str(DomainVals[2])+' '+str(DomainVals[3])+' -3 3 units box'
        lines_to_change = [2,29,30,43,49,53]
    else:
        #cirlce
        pass
    new_line_lammps = [DiameterData,InitData,DomainSet,Dump,Restart,Fix1]
    change_input(LammpsFile+"_init",lines_to_change,new_line_lammps)


def Update_Lammps(Sim_name,LammpsFile):
    RestartRead = 'read_restart  	/home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/LAMMPSFILES/restart1'
    Dump = 'dump pos 	all custom 100 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/LAMMPSFILES/pos_lammps_out.txt id type x y z vx vy vz'
    Restart = 'restart		100 PrimaryFiles/'+Sim_name+'/LAMMPSFILES/restart1 PrimaryFiles/'+Sim_name+'/LAMMPSFILES/restart2'
    Fix1 = 'fix		1 all viscous/field 0.5 /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsX.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/VelForLammpsY.txt /home/crhea/Dropbox/Thesis/PrimaryFiles/'+Sim_name+'/Viscosity.txt'
    lines_to_change = [1,31,36,43]
    new_line_lammps2 = [RestartRead,Dump,Restart,Fix1]
    change_input(LammpsFile,lines_to_change,new_line_lammps2)


def Update_Porosity(Sim_name,Porosity_file,Mesh,nparticles,radius,nnodes,nelements,ann_r,dom_r,NN):
    input_path = "string input_path = \"/home/crhea/Dropbox/Thesis/Mesh/\";"
    input_path_lammps_Data = "string input_path_lammps_Data = \"/home/crhea/Dropbox/Thesis/PrimaryFiles/"+Sim_name+"/LAMMPSFILES/\";"
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
    lines_to_change = [686,687,688,689,690,691,692,693,694,695,697,699,701,702]
    new_lines = [input_path,input_path_lammps_Data,output_path,mesh_to_read,mesh_connectivity,file_name,output,domain_radius,annulus_radius,num_partic_lines,nnodes,number_cell_elements,num_of_NN,rad]
    change_input(Porosity_file+'.cpp',lines_to_change,new_lines)
