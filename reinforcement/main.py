from get_dict import get_dict
from get_R_Q import initial_R
from get_R_Q import initial_Q
from get_result import get_result
from visualization import get_start_end_point
from visualization import get_nodes_to_bbox
from visualization import get_node_id
from visualization import get_coordinate_info
from visualization import change_node_id_to_lat_lon
from visualization import visualization_route

import pandas as pd
import time
from datetime import datetime

sta_lat_lon, des_lat_lon = get_start_end_point()
G = get_nodes_to_bbox(sta_lat_lon)

data = pd.read_csv("graph.csv")
graph = get_dict(data)

A = graph["A"]
Z = graph["Z"]
weight = graph["weight"]
A_Z_dict = graph["A_Z_dict"]

data = pd.read_csv("node_lat_lon.csv", names=['vertex','x','y'])
# data = pd.read_csv("node_lat_lon.csv")

coordinate_info = get_coordinate_info(data)
start_node, destination_node = get_node_id(G, sta_lat_lon, des_lat_lon)

start = 5034061178
end = [6598411369]
R = initial_R(A,Z,weight,A_Z_dict)
Q = initial_Q(R)
#coordinate_info = initial_Coordinate(R)


alpha = 0.7 # learning rate
epsilon = 0.1 # greedy policy
n_episodes = 1000

time0 = time.time()
result = get_result(R,Q,coordinate_info,alpha,epsilon,n_episodes,start,end)
path_lat_lon = change_node_id_to_lat_lon(G, result["routes"][0])

print("time is:",time.time() - time0)
print("route:", result['routes'][0])
print(result["ends_find"])
print(result["cost"])
print(result["routes_number"])

visualization_route(path_lat_lon)



