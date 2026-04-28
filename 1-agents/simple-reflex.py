import random

# cleans a room based on current percept, with an environment where state changes randomly each step

class Environment:
    def __init__(self):
        self.state = random.choice(['Dirty', 'Clean'])

    def get_percept(self):
        return self.state

    def clean_room(self):
        self.state = 'Clean'


class SimpleReflexAgent:
    def __init__(self):
        pass

    def act(self, percept):
        if percept == 'Dirty':
            return 'Clean the room'
        
        else:
            return 'Room is already clean'


def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)

        print(f"Step {step + 1}: Percept - {percept}, Action - {action}")

        if percept == 'Dirty':
            environment.clean_room()

        environment.state = random.choice(['Dirty', 'Clean'])

agent = SimpleReflexAgent()
environment = Environment()

run_agent(agent, environment, 5)

# in a 3x3 grid vacuum world

class Environment:
    def __init__(self):
        self.grid = [
            'Clean', 'Dirty', 'Clean',
            'Clean', 'Dirty', 'Dirty',
            'Clean', 'Clean', 'Clean'
        ]

    def get_percept(self, position):
        return self.grid[position]

    def clean_room(self, position):
        self.grid[position] = 'Clean'

    def display_grid(self, agent_position):
        print("\nCurrent Grid State:")
        grid_with_agent = self.grid[:]  # Copy the grid
        grid_with_agent[agent_position] = "A"  # Place the agent at current position
        for i in range(0, 9, 3):
            print(" | ".join(grid_with_agent[i:i + 3]))
        print()  


class SimpleReflexAgent:
    def __init__(self):
        self.position = 0  

    def act(self, percept, grid):
        if percept == 'Dirty':
            grid[self.position] = 'Clean'
            return 'Clean the room'
        else:
            return 'Room is clean'

    def move(self):
        if self.position < 8:
            self.position += 1


def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept(agent.position)
        action = agent.act(percept, environment.grid)
        print(f"Step {step + 1}: Position {agent.position} -> Percept - {percept}, Action - {action}")
        
        environment.display_grid(agent.position)  
        
        agent.move()

agent = SimpleReflexAgent()
environment = Environment()

run_agent(agent, environment, 9)