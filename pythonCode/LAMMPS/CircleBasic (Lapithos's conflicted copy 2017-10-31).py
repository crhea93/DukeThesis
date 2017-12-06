'''
File to create square of particles for lammps
'''

import numpy as np
def disk(x_part,y_part,x_cen,y_cen,rad1,rad2):
    if (rad1<=np.sqrt(x_part**2+y_part**2)<=rad2):
        return True
    else:
        return False
def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)
#Collision function


def place_particle_disk(particles,rad1,rad2,radius,count,num_parts_total):
    collide = False
    count += 1
    xp_possible = np.random.uniform(-1,1)
    xv_possible = np.random.uniform(-1,1)
    yp_possible = np.random.uniform(-1,1)
    yv_possible = np.random.uniform(-1,1)
    #radius_possible = np.random.uniform(1,1)u
    radius_possible = radius;
    #Check that particle is fully contained within domain
    if disk(xp_possible,yp_possible,0.0,0.0,rad1,rad2) == False and count<num_parts_total:
        return place_particle_disk(particles,rad1,rad2,radius,count,num_parts_total) #If not fully in try again
    else:
        pass #Particle in domain of interest
    for i in range(len(particles)):
        distance_parts = distance(xp_possible,yp_possible,particles[i].xp,particles[i].yp)
        rad_plus = radius_possible+particles[i].rad
        if (distance_parts<=rad_plus):
            collide = True #collision occurs
            break #get out of for loop
    #Now lets take a recurse in case collide is True
    if (collide==True) and (count<num_parts_total):
        return place_particle_disk(particles,rad1,rad2,radius,count,num_parts_total)
    elif (count > num_parts_total):
        print("Recursion Depth set by Carter Rhea Reached")
    else:
        pass
    return [xp_possible,xv_possible,yp_possible,yv_possible,radius_possible]


# Set each particle as a class
class particle:
    def __init__(self):
        self.xp = 0 # x coordinate
        self.xv = 0 # x velocity
        self.yp = 0 # y coordinate
        self.yv = 0 # y velocity
        self.rad = 0.001# particle radius
        self.m = 0 # mass
    def randomize(self,particles,xmin,xmax,ymin,ymax,radius,count):
        [xp_p,xv_p,yp_p,yv_p,radius_p] = place_particle(particles,xmin,xmax,ymin,ymax,radius,count)
        self.xp = xp_p
        self.xv = xv_p
        self.yp = yp_p
        self.yv = yv_p
        self.rad = radius_p
        self.m = np.random.uniform(0,1)
    def randomize_circ(self,particles,rad1,rad2,radius,count,num_parts):
        [xp_p,xv_p,yp_p,yv_p,radius_p] = place_particle_disk(particles,rad1,rad2,radius,count,num_parts)
        self.xp = xp_p
        self.xv = xv_p
        self.yp = yp_p
        self.yv = yv_p
        self.rad = radius_p
        self.m = np.random.uniform(0,1)
    def updateRK(self,new_vals):
        self.xp = new_vals.item(0) #RKsolve first Element
        self.xv = new_vals.item(1)
        self.yp = new_vals.item(2)
        self.yv = new_vals.item(3)
    def updateEuler(self,new_vals):
        self.xp = new_vals.item(0) #Eulre solve first Element
        self.xv = new_vals.item(1)
        self.yp = new_vals.item(2)
        self.yv = new_vals.item(3)
    def assign(self,xpos,xvel,ypos,yvel):
        self.xp = xpos
        self.xv = xvel
        self.yp = ypos
        self.yv = yvel
        self.rad = 0.001
        self.m = 1


#Create particle

def create_map_circle(rad1,rad2,num_particles):
    particles = []
    count = 0
    particle_0 = particle()
    particle_0.randomize_circ(particles,rad1,rad2,particle_0.rad,count,num_particles)
    particles.append(particle_0)
    for i in range(num_particles-1):
        if (i%1000==0):
            print("We are on particle number "+str(i))
        count = 0;
        new_particle = particle()
        new_particle.randomize_circ(particles,rad1,rad2,new_particle.rad,count,num_particles)
        particles.append(new_particle)
    return particles




def main(min_rad,max_rad,num_parts,output):
    particlesList = create_map_circle(min_rad,max_rad,num_parts)
    f = open(output,"w")
    f.write("LAMMPS Data File for updated particles")
    f.write('\n')
    f.write(str(num_parts)+" atoms")
    f.write('\n')
    f.write('\n')
    f.write('1 atom types')
    f.write('\n')
    f.write(str(-1.0)+" "+str(1.0)+" xlo xhi")
    f.write('\n')
    f.write(str(-1.0)+" "+str(1.0)+" "+" ylo yhi")
    f.write('\n')
    f.write('-0.5 0.5 zlo zhi')
    f.write('\n')
    f.write('\n')
    f.write('Atoms')
    f.write('\n')
    f.write('\n')
    #write Positions
    for i in range(num_parts):
        f.write(str(i+1)+" 1 1 1 "+str(particlesList[i].xp)+" "+str(particlesList[i].yp)+ " 0 0 0 0"+'\n')

main(0.05,1.0,100000,'/home/crhea/Dropbox/Thesis/lammps_disk_100000.lj')
