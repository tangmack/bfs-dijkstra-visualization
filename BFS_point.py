import numpy as np
import cv2
import generate_map
from collections import deque


world_map = generate_map.create_map()
max_row_index = world_map.shape[0] - 1
max_col_index = world_map.shape[1] - 1
######################################
# Collect User Input
user_input_good = False
while user_input_good != True:
    try:
        i_start_row, i_start_col = input("Enter row col index numbers of ++++START++++ here, ie. 30 30: ").split()
        i_goal_row, i_goal_col = input("Enter row col index numbers of ====GOAL==== here, ie. 165 389: ").split()

        start_row, start_col = int(i_start_row), int(i_start_col)
        goal_row, goal_col = int(i_goal_row), int(i_goal_col)
    except:
        print("Problem with input, please re-enter user input.")
        continue

    if max_row_index >= start_row >= 0 \
            and max_col_index >= start_col >= 0 \
            and max_row_index >= goal_row >= 0 \
            and max_col_index >= goal_col >= 0:
        user_input_good = True
        print("Good user input, starting...")

    else:
        print("Please correct user input, minimum is 0 0, maximum is 299 399.")

desired_start = [int(start_row),int(start_col)]
desired_goal = [int(goal_row),int(goal_col)]


# desired_start = [30,30]
# desired_start = [299,399]

# desired_goal = [46,213]
# desired_goal = [0,0]
# desired_goal = [165,389]
######################################

robot_start = np.array(desired_start)
goal_position = np.array(desired_goal)
world_map[goal_position[0],goal_position[1]] = 200

world_viz = cv2.cvtColor(world_map, cv2.COLOR_GRAY2BGR)


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('start'+'-'+ str(desired_start[0])+'-'+ str(desired_start[1])+'-'+'goal-'+str(desired_goal[0])+'-'+str(desired_goal[1])+'.mp4', 0x7634706d , 800.0, (400,300))




action_set = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
action_set = list(map(lambda x: np.array(x), action_set))




q = deque()
q.append(tuple(robot_start))
past_nodes = set()
child_parent_dict = {}  # keys are children, values are parents

goal_found = False



while(len(q) > 0):
    if goal_found:
        break

    world_viz[q[0]] = (0,0,255)
    out.write(world_viz)
    cv2.imshow("world_viz",world_viz)
    cv2.waitKey(1)
    for action in action_set:
        current_position = tuple(np.array(q[0]) + action)
        if current_position[0]>=0 and  current_position[0]<=max_row_index and current_position[1]>=0 and current_position[1]<=max_col_index >= 0: # must be within map
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

for f in range(0,200): # repeat 200 frames worth of showing the solution path at end
    cv2.imshow("world_viz", world_viz)
    out.write(world_viz)

cv2.imshow("world_viz", world_viz)
cv2.waitKey(0)



pass
