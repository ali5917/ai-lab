# Loan Approval Classification -- You are working for a bank to automate loan approvals. 
# The dataset contains customer details
# such as income, employment status, credit score, loan amount, and marital status. 

# Classify whether a loan should be approved (1) or rejected (0).
# Perform the following tasks:
# Preprocess the dataset:
# Handle missing values
# Encode categorical variables (e.g., employment status, marital status)
# Perform feature selection to identify key factors influencing loan approval
# Train a classification model (Decision Tree)
# Split the dataset into training and testing sets
# Evaluate the model using metrics like accuracy, precision, recall, and F1-score
# Use the model to predict loan approval for a new applicant

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load Dataset
df = pd.read_csv("customers.csv")

# Study dataset
print(df.info())

# Clean Dataset

# drop id, not a feature 
df = df.drop("applicant_id", axis=1)

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

# Feature Selection (Correlation)
featureCorr = df[numCols].corr()['loan_approved'].drop('loan_approved')  # exclude itself
topFeatures = featureCorr.sort_values(ascending=False)

print("\nTop Features by Correlation with Loan Approval:")
print(topFeatures)

plt.figure(figsize=(12, 10))
sns.heatmap(df[numCols].corr(), cmap='coolwarm')
plt.title("Correlation Matrix of Features")
plt.show()

# Train/Test Split
X = df.drop("loan_approved", axis=1)
y = df["loan_approved"]

XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Decision Tree Model
dt = DecisionTreeClassifier(random_state=42)    # defines model
dt.fit(XTrain, yTrain)                          # trains model
yPred = dt.predict(XTest)

# Evaluation
print("\nEvaluation")
print(f"Training Accuracy: {dt.score(XTrain, yTrain) * 100:.2f}%")
print(f"Testing Accuracy: {accuracy_score(yTest, yPred) * 100:.2f}%")
print("Precision:", precision_score(yTest, yPred, zero_division=0))
print("Recall:", recall_score(yTest, yPred, zero_division=0))
print("F1 Score:", f1_score(yTest, yPred, zero_division=0))

# Predict new applicant
featureNames = X.columns.tolist()

# Method 1: Manual entry (provide values for all features in X)
# newApplicantValues = [ ... ] 
# newApplicantDf = pd.DataFrame([newApplicantValues], columns=featureNames)

# Method 2: Using median values
newApplicantDf = pd.DataFrame([X.median()], columns=featureNames)

pred = dt.predict(newApplicantDf)[0]
label = "APPROVED" if pred == 1 else "REJECTED"
print(f"\nNew Applicant (Median Profile): {label}")