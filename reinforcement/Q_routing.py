from get_all_routes import get_best_nodes
from get_all_routes import get_best_net
from get_all_routes import get_all_best_routes
from get_all_routes import get_cost
from get_all_routes import count_routes
from collections import Counter

import numpy as np
import copy
import random
import math

def update_Q(T,Q,coordinate_info,prior_state, current_state, next_state, alpha):
    current_t = T[current_state][next_state]
    current_q = Q[current_state][next_state]
    print('Prior Vertex:', prior_state)
    print('Current Vertex:', current_state)
    print('Next Vertex:', next_state)
    theta = 0
    if prior_state != None:
        a = np.array([coordinate_info[prior_state]['x'],coordinate_info[prior_state]['y']])
        b = np.array([coordinate_info[current_state]['x'],coordinate_info[current_state]['y']])
        c = np.array([coordinate_info[next_state]['x'],coordinate_info[next_state]['y']])
        
        # create vectors
        ba = a - b
        bc = c - b

        # calculate angle
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        if cosine_angle > 1:
            cosine_angle = 1
        elif cosine_angle < -1:
            cosine_angle = -1
        angle = np.arccos(cosine_angle)
        theta = round(np.degrees(angle),5)
        theta = abs(180-abs(theta))
        print('theta:', theta)

        theta = abs(theta)/20
    
    new_q = (1-alpha) * current_q + alpha * ((current_t+theta) + min(Q[next_state].values()))
    print('')
    Q[current_state][next_state] = new_q   
    return Q


def get_min_state(dic,valid_moves):
    """input dic is like {3: -0.5, 10: -0.1}
    valid_moves is like [1,3,5]"""
    new_dict = dict((k, dic[k]) for k in valid_moves)
    return min(new_dict, key=new_dict.get)


def get_route(Q,start,end):
    """ input is  Q-table is like:{1: {2: 0.5, 3: 3.8},
                                   2: {1: 5.9, 5: 10}} """   
    single_route = [start]
    while single_route[-1] not in end:
        next_step = min(Q[single_route[-1]],key=Q[single_route[-1]].get)
        single_route.append(next_step)
        if len(single_route) > 2 and single_route[-1] in single_route[:-1]:
            break
    return single_route

def get_key_of_min_value(dic):
        min_val = min(dic.values())
        print(min_val)
        print([k for k, v in dic.items() if v == min_val])
        return [k for k, v in dic.items() if v == min_val]

def Q_routing(T,Q,coordinate_info,alpha,epsilon,n_episodes,start,end):
    nodes_number = [0,0]
    for e in range(n_episodes):
        current_state = start
        goal = False
        prior_state = None
        print('================= ' + str(e) + ' =================')
        while not goal:
            valid_moves = list(Q[current_state].keys())
            
            if len(valid_moves) <= 1:
                next_state = valid_moves[0]
            else:
                best_action = random.choice(get_key_of_min_value(Q[current_state]))
                if random.random() < epsilon:
                    valid_moves.pop(valid_moves.index(best_action))
                    next_state = random.choice(valid_moves)
                else:
                    next_state = best_action
            
            Q = update_Q(T,Q,coordinate_info,prior_state, current_state, next_state, alpha)
            prior_state = current_state
            if next_state in end:
                goal = True
            current_state = next_state
            #current_route.append(next_state)
        #print "current:",current_route   
        #print get_route(Q,start,end)
        # check stop standard
        # if e in range(0,1000,200):
        #     for i in Q.keys():
        #         for  j in Q[i].keys():
        #             Q[i][j]  = round(Q[i][j],6)
        #     nodes = get_best_nodes(Q,start,end)
        #     nodes_number.append(len(nodes))
        #     print("nodes:",nodes_number)
        #     if len(set(nodes_number[-3:])) == 1:
        #         break
    return Q
    