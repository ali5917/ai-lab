from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# define bayesian network structure
model = DiscreteBayesianNetwork([
    ('AdExposure', 'WebsiteExperience'),
    ('WebsiteExperience', 'Purchase'),
    ('ProductPrice', 'Purchase'),
])

# define CPDs
cpdAdExposure = TabularCPD(
    variable='AdExposure',
    variable_card=2,
    values=[[0.4], [0.6]],
    state_names={'AdExposure': ['No', 'Yes']}
)

cpdWebsiteExperience = TabularCPD(
    variable='WebsiteExperience',
    variable_card=2,
    values=[[0.6, 0.2],   
            [0.4, 0.8]],  
    evidence=['AdExposure'],
    evidence_card=[2],
    state_names={
        'WebsiteExperience': ['Poor', 'Good'],
        'AdExposure': ['No', 'Yes']
    }
)

cpdProductPrice = TabularCPD(
    variable='ProductPrice',
    variable_card=2,
    values=[[0.55], [0.45]],
    state_names={'ProductPrice': ['Low', 'High']}
)

cpdPurchase = TabularCPD(
    variable='Purchase',
    variable_card=2,
    # assuming values since question didnt specify
    values=[[0.6, 0.9, 0.15, 0.4], 
            [0.4, 0.1, 0.85, 0.6]],
    evidence=['WebsiteExperience', 'ProductPrice'],
    evidence_card=[2, 2],
    state_names={
        'Purchase': ['No', 'Yes'],
        'WebsiteExperience': ['Poor', 'Good'],
        'ProductPrice': ['Low', 'High']
    }
)

# add CPDs to the model
model.add_cpds(cpdAdExposure, cpdWebsiteExperience, cpdProductPrice, cpdPurchase)
assert model.check_model()

# query
inf = VariableElimination(model)
result = inf.query(
    variables=['Purchase'],
    evidence={'AdExposure': 'Yes', 'ProductPrice': 'Low'}
)
print(result)