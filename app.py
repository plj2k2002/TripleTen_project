# Import necessary libraries
import pandas as pd
import plotly.express as px
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/plj2k2002/TripleTen_project/main/vehicles_us.csv')

# Verify column names
print(df.columns)

# Rename columns if necessary
df.rename(columns={'cylinders': 'cylindres'}, inplace=True)

# Fill missing values
df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
df['cylindres'] = df.groupby('model')['cylindres'].transform(lambda x: x.fillna(x.median()))
df['odometer'] = df.groupby(['model', 'model_year'])['odometer'].transform(lambda x: x.fillna(x.median()))

# Remove outliers for model_year and price
df = df[(np.abs(stats.zscore(df['model_year'].dropna())) < 3)]
df = df[(np.abs(stats.zscore(df['price'].dropna())) < 3)]

# Display statistics
print("Statistics for Price:")
print(df['price'].describe())

print("\nStatistics for Odometer:")
print(df['odometer'].describe())

print("\nStatistics for Model Year:")
print(df['model_year'].describe())

# Create visualizations with annotations for statistics

# Histogram for 'price'
fig_hist_price = px.histogram(df, x='price', title='Distribution of Price')
mean_price = df['price'].mean()
median_price = df['price'].median()
fig_hist_price.add_vline(x=mean_price, line_width=3, line_dash="dash", line_color="red", annotation_text='Mean', annotation_position='top')
fig_hist_price.add_vline(x=median_price, line_width=3, line_dash="dash", line_color="blue", annotation_text='Median', annotation_position='top')

# Histogram for 'odometer'
fig_hist_odometer = px.histogram(df, x='odometer', title='Distribution of Odometer')
mean_odometer = df['odometer'].mean()
median_odometer = df['odometer'].median()
fig_hist_odometer.add_vline(x=mean_odometer, line_width=3, line_dash="dash", line_color="red", annotation_text='Mean', annotation_position='top')
fig_hist_odometer.add_vline(x=median_odometer, line_width=3, line_dash="dash", line_color="blue", annotation_text='Median', annotation_position='top')

# Scatterplot for 'price' vs 'model_year'
fig_scatter_price_model_year = px.scatter(df, x='model_year', y='price', title='Price vs Model Year')
fig_scatter_price_model_year.add_hline(y=mean_price, line_width=3, line_dash="dash", line_color="red", annotation_text='Mean Price', annotation_position='top right')

# Scatterplot for 'price' vs 'odometer'
fig_scatter_price_odometer = px.scatter(df, x='odometer', y='price', title='Price vs Odometer')
fig_scatter_price_odometer.add_hline(y=mean_price, line_width=3, line_dash="dash", line_color="red", annotation_text='Mean Price', annotation_position='top right')

# Display the plots
fig_hist_price.show()
fig_hist_odometer.show()
fig_scatter_price_model_year.show()
fig_scatter_price_odometer.show()
