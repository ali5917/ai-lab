# Predict whether a customer will leave its service based on historical data.

# The dataset includes the following features:
#     MonthlyCharges, Tenure, ContractType, SupportCalls
#     Target variable: Churn

# The dataset contains:
# Categorical features
# Missing values
# Potential imbalance in target classes

# Tasks
# 1. Preprocessing
# 2. Model Training
# Train at least two classification models

# 3. Evaluation & Comparison
# Output accuracy metrics for both training and testing phases
# Compare model performance
# Highlight which model is more suitable for this problem

# 4. Additional Considerations
# Handle class imbalance or overfitting if observed during evaluation

from sklearn.model_selection import train_test_split   
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix


df = pd.read_csv("customer_churn.csv")

# print(df.info())
# print(df.isna().sum().sum())

# cleaning
df = df.drop('CustomerID', axis=1)
numCols = df.select_dtypes(include=['number']).columns
catCols = df.select_dtypes(exclude=['number']).columns

for col in numCols:
    df[col] = df[col].fillna(df[col].median())

for col in catCols:
    df[col] = df[col].fillna(df[col].mode()[0])

# encoding
le = LabelEncoder()
for col in catCols:
    df[col] = le.fit_transform(df[col])
    
numCols = df.select_dtypes(include=['number']).columns

# SVM
X = df[numCols].drop('Churn', axis=1)
y = df['Churn']

# scaling
scaler = StandardScaler()
scaledX = scaler.fit_transform(X)

# train/test split
Xtrain, Xtest, ytrain, ytest = train_test_split(scaledX, y, test_size=0.2, random_state=42, stratify=y)

svm = SVC(kernel='rbf', C=1, gamma='scale', class_weight='balanced')
svm.fit(Xtrain, ytrain)
yPred1 = svm.predict(Xtest)

print("\nEvaluation of SVM")
print("Training Accuracy: ", svm.score(Xtrain, ytrain) * 100)
print("Testing Accuracy: ", accuracy_score(ytest, yPred1) * 100)

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

dt = DecisionTreeClassifier(random_state=42, class_weight='balanced')
dt.fit(Xtrain, ytrain)
yPred2 = dt.predict(Xtest)

print("\nEvaluation of Decision Tree Classifier")
print("Training Accuracy: ", dt.score(Xtrain, ytrain) * 100)
print("Testing Accuracy: ", accuracy_score(ytest, yPred2) * 100)