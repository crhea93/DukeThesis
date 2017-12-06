'''
This program will create a cross bar system for the porosity field
'''

import numpy as np
filename = open("/home/crhea/Dropbox/Thesis/bat/input/Porosity.txt",'w') #file printout

file1 = "/home/crhea/Dropbox/Thesis/bat/mesh/square_Ref1_nodes.txt" #read in file
mynumbers = []
with open(file1) as f:
    for line in f:
        mynumbers.append([float(n) for n in line.strip().split(' ')])
for pair in mynumbers:
    x,y = pair[0],pair[1]
    if -0.1<=y<=0.1:
        filename.write(str(x) + " " + str(y) + " " + str(0.1))
    else:
        filename.write(str(x) + " " + str(y) + " " + str(1.0))
    filename.write('\n')
filename.close()

filename = open("/home/crhea/Dropbox/Thesis/bat/input/Saturation.txt",'w') #file printout

file1 = "/home/crhea/Dropbox/Thesis/bat/mesh/square_Ref1_nodes.txt" #read in file
mynumbers = []
with open(file1) as f:
    for line in f:
        mynumbers.append([float(n) for n in line.strip().split(' ')])
for pair in mynumbers:
    x,y = pair[0],pair[1]
    if -0.5<=x<=0.0 and -0.1<=y<=0.1:
        filename.write(str(x) + " " + str(y) + " " + str(0.95))
    else:
        filename.write(str(x) + " " + str(y) + " " + str(0.0))
    filename.write('\n')
filename.close()

filename = open("/home/crhea/Dropbox/Thesis/bat/input/Pressure.txt",'w') #file printout

file1 = "/home/crhea/Dropbox/Thesis/bat/mesh/square_Ref1_nodes.txt" #read in file
mynumbers = []
with open(file1) as f:
    for line in f:
        mynumbers.append([float(n) for n in line.strip().split(' ')])
for pair in mynumbers:
    x,y = pair[0],pair[1]

    filename.write(str(x) + " " + str(y) + " " + str(1.0))

    filename.write('\n')
filename.close()
