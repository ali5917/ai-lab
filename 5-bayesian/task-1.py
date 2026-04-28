from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# define bayesian network structure
model = DiscreteBayesianNetwork([
    ('Education', 'Interview'),
    ('Experience', 'Interview'),
    ('Interview', 'HiringDecision'),
])

# define CPDs
cpdEducation = TabularCPD(
    variable = 'Education',
    variable_card = 2,
    values = [[0.35], [0.65]],
    state_names={
        'Education': ['Low', 'High']
    }
)

cpdExperience = TabularCPD(
    variable = 'Experience',
    variable_card = 2,
    values = [[0.5], [0.5]],
    state_names={
        'Experience': ['Inexperienced', 'Experienced']
    }
)

cpdInterview = TabularCPD(
    variable = 'Interview',
    variable_card = 2,
    values = [[0.9, 0.7, 0.6, 0.2], [0.1, 0.3, 0.4, 0.8]], # assuming since question didnt specify
    evidence = ['Education', 'Experience'],
    evidence_card = [2, 2],
    state_names={
        'Interview': ['Bad', 'Good'],
        'Education': ['Low', 'High'],
        'Experience': ['Inexperienced', 'Experienced']
    }
)

cpdHiringDecision = TabularCPD(
    variable = 'HiringDecision',
    variable_card = 2,
    # assuming values since question didnt specify
    values = [[0.85, 0.2], [0.15, 0.8]], 
    evidence = ['Interview'],
    evidence_card = [2],
    state_names={
        'HiringDecision': ['NotHired', 'Hired'],
        'Interview': ['Bad', 'Good']
    }
)


# add CPDs to the model
model.add_cpds(cpdEducation, cpdExperience, cpdInterview, cpdHiringDecision)
assert model.check_model()

# query
inf = VariableElimination(model)
result = inf.query(
    variables=['HiringDecision'], 
    evidence={'Interview': 'Good'}
    )
print (result)