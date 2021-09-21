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

        self.center_x = center_x
        self.center_y = center_y
        self.color = color


class VirusKillerEnv(gym.Env):
    metadata = {'render.modes': ['human', 'console'], 'video.frames_per_second': 350}  #the game can either be controlled

    green = (0, 255, 0) #the color of the 'virus' : a green circle
    red = (255, 0, 0)  #not used yet, suitable in case of failure
    white = (255, 255, 255)  #background
    black = (0, 0, 0)
    blue = (0, 0, 255)   #blue or cyan -- sanitizer
    cyan = (0, 255, 255)

    colors = [green, red, white, black, blue, cyan]

    def __init__(self, seed=None):
        self.seed = seed
        if seed is None:
            self.seed = random.randint(0, sys.maxsize)   #random nr greater than 0
        self.virus_radius = 20  #how big the circle representing the "virus" will be
        self.death_line = self.array_height - 2  #the character dies when the virus gets too close (in case it was not killed)
        self.spacing = 30  # in pixels -- represents the spaces between the occuring viruses
        self.window_height = 1000 #pixels
        self.window_width = 850 #pixels
        self.start_x = self.window_width / 2.0
        self.start_y = self.window_height - self.spacing - self.virus_radius
        self.speed = 1  # pixels
        self.action_space = spaces.Discrete(179)

        self.reset()


    def reset(self): #reset the environment
        self.next_virus = Virus(self.start_x, self.start_y,self.colors[0]) #the virus is always green

        self.screen = None
        self.last_board = copy.deepcopy(self.board)
        self.last_positions = []
        self.last_color = None

        return self._get_game_state()



    def step(self, action):  #steps the game fw with 1 step --- must be continued
        action += 1

        if action <= 0 or action >= 180:  # action represents the angle from which the sanitizer is shot : must be in the interval [0,180]
            raise Exception("Invalid action: {}".format(action))

    pass


def render(self, mode='human', close=False):  #renders the game state in the given mode (human or console)
    #if mode == 'console':
        # to do

    # elif statement allows you to check multiple expressions for TRUE and execute a block of code as soon as one of the conditions evaluates to TRUE.
    if mode == 'human':
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

            self.screen.fill((255, 255, 255))  #background is white

            last_x, last_y = None, None

            for position in self.last_positions:
                if last_x is not None and last_y is not None:
                    pygame.gfxdraw.filled_circle(self.screen, round(position[0]), round(position[1]), self.bubble_radius, (0, 255, 0))  #draws a circle of given radius colored green
                    pygame.display.update()
                    clock.tick(self.metadata["video.frames_per_second"])

    else:
        raise error.UnsupportedMode("Unsupported render mode: " + mode)


def get_reward(self, viruses, result):  #calculate the reward for each move : if it hits the virus, an extra 1, if it misses, a -1

    rewards = {"hit": 1,
               "miss": -1,
               "won": 50,
               "lost": -50}

    if len(result) > 0:
        return rewards[result]   #won or lost

    elif viruses == 1:
        return rewards["miss"]  #if the virus was not hit

    elif viruses == 0:
        return rewards["hit"]  #there is no new virus



