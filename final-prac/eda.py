"""
1. Download data.csv

2. Load data.csv into df and preview the first 5 rows

Understanding the Data
3. Print the shape, column names, and data types/null counts
Statistics
4. Print summary statistics for numerical columns
5. Print value counts for the 'Survived' column (normalized)

Filtering
6. What is the average 'Age' of passengers who survived (Survived == 1)?
7. What is the maximum 'Fare' paid by passengers in 3rd class (Pclass == 3) 
   who did NOT survive?

Sorting & Transformations
8. Sort by 'Fare' descending, show top 5
9. Add a new column 'FamilySize' = 'SibSp' + 'Parch'
10. Drop that column immediately after

Groupby
11. Group by 'Survived' and get mean and std of 'Age' and 'Fare' using agg()
Summary Tables
12. Build a crosstab of 'Survived' vs 'Pclass' with totals
13. Build a pivot table of average 'Fare' grouped by 'Pclass'

Visualizations
14. Plot a countplot of 'Pclass' split by 'Survived'
15. Plot a histogram of 'Age'
16. Plot a heatmap of correlations for all numeric columns

Advanced Concepts
17. Identify and handle missing values in 'Age' and 'Cabin' 
18. Remove invalid records such as negative 'Age' or zero/negative 'Fare'.
19. Convert 'BookingDate' to datetime format and extract new features (year, month, day, weekday, hour).
20. Create a new feature 'FarePerPerson' = 'Fare' / ('SibSp' + 'Parch' + 1).
21. Detect and treat outliers in 'Fare' and 'Age' using IQR or Z-score method.
22. Analyze passenger distribution across different embarkation ports ('Embarked') using visualization.
23. Identify the most common 'Ticket' numbers (to find large groups) and visualize results.
24. Perform time-based analysis on the mock 'BookingDate' to find peak booking periods (monthly trend).
25. Display the number of passengers per 'Ticket' to understand group booking behavior.
26. Prepare a Ticket-level dataset by creating aggregated features such as total fare paid, 
    total passenger count, and total family members per ticket.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data.csv')
print(df.head())

print(df.shape)
print(df.info())
print(df.describe())

print(df['Survived'].value_counts())

print(df.loc[df['Survived'] == 1, 'Age'].mean())
# or
print(df[df['Survived'] == 1]['Age'].mean())
print(df.loc[(df['Survived'] == 0) & (df['Pclass'] == 3), 'Fare'].max())

print(df.sort_values('Fare', ascending=False).head())

df['FamilySize'] = df['SibSp'] + df['Parch']
df = df.drop('FamilySize', axis=1)

print(df.groupby('Survived')[['Age', 'Fare']].agg(['mean', 'std']))

print(pd.crosstab(df['Survived'], df['Pclass'], normalize=True, margins=True))
print(df.pivot_table(['Fare'], ['Pclass'], aggfunc='mean'))

plt.figure(figsize=(16,20))
sns.countplot(data=df, x='Pclass', hue='Survived')
plt.show()

plt.figure(figsize=(16,20))
sns.histplot(data=df, x='Age', kde=True)
plt.show()

numCols = df.select_dtypes(include=['number']).columns
plt.figure(figsize=(16,20))
sns.heatmap(df[numCols].corr(), cmap='coolwarm')
plt.show()

# 17. Identify and handle missing values in 'Age' and 'Cabin'
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Cabin'] = df['Cabin'].fillna('Unknown')

# 18. Remove invalid records (negative Age or zero/negative Fare)
df = df[(df['Age'] >= 0) & (df['Fare'] > 0)]

# 19. Convert 'BookingDate' to datetime and extract features
df['BookingDate'] = pd.to_datetime(df['BookingDate'])
df['Year'] = df['BookingDate'].dt.year
df['Month'] = df['BookingDate'].dt.month
df['Day'] = df['BookingDate'].dt.day
df['Weekday'] = df['BookingDate'].dt.day_name()
df['Hour'] = df['BookingDate'].dt.hour

# 20. Create 'FarePerPerson'
df['FarePerPerson'] = df['Fare'] / (df['SibSp'] + df['Parch'] + 1)

# 21. Detect and treat outliers in 'Fare' and 'Age' using IQR
for col in ['Fare', 'Age']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = df[col].clip(lower, upper)


# 22. Analyze passenger distribution across 'Embarked' ports
plt.figure(figsize=(10,6))
sns.countplot(data=df, x='Embarked')
plt.title("Passenger Distribution by Port")
plt.show()

# 23. Identify most common 'Ticket' numbers
topTickets = df['Ticket'].value_counts().head(10)
plt.figure(figsize=(10,6))
plt.bar(topTickets.index, topTickets.values)
plt.title("Top 10 Tickets (Group Bookings)")
plt.show()

# 24. Perform time-based analysis on mock 'BookingDate'
plt.figure(figsize=(10,6))
monthlyTrends = df.groupby('Month')['PassengerId'].count()
plt.plot(monthlyTrends.index, monthlyTrends.values)
plt.title("Booking Trends (Monthly)")
plt.show()

# 25. Number of passengers per 'Ticket'
passengers_per_ticket = df.groupby('Ticket')['PassengerId'].count()
print("\nPassengers per Ticket (First 5):")
print(passengers_per_ticket.head())

# 26. Prepare a Ticket-level dataset with aggregated features
ticket_df = df.groupby('Ticket').agg(
    TotalFare = ('Fare', 'sum'),
    PassengerCount = ('PassengerId', 'count'),
    TotalSibSp = ('SibSp', 'sum'),
    TotalParch = ('Parch', 'sum')
)

print("\nTicket-level Aggregated Dataset (First 5):")
print(ticket_df.head())
