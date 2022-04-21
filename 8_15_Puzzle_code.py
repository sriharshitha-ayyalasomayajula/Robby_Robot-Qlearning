#!/usr/bin/env python
# coding: utf-8
import sys
import json
import math
import time
import collections

class PuzzleBoard:
    def __init__(self, current, goal):

        if len(current) != len(goal):
            print("Initial and Goal sizes are different:", current, goal)

        self.node_width = int(math.sqrt(len(current)))

        self.value = current
        self.goal = goal
        self.f_value = 0
        self.g_value = 0
        self.parent = None
        self.priority = 0

        if self.value == goal:
            print("goal achieved", self.value)

    def priority(self, priority):
        self.priority = priority

    def goal(self):
        return goal

    def parent(self, parent):
        self.parent = parent

    def g_value(self, g_value):
        self.g_value = g_value

    def misplacedTiles(self):
        count = 0
        for element in self.value:
            if element == 'b': continue
            if self.value[element] == self.goal[element]: continue
            count += 1
        return count

    def nextPossibleStates(self):
        current = self.value
        possible_states = []

        index_of_blank = current.index('b')


        # for left mod == 0
        if index_of_blank == 0:
            # no left move
            pass
        else:
            if index_of_blank%(self.node_width) != 0:
                left = index_of_blank - 1

                new_state = []
                for index, element in enumerate(current):
                    if index == index_of_blank:
                        new_state.append(current[left])
                        continue

                    if index == left:
                        new_state.append('b')
                        continue

                    new_state.append(element)

                possible_states.append(new_state)



        if index_of_blank == len(current) - 1:
            # no right move
            pass
        else:
            # for right: mod + 1 == 0
            if index_of_blank%(self.node_width) != (self.node_width) - 1:
                right = index_of_blank + 1

                new_state = []
                for index, element in enumerate(current):
                    if index == index_of_blank:
                        new_state.append(current[right])
                        continue

                    if index == right:
                        new_state.append('b')
                        continue

                    new_state.append(element)

                possible_states.append(new_state)


        # for top subtract width
        top = index_of_blank - (self.node_width)
        if top >= 0:
            #print("top:", top)
            new_state = []
            for index, element in enumerate(current):
                if index == index_of_blank:
                    new_state.append(current[top])
                    continue

                if index == top:
                    new_state.append('b')
                    continue

                new_state.append(element)
            possible_states.append(new_state)

        # for bottom, add with width
        bottom = index_of_blank + (self.node_width)
        if bottom <= (((self.node_width)*(self.node_width)) - 1):
            #print("bottom:", bottom)
            new_state = []
            for index, element in enumerate(current):
                if index == index_of_blank:
                    new_state.append(current[bottom])
                    continue

                if index == bottom:
                    new_state.append('b')
                    continue

                new_state.append(element)
            possible_states.append(new_state)

        return possible_states

def generate_nodes(next_states, parent):
    next_nodes = []
    for each_state in next_states:
        node = PuzzleBoard(each_state, parent.goal)
        node.value = each_state
        node.parent = parent

        next_nodes.append(node)
    return next_nodes

def list_child_nodes_with_priority(possible_nodes, heuristic_function, call):
    list_of_child_nodes = []

    for each_node in possible_nodes:
        if heuristic_function == "misplacedTiles":
            heuristic_priority = misplacedTiles(each_node.value, each_node.goal)

        elif heuristic_function == "manhattanDistance":
            heuristic_priority = manhattanDistance(each_node.value, each_node.goal, each_node.node_width)

        elif heuristic_function == "euclideanDistance":
            heuristic_priority = euclideanDistance(each_node.value, each_node.goal, each_node.node_width)
        else:
            print("ERROR - unknown heuristic attempted! for:", heuristic_function)
            sys.exit(1)

        if call == 'astar':
            # update g_value of child
            each_node.g_value = each_node.parent.g_value + 1

            # update priority of child
            each_node.priority = heuristic_priority + each_node.g_value
        elif call == 'bfs':
            each_node.priority = heuristic_priority


        list_of_child_nodes.append(each_node)

    return list_of_child_nodes

def misplacedTiles(current, goal):
    count = 0
    for element in current:
        if element == 'b': continue
        if current[element] == goal[element]: continue
        count += 1
    return count

