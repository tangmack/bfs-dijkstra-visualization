import numpy as np
import cv2
import generate_map
from collections import deque


world_map = generate_map.create_map()

# world_viz = world_map.copy() # visualization of world

# cv2.imshow("world_map", world_map)
# cv2.waitKey(0)


# action_set = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
action_set = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
action_set = list(map(lambda x: np.array(x), action_set))

robot_start = np.array([30,30])
goal_position = np.array([46,213])
world_map[goal_position[0],goal_position[1]] = 200

world_viz = cv2.cvtColor(world_map, cv2.COLOR_GRAY2BGR)


q = deque()
q.append(tuple(robot_start))
past_nodes = set()
child_parent_dict = {}  # keys are children, values are parents

goal_found = False

max_row_index = world_map.shape[0] - 1
max_col_index = world_map.shape[1] - 1

while(len(q) > 0):
    if goal_found:
        break

    world_viz[q[0]] = (0,0,255)
    cv2.imshow("world_viz",world_viz)
    cv2.waitKey(1)
    for action in action_set:
        current_position = tuple(np.array(q[0]) + action)
        if current_position[0]>0 and  current_position[0]<max_row_index and current_position[1]>0 and current_position[1]<max_col_index > 0: # must be within map
            if (current_position not in past_nodes):
                if world_map[current_position] == 0:
                    # print("free space found")
                    q.append(current_position)
                    past_nodes.add(current_position)
                    child_parent_dict[current_position] = q[0] # current position is child (key), q[0] is parent
                elif world_map[tuple(current_position)] == 255:
                    past_nodes.add(current_position)
                elif world_map[tuple(current_position)] == 200:
                    goal_found = True
                    past_nodes.add(current_position)
                    child_parent_dict[current_position] = q[0] # current position is child (key), q[0] is parent
                    break

    # past_nodes.add(q[0])
    # world_viz[q[0]] = (0,0,0)
    q.popleft()

# Show solution path
node = current_position
start_reached = False
while(start_reached == False):
    node = child_parent_dict[node]
    world_viz[node] = (0,255,0)

    if node == tuple(robot_start):
        start_reached = True

cv2.imshow("world_viz", world_viz)
cv2.waitKey(0)



pass
