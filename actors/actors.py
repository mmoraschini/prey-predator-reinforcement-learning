from typing import Dict

class Animal():
    def __init__(self, x: int, y: int, sex: int):
        self.x = x
        self.y = y
        self.sex = sex
        self.action_result = None
        
        self.pregnant = False
    
    def get_action(self, preys, predators):
        if self.next_action == "die":
            return None
        if self.next_action == "mate":
            return None
        if self.next_action == "eat":
            return None
        
        #TODO: Use RL to calculate next move
        return None

class Prey(Animal):
    def __init__(self, x: int, y: int, sex: int, config: Dict):
        super().__init__(x, y, sex)

        self.max_children = config["Prey"]["max_children"]
        self.round_birth = config["Prey"]["round_birth"]
        self.lifespan = config["Prey"]["lifespan"]
        self.cooldown = config["Prey"]["cooldown"]

class Predator(Animal):
    def __init__(self, x: int, y: int, sex: int, config: Dict):
        super().__init__(x, y, sex)

        self.max_children = config["Predator"]["max_children"]
        self.round_birth = config["Predator"]["round_birth"]
        self.round_death_hunger = config["Predator"]["round_death_hunger"]
        self.lifespan = config["Predator"]["lifespan"]
        self.cooldown = config["Predator"]["cooldown"]

        self.hunger = 0
