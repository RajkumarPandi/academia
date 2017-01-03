import numpy as np
import sys
import random
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path']='/usr/bin/ffmpeg'
import matplotlib.animation as animation
from itertools import product,starmap,islice

n=100
rock = 255
paper = 0
scissors =167
vals = [rock,paper,scissors]
#grid = np.random.choice(vals,n*n,p=[0.3,0.1,0.6]).reshape(n,n)
grid = np.zeros((n,n))
g=len(grid)
for i in range(0,g):
    for j in range(0,(g/3)):
        grid[i][j]=rock
        for j in range((g/3),(g/3)*2):
            grid[i][j]=paper
            for j in range((g/3)*2,g):
                grid[i][j]=scissors

"""VonNeumann model of radius 2"""
def manhattan(grid,i,j):
    i=i+1
    j=j+1
    gridy = np.pad(grid,1,mode='wrap')
    try:
        neighbors = [gridy[i-2][j],gridy[i-1][j],gridy[i+1][j],gridy[i+2][j],gridy[i][j-1],gridy[i][j-2],gridy[i][j+1],gridy[i][j+2],gridy[i-1][j-1],gridy[i-1][j+1],gridy[i+1][j-1],gridy[i+1][j+1]]
    except IndexError:
        neighbors = [gridy[i-2][j],gridy[i-1][j],gridy[i+1][j],gridy[i-5][j],gridy[i][j-2],gridy[i][j-1],gridy[i][j+1],gridy[i][j-5],gridy[i-1][j-1],gridy[i-1][j+1],gridy[i+1][j-1],gridy[i+1][j+1]]
    return neighbors

"""VonNeumann Model of radius 1"""
def orthogonalNeighbor(grid,x,y):
    try:
        neighbors = [grid[x-1][y],grid[x+1][y],grid[x][y-1],grid[x][y+1]]
    except:
        #if x!=y:
        neighbors = [grid[x-1][y],grid[x-x][y],grid[x][y-1],grid[x][y-y]]
        #else:
            #neighbors = [grid[x-1][y],grid[x-3][y],grid[x][y-1],grid[x][y-3]]
    return neighbors

"""Moore Model radius 2"""
def moore_r2(grid,x,j):
    f_element = grid[x][j]
    nei =[]
    for i in range(x-2,x+3):
        if i==n:
            i = -i
        if i>n:
            i=-(i-2)
        try:
            neo = [grid[i][j-1],grid[i][j-2],grid[i][j],grid[i][j+1],grid[i][j+2]]
            if f_element in neo:
                neo.remove(f_element)
        except:
            neo = [grid[i][j-1],grid[i][j-2],grid[i][j],grid[i][(j+1)-j],grid[i][j-j]]
            if f_element in neo:
                neo.remove(f_element)
        nei.extend(neo)
    return nei

"""Moore Model neigborhood radius 1"""
def neigbors(a,i,j):
    if i == 0:
        if i == j:
            b = np.roll(np.roll(a,i+1,axis=0),i+1,axis=1)[:3,:3]
        else:
            i=i+1
            j=j-(j+(1*j-1))
            b = np.roll(np.roll(a, i, axis=0), j, axis=1)[:3,:3]
    else:
        #if i == j:
            #b = np.roll(np.roll(a,i+1,axis=0),i+1,axis=1)[:3,:3]
        #else:
            i=i-(i+(1*i-1))
            j=j-(j+(1*j-1))
            b = np.roll(np.roll(a, i, axis=0), j, axis=1)[:3,:3]
    g = b.flatten()
    return g

def ran_neighbors(data):
    global grid
    global n
    update_grid  = grid.copy()
    for i in range(n):
        for j in range(n):
            ######change this to enable neighborhood of your choice########
            if '-mo' in sys.argv:
                if '-1' in sys.argv:
                    neighbors = list(neigbors(grid,i,j))
		    if grid[i][j] in neighbors:
        		neighbors.remove(grid[i][j])
                if '-2' in sys.argv:
                    neighbors = moore_r2(grid,i,j)
            else:
                if '-vo' in sys.argv:
                    if '-1' in sys.argv:
                        neighbors = orthogonalNeighbor(grid,i,j)

                    if '-2' in sys.argv:
                        neighbors = manhattan(grid,i,j)
                else:
                    exit(0)
            for k in range(len(neighbors)):
                g = random.choice(neighbors)
                if (grid[i,j]==rock and g == paper) or (grid[i,j]==paper and g ==rock):
                    update_grid[i,j] = paper
                elif (grid[i,j]==rock and g == scissors) or (grid[i,j]==scissors and g ==rock):
                    update_grid[i,j] = rock
                else:
                    if(grid[i,j]==paper and g == scissors) or (grid[i,j] == scissors and g==paper):
                        update_grid[i,j] = scissors
                #else:
                    #update_grid[i,j] = grid[i,j]
    mat.set_data(update_grid)
    grid = update_grid
    return [mat]

def all_neigh(data):
    global grid
    global n
    update_grid = grid.copy()
    try:
        for i in range(n):
            for j in range(n):
                #####change this to enable neighborhood of your choice#######
                if '-mo' in sys.argv:
                    if '-1' in sys.argv:
                        neighbors = list(neigbors(grid,i,j))
 			if grid[i][j] in neighbors:
        			neighbors.remove(grid[i][j])
                    if '-2' in sys.argv:
                        neighbors = moore_r2(grid,i,j)
                else:
                  if '-vo' in sys.argv:
                      if '-1' in sys.argv:
                          neighbors = orthogonalNeighbor(grid,i,j)
                      if '-2' in sys.argv:
                          neighbors = manhattan(grid,i,j)
                  else:
                    exit(0)
                for k in range(len(neighbors)):
                    if (grid[i,j]==rock and neighbors[k]==paper) or (grid[i,j] ==paper and neighbors[k] ==rock) :
                        update_grid[i,j]=paper
                    elif (grid[i,j]==rock and neighbors[k]== scissors) or (grid[i,j] ==scissors and neighbors[k] ==rock):
                        update_grid[i,j]=rock
                    else:
                        if(grid[i,j]==paper and  neighbors[k]==scissors) or (grid[i,j] == scissors and neighbors[k] == paper):
                            update_grid[i,j]=scissors
    except:
        e = sys.exc_info()[0]
    mat.set_data(update_grid)
    grid=update_grid
    return [mat]

FFwriter = animation.FFMpegWriter()

fig,ax =plt.subplots()
mat = ax.matshow(grid)
if "-random" in sys.argv:
  ani = animation.FuncAnimation(fig,ran_neighbors,interval=10,save_count=10) 
  ani.save('random.mp4',writer=FFwriter,fps=30)
else:
  if "-all" in sys.argv:
    ani = animation.FuncAnimation(fig,all_neigh,interval=200,save_count=200)
    ani.save('all.mp4',writer=FFwriter,fps=40)
  else:
    exit(0)
    #change the function name to either random neighbors or All
plt.show()

