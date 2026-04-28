# model-based reflex agent for a single-room vacuum world

class Environment:
    def __init__(self, state='Dirty'):
        self.state = state

    def get_percept(self):
        return self.state

    def clean_room(self):
        self.state = 'Clean'

class ModelBasedAgent:
    def __init__(self):
        self.model = {} # stores a simple model of the environment - {'current': 'Dirty'}

    def update_model(self, percept):
        # update internal model with the current percept
        self.model['current'] = percept

    def predict_action(self):
        # decide action based on the internal model
        if self.model['current'] == 'Dirty':
            return 'Clean the room'
        else:
            return 'Room is clean'

    def act(self, percept):
        # update model, then decide action
        self.update_model(percept)
        return self.predict_action()


def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)
        print(f"Step {step + 1}: Percept - {percept}, Action - {action}")

        if percept == 'Dirty':
            environment.clean_room()

agent = ModelBasedAgent()
environment = Environment()

run_agent(agent, environment, 5)