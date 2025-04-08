import os
import sys
import math
import random
import itertools
import pygame as pg
import tkinter as tk
from tkinter import messagebox
import json
import os
from collections import namedtuple

if sys.version_info[0] == 2:
    range = xrange

CAPTION = "GHOST RUNNER"
SCREEN_SIZE = (1200, 600)
CIRCLE = 2*math.pi
SCALE = (SCREEN_SIZE[0]+SCREEN_SIZE[1])/1200.0
FIELD_OF_VIEW = math.pi*0.4
NO_WALL = float("inf")
RAIN_COLOR = (255, 255, 255, 40)

# Semantically meaningful tuples for use in GameMap and Camera class.
RayInfo = namedtuple("RayInfo", ["sin", "cos"])
WallInfo = namedtuple("WallInfo", ["top", "height"])


class Image(object):
    """A very basic class that couples an image with its dimensions"""
    def __init__(self, image):
        """
        The image argument is a preloaded and converted pg.Surface object.
        """
        self.image = image
        self.width, self.height = self.image.get_size()


import time  # Import to track elapsed time if needed

import time  # Import to track elapsed time if needed

class Player:
    from tkinter import simpledialog



    def __init__(self, x, y, direction, size, inventory_limit=10):
        self.current_room = "Room 1"
        self.x = x
        self.y = y
        self.inventory = []
        self.inventory_limit = inventory_limit
        self.direction = direction
        self.speed = 1.40
        self.rotate_speed = CIRCLE / 2
        self.weapon = Image(IMAGES["knife"])
        self.paces = 0
        self.health = 100  # Player's initial health
        self.teleport_timer = 0  # Timer for teleportation delay
        self.teleport_delay = 15  # Time in seconds before teleporting
        self.collected_items = set()  # Track collected items by their positions

    def pick_up_item(self, item):
        """
        Pick up an item if inventory has space.
        :param item: The item instance to pick up.
        """
        if len(self.inventory) < self.inventory_limit:
            self.inventory.append(item)
            print(f"Picked up: {item.name}")
        else:
            print("Inventory full! Cannot pick up the item.")
    def rotate(self, angle):
        """Change the player's direction when appropriate key is pressed."""
        self.direction = (self.direction + angle + CIRCLE) % CIRCLE

    def walk(self, distance, game_map):
        """Calculate the player's next position and move if not colliding with a wall."""
        dx = math.cos(self.direction) * distance
        dy = math.sin(self.direction) * distance
        if game_map.get(self.x + dx, self.y) <= 0:
            self.x += dx
        if game_map.get(self.x, self.y + dy) <= 0:
            self.y += dy
        self.paces += distance

    def take_damage(self, damage):
        """Reduce player's health when attacked."""
        self.health = max(self.health - damage, 0)
        print(f"Player took {damage} damage. Health: {self.health}")
        if self.health == 0:
            answer = messagebox.askyesno("Game Over", "You died! Do you want to play again?")
            if answer:
                self.respawn()
            else:
                self.quit_game()  # Replace this with your quit game logic

    def respawn(self):
        """Respawn the player with default settings."""
        self.x = 0  # Set to your desired respawn x coordinate
        self.y = 0  # Set to your desired respawn y coordinate
        self.direction = 0  # Set to your desired respawn direction
        self.speed = 1.40
        self.rotate_speed = CIRCLE / 2
        self.weapon = Image(IMAGES["knife"])
        self.paces = 0
        self.health = 100  # Reset health to full

    def collect_health_item(self, amount):
        self.health += amount
        print(f"Health increased by {amount}. Current health: {self.health}")
    import tkinter as tk
    from tkinter import simpledialog

    
    import tkinter as tk




    def teleport(self, new_x, new_y, game_map):
        """Teleport the player to a new position if not colliding with a wall."""
        if game_map.get(new_x, new_y) <= 0:
            self.x = new_x
            self.y = new_y
            print(f"Teleported to ({self.x}, {self.y})")
        else:
            print(f"Cannot teleport to ({new_x}, {new_y}): Collision detected.")

    def teleport_to_mirror(self, game_map):
        """Teleport the player to the exact mirror position."""
        mirror_x, mirror_y = game_map.get_mirror_position(self.x, self.y)
        self.teleport(mirror_x, mirror_y, game_map)

    def update(self, keys, dt, game_map):
        """Execute movement and check teleportation conditions."""
        if keys[pg.K_LEFT]:
            self.rotate(-self.rotate_speed * dt)
        if keys[pg.K_RIGHT]:
            self.rotate(self.rotate_speed * dt)
        if keys[pg.K_UP]:
            self.walk(self.speed * dt, game_map)
        if keys[pg.K_DOWN]:
            self.walk(-self.speed * dt, game_map)
