from room import Room
from player import Player
import sys

# Declare all the rooms


room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}

# Link rooms together


class NoRoomThatDirection(Exception):
    pass


def change_rooms(move):
    try:
        attr = move+"_to"

        if getattr(player.room, attr, 'error') == 'error':
            raise NoRoomThatDirection

        player.room = getattr(player.room, attr)

    except NoRoomThatDirection:
        print("There's nowhere to go in that direction, try another direction.")


room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.


print("Please enter name")
name = input()
player = Player(name, room['outside'])
print(player.room.description)

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.


while(True):
    movement = False

    print(player.room.name)
    player.room.print_description()
    player.print_items()

    print('What would you like to do?')
    move = input().lower()


    if move.split(' ')[0] == 'grab':
        item = move[4:]
        if item in player.room.items:
            player.items.append(item)
            player.room.items.remove(item)
            print(f'You have picked up the {item}.')
            movement = True

    elif move.split(' ')[0] == 'drop':
        item = move[5:]
        if item in player.items:
            player.room.items.append(item)
            player.items.remove(item)
            movement = True
            print(f'You have dropped the {item}.')
        else:
            print('You have no items to drop')

    # defining remaining valid moves
    directions = ['n', 's', 'e', 'w']

    # if player entered a direction, move to the room in that direction
    if move in directions:
        change_rooms(move)
        movement = True

    if move == 'q':
        print('Thanks for playing!')
        sys.exit()

    if movement == False:
        print("Not Valid move")
