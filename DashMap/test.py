from production_cleaner import Cleaner as cl
import pandas as pd
import numpy as np

if __name__ == '__main__':
	df = pd.read_csv('../../Data/ICTO_Datasets/ICTO_Datasets.csv')

	df = cl.full_cleaner(df)
	# df = cl.geocoder(df)
	df = cl.feature_engineering(df)
	# df = cl.k_minimizer(df)
	df = cl.map_minimizer(df)

	print(df)
	# df.to_csv('../../Data/ProductionData/cleaned_geospatial_data.csv')
	# print(df.shape)