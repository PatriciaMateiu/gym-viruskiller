import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import sys
import copy
import random
import math

class Virus():
    def __init__(self, center_x=0, center_y=0, color=None):
        # If color is None, bubble is empty
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
 
class VirusKillerEnv(gym.Env):  
    metadata = {'render.modes': ['human', 'console'], 'video.frames_per_second':350}   


    green = (0, 255, 0)
    red = (255, 0 , 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    cyan = (0, 255, 255)

    colors = [green, red, white, black, blue, cyan]


    def __init__(self):
        self.seed = seed
        if seed is None:
            self.seed = random.randint(0, sys.maxsize)
        self.virus_radius = 20
        self.array_height = 14
        self.death_line = self.array_height - 2
        self.spacing = 10 #in pixels
        self.window_height = (self.array_height * self.virus_radius * 2
                              + self.spacing * (self.array_height + 2)
                              + 6 * self.virus_radius)
        self.window_width = 850
        self.start_x = self.window_width / 2.0
        self.start_y = self.window_height - self.spacing - self.virus_radius
        self.speed = 1  # pixels, affects performance, be careful with too high values!
        self.color_dictionary = {}
        self.action_space = spaces.Discrete(179)
        self.observation_space = spaces.Dict({"next_virus": spaces.Discrete(len(self.colors)), "board": spaces.MultiDiscrete([
                                             len(self.colors) for i in range(self.array_height * self.array_height)])})
        self.reset()

    def step(self, action):
        action += 1

        if action <= 0 or action >= 180: #action represents
            raise Exception("Invalid action: {}".format(action))

        self.last_board = copy.deepcopy(self.board)
       
         # shoot bubble until it collides and set it to its new position
        angle = copy.deepcopy(action)
        self.last_positions = []
        while True:
            angle = self._move_next_bubble(angle)
            self.last_positions.append((self.next_bubble.center_x, self.next_bubble.center_y))
            if self._is_collided():
                break
        row, column = self._set_next_bubble_position()
        self.last_positions.append((row, column))

        # calculate all neighbors and delete if two or more of the same color
        # were hit
        neighborhood = self._get_neighborhood(row, column)
        if len(neighborhood) >= 3:
            self._delete_bubbles(neighborhood)
            self._delete_floaters()
            self._update_color_list()

        # create new next_bubble
        
        self.next_bubble = Bubble(
            self.start_x,
            self.start_y,
            self.color_list[0])

        result, done = self._is_over()
        state = self._get_game_state()
        reward = self._get_reward(len(neighborhood), result)
        return state, reward, done, {}
 
    def reset(self):
         self.next_virus = Virus(
            self.start_x,
            self.start_y,
            self.colors[0])

        self.screen = None
        self.last_board = copy.deepcopy(self.board)
        self.last_positions = []
        self.last_color = None

        return self._get_game_state()
 
    def render(self, mode='human', close=False):
        if mode == 'console':
            print(self._get_game_state)
        # elif statement allows you to check multiple expressions for TRUE and execute a block of code as soon as one of the conditions evaluates to TRUE.
        elif mode == 'human':
            try:
                import pygame
                from pygame import gfxdraw
            except ImportError as e:
                raise error.DependencyNotInstalled("{}. (HINT: install pygame using `pip install pygame`".format(e))
            if close:
                pygame.quit()
            else:
                if self.screen is None:
                    pygame.init()
                    self.screen = pygame.display.set_mode((round(self.window_width), round(self.window_height)))
                clock = pygame.time.Clock()

                self.screen.fill((255, 255, 255))
                
                last_x. last_y = None, None

                for position in self.last_positions:
                    if last_x is not None and last_y is not None:
                        pygame.gfxdraw.filled_circle(
                            self.screen, round(
                            last_x), round(
                            last_y), self.bubble_radius, (255,255,255))
                    last_x, last_y = position[0], position[1]
                    pygame.gfxdraw.filled_circle(
                            self.screen, round(
                            position[0]), round(
                            position[1]), self.bubble_radius, (0, 255, 0))
                    pygame.display.update()
                    clock.tick(self.metadata["video.frames_per_second"])
        
        else:
            raise error.UnsupportedMode("Unsupported render mode: " + mode)

     def _get_reward(self, viruses, result):
        """
        This function calculates the reward.
        """
        rewards = {"hit": 1,
                   "miss": -1,
                   "pop": 10,
                   "win": 200,
                   "lost": -200}

        # Return win or loose
        if len(result) > 0:
            return rewards[result]
        # Nothing hit
        elif bubbles == 1:
            return rewards["miss"]
        # Hit at least one bubble of the same color
        elif bubbles < 3:
            return rewards["hit"]
        # Hit enough bubbles to delete
        else:
            return bubbles * rewards["pop"]

        
