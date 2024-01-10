import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('google_data_analitics\\2017_Yellow_Taxi_Trip_Data.csv')

# Learning (acquaitance) with the data
print(df.head(10))
print('The size of the data frame:', df.size)
print('The shape of the data frame:', df.shape)
print(df.describe())
print(df.info())

# Convert data columns to datetime
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
print(df.info())

# Create box plot of trip_distance
plt.figure(figsize=(9,2))
sns.boxplot(x=df['trip_distance'], fliersize=2, color='orange')
plt.title('Trip distance box plot')
plt.show() # The dots from the right side of the box plot are outliers - in next part we must throw away them

# Create histogram of trip_distance
plt.figure(figsize=(9,5))
sns.histplot(x=df['trip_distance'],bins=range(0, 26, 1), color='orange') # bins breaks the data onto groups
plt.title('Trip distance histogram')
plt.show()

# Create box plot of total_amount
plt.figure(figsize=(9, 2))
sns.boxplot(x=df['total_amount'], fliersize=2, color='green')
plt.title('Total amount box plot')
plt.show()

# Create histogram of total_amount
plt.figure(figsize=(13,5))
total_amount_hist = sns.histplot(x=df['total_amount'], bins=range(-10,101,5), color='green')
plt.title('Total amount histogram')
total_amount_hist.set_xticks(range(-10,101,5))
total_amount_hist.set_xticklabels(range(-10,101,5))
plt.show()

# Create box plot of tip_amount
plt.figure(figsize=(9, 2))
sns.boxplot(x=df['tip_amount'], fliersize=2, color='red')
plt.title('Tip amount box plot')
plt.show()

# Create histogram of tip_amount
plt.figure(figsize=(10, 5))
total_tip_amount_hist = sns.histplot(x=df['tip_amount'], bins=(range(0, 26, 1)), color='red')
total_tip_amount_hist.set_xticks(range(0, 26, 1)) # ticks are the measure for this axis
total_tip_amount_hist.set_xticklabels(range(0, 26, 1))
plt.title('Tip amount histogram')
plt.show()

# Create histogram of tip_amount by vendor
plt.figure(figsize=(7, 5))
tip_amount_by_vendor = sns.histplot(x=df['VendorID'], y=df['tip_amount'], color='yellow')
tip_amount_by_vendor.set_xticks(range(1,3,1))
tip_amount_by_vendor.set_xticklabels(range(1,3,1))
plt.title('Histogram of tip amount by vendor')
plt.show()

#Create histogram of tip_amount by vendor - ANOTHER ONE
plt.figure(figsize=(15, 9))
hist_tip_amount_by_vendor = sns.histplot(x=df['tip_amount'], 
                                         hue=df['VendorID'], 
                                         multiple='stack', 
                                         bins=(range(0, 26, 1)),
                                         palette='colorblind')
hist_tip_amount_by_vendor.set_xticks(range(0, 26, 1))
hist_tip_amount_by_vendor.set_xticklabels(range(0, 26, 1))
plt.title('Histogram of tip amount by vendor')
plt.show()

# Create histogram of tip_amount by vendor for tips > $10
mask_for_tips = df['tip_amount'] > 10
plt.figure(figsize=(15, 9))
plt.title('Histogram of tip amount by vendor for tips > $10')
part_of_tip_amount_by_vendor = sns.histplot(x=df[mask_for_tips]['tip_amount'], 
                                            hue=df['VendorID'],
                                            bins=(range(10, 26, 1)),
                                            multiple='stack',
                                            palette='colorblind')
part_of_tip_amount_by_vendor.set_xticks(range(10, 26, 1))
part_of_tip_amount_by_vendor.set_xticklabels(range(10, 26, 1))
plt.show()

# Examine the unique values in the `passenger_count` column
print(df['passenger_count'].value_counts())

# Calculate mean tips by passenger_count
print('The mean tips by passenger_count:')
mean_tips_by_passenger_amount = df.groupby(['passenger_count']).mean()[['tip_amount']]
mean_tips_by_passenger_amount

# Create bar plot for mean tips by passenger count
data = mean_tips_by_passenger_amount.tail(-1)
pal = sns.color_palette('ch:start=.2,rot=-.3', len(data))
rank = data['tip_amount'].argsort().argsort()
plt.figure(figsize=(12,7))
bar_plot_for_mean_tips = sns.barplot(x=data.index,
                                     y=data['tip_amount'],
                                     palette=np.array(pal[::-1])[rank])
