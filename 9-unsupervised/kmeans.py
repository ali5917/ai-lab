# K-Means Clustering on Mall Customers Dataset
# Goal: Group customers based on Annual Income and Spending Score

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load Dataset
df = pd.read_csv("Mall_Customers.csv")

print("Dataset shape:", df.shape)
print(df.head())

# Extract Features
# We use Annual Income (index 3) and Spending Score (index 4)
X = df.iloc[:, [3, 4]].values

# Feature Scaling (Important for K-Means distance math)
scaler = StandardScaler()
XScaled = scaler.fit_transform(X)

# Elbow Method to find optimal K
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, random_state=42)
    kmeans.fit(XScaled)
    wcss.append(kmeans.inertia_)
print(wcss)

# Train Final KMeans Model (K=5 chosen from elbow)
kmeans = KMeans(n_clusters=5, init='k-means++', n_init=10, random_state=42)
y_kmeans = kmeans.fit_predict(XScaled)

# Visualize Clusters
plt.figure(figsize=(10, 7))

colors = ['red', 'blue', 'green', 'cyan', 'magenta']
for i in range(5):
    plt.scatter(
        X[y_kmeans == i, 0], X[y_kmeans == i, 1], 
        s=100, c=colors[i], 
        label=f'Cluster {i+1}'
    )

# Plot Centroids (Inverse scale to plot on original values)
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='yellow', label='Centroids', edgecolors='black')

plt.title('Clusters of Customers')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()