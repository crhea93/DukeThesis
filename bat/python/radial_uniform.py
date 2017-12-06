##this file is meant to create an IC for the packing fraction such that there will be two branching chanels and the PF
##outside of the channels will be significantly greater than that in the channels.

import numpy as np

PF = open("/home/crhea/Dropbox/Thesis/bat/mesh/Tests/Radial/Radial_ref1.txt",'w')
file1 = "/home/crhea/Dropbox/Thesis/bat/mesh/Tests/square_Ref1_nodes.txt"

##get x and y coordinates
mynumbers = []
with open(file1) as f:
    for line in f:
        mynumbers.append([float(n) for n in line.strip().split(' ')])
circles = [0.0,0.1,0.2,0.3,0.4,0.5]
values = [0.15,0.35,0.55,0.75,0.95]
written = False
for pair in mynumbers:
    x,y = pair[0],pair[1]
    dist = np.sqrt(x**2+y**2)
    for i in range(len(circles)-1):
        if dist>=circles[i] and dist<=circles[i+1]:
            written = True
            circle_part = i
            break
    if (written == True):
        PF.write(str(x) + " " + str(y) + " " + str(values[circle_part]))
    else:
        PF.write(str(x) + " " + str(y) + " " + str(0.99))
    PF.write('\n')
PF.close()
