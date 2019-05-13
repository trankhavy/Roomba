from classes import SetUp, Roomba
from visualize import visualize
import numpy as np
import matplotlib.pyplot as plt
# Coverage
coverage_rw = []
coverage_ga = []
coverage_gd = []

repeat_rw = []
repeat_ga = []
repeat_gd = []

dist_rw = []
dist_ga = []
dist_gd = []


def single_step(r,strategy):
    step = r.step(strategy)[0]
    x = step[0]
    y = step[1]
    r.move_to(x,y)
    return r.calculate_coverage()

for i in range(100):
    print(i)
    temp_rw = []
    temp_ga = []
    temp_gd = []
    room = SetUp()
    room.create_obstacle()
    rw = Roomba(room)
    ga = Roomba(room)
    gd = Roomba(room)
    for i in range(100):
        temp_rw.append(single_step(rw,'random_walk'))
        temp_ga.append(single_step(ga,'genetic_algorithm'))
        temp_gd.append(single_step(gd,'greedy_algorithm'))

    coverage_rw.append(temp_rw)
    coverage_ga.append(temp_ga)
    coverage_gd.append(temp_gd)

    repeat_rw.append(rw.repeated_cell)
    repeat_ga.append(ga.repeated_cell)
    repeat_gd.append(gd.repeated_cell)

    dist_rw.append(rw.dist_travelled)
    dist_ga.append(ga.dist_travelled)
    dist_gd.append(gd.dist_travelled)

coverage_rw = np.array(coverage_rw)
coverage_ga = np.array(coverage_ga)
coverage_gd = np.array(coverage_gd)

repeat_rw = np.array(repeat_rw)
repeat_ga = np.array(repeat_ga)
repeat_gd = np.array(repeat_gd)

dist_rw = np.array(dist_rw)
dist_ga = np.array(dist_ga)
dist_gd = np.array(dist_gd)

x = np.arange(100)

y_rw = np.mean(coverage_rw,axis=0).flatten()
y_rw_25 = np.percentile(coverage_rw,25,axis=0).flatten()
y_rw_75 = np.percentile(coverage_rw,75,axis=0).flatten()

y_ga = np.mean(coverage_ga,axis=0).flatten()
y_ga_25 = np.percentile(coverage_ga,25,axis=0).flatten()
y_ga_75 = np.percentile(coverage_ga,75,axis=0).flatten()

y_gd = np.mean(coverage_gd,axis=0).flatten()
y_gd_25 = np.percentile(coverage_gd,25,axis=0).flatten()
y_gd_75 = np.percentile(coverage_gd,75,axis=0).flatten()


plt.plot(x,y_rw,color='purple',label='Random walk')
plt.fill_between(x,y_rw_25,y_rw_75,color='purple',alpha=0.1)

plt.plot(x,y_ga,color='blue',label='Genetic algorithm')
plt.fill_between(x,y_ga_25,y_ga_75,color='blue',alpha=0.1)

plt.plot(x,y_gd,color='red',label='Greedy algorithm')
plt.fill_between(x,y_gd_25,y_gd_75,color='red',alpha=0.1)

plt.xlabel("Step")
plt.ylabel("Coverage percentage (%)")
plt.title("Coverage percentage by different algorithms")
plt.legend()
plt.show()
plt.clf()

# Repeated cell distribution
plt.hist(repeat_rw,histtype='bar',color='purple',rwidth=0.8,alpha=0.6)
plt.axvline(repeat_rw.mean(), color='k', linestyle='dashed', linewidth=1)
plt.suptitle("Repeated cells distribution for random walk")
string = "25% and 75% range: [{0},{1}]".format(np.percentile(repeat_rw,25),np.percentile(repeat_rw,75))
plt.title(string)
plt.show()
plt.clf()

plt.hist(repeat_ga,histtype='bar',color='blue',rwidth=0.8,alpha=0.6)
plt.axvline(repeat_ga.mean(), color='k', linestyle='dashed', linewidth=1)
plt.suptitle("Repeated cells distribution for genetic algorithm")
string = "25% and 75% range: [{0},{1}]".format(np.percentile(repeat_ga,25),np.percentile(repeat_ga,75))
plt.title(string)
plt.show()
plt.clf()

plt.hist(repeat_gd,histtype='bar',color='red',rwidth=0.8,alpha=0.6)
plt.axvline(repeat_gd.mean(), color='k', linestyle='dashed', linewidth=1)
plt.suptitle("Repeated cells distribution for greedy algorithm")
string = "25% and 75% range: [{0},{1}]".format(np.percentile(repeat_gd,25),np.percentile(repeat_gd,75))
plt.title(string)
plt.show()
plt.clf()

# Distance travelled distribution
plt.hist(dist_rw,histtype='bar',color='purple',rwidth=0.8,alpha=0.6)
plt.axvline(dist_rw.mean(), color='k', linestyle='dashed', linewidth=1)
plt.suptitle("Distance travelled distribution for random walk")
string = "25% and 75% range: [{0},{1}]".format(round(np.percentile(dist_rw,25),2),round(np.percentile(dist_rw,75),2))
plt.title(string)
plt.show()
plt.clf()

plt.hist(dist_ga,histtype='bar',color='blue',rwidth=0.8,alpha=0.6)
plt.title("Distance travelled distribution for genetic algorithm")
plt.show()
plt.clf()

plt.hist(dist_gd,histtype='bar',color='red',rwidth=0.8,alpha=0.6)
plt.title("Distance travelled distribution for greedy algorithm")
plt.show()
plt.clf()
