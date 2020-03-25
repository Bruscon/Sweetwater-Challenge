import pandas as pd
import random


trails = pd.read_excel("trails.xlsx")

nodes = []

#get list of all nodes
for index, trail in trails.iterrows():
    if trail["from"] not in nodes:
        nodes.append(trail["from"])

#enumerate node interconnections
connections = {}

for node in nodes:
    connections[node] = trails.loc[trails['from']==node].to.to_list()
    
for item in connections:
    connections[item] = list(set(connections[item])) #remove duplicates
    for i in connections[item]:
        if item not in connections[i]:
            connections[i].append(item)
            
            
best_score = 35
best_route = []
difficulty_factor = 1
iteration = 0
num_iters = 5000

while iteration < num_iters:
    
    current_node = nodes[0]
    route = ['a']
    score = 0
    trails_left = trails.copy()
    
    while True:
        
        #pick the next node
        next_node = random.choice(connections[current_node])
        route.append(next_node)
        
        #find the trail to get there
        trails_from_cnode = trails.loc[trails['from']==current_node]
        selected_trail = trails_from_cnode.loc[trails_from_cnode.to == next_node]
        
        if selected_trail.empty:
            trails_from_cnode = trails.loc[trails['from']==next_node]
            selected_trail = trails_from_cnode.loc[trails_from_cnode.to == current_node]
            
        #fix case where theres multiple trails between two nodes
        if len(selected_trail) > 1:
            selected_trail = selected_trail.sample(n=1)
        
        #remove trail from remaing trails list
        if selected_trail.index in trails_left.index.to_list():
            trails_left.drop(index=selected_trail.index,inplace=True)
        
        #increase score
        if str(selected_trail.difficulty) == 'b':
            score += float(selected_trail.distance*difficulty_factor)
        else:
            score += float(selected_trail.distance)

        #break if the challenge is complete
        if trails_left.empty and current_node == 'a':
            break
        if score > best_score:
            break
        
        current_node = next_node
        
    if score < best_score:
        best_score = score
        best_route = route
    
    iteration += 1

print(route)
print(score)