# Initialize a flag to track if the health item has been collected
        self.health_item_collected = False

        # Check if the player is at the health item's position and hasn't collected it yet
        item_position = (9, 9)  # Define the position of the health item
        item_position2 = (3, 3)  # Define the position of the health item

        # Check if the player is at the health item's position and it hasn't been collected yet
        if (int(self.x), int(self.y)) == item_position and item_position not in self.collected_items:
            self.collect_health_item(50)  # Increase health by 20
            self.collected_items.add(item_position)  # Mark the item as collected
            print(f"Health item collected at {item_position}")
        if (int(self.x), int(self.y)) == item_position2 and item_position2 not in self.collected_items:
            self.collect_health_item(20)  # Increase health by 20
            self.collected_items.add(item_position2)  # Mark the item as collected
            print(f"Health item collected at {item_position}")

        # Check teleportation condition
        if any(
            x1 <= int(self.x) < x2 and y1 <= int(self.y) < y2
            for (x1, y1, x2, y2) in game_map.tiny_rooms.keys()
        ):
            self.teleport_timer += dt
            if self.teleport_timer >= self.teleport_delay:
                self.teleport_to_mirror(game_map)
                self.teleport_timer = 0
        else:
            self.teleport_timer = 0

        # Debugging
        print(f"Position: ({self.x}, {self.y}), Direction: {self.direction}, Health: {self.health}")





# Example usage
# Replace with your actual size value when creating the player
size = 100  # Example size; replace it with your actual game size




class NPC(object):
    """Handles the NPC's position, rotation, basic AI, and attacking."""
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1.3
        self.attack_range = 0.5  # Distance at which NPC can attack
        self.attack_damage = 1  # Damage dealt to the player per attack
        self.attack_cooldown = .5  # Time in seconds between attacks
        self.time_since_last_attack = 0  # Tracks time since the last attack
        self.paces = 0

    def rotate(self, angle):
        """Rotate the NPC in the specified direction."""
        self.direction = (self.direction + angle + CIRCLE) % CIRCLE

    def walk(self, distance, game_map):
        """Move the NPC forward if it doesn't collide with a wall."""
        dx = math.cos(self.direction) * distance
        dy = math.sin(self.direction) * distance
        if game_map.get(self.x + dx, self.y) <= 0:
            self.x += dx
        if game_map.get(self.x, self.y + dy) <= 0:
            self.y += dy
        self.paces += distance

    def attack(self, player):
        """Attack the player if within range and cooldown has expired."""
        distance_to_player = math.hypot(player.x - self.x, player.y - self.y)
        if distance_to_player <= self.attack_range and self.time_since_last_attack <= 0:
            player.take_damage(self.attack_damage)
            self.time_since_last_attack = self.attack_cooldown

    def update(self, dt, game_map, player):
        """Basic AI for the NPC to follow and attack the player."""
        angle_to_player = math.atan2(player.y - self.y, player.x - self.x)
        self.direction = angle_to_player
        self.walk(self.speed * dt, game_map)
        
        # Update time since last attack
        if self.time_since_last_attack > 0:
            self.time_since_last_attack -= dt

        # Attempt to attack the player if in range
        self.attack(player)
        
        # Debugging
        print(f"NPC Position: ({self.x}, {self.y}), Direction: {self.direction}, Time since last attack: {self.time_since_last_attack}")


