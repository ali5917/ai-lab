# K-Means Steps 

# 1. Load Dataset: Read CSV using pandas.

# 2. Select Features: 
#    - Option A: X = df[['Col1', 'Col2']].values (Simple 2D)
#    - Option B: X = df.select_dtypes(include=['number']).drop('ID', axis=1).values (Multi-feature)

# 3. Scale Features: Use StandardScaler (K-Means needs distance math).

# 4. Elbow Method: Loop K, fit(XScaled), record inertia_.

# 5. Final Model: Fit with best K, get yKmeans labels.

# 6. Visualization (2D Plot of Multi-feature clusters):
#    - Pick two columns to plot (usually index 0 and 1).
#    - plt.scatter(X[yKmeans == i, 0], X[yKmeans == i, 1], s=100, c=colors[i])

# 7. Centroids:
#    - centroids = scaler.inverse_transform(kmeans.cluster_centers_)
#    - plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='yellow')