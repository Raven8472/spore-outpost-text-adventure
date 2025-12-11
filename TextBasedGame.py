# TextBasedGame.py
# Author: Dakota Leahy
# IT-140 Project Two - Text-Based Adventure Game "Spore Lab"


# ANSI color codes for green output
GREEN = "\033[92m"
RESET = "\033[0m"

# Make all prints gren automatically
import builtins
old_print = print

def print(*args, **kwargs):
    old_print(GREEN, end="")
    old_print(*args, **kwargs)
    old_print(RESET, end="")


def show_instructions():
    """Display the game title and basic instructions."""
    print("========================================")
    print("  SPORE OUTPOST: DATA RECOVERY PROTOCOL ")
    print("========================================")
    print("You are the last investigator at a remote research outpost.")
    print("Collect all 4 data pads and 2 critical peices of equipment before")
    print("encountering the spore organism in the lower cavern.\n")
    print("Move commands: go North, go South, go East, go West")
    print("Item commands: get <item name>")
    print("Type 'quit' to exit the game.\n")


def show_status(current_room, inventory, rooms):
    """
    Show the player's current status:
    - Current room
    - Inventory contents
    - Visible item in the room, if any
    """
    print("\n------------------------------")
    print(f"You are in: {current_room}")
    print(f"Inventory: {inventory}")

    # If the room has an item, show it
    room_data = rooms.get(current_room, {})
    item = room_data.get('item')

    if item:
        print(f"You see: {item}")
    else:
        print("You do not see any items here.")

    #Show tex craeture near by
    print("------------------------------")
        # Room-specific atmospheric flavor text
    if current_room == "Armory":
        print("A narrow tunnel cuts into the wall to the South. You hear an eerie sound echoing from below.")

    if current_room == "Storage Room":
        print("A jagged opening leads East into darkness. Something shifts beyond the tunnel.")



def main():
    """Main function containing the game loop and logic."""

    # Dictionary of rooms, their connections, and items
    rooms = {
    'Command Center': {
        'East': 'Laboratory'
    },

    'Communications Hub': {
        'South': 'Laboratory',
        'item': 'Data Pad 4'
    },

    'Laboratory': {
        'North': 'Communications Hub',
        'East': 'Medical Bay',
        'South': 'Crew Quarters',
        'West': 'Crew Command Center',
        'item': 'Data Pad 1'
    },

    'Crew Quarters': {
        'North': 'Laboratory',
        'South': 'Storage Room',
        'item': 'Data Pad 2'
    },

    'Storage Room': {
        'North': 'Crew Quarters',
        'East': 'Subterranean Cavern',
        'item': 'Data Pad 3'
    },

    'Medical Bay': {
        'West': 'Laboratory',
        'South': 'Armory',
        'item': 'Inoculation'
    },

    'Armory': {
        'North': 'Medical Bay',
        'South': 'Subterranean Cavern',
        'item': 'Photo Rifle'
    },

    'Subterranean Cavern': {
        'North': 'Armory',
        'West': 'Storage Room',
        'item': 'Spore'
    }
}


    # Game setup
    current_room = 'Command Center'
    inventory = []

    villain_room = 'Subterranean Cavern'
    # Number of items required to win (all data pads + inoculation + rifle)
    required_items_count = 6

    show_instructions()

    # Main game loop
    while True:
        # Check win/lose state when entering a room
        if current_room == villain_room:
            if len(inventory) == required_items_count:
                # Win condition text (your custom flavor)
                print("\nThe spore floats above the air as you fire the Photo Rifle.")
                print("Good work! You have saved the project, and the investors")
                print("will provide 5 more years of research funding based on the")
                print("information you recovered from the data pads.")
                print("Mission successful. Thanks for playing!")
            else:
                # Lose condition (serious sci-fi horror tone)
                print("\nThe spores overwhelm your senses. Your vision blurs")
                print("as the organism envelops you in the darkness of the cavern.")
                print("Mission failed. The outpost falls silent once more.")
                print("GAME OVER.")
            break  # End the game loop after win or loss

        # Show current status
        show_status(current_room, inventory, rooms)

        # Get player input
        user_input = input("Enter your move: ").strip()

        # Allow the player to quit
        if user_input.lower() == 'quit':
            print("Exiting the mission. See you next time.")
            break

        # Validate non-empty input
        if not user_input:
            print("Invalid command. Please enter a move or item command.")
            continue

        # Parse command and arguments
        parts = user_input.split()
        command = parts[0].lower()

        # Handle movement commands
        if command == 'go':
            if len(parts) < 2:
                print("Please specify a direction (North, South, East, West).")
                continue

            direction = parts[1].capitalize()  # Match the room dict keys

            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
            else:
                print("You can't go that way from here.")

        # Handle itm pickup
        elif command == 'get':
            if len(parts) < 2:
                print("Please specify the item you want to get.")
                continue

            # Rebuild the item name from the remaining words
            requested_item = " ".join(parts[1:])
            room_item = rooms[current_room].get('item')

            # Check if the room has that item and it matchs (case-insensitive)
            if room_item and requested_item.lower() == room_item.lower():
                # Add item to inventory and remove it from the room
                inventory.append(room_item)
                del rooms[current_room]['item']

                # Item pickup flavor
                print(f"You picked up {room_item}.")
                print(f"{room_item} secured. Upload status to Command Center archives pending.")
            else:
                print("You can't pick up that item here.")

        else:
            # Any other input is invalid
            print("Invalid command. Use 'go <direction>' or 'get <item name>'.")


# Standard call main()
if __name__ == "__main__":
    main()
