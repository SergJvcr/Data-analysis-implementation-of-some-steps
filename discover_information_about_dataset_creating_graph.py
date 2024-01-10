import pandas as pd
import matplotlib.pyplot as plt

# Importing the data.
companies = pd.read_csv("google_data_analitics\\Unicorn_Companies.csv")

# Data exploration.
print(companies.head(10))
print('The size of the dataset:', companies.size)
print('The shape of the dataset:', companies.shape)

# Get basic information about the dataset.
print(companies.info())

# Finding descriptive statistics.
print(companies.describe())

# Converting the Date Joined column to datetime.
# This is an important step in data cleaning, as it makes the data in this column
# easier to use in tasks you may encounter. To name a few examples, 
# you may need to compare "date joined" between companies or determine 
# how long it took a company to become a unicorn. 
# Having "date joined" in datetime form would help you complete such tasks.
companies['Date Joined'] = pd.to_datetime(companies['Date Joined'])
# Use .info() to confirm that the update actually took place
print(companies.info())

# Create a new column: 'Year Joined'.
companies['Year Joined'] = companies['Date Joined'].dt.year # you can extract month and day
# To demonstrate the new column.
print(companies.head(10))

# Results and evaluation.
# Take a sample of the data.
# It is not necessary to take a sample of the data in order 
# to conduct the visualizations and EDA that follow. 
# But you may encounter scenarios in the future where you will need 
# to take a sample of the data due to time and resource limitations.
companies_sampled = companies.sample(n=50,  random_state=42)

# Visualize the time it took companies to reach unicorn status.
# Prepare data for plotting
companies_sampled['to be a unicorn'] = companies_sampled['Year Joined'] - companies_sampled['Year Founded']
grouped_data_for_plotting = (companies_sampled[['Industry', 'to be a unicorn']]
           .groupby('Industry')
           .max()
           .sort_values(by="to be a unicorn", ascending=True))

print(grouped_data_for_plotting)

# Create bar plot
# with the various industries as the categories of the bars
# and the time it took to reach unicorn status as the height of the bars.
plt.bar(x=grouped_data_for_plotting.index, height=grouped_data_for_plotting['to be a unicorn'], color='green')
# Set title
plt.title('The time it took companies to reach unicorn status for each industry')
# Set x-axis label
plt.xlabel('Industry')
# Set y-axis label
plt.ylabel('Time to be a unicorn')
# Rotate labels on the x-axis as a way to avoid overlap in the positions of the text
plt.xticks(rotation=45, horizontalalignment='right')
# Display the plot
plt.show()

# Visualize the maximum unicorn company valuation per industry.
# Visualize unicorn companies' maximum valuation for each industry represented in the sample.
# Create a column representing company valuation as numeric data
# Create new column
companies_sampled['valuation billions'] = companies_sampled['Valuation']
# Remove the '$' from each value
companies_sampled['valuation billions'] = companies_sampled['valuation billions'].str.replace('$', '')
# Remove the 'B' from each value
companies_sampled['valuation billions'] = companies_sampled['valuation billions'].str.replace('B', '')
# Convert column to type int
companies_sampled['valuation billions'] = companies_sampled['valuation billions'].astype('int')
print(companies_sampled.head())

# Prepare data for modeling
grouped_ = (companies_sampled[["Industry", "valuation billions"]]
           .groupby("Industry")
           .max()
           .sort_values(by="valuation billions", ascending=True)
          )
print(grouped_)

# Create bar plot
# with the various industries as the categories of the bars
# and the maximum valuation for each industry as the height of the bars
plt.bar(x=grouped_.index, height=grouped_['valuation billions'], color='orange')
# Set title
plt.title('The maximum unicorn company valuation per industry')
# Set x-axis label
plt.xlabel('Industry')
# Set y-axis label
plt.ylabel('Valuation billions')
# Rotate labels on the x-axis as a way to avoid overlap in the positions of the text  
plt.xticks(rotation=45, horizontalalignment='right')
# Display the plot
plt.show()

