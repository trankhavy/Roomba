import visualize
from classes import SetUp, Roomba
from visualize import visualize

room = SetUp()
room.create_obstacle(seed=0)


rw = Roomba(room)
visualize(rw,'random_walk')
