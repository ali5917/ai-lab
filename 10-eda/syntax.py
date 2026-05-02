import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 1. Loading and Viewing Data

df = pd.read_csv('house_prices_practice.csv')
print(df.head())       # first 5 rows
print(df[12:15])       # rows 12 to 14
print(df[-1:])         # last row

# 2. Understanding the Data Structure

print(df.shape)    # rows × columns
print(df.columns)  # lists all column names
print(df.info())   # data types + non-null counts

# 3. Changing Feature Types

df['LotArea'] = df['LotArea'].astype('float64')

# 4. Basic Data Overview/Statistics (mean, std, min, max...)

print(df.describe())  

# For categorical/boolean features, value_counts() is more useful:
print(df['LotShape'].value_counts())                  # raw counts
print(df['LotShape'].value_counts(normalize=True))    # proportions

# 5. Sorting Data

# Sort by one column (descending)
print(df.sort_values(by='Id', ascending=False).head())
# Sort by multiple columns
print(df.sort_values(by=['LotFrontage', 'YrSold'], ascending=[True, False]).head())

# 6. Indexing and Retrieving Data

# Single Column Access
print(df['SalePrice'].mean())   # average sale price

# Boolean indexing — filter rows by condition: 
# average of all features for houses with central air - numerical_only=True needed for full dataframe
print(df[df['CentralAir'] == 'Y'].mean(numeric_only=True))   

# average price of houses with central air
print(df[df['CentralAir'] == 'Y']['SalePrice'].mean()) 

# maximum price for houses with central air and more than 1 full bath
print(df[(df['CentralAir'] == 'Y') & (df['FullBath'] > 1)]['SalePrice'].max()) 

# loc — by label name (inclusive on both ends)
print(df.loc[0:5, 'MSZoning':'LotArea']) 

# iloc — by position number (end excluded)
print(df.iloc[0:4, 0:3])

# 7. Applying Functions
# apply() — apply a function to every column or row:
print(df.select_dtypes(include=[np.number]).apply(np.max))        # max of every column
print(df.select_dtypes(include=[np.number]).apply(np.max, axis=1)) # max of every row

# Lambda functions — small anonymous one-line functions:
# Select all houses in neighborhoods starting with 'N' (like North Ames, Northwest Ames)
print(df[df['Neighborhood'].apply(lambda x: x[0] == 'N')].head())

# map() — replace values using a dictionary:
d = {'N': False, 'Y': True}
df['CentralAirMapped'] = df['CentralAir'].map(d)

# replace() — same idea, slightly different syntax:
# df = df.replace({'CentralAir': d})

# 8. Grouping Data
columnsToShow = ['SalePrice', 'LotArea']
print(df.groupby(['SaleCondition'])[columnsToShow].agg([np.mean, np.std, np.min, np.max]))

# groupby() works in three steps:
# 1. Split the data by the grouping column's values
# 2. Select the columns you care about
# 3. Apply an aggregation function (mean, std, min, max, etc.)

# 9. Summary Tables
# crosstab — contingency table between two variables:
print(pd.crosstab(df['MSZoning'], df['Street']))
print(pd.crosstab(df['MSZoning'], df['Street'], margins=True))  # adds totals
print(pd.crosstab(df['MSZoning'], df['LotShape'], normalize=True))   # shows proportions

# pivot_table:
print(df.pivot_table(['SalePrice', 'LotArea'], ['MSZoning'], aggfunc='mean'))
# Parameters: values (what to compute), index (group by), aggfunc (how to aggregate).

# 10. DataFrame Transformations
# Adding columns:
# Method 1: insert at a specific position (end in this case due to loc(len(df.columns)))
totalBath = df['FullBath'] + df['HalfBath']
df.insert(loc=len(df.columns), column='TotalBath', value=totalBath)
# Method 2: direct assignment at end (simpler)
df['PricePerSqFt'] = df['SalePrice'] / df['LotArea']

