from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# define bayesian network structure
model = DiscreteBayesianNetwork([
    ('Fault', 'CarWontStart'),
    ('Fault', 'DimLights'),
    ('Fault', 'StrangeNoise'),
])

# define CPDs
cpdFault = TabularCPD(
    variable = 'Fault',
    variable_card = 2,
    values = [[0.4], [0.6]],
    state_names={
        'Fault': ['EngineIssue', 'BatteryIssue']
    }
)

cpdCarWontStart = TabularCPD(
    variable = 'CarWontStart',
    variable_card = 2,
    values = [[0.15, 0.3], [0.85, 0.7]],
    evidence = ['Fault'],
    evidence_card = [2],
    state_names={
        'CarWontStart': ['No', 'Yes'],
        'Fault': ['EngineIssue', 'BatteryIssue']
    }
)

cpdDimLights = TabularCPD(
    variable = 'DimLights',
    variable_card = 2,
    values =  [[0.7, 0.2], [0.3, 0.8]],
    evidence = ['Fault'],
    evidence_card = [2],
    state_names={
        'DimLights': ['No', 'Yes'],
        'Fault': ['EngineIssue', 'BatteryIssue']
    }
)

cpdStrangeNoises = TabularCPD(
    variable = 'StrangeNoise',
    variable_card = 2,
    values = [[0.25, 0.8], [0.75, 0.2]],
    evidence = ['Fault'],
    evidence_card = [2],
    state_names={
        'StrangeNoise': ['No', 'Yes'],
        'Fault': ['EngineIssue', 'BatteryIssue']
    }
)

# add CPDs to the model
model.add_cpds(cpdFault, cpdCarWontStart, cpdDimLights, cpdStrangeNoises)
assert model.check_model()

# query
inf = VariableElimination(model)
result = inf.query(
    variables=['Fault'], 
    evidence={'CarWontStart': 'Yes', 'DimLights': 'Yes', 'StrangeNoise': 'Yes'}
    )
print (result)