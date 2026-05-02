from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
iris = datasets.load_iris()
X = iris.data       # 2d array of features
y = iris.target     # 1d array of labels

# Split data
XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Decision Tree model
dt = DecisionTreeClassifier(random_state=42)    # defines model
dt.fit(XTrain, yTrain)                          # trains model

# Make predictions
yPred = dt.predict(XTest)

# Evaluate the model
trainAccuracy = dt.score(XTrain, yTrain) * 100
testAccuracy  = accuracy_score(yTest, yPred) * 100

print(f"Training Accuracy: {trainAccuracy:.2f}%")
print(f"Testing Accuracy : {testAccuracy:.2f}%")