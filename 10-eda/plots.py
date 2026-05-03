# Histogram (Seaborn) - Used to see the distribution of a single numeric variable
sns.histplot(data=df, x='Calories_Burned', kde=True)
sns.histplot(data=df, x='SalePrice', bins=100, kde=True)

# Scatter Plot (Seaborn) - Used to see the relationship between two numeric variables
sns.scatterplot(data=df, x='Steps', y='Calories_Burned')

# Count Plot (Seaborn) - Used to see frequencies of categorical variables
sns.countplot(data=df, x='MSZoning')
sns.countplot(data=df, x='CentralAir', hue='HighPrice')

# Heatmap (Seaborn) - Used to see correlation between all numeric features
sns.heatmap(dfNum.corr(), cmap='coolwarm')

# Histogram Grid (Pandas) - Used for a quick overview of all numeric distributions at once
dfNum.hist(figsize=(16, 20), bins=50)

# Line Plot (Matplotlib) - Used for Elbow Method in Unsupervised Learning
plt.plot(range(1, 11), wcss) 

# Scatter Plot (Matplotlib) - Used for plotting Clusters & Centroids using Numpy arrays
plt.scatter(X[:, 0], X[:, 1], c=yPred, cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='yellow', label='Centroids')