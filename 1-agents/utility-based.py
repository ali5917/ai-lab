# utility-based agent simulation for a single-room vacuum world

class Environment:
    def __init__(self, state='Dirty'):
        self.state = state

    def get_percept(self):
        return self.state

    def clean_room(self):
        self.state = 'Clean'

class UtilityBasedAgent:
    def __init__(self):
        # utility values for each percept
        self.utility = {'Dirty': -10, 'Clean': 10}

    def calculate_utility(self, percept):
        # return the utility value of the current percept
        return self.utility[percept]

    def select_action(self, percept):
        # define possible actions
        actions = ['Clean the room', 'Do nothing']
        best_action = None
        max_utility = -float('inf')

        for action in actions:
            # simulate result of action
            if action == 'Clean the room':
                resulting_state = 'Clean'
            else:
                resulting_state = percept  # nothing changes

            utility = self.utility[resulting_state]

            if utility > max_utility:
                max_utility = utility
                best_action = action

        return best_action


    def act(self, percept):
        # select action
        action = self.select_action(percept)
        return action

def run_agent(agent, environment, steps):
    total_utility = 0
    for step in range(steps):
        percept = environment.get_percept()
        action = agent.act(percept)
        utility = agent.calculate_utility(percept)
        print(f"Step {step + 1}: Percept - {percept}, Action - {action}, Utility - {utility}")

        total_utility += utility

        if percept == 'Dirty':
            environment.clean_room()

    print("Total Utility:", total_utility)

agent = UtilityBasedAgent()
environment = Environment()

run_agent(agent, environment, 5)


# utility-Based Agent for selecting movies

class Environment:
    def __init__(self, movies):
        self.movies = movies # dictionary of movie names -> review scores

    def get_percept(self):
        return self.movies


class UtilityBasedAgent:
    def __init__(self, mood_factor = 0.7):
        # mood_factor scales the importance of reviews
        self.mood_factor = mood_factor

    def utility(self, review):
        # compute utility based on review score and mood factor
        return review * self.mood_factor

    def act(self, percept):
        best_movie = None
        best_utility = -float('inf')

        for movie, review in percept.items():
            movie_utility = self.utility(review)
            if movie_utility > best_utility:
                best_movie = movie
                best_utility = movie_utility

        return best_movie


def run_agent(agent, environment):
    percept = environment.get_percept()
    best_choice = agent.act(percept)
    print(f"Available Movies: {percept}")
    print(f"Best Movie to Watch: {best_choice}")

movies = {'Movie A': 7, 'Movie B': 9, 'Movie C': 5}
environment = Environment(movies)
agent = UtilityBasedAgent(mood_factor = 0.8)

run_agent(agent, environment)