from typing import Dict

import pygame
import numpy as np
import gym

from actors.actors import Prey, Predator

W_WIDTH = 1000
W_HEIGHT = 1000

# ###############
# Reward system #
# ###############
# - Prey
# alive = 1
# mate = 2
# eaten = -5
#
# - Predator
# alive = 1
# mate = 2
# eat | hunger < 50 = 2
# eat | hunger > 50 = 3
# die = -5
#################

class CustomEnv(gym.Env):
    def __init__(self, config: Dict={}):
        n_preys = config["n_preys"]
        n_predators = config["n_predators"]

        self.preys = np.empty(n_preys, dtype=Prey)
        self.predators = np.empty(n_predators, dtype=Predator)

        self.reward_system = config["rewards"]

        for i in range(n_preys):
            x = np.random.randint(0, W_WIDTH)
            y = np.random.randint(0, W_HEIGHT)
            sex = np.random.randint(0, 2)
            self.preys[i] = Prey(x, y, sex)
        
        for i in range(n_predators):
            x = np.random.randint(0, W_WIDTH)
            y = np.random.randint(0, W_HEIGHT)
            sex = np.random.randint(0, 2)
            self.preys[i] = Predator(x, y, sex)

    def init_render(self):
        import pygame
        pygame.init()
        self.window = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        self.clock = pygame.time.Clock()

    def reset(self):
        return 0

    def step(self, actions: Dict[str, np.array]):

        preys_rewards = np.full(self.preys.size, 0, dtype=int)
        predators_rewards = np.full(self.predators.size, 0, dtype=int)
        for i, a in enumerate(actions["preys"]):
            self.preys[i].execute_action(a)

        for i, a in enumerate(actions["predators"]):
            self.predators[i].execute_action(a)
        
        for i, p_i in enumerate(self.preys):
            for j, p_j in enumerate(self.preys[i + 1:]):
                if (p_i.x == p_j.x) and (p_i.y == p_j.y) and \
                        (p_i.sex != p_j.sex) and \
                        (p_i.next_action != "mate") and (p_j.next_action != "mate") and \
                        (p_i.pregnant == False) and (p_j.pregnant == False) and \
                        (p_i.cooldown == 0) and (p_j.cooldown == 0) and \
                        (p_i.next_action == None) and (p_j.next_action == None):
                    p_i.next_action = "mate"
                    p_j.next_action = "mate"
                    preys_rewards[i] += self.reward_system["prey"]["mate"]
                    preys_rewards[j] += self.reward_system["prey"]["mate"]
                else:
                    if (p_i.next_action == None):
                        preys_rewards[i] += self.reward_system["prey"]["alive"]
                    if (p_j.next_action == None):
                        preys_rewards[j] += self.reward_system["prey"]["alive"]

        for i, py in enumerate(self.predators):
            for j, pr in enumerate(self.preys):
                if (py.x == pr.x) and (py.y == pr.y) and (py.next_action != "die"):
                    py.next_action = "die"
                    pr.next_action = "eat"
                    preys_rewards[i] += self.reward_system["prey"]["die"]
                    predators_rewards[j] += self.reward_system["prey"]["eat"]
                # Implement mating

            
        observation, reward, done, info = 0., 0., False, {}
        return observation, reward, done, info
    
    def render(self):
        self.window.fill((0,0,0))
        pygame.draw.circle(self.window, (0, 200, 200), (int(self.x), int(self.y)), 6)
        # draw orientation
        p1 = (self.x - 10 * np.cos(self.ang),self.y + 10 * np.sin(self.ang))
        p2 = (self.x + 15 * np.cos(self.ang),self.y - 15 * np.sin(self.ang))
        pygame.draw.line(self.window,(0,100,100),p1,p2,2)
        pygame.display.update()

environment = CustomEnv()
environment.init_render()
run = True
while run:
    environment.clock.tick(30)

    actions = {
        "preys": [],
        "predators": []
    }

    for i, p in enumerate(environment.preys):
        p.get_action(environment.preys, environment.predators)

    for i, p in enumerate(environment.predators):
        p.get_action(environment.preys, environment.predators)

    environment.step(actions)
    environment.render()

pygame.quit()