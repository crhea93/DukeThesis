'''
Reformat Atom Position Files for read in for porosity
'''
def reconfig(simulation,LammpsFileDir,inputfile,num_part):
    count = 0
    outputfile = open(LammpsFileDir+'/lammps_pos_out_simple.txt','w')
    for line in open(inputfile):
        if count>9 and count<num_part+9:
            lineSplit = line.split(" ")
            outputfile.write(str(lineSplit[2])+" "+str(lineSplit[3])+'\n')
        count += 1

def reconfigInit(simulation,LammpsFileDir,inputfile,num_part):
    count = 0
    outputfile = open(LammpsFileDir+'/lammps_pos_out_simple.txt','w')
    for line in open(inputfile):
        if count>9 and count<num_part+10:
            lineSplit = line.split(" ")
            outputfile.write(str(lineSplit[4])+" "+str(lineSplit[5])+'\n')
        count += 1
