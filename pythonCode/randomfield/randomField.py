#Randomized Field Creator
import numpy as np
from plotting import plot_part_save
#distance function
def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)
#Function defining borders:CCheck if particle is in boundaries
def box(xmin,xmax,ymin,ymax,xpart,ypart,radius):
    if (xpart+radius>xmax)or(xpart-radius<xmin)or(ypart+radius>ymax)or(ypart-radius<ymin):
        return False #Particle not in domain
    else:
        return True

#Collision function
def place_particle(particles,xmin,xmax,ymin,ymax):
    collide = False
    xp_possible = np.random.uniform(xmin,xmax)
    xv_possible = np.random.uniform(-1,1)
    yp_possible = np.random.uniform(ymin,ymax)
    yv_possible = np.random.uniform(-1,1)
    radius_possible = np.random.uniform(1,1)
    #Check that particle is fully contained within domain
    if box(xmin,xmax,ymin,ymax,xp_possible,yp_possible,radius_possible) == False:
        return place_particle(particles,xmin,xmax,ymin,ymax) #If not fully in try again
    for i in range(len(particles)):
        distance_parts = distance(xp_possible,yp_possible,particles[i].xp,particles[i].yp)
        rad_plus = radius_possible+particles[i].rad
        if (distance_parts<=rad_plus):
            collide = True #collision occurs
            break #get out of for loop
    #Now lets take a recurse in case collide is True
    if (collide==True):
        return place_particle(particles,xmin,xmax,ymin,ymax)
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
        self.rad = 0# particle radius
        self.m = 0 # mass
    def randomize(self,particles,xmin,xmax,ymin,ymax):
        [xp_p,xv_p,yp_p,yv_p,radius_p] = place_particle(particles,xmin,xmax,ymin,ymax)
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
        self.rad = 0.1
        self.m = 1


#Create particle
def create_map(x_min,x_max,y_min,y_max,num_particles):
    particles = []
    particle_0 = particle()
    particle_0.randomize(particles,x_min,x_max,y_min,y_max)
    particles.append(particle_0)
    for i in range(num_particles-1):
        new_particle = particle()
        new_particle.randomize(particles,x_min,x_max,y_min,y_max)
        particles.append(new_particle)
    #plot_part_save(particles,'example_RFP')
    return particles

def square_lattice(x_min,x_max,y_min,y_max,num_particles):
    particles = []
    x = np.arange(x_min,x_max+1)
    y = np.arange(y_min,y_max+1)

    for i in range(x_max+1):
        for j in range(y_max+1):
            new_particle = particle()
            new_particle.assign(x[i],0,y[j],0)
            particles.append(new_particle)
    return particles
