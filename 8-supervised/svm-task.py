# Customer Churn Prediction -- You are working for a telecom company.
# Your task is to predict whether a customer will churn (leave the service) or not.
# The dataset includes: Monthly charges, Contract type, Tenure, Internet service type, Customer support calls

# Perform the following tasks:
# Clean the dataset (handle missing values, detect and treat outliers)
# Convert categorical variables into numerical form
# Perform feature scaling if needed
# Split the dataset into training and testing sets
# Train a classification model (SVM)
# Extract rules or feature importance from the model
# Evaluate performance using confusion matrix, accuracy, precision, recall, and F1-score
# Predict whether a new customer will churn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score,
    ConfusionMatrixDisplay
)

# Load Dataset
df = pd.read_csv("churn.csv")

# Study dataset
print(df.info()) 

# Clean Dataset

# drop id, not a feature 
df = df.drop("customerID", axis=1)
  
# handle TotalCharges - should be numbers but is str from df.info() - possibly contain " "
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# fill missing values (numeric - median, categorical - mode)
numCols = df.select_dtypes(include=['number']).columns
for col in numCols:
    df[col] = df[col].fillna(df[col].median())

catCols = df.select_dtypes(exclude=['number']).columns
for col in catCols:
    df[col] = df[col].fillna(df[col].mode()[0])

# treat outliers using IQR (only to numeric columns)
def treatOutliers(df, col):
    Q1  = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = df[col].clip(lower, upper)

for col in numCols:
    treatOutliers(df, col)

print("\nMissing values after cleaning:", df.isnull().sum().sum())

# Encode Categorical Values

# Encoding all text columns to numbers
le = LabelEncoder()
textCols = df.select_dtypes(include=["str", "object"]).columns
for col in textCols:
    df[col] = le.fit_transform(df[col])

# update numCols to include newly encoded numeric columns
numCols = df.select_dtypes(include=['number']).columns

# Feature Scaling

X = df.drop("Churn", axis=1)
y = df["Churn"]
featureNames = X.columns.tolist()

scaler = StandardScaler()
XScaled = scaler.fit_transform(X)
XScaled = pd.DataFrame(XScaled, columns=featureNames)

# Train/Test Split
XTrain, XTest, yTrain, yTest = train_test_split(XScaled, y, test_size=0.2, random_state=42, stratify=y)

# Train SVM Model
svm = SVC(kernel="rbf", C=1, gamma="scale", random_state=42)
svm.fit(XTrain, yTrain)
yPred = svm.predict(XTest)

# Feature Importance (Correlation)

featureCorr = df[numCols].corr()['Churn'].drop('Churn')       # exclude itself
topFeatures = featureCorr.sort_values(ascending=False)

print("\nTop Features by Correlation with Churn:")
print(topFeatures)

plt.figure(figsize=(12, 10))
sns.heatmap(df[numCols].corr(), cmap='coolwarm')
plt.title("Correlation Matrix of Features")
plt.show()

# Evaluation
print("\nEvaluation")
print("Accuracy :", accuracy_score(yTest, yPred))
print("Precision:", precision_score(yTest, yPred, zero_division=0))
print("Recall   :", recall_score(yTest, yPred, zero_division=0))
print("F1 Score :", f1_score(yTest, yPred, zero_division=0))

cm = confusion_matrix(yTest, yPred)
print("\nConfusion Matrix")
print(cm)

# Predict new customer 
# Creating a dummy customer with median values (as a DataFrame to keep feature names)
newCustDf = pd.DataFrame([X.median()], columns=featureNames)
newCustScaled = scaler.transform(newCustDf)

pred = svm.predict(newCustScaled)[0]

label = "CHURN" if pred == 1 else "NO CHURN"
print(f"\nNew Customer: {label}")