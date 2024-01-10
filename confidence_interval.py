# Import relevant packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

aqi = pd.read_csv('google_data_analitics\\c4_epa_air_quality.csv')

# Collecting information about our dataset
print(aqi.describe(include='all'))
print(aqi.info())
print(aqi.shape)

# For a more thorough examination of observations by state use values_counts()
print(aqi['state_name'].value_counts())

# Summarize the mean AQI for RRE states (California, Florida, Michigan, Ohio, Pennsylvania, and Texas)

# Create a list of RRE states
pre_states = ['California', 'Florida', 'Michigan', 'Ohio', 'Pennsylvania', 'Texas']
# Subset `aqi` to only consider these states
aqi_pre_states = aqi[aqi['state_name'].isin(pre_states)]
# Find the mean aqi for each of the RRE states
mean_aqi_pre_states = aqi_pre_states['aqi'].mean()

print(f'The mean aqi for all of the RRE states is {round(mean_aqi_pre_states, 3)}')
print('The mean aqi for each of the RRE states:')

mean_aqi_for_each_pre_states = aqi_pre_states.groupby(['state_name']).agg({'aqi':'mean', 'state_name':'count'})

print(mean_aqi_for_each_pre_states)

# Creating an in-line visualization showing the distribution of aqi by state_name
# The United States is considering a new federal policy that would create a subsidy 
# for renewable energy in states observing an average AQI of 10 or above
plt.figure(figsize=(10, 7))
sns.boxplot(data=aqi_pre_states, x=aqi_pre_states['state_name'], y=aqi_pre_states['aqi'], 
            flierprops={"marker": "x"}, fliersize=7) #flierprops are outliers
plt.axhline(y=10, color='red', alpha=0.9, linestyle='--', label='AQI = 10 points')
plt.legend()
plt.title('The distribution of aqi by state_name')
plt.show()

# Construct your sample statistic for the state that has the value of AQI 
# more than 10 points. In this case this is California, as you can see
# Find the mean aqi for your state
mask_cali = aqi['state_name'] == 'California'
cali_aqi = aqi[mask_cali]['aqi']
cali_aqi_mean = cali_aqi.mean()

print(f'The mean AQI for California is {round(cali_aqi_mean, 2)}')

# Input a confidence level:
confidence_level = 0.95

# Calculate the margin of error
# Begin by identifying the z associated with your chosen confidence level
z_score = 1.96 # for the confidence_level = 0.95
# Next, calculate your standard error.
standard_error = cali_aqi.std() / np.sqrt(cali_aqi.shape[0])
# Lastly, use the preceding result to calculate your margin of error
margin_of_error = z_score * standard_error

print(f'The margin of error for data from the California is {round(margin_of_error, 3)}')

# Calculate the confidence interval (CI) 
upper_limit = cali_aqi_mean + margin_of_error
lower_limit = cali_aqi_mean - margin_of_error

print(f'{confidence_level * 100}% CI [{round(lower_limit, 2)}, {round(upper_limit, 2)}]') # this is the CI

# Alternative: Construct the interval using scipy.stats.norm.interval()
auto_calc_conf_interval = stats.norm.interval(confidence=confidence_level, loc=cali_aqi_mean, scale=standard_error)

print('This is also the confidence interval:', auto_calc_conf_interval)
print(f'{confidence_level * 100}% CI [{round(auto_calc_conf_interval[0], 2)}, {round(auto_calc_conf_interval[1], 2)}]')
