import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import math
import time

class SetUp(object):

    """
    A class to set up the room environment.

    Attributes:

    layout: An array to store the room environment. 0 is empty, 1 is cleaned, 2 is obstacle
    nx: The width of the room
    ny: The length of the room
    num_obstacle: The number of obstacles in the room (note: obstacles can have different size)

    Methods:

    create_obstacle(self,seed=None): Randomly mark some cells as obstacle, size of obstacles are random
    display(self): Display the current state of the room
    """

    def __init__(self,nx=10,ny=10,num_obstacle=10):
        """
        obstacle: number of obstacles
        """
        self.nx = nx
        self.ny = ny
        # Initialize an empty room
        self.layout = np.zeros((nx,ny))
        # Color code: white - empty uncleaned area, grey - obstacles, green - cleaned
        # Number code: 0 - empty uncleaned area, 1 - cleaned area, 2 - obstacle
        self.num_obstacle = num_obstacle



    def create_obstacle(self,seed=None):
        if seed != None:
            np.random.seed(seed)
        for obs in range(self.num_obstacle):
            # x-coordinate of the obstacle
            rx = np.random.randint(low=1,high=self.nx)
            # y-coordinate of the obstacle
            ry = np.random.randint(low=1,high=self.ny)
            # size of obstacle
            size_x = np.random.randint(low=0,high=self.nx//2)
            size_y = np.random.randint(low=0,high=self.ny//2)
            self.layout[rx:(rx+size_x)%self.nx,ry:(ry+size_y)%self.ny] = 2

    def display(self):
        fig,ax = plt.subplots(figsize=(10,10))
        ax.grid(which='major',axis='both',color='k',linewidth=2)
        ax.set_xticks(np.arange(0,self.nx+1,1))
        ax.set_xticklabels(np.arange(0,self.nx+1,1))
        ax.set_yticks(np.arange(0,self.ny+1,1))
        ax.set_yticklabels(np.arange(0,self.ny+1,1)[::-1])
        cmap = colors.ListedColormap(['white','green','grey'])
        image = ax.imshow(self.layout,vmin=0, vmax=len(cmap.colors),cmap=cmap,extent=[0, self.nx, 0, self.ny],interpolation=None)
        plt.show()


class Roomba(object):

    """
    A class for the Roomba robot

    Input: The room environment created by SetUp class

    Attributes:

    x_start, y_start: Starting place for the Roomba
    room: The input room object
    layout: A copy of the layout of the room
    sensor_range: The number of cells the robot can check from its current position
    pass_through: A mental map of all the place it has been through to avoid repeated cells
    dist_travelled: Total distance travelled by the robot so far
    repeated_cell: Total number of repeated cells

    Methods:

    step(self,strategy): Calculate the next step to move based on the input strategy
    random_step(self): Calculate the next step to move based on random walk strategy
    ga_step(self,population=50,generations=300,cross_over=0.85,mutation=0.2): Calculate
    the next step to move based on genetic algorithm with the given hyperparameters.
    Note that in this implementation we reuse the ga_step function for greedy algorithm
    by simply changing the hyperparameters.
    create_minipath(self): Create one minipath based on the robot's current position. Used
    for genetic algorithm and greedy algorithm.
    evaluate_fitness(self,minipath,A,B,C,D): Evaluate the fitness score for a given minipath (gene)
    using the fitness formula A*dist_minipath + B*free_cell + C*dist_x + D*repeated_cell. Used
    for genetic algorithm and greedy algorithm.
    check_clean(self): Check if the whole floor is cleaned. Return a boolean.
    move_to(self,x,y): Change the position of the robot and change the state of the visited cells
    calculate_coverage(self): Return the percentage of coverage so far in the simulation

    """
    def __init__(self,room,sensor_range=1):
        """
        room_setup: an array represents the set up of the room
        """
        # Choose a starting point at the corner
        self.x_start = 0
        self.y_start = 0
        self.room = room
        self.layout = np.copy(room.layout)
        self.sensor_range = sensor_range
        self.pass_through = []
        self.dist_travelled = 0
        self.repeated_cell = 0
        self.movement = 0

        while self.layout[self.x_start,self.y_start] != 0:
            self.x_start = np.random.randint(low=0,high=room.nx)
            self.y_start = np.random.randint(low=0,high=room.ny)

        self.current_x = self.x_start
        self.current_y = self.y_start
        self.move_to(self.x_start,self.y_start)

    def step(self,strategy):
        """
        Calculate the next step to move based on the input strategy
        Input:
        strategy: string. Either "random_walk", "genetic_algorithm" or "greedy_algorithm"
        Return:
        The x and y index indicating the next position the robot should go to
        """
        if strategy == 'random_walk':
            return self.random_step()
        elif strategy == 'genetic_algorithm':
            return self.ga_step()
        else:
            return self.ga_step(generations=1)

    def random_step(self):
        """
        Determine the next tile to get to using random walk strategy
        Return the coordinate of that tile.
        """
        possible_tiles = []
        for x in range(-1,2):
            for y in range(-1,2):
                if x==0 and y == 0:
                    break
                else:
                    # Check to ensure it's valid coordinate
                    if ((self.current_x+x)<self.room.nx) and ((self.current_x+x)>=0) and \
                    ((self.current_y+y)<self.room.ny) and ((self.current_y+y)>=0):
                        # If the tile is not an obstacle
                        if self.layout[self.current_x+x,self.current_y+y] != 2:
                            possible_tiles.append([self.current_x+x,self.current_y+y])
        next_tile = np.random.choice(len(possible_tiles))
        x = possible_tiles[next_tile][0]
        y = possible_tiles[next_tile][1]
        return [[x,y]]

    def ga_step(self,population=50,generations=300,cross_over=0.85,mutation=0.2):
        """
        Determine the next tile to get to using genetic algorithm
        Return the coordinate of that tile.
        """
        # Create mini paths
        gene_pool = []
        score_array = []
        # Initialize population
        for i in range(population):
            mini_path = self.create_minipath()
            score = self.evaluate_fitness(mini_path)
            gene_pool.append(mini_path)
            score_array.append(score)

        # Iterate over generations
        for i in range(generations):
            gene_pool = np.array(gene_pool)
            score_array = np.array(score_array)
            # Get the 20 best genes
            best = np.argsort(score_array)[::-1][:20]
            gene_pool = gene_pool[best]
            score_array = score_array[best]

            # Genetic operation
            for j in range(population//2):
                parent1 = np.random.randint(len(gene_pool))
                parent2 = np.random.randint(len(gene_pool))
                child1 = np.copy(gene_pool[parent1])
                child2 = np.copy(gene_pool[parent2])
                for k in range(1,self.sensor_range):
                    # Cross over
                    if np.random.rand() < cross_over:
                        # Check if it's a reasonable new path before crossing
                        if abs(gene_pool[parent2][k][0]-child1[k-1][0]) <= 1 and abs(gene_pool[parent2][k][1]-child1[k-1][1])<=1:
                            child1[k] = gene_pool[parent2][k]
                        if abs(gene_pool[parent1][k][0]-child2[k-1][0]) <= 1 and abs(gene_pool[parent1][k][1]-child2[k-1][1])<=1:
                            child2[k] = gene_pool[parent1][k]
                    # Mutation
                    if np.random.rand() < mutation:
                        # Check if it's a reasonable new path before mutate
                        if (child1[k][0]+1) < self.room.nx and (child1[k][1]-1) >= 0:
                            child1[k][0] += 1
                            child1[k][1] -= 1

                        if (child2[k][0]+1) < self.room.nx and (child2[k][1]-1) >= 0:
                            child2[k][0] += 1
                            child2[k][1] -= 1

                # Add the children to the gene pool
                gene_pool = list(gene_pool)
                gene_pool.append(child1)
                gene_pool.append(child2)
                score_array = list(score_array)
                score_array.append(self.evaluate_fitness(child1))
                score_array.append(self.evaluate_fitness(child2))
        # If the best solution is to stay where the robot is
        if score_array[0] == 0:
            # Just randomly go somewhere else, otherwise we would get stuck in a region
            path = self.create_minipath()
            return path
        return gene_pool[0]

    def create_minipath(self):
        """
        Create one minipath based on the robot's current position.
        Return a list containing the coordinates to visit sequentially
        """
        path = []
        current_x = self.current_x
        current_y = self.current_y
        for i in range(self.sensor_range):
            possible_tiles = []
            for x in range(-1,2):
                for y in range(-1,2):
                    # We do not want to include the current position in the possible tiles
                    if x!=0 or y!=0:
                        # Check to ensure it's valid coordinate
                        if ((current_x+x)<self.room.nx) and ((current_x+x)>=0) and \
                        ((current_y+y)<self.room.ny) and ((current_y+y)>=0):
                            # If the tile is not an obstacle
                            if self.layout[current_x+x,current_y+y] != 2:
                                possible_tiles.append([current_x+x,current_y+y])
            if len(possible_tiles) == 0:
                print("No possible tile to move")
                print(current_x,current_y)
                time.sleep(100000)
            next_tile = np.random.choice(len(possible_tiles))
            path.append(possible_tiles[next_tile])
            current_x = possible_tiles[next_tile][0]
            current_y = possible_tiles[next_tile][1]
        return path

    def evaluate_fitness(self,minipath,A=-30,B=50,C=-12,D=-1):
        """
        Input:
        minipath (gene): a list containing coordinates to visit sequentially

        Return:
        Fitness score based on the fitness function: A*dist_minipath + B*free_cell + C*dist_x + D*repeated_cell
        """
        dist = 0
        uncleaned_cells = 0
        #delta_dist: the distance on the x-axis between the current robot position and the unclean cell position
        delta_dist = 0
        current_x = self.current_x
        current_y = self.current_y
        pass_through = []
        repeat = 0
        for index,cell in enumerate(minipath):
            # Evaluate the distance of the minipath
            x = minipath[index][0]
            y = minipath[index][1]
            if abs(x-current_x) > 1 or abs(y-current_y) > 1:
                dist += float('inf')
            elif self.layout[x,y] == 2:
                dist += float('inf')
            else:
                # Euclidean distance
                dist += math.sqrt(((current_x-x))**2 + ((current_y-y))**2)

            # Evaluate the number of unvisited cells
            if self.layout[x,y] == 0 and (x,y) not in pass_through:
                uncleaned_cells += 1
                # Evaluate delta_dist
                delta_dist += y - current_y
            current_x = x
            current_y = y
            pass_through.append((x,y))

            repeat += self.pass_through.count((x,y))

        return (A*dist + B*uncleaned_cells + C*delta_dist + D*repeat)

    def check_clean(self):
        """
        Check if the entire floor is clean. Return a boolean
        """
        return not(np.any(self.layout==0))

    def move_to(self,x,y):
        """
        Change the robot's position and the state of the floor
        Input:
        x,y: coordinate of the cell that the robot need to move to
        """
        # Euclidean distance
        self.dist_travelled += math.sqrt(((self.current_x-x))**2 + ((self.current_y-y))**2)
        if (x,y) in self.pass_through:
            self.repeated_cell += 1
        self.layout[x,y] = 1
        self.current_x = x
        self.current_y = y
        self.pass_through.append((x,y))

    def calculate_coverage(self):
        """
        Return: The coverage percentage so far
        """
        return ((self.layout==1).sum() / ( (self.layout==0).sum() + (self.layout==1).sum() ))*100
