'''Python File to compare porosity files'''
import numpy as np
line_numbers = 0
for line in open("porosity_standard.txt"):
    line_numbers+=1
standard = np.zeros((line_numbers,1))
count = 0
for line in open("porosity_standard.txt"):
    standard[count] = line.split(" ")[2]
    count += 1
new = np.zeros((line_numbers,1))
count = 0
for line in open("porosity_openmp.txt"):
    new[count] = line.split(" ")[2]
    count += 1
residual_sum = 0
for i in range(line_numbers):
    residual_sum += standard[i] - new[i]
print(residual_sum[0])