def manhattanDistance(current, goal, node_width):
    manhattan_distance = 0
    abs_distance = 0
    for element in current:
        if element == 'b': continue

        current_index = current.index(element)
        goal_index = goal.index(element)

        if (current_index == goal_index): continue

        distance = 0
        abs_x = abs(current_index%(node_width) - goal_index%(node_width))
        abs_y = abs(current_index//(node_width) - goal_index//(node_width))
        distance = abs_x + abs_y

        #print("el:", element, ":", distance)
        manhattan_distance += distance
    return manhattan_distance

def euclideanDistance(current, goal, node_width):
    print("euclideanDistance current:", current)
    print("euclideanDistance goal:", goal)

    euclidean_distance = 0

    for element in current:
        #print("element:", element)
        if element == 'b': continue

        current_index = current.index(element)
        goal_index = goal.index(element)
        #print("found:", current_index, goal_index)

        if (current_index == goal_index):
            #print("skipped:", current_index, goal_index)
            continue

        distance = 0
        abs_x = abs(current_index%(node_width) - goal_index%(node_width))
        abs_y = abs(current_index//(node_width) - goal_index//(node_width))
        distance = math.sqrt(abs_x*abs_x + abs_y*abs_y)

        #print("dist:", distance, "x,y", abs_x, ",", abs_y)
        euclidean_distance += distance
    print("euclidean_distance calculated as:", euclidean_distance)

    return euclidean_distance

def generate_path(node):
    count = 0
    #path = collections.deque()
    while node:
        count = count + 1
        #path.appendleft(path,node.value)
        print(node.value)
        node = node.parent
    print("steps: ", count)

def get_highest_priority_node(queue):
    # which is the node with the smallest value for priority
    highest_priority = float('inf')
    highest_priority_node = None

    for node in queue:
        if node.priority < highest_priority:
            highest_priority = node.priority
            highest_priority_node = node
    #print("highest_priority_node", highest_priority_node)
    return highest_priority_node

def bfs(current, heuristic):
    visited = []
    queue = [current]

    while(queue):
        current_node = get_highest_priority_node(queue)
        #print("queue:", queue)
        #print("current_node", current_node)
        queue.remove(current_node)

        if current_node.value in visited: continue
        visited.append(current_node.value)

        #print("current_node:", current_node.value)
        if current_node.value == current_node.goal:
            print("path reached current_node:", current_node.value)
            return current_node

        priority_queue = dict()
        heuristic_priority_set = set()

        next_states = current_node.nextPossibleStates()
        next_state_nodes = generate_nodes(next_states, current_node)

        if heuristic == "misplacedTiles":
            child_nodes_with_priority = list_child_nodes_with_priority(next_state_nodes, "misplacedTiles", "bfs")
        elif heuristic == "manhattanDistance":
            child_nodes_with_priority = list_child_nodes_with_priority(next_state_nodes, "manhattanDistance", "bfs")
        elif heuristic == "euclideanDistance":
            child_nodes_with_priority = list_child_nodes_with_priority(next_state_nodes, "euclideanDistance", "bfs")
        else:
            print("ERROR - unknown heuristic")
            sys.exit(1)


        for each_node in child_nodes_with_priority:
            queue.append(each_node)

    print("no path found")

def astar(current, heuristic):
    visited = []
    queue = [current]

    while(queue):
        current_node = get_highest_priority_node(queue)
        #print("queue:", queue)
        #print("current_node", current_node)
        queue.remove(current_node)

        if current_node.value in visited: continue
        visited.append(current_node.value)

        #print("current_node:", current_node.value)
        if current_node.value == current_node.goal:
            print("path reached current_node:", current_node.value)
            return current_node

        priority_queue = dict()
        heuristic_priority_set = set()

        next_states = current_node.nextPossibleStates()
        next_state_nodes = generate_nodes(next_states, current_node)

        if heuristic == "misplacedTiles":
            child_nodes_with_priority = list_child_nodes_with_priority(next_state_nodes, "misplacedTiles", "astar")
        elif heuristic == "manhattanDistance":
            child_nodes_with_priority = list_child_nodes_with_priority(next_state_nodes, "manhattanDistance", "astar")
        elif heuristic == "euclideanDistance":
            child_nodes_with_priority = list_child_nodes_with_priority(next_state_nodes, "euclideanDistance", "astar")
        else:
            print("ERROR - unknown heuristic")
            sys.exit(1)


        for each_node in child_nodes_with_priority:
            queue.append(each_node)

    print("no path found")

#Input for 8 puzzle
input = [8,1,3,4,'b',2,7,6,5 ]

# Input for 15 puzzle
# input = [1,2,3,'b',5,6,8,4,9,10,7,11,13,14,15,12]

print("input:", input)

#Goal state
goal = [1,2,3,4,5,6,7,8,'b']
print("goal:", goal)

current_board = PuzzleBoard(input, goal)
heuristic = "manhattanDistance"
heuristic = "euclideanDistance"
heuristic = "misplacedTiles"
print(heuristic)
print("BFS")
result_node = bfs(current_board, heuristic)
generate_path(result_node)
print()
print("ASTAR")
result_node_a = astar(current_board, heuristic)
generate_path(result_node_a)