bar_plot_for_mean_tips.axhline(df['tip_amount'].mean(), ls='--', color='red', label='general mean tips')
bar_plot_for_mean_tips.legend()
plt.title('Mean tip amount by passenger count', fontsize=16)
plt.show()

print('General mean tips:', df['tip_amount'].mean())

# Create a month column and a day column
df['month'] = df['tpep_pickup_datetime'].dt.month_name()
df['day'] = df['tpep_pickup_datetime'].dt.day_name()
print(df.head(10))

# Get total number of rides for each month
tn_of_rides_per_month = df['month'].value_counts()
print(tn_of_rides_per_month)

# Reorder the monthly ride list so months go in order
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']
tn_of_rides_per_month = tn_of_rides_per_month.reindex(month_order)
print(tn_of_rides_per_month)

# Show the index - we will use indexes like values for x-axis if histograms
print(tn_of_rides_per_month.index)

# Create a bar plot of total rides per month
plt.figure(figsize=(12,6))
sns.barplot(x=tn_of_rides_per_month.index, y=tn_of_rides_per_month, palette='colorblind')
plt.title('The bar plot of total rides per month', fontsize=16)
plt.show()

# Repeat the above process, this time for rides by day
day_order = df['day'].value_counts()
day_right_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_order = day_order.reindex(day_right_order)
print(day_order)

# Create bar plot for ride count by day
plt.figure(figsize=(12,6))
sns.barplot(x=day_order.index, y=day_order, palette='colorblind')
plt.title('The bar plot for ride count by day', fontsize=16)
plt.show()

# Plot total revenue by day of the week
# Repeat the process, this time for total revenue by day
total_amount_by_day = df.groupby(['day']).sum()[['total_amount']]
total_amount_by_day = total_amount_by_day.reindex(day_right_order)
print(total_amount_by_day)

# Create bar plot of total revenue by day
plt.figure(figsize=(12,6))
total_revenue_by_day = sns.barplot(x=total_amount_by_day.index, 
                                   y=total_amount_by_day['total_amount'], 
                                   palette='colorblind')
plt.title('The bar plot of total revenue by day', fontsize=16)
total_revenue_by_day.set_xlabel('The day of the week')
total_revenue_by_day.set_ylabel('Revenue (USD)')
plt.show()

# Plot total revenue by month
# Repeat the process, this time for total revenue by month
total_amount_by_month = df.groupby(['month']).sum()[['total_amount']]
total_amount_by_month = total_amount_by_month.reindex(month_order)
print(total_amount_by_month)

# Create a bar plot of total revenue by month
plt.figure(figsize=(12,6))
total_revenue_by_month = sns.barplot(x=total_amount_by_month.index,
                                     y=total_amount_by_month['total_amount'],
                                     palette='colorblind')
plt.title('The bar plot of total revenue by month', fontsize=16)
total_revenue_by_month.set_xlabel('Month')
total_revenue_by_month.set_ylabel('Revenue (USD)')
plt.show()

# Plot mean trip distance by drop-off location
# Get number of unique drop-off location IDs
print(df['DOLocationID'].nunique())

# Calculate the mean trip distance for each drop-off location
mean_trip_distance_for_drop_off = df.groupby(['DOLocationID']).mean()[['trip_distance']]
# Sort the results in descending order by mean trip distance
mean_trip_distance_for_drop_off = mean_trip_distance_for_drop_off.sort_values(by='trip_distance')
print(mean_trip_distance_for_drop_off)

# Create a bar plot of mean trip distances by drop-off location in ascending order by distance
plt.figure(figsize=(10,6))
mean_trip_distances_by_drop_off = sns.barplot(x=mean_trip_distance_for_drop_off.index,
                                              y=mean_trip_distance_for_drop_off['trip_distance'],
                                              order=mean_trip_distance_for_drop_off.index)
plt.title('The bar plot of mean trip distances by drop-off location in ascending order by distance', fontsize=16)
mean_trip_distances_by_drop_off.set_xticks([])
mean_trip_distances_by_drop_off.set_xticklabels([])
plt.show()

# Calcutating time in/on the trip and show it in a minutes
df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime'])
df['trip_duration'] = df['trip_duration'].dt.total_seconds() / 60
print(df.head(10))