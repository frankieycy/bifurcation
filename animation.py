import numpy as np
import matplotlib.pyplot as plt
import os, glob, imageio, re
from breedModel import *
from matplotlib import rc
rc('text', usetex=True)

rStart = 1.5
rEnd = 3.0
rStep = 0.001
retain = 1000

# generate fixed point data
myBins = np.arange(rStart,rEnd,rStep)
myModel = breedModel(F,0.1,myBins,10000)
myModel.evolve()
myModel.printLastPopulations(retain)

# load fixed point data
data = np.loadtxt('breedModel.txt')
adjParams = data[:,0]
stablePoints = data[:,1]

# plot branching diagram
fig = plt.figure()
plt.ylim(0,2.5)
plt.scatter(adjParams,stablePoints,s=.001,c='k')
plt.title('Branching diagram')
plt.xlabel('adjustment parameter $r$')
plt.ylabel('stable points $X^*$')
fig.tight_layout()
fig.savefig('branching.png',dpi=500)

# set up plt folder for collecting plots
plotLocation = './plt'
if not os.path.isdir(plotLocation):
    os.mkdir(plotLocation)
oldPlots = glob.glob(os.path.join(plotLocation,'*.png'))
for f in oldPlots:
    os.remove(f)

# animation parameters
rStartAni = 1.8
rEndAni = 2.68
rStepAni = 0.02
plotBins = np.arange(rStartAni,rEndAni,rStepAni)

# for each r, plot branching diagram
fig = plt.figure()
plt.xlim(rStartAni,rEndAni)
plt.ylim(0,2.5)
plt.title('Branching diagram')
plt.xlabel('adjustment parameter $r$')
plt.ylabel('stable points $X^*$')
fig.tight_layout()

count = 0
prevParam = rStartAni
for adjParam in plotBins:
    prevIdx = int((prevParam-rStart)/rStep)*retain+retain
    idx = int((adjParam-rStart)/rStep)*retain+retain
    prevParam = adjParam
    plt.scatter(adjParams[prevIdx:idx],stablePoints[prevIdx:idx],s=.001,c='k')
    fig.savefig('plt/branching_'+str(count).rjust(2,'0')+'.png',dpi=300)
    count += 1

# for each r, plot population
count = 0
for adjParam in plotBins:
    fig = plt.figure()
    plt.xticks([])
    plt.ylim(0,2.5)
    plt.title('Seasonal population: $r={:.2f}$'.format(adjParam))
    plt.xlabel('time $t$')
    plt.ylabel('population $X_t$')
    idx = int((adjParam-rStart)/rStep)*retain+retain
    plt.scatter(np.arange(retain),stablePoints[idx:(idx+retain)],s=.1,c='k')
    fig.tight_layout()
    fig.savefig('plt/population_'+str(count).rjust(2,'0')+'.png',dpi=300)
    count += 1
    plt.close()

# for each r, plot F,F2,F4
count = 0
x = np.linspace(0,2.5,200)
for adjParam in plotBins:
    fig = plt.figure()
    plt.xlim(0,2.5)
    plt.ylim(0,2)
    plt.plot(x,F(adjParam,x),'k',label='$F$')
    plt.plot(x,F(adjParam,F(adjParam,x)),'g--',label='$F^{(2)}$')
    plt.plot(x,F(adjParam,F(adjParam,F(adjParam,F(adjParam,x)))),'b--',label='$F^{(4)}$')
    plt.plot(x,x,'r',label='$45^\circ$ line')
    idx = int((adjParam-rStart)/rStep)*retain+retain
    plt.scatter(stablePoints[idx:(idx+retain)],[0]*retain,s=25,c='r')
    plt.scatter(stablePoints[idx:(idx+retain)],stablePoints[idx:(idx+retain)],s=25,c='r')
    plt.title('$F, F^{{(2)}}, F^{{(4)}}: r={:.2f}$'.format(adjParam))
    plt.xlabel('population $X_t$')
    plt.legend()
    fig.tight_layout()
    fig.savefig('plt/F_'+str(count).rjust(2,'0')+'.png',dpi=300)
    count += 1
    plt.close()

# combine plots into animations
def file_num(f):
    return int(re.split('[_ .]',f)[1])

files = glob.glob("plt/branching_*.png")
images = []
for f in sorted(files,key=file_num):
    images.append(imageio.imread(f))
imageio.mimsave('branching_ani.gif',images,duration=0.2)

files = glob.glob("plt/population_*.png")
images = []
for f in sorted(files,key=file_num):
    images.append(imageio.imread(f))
imageio.mimsave('population_ani.gif',images,duration=0.2)

files = glob.glob("plt/F_*.png")
images = []
for f in sorted(files,key=file_num):
    images.append(imageio.imread(f))
imageio.mimsave('F_ani.gif',images,duration=0.2)
