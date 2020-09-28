from room import Room
from player import Player
from world import World
from stack import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Place the player into the starting room
player = Player(world.starting_room)

# Put starting room in to current room
current_room = world.starting_room

# Set to store visited rooms
visited = set()

# Referenc dict for reverse 
back_track = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

# using stack data structure
stack = Stack()

# add current room to set()
visited.add(player.current_room.id)

# Set to store exits
visited_exits = set()

# Populate visited set with rooms
while len(visited) != len(room_graph):

    # add Current room to visited_exits set()
    visited_exits.add(current_room)

    # get current room's exits
    exits = current_room.get_exits()

    #check if room has been visited if not add to visited set()
    if current_room.id not in visited:
        visited.add(current_room.id)

    # check if current room's exits and direction not in visited_exits set()
    if "n" in exits and current_room.get_room_in_direction('n') not in visited_exits:
        # Add to stack to track moves
        stack.push('n')
        # Add to traversal_path since not visited
        traversal_path.append('n')
        # reassign current room
        current_room = current_room.get_room_in_direction("n")

    elif "s" in exits and current_room.get_room_in_direction("s") not in visited_exits:
        stack.push("s")
        traversal_path.append("s")
        current_room = current_room.get_room_in_direction("s")

    elif "e" in exits and current_room.get_room_in_direction("e") not in visited_exits:
        stack.push("e")
        traversal_path.append("e")
        current_room = current_room.get_room_in_direction("e")

    elif "w" in exits and current_room.get_room_in_direction("w") not in visited_exits:
        stack.push("w")
        traversal_path.append("w")
        current_room = current_room.get_room_in_direction("w")
    
    # back_track
    else:
        # Remove last valid direction from the stack
        direction = stack.pop()
        # get the reverse direction from the back_track dic
        reverse = back_track.get(direction)
        # add the reverse direction to the traversal path
        traversal_path.append(reverse)
        # change current room to back_track path
        current_room = current_room.get_room_in_direction(reverse)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
