'''
Plotting Functions
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
def plot_part_save(particles,figname):
    #plot particles
    x_parts = []
    y_parts = []
    rad_parts = []
    cir_parts = []
    for i in range(len(particles)):
        ThisParticle = particles[i]
        x_parts.append(ThisParticle.xp)
        y_parts.append(ThisParticle.yp)
        rad_parts.append(ThisParticle.rad)
        cir_parts.append((np.pi*ThisParticle.rad**2))

    fig,ax = plt.subplots(1,1)
    #ax = subplot(aspect='equal')
    #circles(x_parts,y_parts,rad_parts)
    import pylab
    circles = []
    ax = pylab.axes(aspect=1) #Creates empty axes (aspect=1 means scale things so that circles look like circles)

    for i  in range(len(particles)):
        ax.add_patch(pylab.Circle((x_parts[i],y_parts[i]),radius=rad_parts[i]))
    pylab.xlim(-0.5,0.5)
    pylab.ylim(-0.5,0.5)
    #pylab.show()
    plt.savefig(figname+'.png')
def plot_part(particles):
    #plot particles
    x_parts = []
    y_parts = []
    rad_parts = []
    cir_parts = []
    import pylab
    for i in range(len(particles)):
        ThisParticle = particles[i]
        x_parts.append(ThisParticle.xp)
        y_parts.append(ThisParticle.yp)
        rad_parts.append(ThisParticle.rad)
        cir_parts.append((np.pi*ThisParticle.rad**2))


    circles = []
    ax = pylab.axes(aspect=1) #Creates empty axes (aspect=1 means scale things so that circles look like circles)
    for i  in range(len(particles)):
        ax.add_patch(pylab.Circle((x_parts[i],y_parts[i]),radius=rad_parts[i]))
    pylab.xlim(-10,10)
    pylab.ylim(-10,10)
    pylab.show()
def plot_part_save_inc(particles,figname,increment,xmin,xmax,ymin,ymax):
    #plot particles
    x_parts = []
    y_parts = []
    rad_parts = []
    cir_parts = []
    import pylab
    for i in range(len(particles)):
        ThisParticle = particles[i]
        x_parts.append(ThisParticle.xp)
        y_parts.append(ThisParticle.yp)
        rad_parts.append(ThisParticle.rad)
        cir_parts.append((np.pi*ThisParticle.rad**2))
    circles = []
    ax = pylab.axes(aspect=1) #Creates empty axes (aspect=1 means scale things so that circles look like circles)

    for i  in range(len(particles)):
        ax.add_patch(pylab.Circle((x_parts[i],y_parts[i]),radius=rad_parts[i]))
    pylab.xlim(xmin-1,xmax+1)
    pylab.ylim(ymin-1,ymax+1)
    #pylab.show()
    plt.savefig(figname+"_"+str(increment)+'.png')
