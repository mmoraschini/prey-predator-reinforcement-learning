from typing import Dict, Tuple

import pygame
import numpy as np
import gym

from actors.actors import Animal, Prey, Predator

W_WIDTH = 1000
W_HEIGHT = 1000

PREY_COLOR = (0, 0, 255)
PREDATOR_COLOR = (255, 0, 0)

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

class WorldEnvironment(gym.Env):
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
        pygame.init()
        self.window = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        self.clock = pygame.time.Clock()

    def reset(self):
        return 0
    
    def _execute_action(self, action: Dict, animal: Animal):
        animal.x += action[0]
        animal.y += action[1]

    def step(self, actions: Dict[Animal, Tuple[int, int]]):

        # Execute calculated actions
        for p in self.preys:
            self._execute_action(actions[p], p)

        for p in self.predators:
            self._execute_action(actions[p], p)
        
        # Calculate new rewards
        preys_rewards = np.full(self.preys.size, 0, dtype=int)
        predators_rewards = np.full(self.predators.size, 0, dtype=int)
        
        # Rewards for predators
        for i, pr in enumerate(self.predators):
            
            # Check if predator already has an action
            if (pr.action_result != None):
                continue
            
            for j, py in enumerate(self.preys):
                if (py.x == pr.x) and (py.y == pr.y) and (py.action_result != "die"):
                    py.action_result = "die"
                    pr.action_result = "eat"
                    preys_rewards[i] += self.reward_system["prey"]["die"]
                    predators_rewards[j] += self.reward_system["prey"]["eat"]
                    
                    break
            
            # Check if a new action was given after interaction with other predators
            if (pr.action_result != None):
                continue
            
            # Interact with other predators
            for j, pr_j in enumerate(self.predators[i + 1:]):
                
                # Check if predator already has an action
                if (pr_j.action_result != None):
                    continue
                
                if (pr.x == pr_j.x) and (pr.y == pr_j.y) and \
                        (pr.sex != pr_j.sex) and \
                        (pr.action_result != "mate") and (pr_j.action_result != "mate") and \
                        (pr.pregnant == False) and (pr_j.pregnant == False) and \
                        (pr.cooldown == 0) and (pr_j.cooldown == 0) and \
                        (pr.action_result == None) and (pr_j.action_result == None):
                    pr.action_result = "mate"
                    pr_j.action_result = "mate"
                    predators_rewards[i] += self.reward_system["predator"]["mate"]
                    predators_rewards[j] += self.reward_system["predator"]["mate"]
                    
                    break
                else:
                    if (pr.action_result == None):
                        predators_rewards[i] += self.reward_system["predator"]["alive"]
                    if (pr_j.action_result == None):
                        predators_rewards[j] += self.reward_system["predator"]["alive"]
        
        # Rewards for preys
        for i, p_i in enumerate(self.preys):
            
            if (p_i.action_result != None):
                continue
            
            for j, p_j in enumerate(self.preys[i + 1:]):
                
                if (p_j.action_result != None):
                    continue
                
                if (p_i.x == p_j.x) and (p_i.y == p_j.y) and \
                        (p_i.sex != p_j.sex) and \
                        (p_i.action_result != "mate") and (p_j.action_result != "mate") and \
                        (p_i.pregnant == False) and (p_j.pregnant == False) and \
                        (p_i.cooldown == 0) and (p_j.cooldown == 0) and \
                        (p_i.action_result == None) and (p_j.action_result == None):
                    p_i.action_result = "mate"
                    p_j.action_result = "mate"
                    preys_rewards[i] += self.reward_system["prey"]["mate"]
                    preys_rewards[j] += self.reward_system["prey"]["mate"]
                    
                    break
                else:
                    if (p_i.action_result == None):
                        preys_rewards[i] += self.reward_system["prey"]["alive"]
                    if (p_j.action_result == None):
                        preys_rewards[j] += self.reward_system["prey"]["alive"]

        observation, reward, done, info = 0., 0., False, {}
        return observation, reward, done, info
    
    def render(self):
        
        for p in self.preys:
            pygame.draw.circle(self.window, PREY_COLOR, (p.x, p.y), 6)
        
        for p in self.predators:
            pygame.draw.circle(self.window, PREDATOR_COLOR, (p.x, p.y), 6)
        
        pygame.display.update()

environment = WorldEnvironment()
environment.init_render()
run = True
while run:
    environment.clock.tick(30)

    actions = {
        "preys": [],
        "predators": []
    }

    actions = {}
    # Calculate new actions
    for i, p in enumerate(environment.preys):
        actions[p] = p.get_action(environment.preys, environment.predators)

    for i, p in enumerate(environment.predators):
        actions[p] = p.get_action(environment.preys, environment.predators)

    # Execute the actions and calculate the rewads
    environment.step(actions)
    
    # Draw the new world after the time step
    environment.render()

pygame.quit()