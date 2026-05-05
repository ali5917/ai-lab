# A fitness analytics company has collected a dataset containing the following user activity features:
#     Steps, Workout Duration, Calories Burned, Heart Rate, Sleep Hours    
# The dataset contains missing values and potential inconsistencies due to sensor errors.

# Clean the dataset by handling missing values and fixing inconsistencies caused by sensor errors.

# Explore patterns in user behavior and generate the following visualizations:
#     Distributions of individual features
#     Relationships between variables

# Unsupervised Clustering
#     Group users into distinct behavioral categories without using any predefined labels.

import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

df = pd.read_csv("fitness_data.csv")

# cleaning
df = df.drop("UserID", axis=1)

# print(df.info())
# print(df.isna().sum().sum())

numCols = df.select_dtypes(include=['number']).columns
catCols = df.select_dtypes(exclude=['number']).columns

for col in numCols:
    df[col] = df[col].fillna(df[col].median())

for col in catCols:
    df[col] = df[col].fillna(df[col].mode()[0])

# print(df.isna().sum().sum())

# encoding category variables
le = LabelEncoder()
for col in catCols:
    df[col] = le.fit_transform(df[col])    

numCols = df.select_dtypes(include=['number']).columns

# exploring patterns in behaviour
# print("Summary: ")
# print(df.describe())

# distribution of features
# df[numCols].hist(figsize=(16, 20), bins=50)
# plt.suptitle("Histograms of all features")
# plt.show()

# correlation of features
# plt.figure(figsize=(16,20))
# sns.heatmap(df[numCols].corr(), cmap='coolwarm')
# plt.title("Correlation of Features")
# plt.show()

# relation of two features
# plt.figure(figsize=(16,20))
# sns.scatterplot(data=df, x='Steps', y='Calories_Burned')
# plt.show()

X = df[numCols].values
scaler = StandardScaler()
scaledX = scaler.fit_transform(X)

wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(scaledX)
    wcss.append(kmeans.inertia_)

plt.plot(range(1,11), wcss)
plt.show()

# choosing 4
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
yPred = kmeans.fit_predict(scaledX)

# visualizing clusters (2 features)
plt.figure(figsize=(16, 20))
colors = ["red", "blue", "green", "pink"]
for i in range(4):
    plt.scatter(X[yPred==i, 0], X[yPred==i, 1], s = 100, c = colors[i])

centroids = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='yellow') 

plt.title('User Activity')
plt.show()   