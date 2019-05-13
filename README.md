**Comparison of different path planning algorithms for cleaner robot**

Roomba is a robot that moves around the house to clean the floor. There are several different moving strategies for the robot, some of them are “random bounce” and “wall following”. The goal is to move around the room in the most even and efficient way as possible. In this project, we explored three different algorithms for robot path planning: naïve random walk, greedy algorithm and genetic algorithm in the context of moving around a dynamic environment without any prior knowledge. The three algorithms are compared based on three metrics: floor coverage percentage, total distance travelled and number of repeated cells.

**Files**

 - classes.py: Includes all the classes created for the simulation
 - visualize.py: Code to visualize different strategy and robot path
 - simulation.py: Conduct multiple simulations and gather statistics
 - sample_rw.py: A sample simulation for random walk strategy
 - sample_ga.py: A sample simulation for genetic algorithm
 - sample_gd.py: A sample simulation for greedy algorithm
 - run.sh: A bash script to run all three sample simulation at once
 - requirements.txt: List of dependencies
 - Simulation results: A folder contains results of the simulations run in simulation.py
 - Final Project.pdf: Report of the simulation and interpretation of the results

**To run the simulation**:

 - Step 1: Create virtual environment
 - Step 2: Install all dependencies listed in requirements.txt
 - Step 3: Run the file run.sh to see all three sample simulations. Otherwise, you can manually run through sample_rw.py, sample_ga.py, sample_gd.py for random walk strategy, genetic algorithm and greedy algorithm simulation.
