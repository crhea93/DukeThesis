'''
This program will create a cross bar system for the porosity field
'''

import numpy as np
filename = open("/home/crhea/Dropbox/Thesis/bat/mesh/Tests/Bumps/bumps_Ref1.txt",'w') #file printout

file1 = "/home/crhea/Dropbox/Thesis/bat/mesh/Tests/square_Ref1_nodes.txt" #read in file
x_vals =[]
y_vals = []
mynumbers = []
found = False
with open(file1) as f:
    for line in f:
        mynumbers.append([float(n) for n in line.strip().split(' ')])
for pair in mynumbers:
    x,y = pair[0],pair[1]
    bumpsx = [0.3, 0.3, -0.3, -0.3]
    bumpsy = [0.3, -0.3 ,0.3 ,-0.3]
    for i in range(len(bumpsy)):
        dist = np.sqrt((x-bumpsx[i])**2+(y-bumpsy[i])**2)
        if dist>0.05:
            found = True
    if (found == True):
        val = 0.1
        filename.write(str(x) + " " + str(y) + " " + str(val))
    else:
        val = 0.9
        filename.write(str(x) + " " + str(y) + " " + str(val))
    filename.write('\n')
filename.close()
