from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
diabetes = datasets.load_diabetes()
X = diabetes.data       # 2d array of features
y = diabetes.target     # 1d array of targets

# Split data
XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
lr = LinearRegression()                 # defines model
lr.fit(XTrain, yTrain)                  # trains model

# Make predictions
yPred = lr.predict(XTest)

# Evaluate the model 
print("LR Accuracy")
r2 = r2_score(yTest, yPred)
accuracy = r2 * 100
print(f"Accuracy: {accuracy:.2f}%")
print(f"MSE:", {mean_squared_error(yTest, yPred)})