import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv(r'C:\Users\Stackedadmin\Desktop\Python\Property_Price_Register_Ireland-28-05-2021.csv')
# set view using pandas and numpy
desired_width = 320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns', 10)

# Use below print functions to :
# Analyse the top five lines.
# The shape
# Type of data
# Column Names
# Statistics of data


print(df.head())
print(df.shape)
print(df.info)
print(df.columns)
print(df.describe())

print(df.sort_values('SALE_PRICE', ascending=False))  # To check highest value property
d18 = df['POSTAL_CODE'].isin(['Dublin 18'])
print(df[d18])  # Just to double check data is pulling through correctly -
# Sorted CSV D18 homes verses Dataframe

print(df.isnull().sum())    #  check column nulls
print(df['PROPERTY_SIZE_DESC'].isnull().sum()) # a lot of nulls in this column

df['PROPERTY_SIZE_DESC'].fillna('No Available Data', inplace=True)  # As so many nulls replaced with string data
print(df['PROPERTY_SIZE_DESC'].isnull().sum())  # Nulls removed
df['POSTAL_CODE'].fillna('No_Postal_Code', inplace=True)  # As Above replaced with String data
print(df['POSTAL_CODE'].isnull().sum())
print(df.isnull().sum())  # all Nulls removed

print(df['ADDRESS'].value_counts(sort=True))
# As Address is only field I would be concerned about duplicates I checked this.
# There are duplicates in there but as data is over 10 year period have to presume they are either
# 1) new development with shared address or 2) repeated sales of the same house


avg_county = df.groupby('COUNTY')['SALE_PRICE'].mean()  # To get average sale price by county
# print(avg_county) - Use group by to get average sales price by county

# Use pd.to_datetime to parse out year as dataset so big. Will make graphs easier to analyse

df['SALE_DATE'] = pd.to_datetime(df['SALE_DATE'])
df['year'] = pd.DatetimeIndex(df['SALE_DATE']).year
avg_year = df.groupby(df['year'])['SALE_PRICE'].mean()  # to get average house price by year
year_df = pd.DataFrame(avg_year)  # changed to DataFrame so I can merge it seperatley
print(year_df)
#
# This is to show comparison between House prices and Annual Salaries Ireland between 2010 and 2020
# Using Dictionary made sense here as two values - year and Avg Salary could be used as Key:Value
wages_dict = {2000: 36754, 2001: 38067, 2002: 38384, 2003: 39617, 2004: 40946, 2005: 42450, 2006: 42825,
              2007: 44021, 2008: 45842, 2009: 4942, 2010: 49487, 2011: 48962, 2012: 48491, 2013: 47267,
              2014: 46973, 2015: 46965, 2016: 47641, 2017: 48203, 2018: 48412, 2019: 49332, 2020: 49296}
# # taken from https://www.statista.com/statistics/416212/average-annual-wages-ireland-y-on-y-in-euros/
#
for key, value in wages_dict.items():  # parse out key-values
    print(key, value)
wages_items = wages_dict.items()
wages_list = list(wages_items)  # Change from dictionary to list
wages_df = pd.DataFrame(wages_list)  # Change from list to DataFrame so I can merge data with Property Price Register
wages_df.columns = ['year', 'Average Annual Salary']  # Renamed Columns in preparation for merge
house_price_wages = year_df.merge(wages_df, on='year', how='left')  # Used left join as wanted all data from Year_df
print(house_price_wages.isnull().sum())  # Check nulls on new merged dataset. Noticed no salary data for 2021
# house_price_wages.iloc[11:12, 2:4] = house_price_wages.iloc[5:11, 2:3].mean()# Redid below as figure out
# # as I had no salary information from 2021 I used average from 2015 to 2020 to populate this figure. When
# # plotted this looked askew so I looked at % Increase by year to populate this value
new_2021_avg = pd.DataFrame(house_price_wages.loc[(house_price_wages['year'] > 2018) & (
        house_price_wages['year'] < 2021)])  # to check these values
house_price_wages.iloc[11:12, 2:4] = house_price_wages.iloc[10:11, 2:4] * 1.02
# Took previous figure and added 2% for  inflation figure to add in missing value


Looked to plot correlation between Average Annual House price and average annual salary 2010-2020
Best way for me to do this was to show both house price and wages on same plot with same X axis of year
plt.style.use('ggplot')
fig, ax = plt.subplots()
ax.plot(house_price_wages['year'], house_price_wages['SALE_PRICE'], color='blue', linestyle='--',
        marker='<')