# Deleting columns or rows:
# axis=1 → delete columns; axis=0 or nothing → delete rows
# df.drop(['PricePerSqFt', 'TotalBath'], axis=1, inplace=True)  # drop columns - inplace, modifies original df
# print(df.drop([1, 2]).head())                                 # drop rows - not inplace, returns a new df


# 11. Predicting "High Price" — Practical Analysis
# Pattern 1: Central Air + High Price
# Create a 'HighPrice' binary column (1 if price > 200k, else 0)
df['HighPrice'] = (df['SalePrice'] > 200000).astype('int')

# Finding: Houses with Central Air are much more likely to be in the "High Price" category.
print(pd.crosstab(df['HighPrice'], df['CentralAir'], margins=True))

# Pattern 2: Overall Quality + High Price
# Finding: Houses with quality > 7 are almost always in the High Price category.
print(pd.crosstab(df['HighPrice'], df['OverallQual'], margins=True))

# Combining both signals:
print(pd.crosstab((df['OverallQual'] > 7) & (df['CentralAir'] == 'Y'), df['HighPrice']))

# 12. Data Cleaning — Missing Values
# Drop columns with too many missing values (threshold: 30% non-null)
validCols = []
for col in df.columns:
    nonNullCount = df[col].count()
    totalRows = len(df)
    
    if (nonNullCount / totalRows) >= 0.3:
        validCols.append(col)

df = df[validCols]
# df.drop('Id', axis=1, inplace=True) # Already removed if previously run

# 13. Analyzing the Target Variable (SalePrice)
# Finding: Prices are right-skewed — most homes cluster around 100k–200k.
print("*** Dataset Description *** ")
print(df['SalePrice'].describe())

plt.figure(figsize=(9,8))
sns.histplot(x='SalePrice', data=df, bins=100, kde=True)
plt.title('Histogram of SalePrice')
plt.xlabel('SalePrice')
plt.ylabel('Frequency')
plt.show()

# 14. Selecting Numerical Features
dfNum = df.select_dtypes(include=['number'])
print(" *** Numeric values  ***")
print(dfNum.head())

dfNum.hist(figsize=(16, 20), bins=50, xlabelsize=8, ylabelsize=8)
plt.suptitle('Histogram of Numeric Values')
plt.show()

# 15. Correlation Analysis
dfNum = df.select_dtypes(include=['number'])
dfNumCorr = dfNum.corr()['SalePrice'][:-1] # exclude itself
goldenFeaturesList = dfNumCorr[abs(dfNumCorr) > 0.5].sort_values(ascending=False)

print("\nSalePrice Golden Features (High Correlation > 0.5)")
print(goldenFeaturesList)

# Visualizing Correlation Heatmap --- sns.heatmap() for matrix charts
plt.figure(figsize=(12, 10))
sns.heatmap(dfNum.corr(), cmap='coolwarm')
plt.title("Correlation Matrix of Numerical Features")
plt.show()

# 16 Visualizing Categorical Distributions (countplot)
sns.countplot(x='MSZoning', data=df)
plt.title('Frequency of Houses by Zoning')
plt.show()

# countplot with a hue (color-coded by another variable):
# Already created HighPrice in section 11
sns.countplot(x='CentralAir', hue='HighPrice', data=df)
plt.title('High Price Houses vs Central Air')
plt.show()

# 17. Final Exam "Must-Knows"

# --- Checking Unique Values ---
print(df.nunique())                  # How many unique values in every column?
print(df['Neighborhood'].unique())   # List the actual unique names in one column

# --- Handling Missing Values (Imputation) ---
# Instead of dropping, fill missing numbers with the Mean or Median:
df['LotFrontage'] = df['LotFrontage'].fillna(df['LotFrontage'].mean())

# Fill missing text/categories with the "Mode" (most common value):
df['Electrical'] = df['Electrical'].fillna(df['Electrical'].mode()[0])

# --- Renaming Columns ---
df.rename(columns={'YrSold': 'Year_Sold', 'MoSold': 'Month_Sold'}, inplace=True)