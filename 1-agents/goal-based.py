# goal-based agent simulation for a single-room vacuum world

class GoalBasedAgent:
    def __init__(self):
        self.goal = 'Clean' # initialize the goal

    def formulate_goal(self, percept):
    # decide the goal based on current percept
        if percept == 'Dirty':
            self.goal = 'Clean'
        else:
            self.goal = 'No action needed'

    def act(self, percept):
        # formulate goal, then act accordingly
        self.formulate_goal(percept)
        if self.goal == 'Clean':
            return 'Clean the room'
        else:
            return 'Room is clean'


class Environment:
    def __init__(self, state='Dirty'):
        self.state = state

    def get_percept(self):
        return self.state

    def clean_room(self):
        self.state = 'Clean'


def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)
        print(f"Step {step + 1}: Percept - {percept}, Action - {action}")

        if percept == 'Dirty':
            environment.clean_room()

agent = GoalBasedAgent()
environment = Environment()

run_agent(agent, environment, 5)