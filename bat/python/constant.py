'''
This program will create a constant porosity field
'''

import numpy as np
filename = open("/home/crhea/Dropbox/Thesis/bat/mesh/Tests/constant_Ref1.txt",'w') #file printout

file1 = "/home/crhea/Dropbox/Thesis/bat/mesh/Tests/Constant/square_Ref1_nodes.txt" #read in file
mynumbers = []
with open(file1) as f:
    for line in f:
        mynumbers.append([float(n) for n in line.strip().split(' ')])
for pair in mynumbers:
    x,y = pair[0],pair[1]
    filename.write(str(x) + " " + str(y) + " " + str(0.55))
    filename.write('\n')
filename.close()
