# Student Performance Prediction - You are working as a data scientist for a university. 
# Predict a student's final exam score (continuous variable) based on factors 
# such as study hours, attendance, previous grades, participation in class, and internet usage.

# Perform the following tasks:
# Clean the dataset and handle missing values (e.g., missing attendance or study hours).
# Encode categorical variables (e.g., participation level: Low, Medium, High).
# Identify the most important features affecting student performance.
# Train a regression model to predict the final score.
# Evaluate the model using appropriate metrics (e.g., MAE, RMSE, R2).
# Predict the final score for a new student given their features.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load Dataset
df = pd.read_csv("students.csv")

# Study dataset
print(df.info())

# Clean Dataset

# drop id, not a feature
df = df.drop("student_id", axis=1)

# fill missing values (numeric - median, categorical - mode)
numCols = df.select_dtypes(include=['number']).columns
for col in numCols:
    df[col] = df[col].fillna(df[col].median())

catCols = df.select_dtypes(exclude=['number']).columns
for col in catCols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("\nMissing values after cleaning:", df.isnull().sum().sum())

# Encode Categorical Values

le = LabelEncoder()
textCols = df.select_dtypes(include=["str", "object"]).columns
for col in textCols:
    df[col] = le.fit_transform(df[col])

# update numCols to include newly encoded columns
numCols = df.select_dtypes(include=['number']).columns

# Feature Importance (Correlation)

featureCorr = df[numCols].corr()['final_score'].drop('final_score')  # exclude itself
topFeatures = featureCorr.sort_values(ascending=False)

print("\nTop Features by Correlation with Final Score:")
print(topFeatures)

plt.figure(figsize=(12, 10))
sns.heatmap(df[numCols].corr(), cmap='coolwarm')
plt.title("Correlation Matrix of Features")
plt.show()

# Train/Test Split
X = df.drop("final_score", axis=1)
y = df["final_score"]

XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression Model
lr = LinearRegression()             # defines model
lr.fit(XTrain, yTrain)              # trains model
yPred = lr.predict(XTest)

# Evaluation
print("\nEvaluation")
r2 = r2_score(yTest, yPred)
print(f"Accuracy (R2): {r2 * 100:.2f}%")
print("MAE:", mean_absolute_error(yTest, yPred))
print("RMSE:", mean_squared_error(yTest, yPred) ** 0.5)

# Predict new student
featureNames = X.columns.tolist()

# Method 1: Manual entry (provide values for all features in X)
# newStudentValues = [ ... ] 
# newStudentDf = pd.DataFrame([newStudentValues], columns=featureNames)

# Method 2: Using median values
newStudentDf = pd.DataFrame([X.median()], columns=featureNames)

predictedScore = lr.predict(newStudentDf)[0]
print(f"\nNew Student (Median Profile): Predicted Score: {predictedScore:.1f}")