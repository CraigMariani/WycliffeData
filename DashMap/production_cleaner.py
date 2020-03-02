# drop duplicate values and null values and create address
import pandas as pd
import numpy as np

class Cleaner:

	# drops duplicates and null values, works for all data sets
	def full_cleaner(df):
		df = df.dropna() # drop null values
		df = df.drop_duplicates() # drop duplicate records

		# delete records from other countrues that are not United States
		indexNames = df[ df['Country'] != 'United States of America'].index
		df.drop(indexNames, inplace=True)

		df = df.drop(columns='Index')

		df['Index'] = np.arange(df.shape[0])

		return df
		
	# creates new attributes like Mnths Passed and Address, needs StartDate/EndDate and City, State, Country
	def feature_engineering(df):
		
		try:
			# df['StartDate'] = df['StartDate'].astype('datetime64').astype(int)
			# df['EndDate'] = df['EndDate'].astype('datetime64').astype(int)

			df['StartDate'] = pd.to_datetime(df['StartDate'])
			df['EndDate'] = pd.to_datetime(df['EndDate'])
			df['ProjectDurationInDays'] = df['EndDate'] - df['StartDate']
			df['ProjectDurationInDays'] = df['ProjectDurationInDays'].astype(str)
			df['ProjectDurationInDays'] = df['ProjectDurationInDays'].str.split(' ').str[0]
			df['ProjectDurationInDays'] = pd.to_numeric(df['ProjectDurationInDays'])
			
			# df['ProjectDurationInDays'] = df['ProjectDurationInDays'].astype('datetime64').astype(int).astype(float)
			# print(splitdays)
			# df['ProjectDurationInDays'] = pd.to_datetime64(df['ProjectDurationInDays'])
		except KeyError:
			print('No date-time values given for feature "TimePassed"')

		try:

			df['Address'] = df['City'] + ', ' + df['State'] + ', ' + df['Country']

		except KeyError:
			print('Not enough geospatial data given for feature "Address"')


		df.to_csv('../../Data/ProductionData/cleaned_geospatialdata.csv')
		return df


	# gets latitudes and longitudes from City, Sate, needs City and State attributes 
	# great for the k means clustering algorithm 
	# where latitude = x and longitude = y
	def geocoder(df):
		df_geo = pd.read_csv('../../Data/OutsideData/us-zip-code-latitude-and-longitude.csv')
		df_geo = df_geo.drop(columns=['Timezone', 'Daylight savings time flag', 'Zip', 'geopoint'], axis=1)
		df_output = pd.merge(df, df_geo, on=['City','State'], how='left')

		df_output = df_output.dropna()
		df_output = df_output.drop_duplicates(subset = list(df.columns))

		return df_output

	# drops non numerical data except Postal Codes, and Address, needs PostalCodes and Address
	# good for choropleth map where non numerical data becomes wasted space
	def map_minimizer(df):
		df_keep = pd.DataFrame({'Index':df['Index'],'Address':df['Address'],'PostalCode':df['PostalCode']})
		# print(df_keep.head())
		df = df.select_dtypes(exclude=['object'])
		df = pd.merge(df, df_keep, on=['Index'], how='left')
		return df

	# drops all non-numerical data 
	# great for the k means clustering algorithm 
	# where categorical attributes are not used 
	def k_minimizer(df):
		# print(df.shape)
		df = df.select_dtypes(exclude=['object', 'datetime'])
		# print(df.shape)
		return df