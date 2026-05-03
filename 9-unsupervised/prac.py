# Fitness Analytics - User Segmentation Task:
# 1. Load and clean fitness data (handle missing values/sensor errors).
# 2. Perform EDA: Generate statistical summaries and visualizations (distributions & relationships).
# 3. Clustering: Group similar users into categories using K-Means (unsupervised).
# 4. Visualization: Plot resulting clusters and their centroids.
# 5. Interpretation: Output cluster centers and interpret user groups based on features.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Load Dataset
df = pd.read_csv("fitness_data.csv")
print("Data Summary")
print(df.info())

# # 2. Data Cleaning
# Handle missing values (Numeric: median, Categorical: mode)
numCols = df.select_dtypes(include=['number']).columns
for col in numCols:
    df[col] = df[col].fillna(df[col].median())

catCols = df.select_dtypes(exclude=['number']).columns
for col in catCols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("\nMissing values after cleaning:", df.isnull().sum().sum())

# 3. Exploratory Data Analysis (EDA)
print("\nStatistical Summary")
print(df.describe())

# Distribution of a key variable (for example - Calories Burned)
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='Calories_Burned', kde=True)
plt.title("Distribution of Calories Burned")
plt.show()

# Relationship between two variables (for example - Steps vs Calories)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Steps', y='Calories_Burned')
plt.title("Steps vs Calories Burned")
plt.show()

# 4. K-Means Clustering (Using all numeric features for accuracy)
df = df.drop('UserID', axis=1)
dfNum = df.select_dtypes(include=['number'])
X = dfNum.values
featureNames = dfNum.columns.tolist()

# Feature Scaling
scaler = StandardScaler()
XScaled = scaler.fit_transform(X)

# Elbow Method to find K
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(XScaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('WCSS')
plt.show()

# Final Model (Assuming K=3)
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
yPred = kmeans.fit_predict(XScaled)

# 5. Visualize Clusters (Plotting first two features)
plt.figure(figsize=(10, 7))
colors = ['red', 'blue', 'green']
for i in range(3):
    plt.scatter(X[yPred == i, 0], X[yPred == i, 1], s=100, c=colors[i], label=f'Cluster {i+1}')

# Plot Centroids
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='yellow', label='Centroids')

plt.title('User Activity Segments')
plt.xlabel(featureNames[0])
plt.ylabel(featureNames[1])
plt.legend()
plt.show()

# 6. Interpretation
print("\nInterpretation")
centersDf = pd.DataFrame(centroids, columns=featureNames)
print(centersDf)

for i, center in enumerate(centroids):
    steps = center[0]
    if steps > 9000:
        label = "Athletes"
    elif steps > 5000:
        label = "Active"
    else:
        label = "Casual"
    print(f"Cluster {i+1} ({label}): Steps={steps:.0f}, Duration={center[1]:.0f}, HeartRate={center[3]:.0f}")