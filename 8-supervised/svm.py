from sklearn import datasets
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
iris = datasets.load_iris()
X = iris.data       # 2d array of features 
y = iris.target     # 1d array of labels

# Convert to binary classification problem
y = (y == 0).astype(int) 

# Split data
XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train SVM model
svm = SVC(kernel='rbf', C=1, gamma='scale', random_state=42)      # defines model
svm.fit(XTrain, yTrain)                                           # trains model

# Make predictions
yPred = svm.predict(XTest)

# Evaluate the model
print("SVM Accuracy:", accuracy_score(yTest, yPred))