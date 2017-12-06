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

def disk(x_part,y_part,x_cen,y_cen,rad1,rad2):
    if (rad1<=np.sqrt(x_part**2+y_part**2)<=rad2):
        return True
    else:
        return False

#Collision function
def place_particle_box(particles,xmin,xmax,ymin,ymax,radius,count):
    collide = False
    count += 1
    xp_possible = np.random.uniform(xmin,xmax)
    xv_possible = np.random.uniform(-1,1)
    yp_possible = np.random.uniform(ymin,ymax)
    yv_possible = np.random.uniform(-1,1)
    #radius_possible = np.random.uniform(1,1)u
    radius_possible = radius;
    #Check that particle is fully contained within domain
    if box(xmin,xmax,ymin,ymax,xp_possible,yp_possible,radius_possible) == False and count<10000:
        return place_particle(particles,xmin,xmax,ymin,ymax,radius,count) #If not fully in try again
    for i in range(len(particles)):
        distance_parts = distance(xp_possible,yp_possible,particles[i].xp,particles[i].yp)
        rad_plus = radius_possible+particles[i].rad
        if (distance_parts<=rad_plus):
            collide = True #collision occurs
            break #get out of for loop
    #Now lets take a recurse in case collide is True
    if (collide==True) and (count<10000):
        return place_particle(particles,xmin,xmax,ymin,ymax,radius,count)
    elif (count > 10000):
        print("Recursion Depth set by Carter Rhea Reached")
    else:
        pass
    return [xp_possible,xv_possible,yp_possible,yv_possible,radius_possible]



def place_particle_disk(particles,rad1,rad2,radius,count):
    collide = False
    count += 1
    xp_possible = np.random.uniform(-1,1)
    xv_possible = np.random.uniform(-1,1)
    yp_possible = np.random.uniform(-1,1)
    yv_possible = np.random.uniform(-1,1)
    #radius_possible = np.random.uniform(1,1)u
    radius_possible = radius;
    #Check that particle is fully contained within domain
    if disk(xp_possible,yp_possible,0.0,0.0,rad1,rad2) == False and count<10000:
        return place_particle_disk(particles,rad1,rad2,radius,count) #If not fully in try again
    else:
        pass #Particle in domain of interest
    for i in range(len(particles)):
        distance_parts = distance(xp_possible,yp_possible,particles[i].xp,particles[i].yp)
        rad_plus = radius_possible+particles[i].rad
        if (distance_parts<=rad_plus):
            collide = True #collision occurs
            break #get out of for loop
    #Now lets take a recurse in case collide is True
    if (collide==True) and (count<10000):
        return place_particle_disk(particles,rad1,rad2,radius,count)
    elif (count > 10000):
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
        self.rad = 0.0005# particle radius
        self.m = 0 # mass
    def randomize(self,particles,xmin,xmax,ymin,ymax,radius,count):
        [xp_p,xv_p,yp_p,yv_p,radius_p] = place_particle(particles,xmin,xmax,ymin,ymax,radius,count)
        self.xp = xp_p
        self.xv = xv_p
        self.yp = yp_p
        self.yv = yv_p
        self.rad = radius_p
        self.m = np.random.uniform(0,1)
    def randomize_circ(self,particles,rad1,rad2,radius,count):
        [xp_p,xv_p,yp_p,yv_p,radius_p] = place_particle_disk(particles,rad1,rad2,radius,count)
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
        self.rad = 0.0005
        self.m = 1


#Create particle
def create_map_box(x_min,x_max,y_min,y_max,num_particles):
    particles = []
    count = 0
    particle_0 = particle()
    particle_0.randomize(particles,x_min,x_max,y_min,y_max,particle_0.rad,count)
    particles.append(particle_0)
    for i in range(num_particles-1):
        count = 0;
        new_particle = particle()
        new_particle.randomize(particles,x_min,x_max,y_min,y_max,new_particle.rad,count)
        particles.append(new_particle)
    plot_part_save(particles,'example_RPF')
    return particles

def create_map_circle(rad1,rad2,num_particles):
    particles = []
    count = 0
    particle_0 = particle()
    particle_0.randomize_circ(particles,rad1,rad2,particle_0.rad,count)
    particles.append(particle_0)
    for i in range(num_particles-1):
        count = 0;
        new_particle = particle()
        new_particle.randomize_circ(particles,rad1,rad2,new_particle.rad,count)
        particles.append(new_particle)
    plot_part_save(particles,'example_RPF')
    return particles



def main():
    #particlesList = create_map(-0.5,0.5,-0.5,0.5,2000)
    particlesList = create_map_circle(0.05,1.0,10000)
    output = open('output.csv','w')
    outputtxt = open('output.txt','w')
    output.write('X , Y'+'\n')
    for i in range(10000):
        output.write(str(particlesList[i].xp)+","+str(particlesList[i].yp)+'\n')
        outputtxt.write(str(particlesList[i].xp)+ " " + str(particlesList[i].yp)+'\n')



main()
