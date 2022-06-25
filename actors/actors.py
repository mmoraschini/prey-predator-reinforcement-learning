from typing import Dict

class Animal():
    def __init__(self, x: int, y: int, sex: int):
        self.x = x
        self.y = y
        self.sex = sex
        self.next_action = None
        
        self.pregnant = False
    
    def execute_action(self, action: Dict):
        if action["action"] == "mate":
            if self.sex == 0:
                self.pregnant = True
        elif action["action"] == "move":
            self.x += action["x"]
            self.y += action["y"]
    
    def get_action(self, preys, predators):
        # Implement
        pass

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
