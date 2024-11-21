import pandas as pd
import numpy as np
from numpy.ma.core import less_equal
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
### YOUR CODE HERE

# Utilize Pandas to import data into dataframe
data_filepath = ('../../data/drop-jump/all_participant_data_rsi.csv')
df = pd.read_csv(data_filepath, header = 0)

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

### YOUR CODE HERE

# Extract each column from the dataframe and convert to numpy array
trial = df['trial'].to_list()
force_plate_rsi = df['force_plate_rsi'].to_numpy()
accelerometer_rsi = df['accelerometer_rsi'].to_numpy()
percent_error = df['percent_error'].to_numpy()

# Calculate standard deviation and mean for force plate and accel rsi
(f_mean, f_std) = norm.fit(force_plate_rsi)
(a_mean, a_std) = norm.fit(accelerometer_rsi)

# Print mean and standard deviation values
print('Force Plate: STD = ',f_std.round(4),' , MU = ',f_mean.round(4))
print('Accelerometer: STD = ',a_std.round(4),' , MU = ',a_mean.round(4))

# Create axis conditions
fx = np.linspace(start=(f_mean-(4*f_std)), stop=f_mean+((4*f_std)), num=10000)
fy = norm.pdf(fx, loc=f_mean, scale=f_std)
ax = np.linspace(start=(a_mean-(4*a_std)), stop=a_mean+((4*a_std)), num=10000)
ay = norm.pdf(ax, loc=a_mean, scale=a_std)

# Plot force plate and accelerometer rsi
fig, axs = plt.subplots(1,2, figsize=(15,5))
axs[0].plot(fx, fy, label='Force Plate')
axs[0].plot(ax, ay, label='Accelerometer')
axs[0].set_title('Fitted Normal Curve')
axs[0].set_xlabel('RSI')
axs[0].set_ylabel('Probability')
axs[0].legend()

"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), with the 10th bin encompassing [2,inf). An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

"""
Force Plate
"""
### YOUR CODE HERE

# bin the examples
f_bins = np.linspace(0, 2, 9)  # Create 10 bins
f_bins = np.r_[-np.inf, f_bins, np.inf]

# place observations into bins
observed_counts, observed_edges = np.histogram(force_plate_rsi, bins=f_bins, density=False)

# CDF difference gives probabilities for each bin. Provided probability of value being within each bin.
expected_prob = np.diff(norm.cdf(f_bins, loc=f_mean, scale=f_std))

# Expected frequency for each bin
expected_counts = expected_prob * len(force_plate_rsi)

# Conduct chi2 test
(f_chi_stat, f_p_value) = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)
print('Force Plate Chi2 stat: ',f_chi_stat, '\nForce Plate p-value: ', f_p_value)

# Test Alpha Value against p value
alpha = 0.05
print('Alpha = ',alpha)

if f_p_value < alpha:
    print('Reject null hypothesis. Force Plate Chi2 P-Value < Alpha')
else:
    print('Accept null hypothesis. Force Plate Chi2 P-Value > Alpha')

print('\n')

"""
Acceleration
"""

### Repeat for Acceleration
bins = np.linspace(0, 2, 9)  # Create 10 bins
bins = np.r_[-np.inf, bins, np.inf]
observed_counts, observed_edges = np.histogram(accelerometer_rsi, bins=bins, density=False)
expected_prob = np.diff(norm.cdf(bins, loc=f_mean, scale=f_std))
expected_counts = expected_prob * len(accelerometer_rsi)
(a_chi_stat, a_p_value) = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)
print('Accelerometer Chi2 stat: ', a_chi_stat, '\nAccelerometer p-value: ', a_p_value)
alpha = 0.05
print('Alpha = ',alpha)
if a_p_value < alpha:
    print('Reject null hypothesis. Accelerometer Chi2 P-Value < Alpha')
else:
    print('Accept null hypothesis. Accelerometer Chi2 P-Value > Alpha')


"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
"""
print('\n\n-----Question 3-----')

### YOUR CODE HERE

# Perform two sided t test on force plate and accelerometer rsi
(comp_stat, comp_p_value) = ttest_ind(force_plate_rsi,accelerometer_rsi, equal_var=True)
print('Two Sided T-Test:', '\nStat = ', comp_stat, '\nP Value = ', comp_p_value, '\nAlpha =', alpha)

# Compare resulting p value to alpha
if comp_p_value < alpha:
    print('Conclusion: Reject null hypothesis. Comparable Chi2 P-Value < Alpha. The datasets are not statistically different.')
else:
    print('Conclusion: Accept null hypothesis. Comparable Chi2 P-Value > Alpha. The datasets are statistically different.')


"""
Question 4 (Bonus): Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""

### YOUR CODE HERE

# Calculate Error, Error STD, and Error Mean
error = force_plate_rsi - accelerometer_rsi
e_mean = np.mean(error)
e_std = np.std(error)

# Bin and plot samples
num_bins = 30
count, bins, ignored = plt.hist(error, bins=num_bins, density=True,
                                label='Sampled and Binned Normal Distribution',edgecolor='k')
# Plot expected distribution
x = np.linspace(min(error), max(error), 100)
axs[1].plot(x, norm.pdf(x, loc=e_mean, scale=e_std), linewidth=2, color='r', label='Expected Normal Distribution')
axs[1].set_title('Error Distribution; Sampled VS Expected')
axs[1].set_xlabel('RSI')
axs[1].set_ylabel('Bin Count')
axs[1].legend()

plt.tight_layout()
plt.show()