ax.set_xlabel('Year')
ax.set_ylabel('Average Yearly House Sell Price IRE', color='blue')
ax.tick_params('y', color='blue')
ax2 = ax.twinx()
ax2.plot(house_price_wages['year'], house_price_wages['Average Annual Salary'], color='red', linestyle='--',
         marker='<')
ax2.set_ylabel('Average Annual Salary IRE', color='red')
ax2.tick_params('y', color='red')
plt.title('Avg House Price:Avg Salary 10:21')

# Wanted to see the change up or down in house price increase or decrease and salary increase or
# decrease over the years
# so used .pct_change() pandas function. I then used bar chart to visualise this.
house_price_wages['% Change Salary'] = house_price_wages['Average Annual Salary'].pct_change()
house_price_wages['% Change House Price'] = house_price_wages['SALE_PRICE'].pct_change()
print(house_price_wages)
plt.style.use('bmh')
fig, ax = plt.subplots()
ax.bar(house_price_wages['year'], house_price_wages['% Change House Price'], label='House Price % Change', color='red')
ax.bar(house_price_wages['year'], house_price_wages['% Change Salary'], label='Salary % Change', color='black')
ax.set_xlabel('Year')
ax.set_ylabel('% Difference')
ax.set_title('House Price Growth Verses Salary Growth By Year%')
plt.legend()

# Wanted to add a new Column to give simple Bolean value to Visualise New verses second hand home
df['New_Home'] = df['PROPERTY_DESC'].apply(lambda x: True if x == 'New Dwelling house /Apartment' else False)

print(df.head())
print(df.describe())
# Best way to visualise New home verses second hand home by county was by using
# countplot with the County on X Axis with count on Y with Hue as New verses second hand
sns.set_theme(style="darkgrid")
hue_colors = {0: 'black', 1: 'red'}
f, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x='COUNTY', hue='New_Home', data=df, palette=hue_colors)
plt.xticks(rotation=90)
plt.title('New_Home_Sales Verses 2nd Hand')

# To show how big a gap there is overall I used Pie chart to show lack of new home sales with new column
# Ne_Home as basis for data
df2 = df['New_Home'].value_counts()
print(df2)

# to show overall % of new verses secondhand
sns.set_theme(style="darkgrid")
labels = '2nd Hand Home', 'New_home'
explode = (0, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(df2, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('%New Verses SecondHand Homes Sold')



'''
Wanted to be able to Visualise Sale price 
by County depending on price so used a function for this purpose
also wanted to see if market price met
'''


def county_sale_price(x, y):
    by_county = df[(df['COUNTY'] == x) & (df['SALE_PRICE'] > y)]
    hue_colours = {1: 'red', 0: 'black'}
    sns.set_theme(style='whitegrid')
    sns.scatterplot(x=by_county['year'], y=by_county['SALE_PRICE'], hue=by_county['IF_MARKET_PRICE'],
                    palette=hue_colours, hue_order=(0, 1))
    plt.xlabel('Year')
    plt.ylabel('Sale_Price')
    plt.title(f'Sales for {x} greater than {y}')

    return by_county, plt.show()


# print(county_sale_price('Dublin', 500000))# Run this separately
## Want to look at which months over teh course of the 11 years where sales go up to identify future bottle necks
# used line plot for this with Year as Hue. I needed to parse month name so I again used pd.DatetimeIndex.
# Found str.slice() on google which enabled reduction of month name to three

df['Month'] = pd.DatetimeIndex(df['SALE_DATE']).month
df['Month'] = pd.to_datetime(df['Month'], format='%m').dt.month_name().str.slice(stop=3)
# print(df['Month'])

sns.set_theme(style='darkgrid')
sns.relplot(x=df['Month'], y='SALE_PRICE', data=df, kind='line', hue=df['year'], style='year')
plt.show()

# Wanted to use Numpy to look at different statistics of the data. Pivot table was handy for this.
pivot = df.pivot_table(values='SALE_PRICE', index=df['year'], aggfunc=np.median)  # get median sale price by year
pivot_2 = df.pivot_table(values='SALE_PRICE', index=df['year'], aggfunc=np.mean) # get mean sale price by year
pivot_3 = df.pivot_table(values='ADDRESS', index='COUNTY', aggfunc=np.count_nonzero) # Count no of counties by year
pivot_4 = df.pivot_table(values='SALE_PRICE', index=df['year'], aggfunc=np.std) # Get standard deviation on Sales price by year
print(pivot)
print(pivot_2)
print(pivot_3)
print(pivot_4)
