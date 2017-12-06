'''
Change of Inputs for MOOSE and LAMMPS
'''
# CHANGE INPUT FILES
def change_input(filename,lines,new):
    with open(filename, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
    # now change the desired line, note that you have to add a newline
    num_count = 0
    for val in lines:
        if isinstance(new[num_count],str) != True:
            new[num_count] = str(new[num_count])
        data[val-1] = new[num_count]+'\n'
        num_count += 1
    # and write everything back
    with open(filename, 'w') as file:
        file.writelines( data )