def draw_health(screen, player):
    """Draw the player's health bar on the screen."""
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = 20
    health_bar_y = 20
    health_percentage = player.health / 100
    health_color = (255, 0, 0) if player.health < 30 else (0, 255, 0)
    pg.draw.rect(screen, (128, 128, 128), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pg.draw.rect(screen, health_color, (health_bar_x, health_bar_y, health_bar_width * health_percentage, health_bar_height))
    font = pg.font.Font(None, 24)
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    screen.blit(health_text, (health_bar_x + 5, health_bar_y - 25))

import math
import random

class Item:
    def __init__(self, name, position, sprite, effect=None):
        """
        Initialize an item.
        :param name: Name of the item.
        :param position: Tuple (x, y) representing the item's position on the map.
        :param sprite: Pygame surface for the item's sprite.
        :param effect: Function to apply the item's effect (optional).
        """
        self.name = name
        self.position = position
        self.sprite = sprite
        self.effect = effect  # A function that defines what the item does

    def apply_effect(self, player):
        """
        Apply the item's effect to the player.
        :param player: The player instance to apply the effect to.
        """
        if self.effect:
            self.effect(player)



class GameMap:
    def __init__(self, width=32, height=32):
        self.width = width
        self.height = height
        # Other initialization logic

        self.tiles = [[0 for _ in range(width)] for _ in range(height)]  # Example map structure
        self.items = []  # List to hold items in the game world
        self.size = size
        self.wall_grid = self.create_map()
        self.sky_box = Image(IMAGES["sky"])
        self.wall_texture = Image(IMAGES["texture"])
        self.light = 0

        # Tiny room timer and teleportation setup
        self.player_in_tiny_room = False
        self.tiny_room_timer = 0
        self.player_position = None  # Store player's position

        # Define the coordinates for tiny rooms and their mirrored counterparts
        self.tiny_rooms = {
            (4, 4, 9, 9): (17, 4, 22, 9),    # Top-left room mirrors to top-right
            (17, 4, 22, 9): (4, 4, 9, 9),    # Top-right room mirrors to top-left
            (4, 17, 9, 22): (17, 17, 22, 22), # Bottom-left room mirrors to bottom-right
            (17, 17, 22, 22): (4, 17, 9, 22)  # Bottom-right room mirrors to bottom-left
        }


    def add_item(self, item):
        """
        Add an item to the game map.
        :param item: An instance of the Item class.
        """
        self.items.append(item)

    import math

    def draw_items(self, game_map):
        """
        Draw items on the map, ensuring they're positioned correctly in relation to the player.
        :param game_map: The GameMap instance containing the items.
        """
        for item in game_map.items:
            # Calculate the item's position relative to the player
            dx = item.position[0] - self.player.x
            dy = item.position[1] - self.player.y
            distance = math.hypot(dx, dy)

            # Calculate the angle to the item from the player's perspective
            angle = math.atan2(dy, dx) - self.player.direction
            angle = (angle + math.pi) % (2 * math.pi) - math.pi  # Normalize angle

            # Only render the item if it's within the player's field of view
            if abs(angle) < FIELD_OF_VIEW / 2:
                # Project the item position onto the screen based on its distance and angle
                screen_x = self.width / 2 + math.tan(angle) * self.width / (2 * distance)
                screen_y = self.height / 2 - (self.height / distance)

                # Make sure the item is within the screen bounds
                if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                    # Draw the item sprite at the calculated position
                    self.screen.blit(item.sprite, (screen_x - item.sprite.get_width() // 2, screen_y))

                    # Debugging output (optional)
                    print(f"Item at {item.position} projected to ({screen_x}, {screen_y})")



    def handle_item_pickup(self):
        """
        Check if the player is on the health item tile and increase health if they step on it.
        """
        item_positions = [(9, 9), (3, 3)]  # List of item positions

        for item_position in item_positions:
            # Check if the player is standing on the exact tile (item_position)
            if (int(self.x), int(self.y)) == item_position and item_position not in self.collected_items:
                # Check which item was collected (different health for each item)
                if item_position == (9, 9):
                    self.collect_health_item(50)  # Increase health by 50
                elif item_position == (3, 3):
                    self.collect_health_item(20)  # Increase health by 20

                self.collected_items.add(item_position)  # Mark the item as collected
                print(f"Health item collected at {item_position}")

        # Debugging
        print(f"Position: ({self.x}, {self.y}), Health: {self.health}")



    def draw_items(self, screen, scale):
        """
        Draw items on the map.
        :param screen: The pygame screen.
        :param scale: The scale factor for drawing items.
        """
        for item in self.items:
            screen.blit(
                item.sprite,
                (item.position[0] * scale, item.position[1] * scale)
            )
    def get(self, x, y):
        """A method to check if a given coordinate is colliding with a wall."""
        point = (int(math.floor(x)), int(math.floor(y)))
        return self.wall_grid.get(point, -1)

    def get_mirror_position(self, px, py):
        """Calculate the mirrored position for the player in the opposite tiny room."""
        for (x1, y1, x2, y2), (mx1, my1, mx2, my2) in self.tiny_rooms.items():
            if x1 <= px < x2 and y1 <= py < y2:
                # Calculate the offset within the current tiny room
                offset_x = px - x1
                offset_y = py - y1
                # Map to mirrored room with the same offset
                mirror_x = mx1 + offset_x
                mirror_y = my1 + offset_y
                return mirror_x, mirror_y
        return px, py  # Return the original position if not in a tiny room

    def create_map(self):
        """
        Create a map where the top-left room has an opening, and all tiny rooms have openings
        at the top, similar to the top-left tiny room.
        Additionally, an opening is added to one of the bottom-left or bottom-right enclosures.
        """
        wall_grid = {}

        # Initialize the map with empty spaces
        for x in range(self.size):
            for y in range(self.size):
                wall_grid[(x, y)] = False  # False represents empty space

        # Define the unique top-left room with an opening
        top_left_area = ((1, 1), (13, 15), (8, 1))  # Top-left room with opening
        start, end, opening = top_left_area

        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                if x == start[0] or y == start[1] or x == end[0] - 1 or y == end[1] - 1:
                    wall_grid[(x, y)] = True  # Add walls
        wall_grid[opening] = False  # Create the opening for the top-left room

        # Define the identical enclosed rooms (no openings initially)
        identical_rooms = [
            ((14, 1), (26, 15)),  # Top-right room
            ((14, 16), (26, 30)),  # Bottom-right room
            ((1, 16), (13, 30))  # Bottom-left room
        ]

        for start, end in identical_rooms:
            for x in range(start[0], end[0]):
                for y in range(start[1], end[1]):
                    if x == start[0] or y == start[1] or x == end[0] - 1 or y == end[1] - 1:
                        wall_grid[(x, y)] = True  # Add walls

        # Add an opening in one of the bottom rooms
        bottom_left_opening = (7, 29)  # Adjusted to create an opening at the bottom
        bottom_right_opening = (20, 29)  # Adjusted to create an opening at the bottom

        # Choose which opening to create (you can modify this logic as needed)
        wall_grid[bottom_left_opening] = False  # Uncomment if you prefer bottom-left
        # wall_grid[bottom_right_opening] = False  # Uncomment if you prefer bottom-right

        # Define tiny rooms with top openings
        tiny_rooms = [
            ((4, 4), (9, 9), (6, 4)),          # Small room in top-left with top opening
            ((17, 4), (22, 9), (19, 4)),       # Small room in top-right with top opening
            ((17, 19), (22, 24), (19, 19)),    # Small room in bottom-right with top opening
            ((4, 19), (9, 24), (6, 19))        # Small room in bottom-left with top opening
        ]

        self.tiny_rooms = {}  # Store tiny room boundaries and mirrored counterparts

        for start, end, opening in tiny_rooms:
            for x in range(start[0], end[0]):
                for y in range(start[1], end[1]):
                    if x == start[0] or y == start[1] or x == end[0] - 1 or y == end[1] - 1:
                        wall_grid[(x, y)] = True  # Add walls
            wall_grid[opening] = False  # Create the top opening for the tiny room

            # Store mirrored room info for teleportation
            mirrored_x1 = self.size - end[0]
            mirrored_x2 = self.size - start[0]
            self.tiny_rooms[(start[0], start[1], end[0], end[1])] = (mirrored_x1, start[1], mirrored_x2, end[1])

        return wall_grid




    def update(self, dt, player_position=None):
        # Update light behavior
        decay_rate = 10
        replenish_chance = 5
        if self.light > 0:
            self.light = max(self.light - decay_rate * dt, 0)
        elif random.random() * replenish_chance < dt:
            self.light = 2

        # Update player position if provided
        if player_position:
            self.player_position = player_position

        # Check if there's a valid player position for teleportation logic
        if not self.player_position:
            return  # Skip teleportation if no player position is provided

        # Check if the player is in any tiny room
        for (x1, y1, x2, y2), (mx1, my1, mx2, my2) in self.tiny_rooms.items():
            px, py = self.player_position
            if x1 <= px < x2 and y1 <= py < y2:
                if not self.player_in_tiny_room:
                    self.player_in_tiny_room = True
                    self.tiny_room_timer = 0  # Reset timer on entry

                self.tiny_room_timer += dt

                if self.tiny_room_timer >= 10:  # After 10 seconds in the room
                    # Calculate mirrored position in the mirrored room
                    offset_x = px - x1
                    offset_y = py - y1
                    self.player_position[0] = mx1 + offset_x
                    self.player_position[1] = my1 + offset_y
                break
        else:
            # Player is not in any tiny room; reset the status
            self.player_in_tiny_room = False
            self.tiny_room_timer = 0







    def cast_ray(self, point, angle, cast_range):
        """
        The meat of our ray casting program. Given a point,draw min
        an angle (in radians), and a maximum cast range, check if any
        collisions with the ray occur. Casting will stop if a collision is
        detected (cell with greater than 0 height), or our maximum casting
        range is exceeded without detecting anything.
        """
        info = RayInfo(math.sin(angle), math.cos(angle))
        origin = Point(point)
        ray = [origin]

        # Increase the cast_range to allow the player to see further
        max_cast_range = 16  # Adjust this value to increase visibility

        while origin.height <= 0 and origin.distance <= max_cast_range:
            dist = origin.distance
            step_x = origin.step(info.sin, info.cos)
            step_y = origin.step(info.cos, info.sin, invert=True)
            
            if step_x.length < step_y.length:
                next_step = step_x.inspect(info, self, 1, 0, dist, step_x.y)
            else:
                next_step = step_y.inspect(info, self, 0, 1, dist, step_y.x)

            ray.append(next_step)
            origin = next_step

        return ray



class Point(object):
    """
    A fairly basic class to assist us with ray casting.  The return value of
    the GameMap.cast_ray() method is a list of Point instances.
    """
    def __init__(self, point, length=None):
        self.x = point[0]
        self.y = point[1]
        self.height = 0
        self.distance = 0
        self.shading = None
        self.length = length

    def step(self, rise, run, invert=False):
        """
        Return a new Point advanced one step from the caller.  If run is
        zero, the length of the new Point will be infinite.
        """
        try:
            x, y = (self.y, self.x) if invert else (self.x, self.y)
            dx = math.floor(x+1)-x if run > 0 else math.ceil(x-1)-x
            dy = dx*(rise/run)
            next_x = y+dy if invert else x+dx
            next_y = x+dx if invert else y+dy
            length = math.hypot(dx, dy)
        except ZeroDivisionError:
            next_x = next_y = None
            length = NO_WALL
        return Point((next_x, next_y), length)

    def inspect(self, info, game_map, shift_x, shift_y, distance, offset):
        """
        Ran when the step is selected as the next in the ray.
        Sets the steps self.height, self.distance, and self.shading,
        to the required values.
        """
        dx = shift_x if info.cos < 0 else 0
        dy = shift_y if info.sin < 0 else 0
        self.height = game_map.get(self.x-dx, self.y-dy)
        self.distance = distance+self.length
        if shift_x:
            self.shading = 2 if info.cos < 0 else 0
        else:
            self.shading = 2 if info.sin < 0 else 1
        self.offset = offset-math.floor(offset)
        return self



class Camera(object):
    """Handles the projection and rendering of all objects on the screen."""
    def __init__(self, screen, resolution):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.resolution = float(resolution)
        self.spacing = self.width / resolution
        self.field_of_view = FIELD_OF_VIEW
        self.range = 8
        self.light_range = 5
        self.scale = SCALE
        self.flash = pg.Surface((self.width, self.height // 2)).convert_alpha()


    # Update the render method to draw the player's health bar.
    def render(self, player, game_map, npcs):
        """Render everything in order."""
        self.draw_sky(player.direction, game_map.sky_box, game_map.light)
        self.draw_columns(player, game_map)
        self.draw_items(game_map, player)  # Pass the player object here
        self.draw_weapon(player.weapon, player.paces)
        self.draw_minimap(player, game_map, npcs)
        self.draw_npcs(npcs, player)
        draw_health(self.screen, player)  # Draw the player's health bar.

# Update the game loop where player and NPC updates are called.



    # Update the draw_npcs method to accept a player parameter
    def draw_npcs(self, npcs, player):
        """Draw all NPCs on the screen."""
        npc_width = 20   # Width of the NPC character
        npc_height = 40  # Height of the NPC character

        for npc in npcs:
            print(f"NPC at map coordinates: ({npc.x}, {npc.y})")
            
            # Create a surface for the NPC
            npc_image = pg.Surface((npc_width, npc_height), pg.SRCALPHA)
            # Draw the body (a rectangle)
            pg.draw.rect(npc_image, (0, 255, 0), (0, npc_height // 4, npc_width, npc_height * 3 // 4))
            
            # Draw the head (a circle)
            pg.draw.ellipse(npc_image, (0, 200, 0), (npc_width // 4, 0, npc_width // 2, npc_height // 4))
            
            dx = npc.x - player.x
            dy = npc.y - player.y
            distance = math.hypot(dx, dy)
            
            print(f"dx: {dx}, dy: {dy}, distance: {distance}")
            
            if distance == 0:  # Skip rendering NPCs at the exact player position
                continue
            
            angle_to_npc = math.atan2(dy, dx) - player.direction
            print(f"Angle to NPC: {angle_to_npc}, Player Direction: {player.direction}")
            
            # Normalize angle to NPC
            angle_to_npc = (angle_to_npc + math.pi) % (2 * math.pi) - math.pi
            
            if abs(angle_to_npc) < FIELD_OF_VIEW / 2:
                # Project the NPC onto the screen
                projected_height = min(self.height // distance, self.height)
                left = self.width / 2 + math.tan(angle_to_npc) * self.width / 2
                
                # Adjust the top position for height perspective, lowering the NPC
                top = (self.height / 2) - (projected_height / 2)
                
                print(f"Projected left: {left}, top: {top}, projected_height: {projected_height}")
                
                if 0 <= left < self.width:
                    # Ensure the NPC is drawn within the screen boundaries
                    self.screen.blit(npc_image, (left - npc_width // 2, top))
                else:
                    print(f"NPC at ({left}, {top}) is outside screen bounds")
            else:
                print(f"NPC at angle {angle_to_npc} is outside player's field of view.")

    def draw_sky(self, direction, sky, ambient_light):
        """
        Calculate the skies offset so that it wraps, and draw.
        If the ambient light is greater than zero, draw lightning flash.
        """
        left = -sky.width * direction / CIRCLE
        self.screen.blit(sky.image, (left, 0))
        if left < sky.width - self.width:
            self.screen.blit(sky.image, (left + sky.width, 0))
        if ambient_light > 0:
            alpha = 255 * min(1, ambient_light * 0.1)
            self.flash.fill((255, 255, 255, alpha))
            self.screen.blit(self.flash, (0, self.height // 2))

    def draw_columns(self, player, game_map):
        """
        For every column in the given resolution, cast a ray, and render that
        column.
        """
        for column in range(int(self.resolution)):
            angle = self.field_of_view * (column / self.resolution - 0.5)
            point = player.x, player.y
            ray = game_map.cast_ray(point, player.direction + angle, self.range)
            self.draw_column(column, ray, angle, game_map)

    def draw_column(self, column, ray, angle, game_map):
        """
        Examine each step of the ray, starting with the furthest.
        If the height is greater than zero, render the column (and shadow).
        Also, draw the ceiling above the walls.
        """
        left = int(math.floor(column * self.spacing))
        
        for ray_index in range(len(ray) - 1, -1, -1):
            step = ray[ray_index]
            if step.height > 0:
                texture = game_map.wall_texture
                width = int(math.ceil(self.spacing))
                texture_x = int(texture.width * step.offset)
                wall = self.project(step.height, angle, step.distance)

                # Draw the wall
                image_location = pg.Rect(texture_x, 0, 1, texture.height)
                image_slice = texture.image.subsurface(image_location)
                scale_rect = pg.Rect(left, wall.top, width, wall.height)
                scaled = pg.transform.scale(image_slice, scale_rect.size)
                self.screen.blit(scaled, scale_rect)

                # Draw the ceiling
                self.draw_ceiling(wall.top, left, width, step.height)

                self.draw_shadow(step, scale_rect, game_map.light)
            self.draw_rain(step, angle, left, ray_index)


    def draw_ceiling(self, wall_top, left, width, wall_height):
        """
        Draw the ceiling above the wall based on the height of the wall.
        The ceiling will be drawn as a black rectangle above the wall.
        """
        # Calculate the position of the ceiling
        ceiling_top = 0  # Starting from the top of the screen
        ceiling_bottom = wall_top  # The bottom of the ceiling is at the top of the wall
        ceiling_rect = pg.Rect(left, ceiling_top, width, ceiling_bottom)
        
        # Draw the ceiling in black
        pg.draw.rect(self.screen, (0, 0, 0), ceiling_rect)  # Black color for the ceiling



    def draw_shadow(self, step, scale_rect, light):
        """
        Render the shadow on a column with regards to its distance and
        shading attribute.
        """
        shade_value = step.distance + step.shading
        max_light = shade_value / float(self.light_range) - light
        alpha = 255 * min(1, max(max_light, 0))
        shade_slice = pg.Surface(scale_rect.size).convert_alpha()
        shade_slice.fill((0, 0, 0, alpha))
        self.screen.blit(shade_slice, scale_rect)

    def draw_rain(self, step, angle, left, ray_index):
        """
        Render a number of rain drops to add depth to our scene and mask
        roughness.
        """
        rain_drops = int(random.random()**3 * ray_index)
        if rain_drops:
            rain = self.project(0.1, angle, step.distance)
            drop = pg.Surface((1, rain.height)).convert_alpha()
            drop.fill(RAIN_COLOR)
            for _ in range(rain_drops):
                self.screen.blit(drop, (left, random.random() * rain.top))
    def draw_items(self, game_map, player):
        """
        Draw items on the map.
        :param game_map: The GameMap instance containing the items.
        :param player: The Player instance to calculate relative positions.
        """
        for item in game_map.items:
            # Calculate the item's position relative to the player
            dx = item.position[0] - player.x
            dy = item.position[1] - player.y

            # Calculate the distance and angle to the item
            distance = math.hypot(dx, dy)
            angle = math.atan2(dy, dx) - player.direction

            # Normalize the angle to the player's field of view
            angle = (angle + math.pi) % (2 * math.pi) - math.pi

            # Only render the item if it's within the player's field of view
            if abs(angle) < FIELD_OF_VIEW / 2:
                # Project the item onto the screen
                projected_height = min(self.height // distance, self.height)
                left = self.width / 2 + math.tan(angle) * self.width / 2

                # Adjust the top position for height perspective
                top = (self.height / 2) - (projected_height / 2)

                # Draw the item if it's within the screen bounds
                if 0 <= left < self.width:
                    self.screen.blit(item.sprite, (left - item.sprite.get_width() // 2, top))
    def draw_weapon(self, weapon, paces):
        """
        Calculate new weapon position based on player's pace attribute,
        and render.
        """
        bob_x = math.cos(paces * 2) * self.scale * 6
        bob_y = math.sin(paces * 4) * self.scale * 6
        left = self.width * 0.66 + bob_x
        top = self.height * 0.6 + bob_y
        self.screen.blit(weapon.image, (left, top))

    def project(self, height, angle, distance):
        """
        Find the position on the screen after perspective projection.
        A minimum value is used for z to prevent slices blowing up to
        unmanageable sizes when the player is very close.
        """
        z = max(distance * math.cos(angle), 0.2)
        wall_height = self.height * height / float(z)
        bottom = self.height / float(2) * (1 + 1 / float(z))
        return WallInfo(bottom - wall_height, int(wall_height))

    def draw_minimap(self, player, game_map, npcs):
        """
        Draw a minimap showing the player's surroundings:
        - If the player is inside an enclosure, display only that enclosure.
        - If the player is outside, display all nearby enclosures.
        """
        minimap_size = 200
        minimap_surface = pg.Surface((minimap_size, minimap_size))
        minimap_surface.fill((50, 50, 50))  # Background color

        # Define enclosures (buildings) with their boundaries
        enclosures = [
            ((1, 1), (13, 15)),      # Top-left room
            ((14, 1), (26, 15)),     # Top-right room
            ((1, 16), (13, 30)),     # Bottom-left room
            ((14, 16), (26, 30))     # Bottom-right room
        ]

        # Scale factor for the minimap
        total_width = max(end[0] for _, end in enclosures)
        total_height = max(end[1] for _, end in enclosures)
        scale_x = minimap_size / total_width
        scale_y = minimap_size / total_height

        # Offset to center the minimap on the player position
        offset_x = minimap_size // 2 - (player.x * scale_x)
        offset_y = minimap_size // 2 - (player.y * scale_y)

        # Determine if the player is inside an enclosure
        current_enclosure = None
        for (start, end) in enclosures:
            if start[0] <= player.x < end[0] and start[1] <= player.y < end[1]:
                current_enclosure = (start, end)
                break

        if current_enclosure:
            # Player is in an enclosure, so draw only that enclosure
            start_x, start_y = current_enclosure[0]
            end_x, end_y = current_enclosure[1]

            # Calculate the scaling factor for the enclosure to fit the minimap
            enclosure_width = end_x - start_x
            enclosure_height = end_y - start_y
            scale_x = minimap_size / enclosure_width
            scale_y = minimap_size / enclosure_height

            # Draw walls within the enclosure
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    if game_map.get(x, y):  # Pass x and y as separate arguments
                        pg.draw.rect(
                            minimap_surface, 
                            (0, 0, 255), 
                            ((x - start_x) * scale_x, (y - start_y) * scale_y, scale_x, scale_y)
                        )

            # Draw the player's position within the scaled enclosure
            player_x_minimap = (player.x - start_x) * scale_x
            player_y_minimap = (player.y - start_y) * scale_y
            pg.draw.circle(minimap_surface, (255, 0, 0), (int(player_x_minimap), int(player_y_minimap)), 5)

            # Draw NPCs within the scaled enclosure
            for npc in npcs:
                if start_x <= npc.x < end_x and start_y <= npc.y < end_y:
                    npc_x_minimap = (npc.x - start_x) * scale_x
                    npc_y_minimap = (npc.y - start_y) * scale_y
                    pg.draw.circle(minimap_surface, (0, 255, 0), (int(npc_x_minimap), int(npc_y_minimap)), 5)
        else:
            # Player is outside, so draw all nearby enclosures
            for (start, end) in enclosures:
                for x in range(start[0], end[0]):
                    for y in range(start[1], end[1]):
                        if game_map.get(x, y):  # Pass x and y as separate arguments
                            pg.draw.rect(
                                minimap_surface,
                                (0, 0, 255), 
                                ((x * scale_x) + offset_x, (y * scale_y) + offset_y, scale_x, scale_y)
                            )

            # Draw the player's position as a red dot
            player_x_minimap = player.x * scale_x + offset_x
            player_y_minimap = player.y * scale_y + offset_y
            pg.draw.circle(minimap_surface, (255, 0, 0), (int(player_x_minimap), int(player_y_minimap)), 5)

            # Draw NPCs as green dots
            for npc in npcs:
                npc_x_minimap = npc.x * scale_x + offset_x
                npc_y_minimap = npc.y * scale_y + offset_y
                pg.draw.circle(minimap_surface, (0, 255, 0), (int(npc_x_minimap), int(npc_y_minimap)), 5)

        # Display the minimap in the top right corner of the screen
        self.screen.blit(minimap_surface, (self.width - minimap_size - 10, 10))  # Adjust position as needed

class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.player = Player(15.3, -1.2, math.pi * 0.3, size)
        self.game_map = GameMap(32, 32)
        self.camera = Camera(self.screen, 300)
        self.npcs = []  # List to hold NPC objects
        self.spawn_npcs_near_player()  # Call to spawn NPCs
        self.spawn_items()  # Call to spawn items

    def spawn_npcs_near_player(self):
        """Spawn NPCs around the player."""
        num_npcs = 5  # Number of NPCs to spawn
        spawn_radius = 100  # Radius around the player to spawn NPCs

        for _ in range(num_npcs):
            # Generate random position within the spawn radius
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, spawn_radius)
            npc_x = self.player.x + distance * math.cos(angle)
            npc_y = self.player.y + distance * math.sin(angle)

            # Ensure NPCs spawn within map boundaries
            npc_x = max(0, min(npc_x, self.game_map.width - 1))
            npc_y = max(0, min(npc_y, self.game_map.height - 1))

            npc = NPC(npc_x, npc_y, random.uniform(0, 2 * math.pi))
            self.npcs.append(npc)

    def spawn_items(self):
        """Spawn items in the game world with different images."""

        # List of tuples: (position, image_path)
        health_item_data = [
            ((9, 9), "covers.png"),
            ((3, 3), "covers2.png"),
        ]

        for pos, image_path in health_item_data:
            # Load and scale the sprite for each item
            item_image = pg.image.load(image_path).convert_alpha()
            item_sprite = pg.transform.scale(item_image, (16, 16))

            # Create the health potion item with its own image
            health_potion = Item(
                name="Health Potion",
                position=pos,
                sprite=item_sprite,
                effect=lambda player: setattr(player, 'health', min(player.health + 40, 100))  # Cap health at 100
            )

            self.game_map.add_item(health_potion)
            print(f"Item spawned at {health_potion.position} with image {image_path}")  # Debug



    def event_loop(self):
        """Quit game on a quit event and update self.keys on any keyup or keydown."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()

    def update(self, dt):
        """Update the game_map, player, and NPCs."""
        self.game_map.update(dt)
        self.player.update(self.keys, dt, self.game_map)
        # Update NPCs
        for npc in self.npcs:
            npc.update(dt, self.game_map, self.player)
        # Check for item pickups
        self.handle_item_pickups()

    def handle_item_pickups(self):
        """Check if the player is on an item tile and pick it up."""
        for item in self.game_map.items[:]:  # Use a copy to modify the list while iterating
            # Check if the player's position matches the item's position
            if (int(self.player.x), int(self.player.y)) == item.position:
                self.player.pick_up_item(item)
                self.game_map.items.remove(item)  # Remove the item from the game map
                print(f"Item collected at {item.position}")  # Debugging


    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def render_items(self):
        """Render items on the map."""
        for item in self.game_map.items:
            # Scale the item's position to fit the screen
            item_x = int(item.position[0] * 20)  # Adjust scale as needed
            item_y = int(item.position[1] * 20)  # Adjust scale as needed
            self.screen.blit(item.sprite, (item_x, item_y))

    def main_loop(self):
        """Process events, update, and render."""
        while not self.done:
            # Process events (e.g., keyboard input, window close)
            self.event_loop()

            # Calculate delta time (time since last frame)
            dt = self.clock.tick(self.fps) / 1000.0

            # Update game state (e.g., player, NPCs, items)
            self.update(dt)

            # Render the game world
            self.camera.render(self.player, self.game_map, self.npcs)

            # Render items on top of the game world
            self.render_items()

            # Update the display
            pg.display.update()

            # Display the current FPS in the window caption
            self.display_fps()


def load_resources():
    """
    Return a dictionary of our needed images; loaded, converted, and scaled.
    """
    images = {}
    knife_image = pg.image.load("knife.png").convert_alpha()
    knife_w, knife_h = knife_image.get_size()
    knife_scale = (int(knife_w*SCALE), int(knife_h*SCALE))
    images["knife"] = pg.transform.smoothscale(knife_image, knife_scale)
    images["texture"] = pg.image.load("wall.jpg").convert()
    sky_size = int(SCREEN_SIZE[0]*(CIRCLE/FIELD_OF_VIEW)), SCREEN_SIZE[1]
    sky_box_image = pg.image.load("sky.jpg").convert()
    images["sky"] = pg.transform.smoothscale(sky_box_image, sky_size)
    return images


def main():
    """Prepare the display, load images, and get our programming running."""
    global IMAGES
    os.environ["SDL_VIDEO_CENTERED"] = "True"
    pg.init()
    pg.display.set_mode(SCREEN_SIZE)
    IMAGES = load_resources()
    Control().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()