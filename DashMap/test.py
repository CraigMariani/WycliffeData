from production_cleaner import Cleaner as cl
from clustering import MeansLatLong as ml
import pandas as pd
import numpy as np

if __name__ == '__main__':
	# read in data
	df = pd.read_csv('../../Data/ICTO_Datasets/ICTO_Datasets.csv')

	# test cleaner
	df = cl.full_cleaner(df)
	df = cl.geocoder(df)
	df = cl.feature_engineering(df)
	df = cl.k_minimizer(df)
	# df = cl.map_minimizer(df)


	# check out of cleaner
	# print(df)
	df.to_csv('../../Data/ProductionData/cleaned_geospatial_data.csv')
	# print(df.shape)


	# test clustering algorithm
	max_clusters = df.shape[0]
	# X = ml.normalize_data(df)
	# n_clusters = 5
	# y_out, k_means, model = ml.cluster(n_clusters, X, max_clusters)
	# highest_n_clusters, highest_sil_score, highest_ch_score, optimal_n_clusters = ml.test_prediction(sil_score, ch_score, n_clusters)

	sil_score, ch_score, n_clusters, sum_squared_distances = ml.start(df, 4)

	print(sil_score, ch_score, n_clusters, sum_squared_distances)
	def most_optimal_clusters(n_clusters):
		global max_clusters
		y_out, k_means, model = ml.cluster(n_clusters, X, max_clusters)
		sil_score, ch_score, n_clusters = ml.calculate_scores(y_out, X, k_means, model)
		highest_n_clusters, highest_sil_score, highest_ch_score, optimal_n_clusters = ml.test_prediction(sil_score, ch_score, n_clusters)
		
		# check the notebook for an increase in ch score with more clusters
		if optimal_n_clusters:
			return highest_n_clusters, highest_sil_score, highest_ch_score 

		else:
			n_clusters += 1
			most_optimal_clusters(n_clusters)

	# highest_n_clusters, highest_sil_score, highest_ch_score = most_optimal_clusters(n_clusters)

	# print('ch score: {}'.format(highest_ch_score))
	# print('sil score: {}'.format(highest_sil_score))
	# print('n clusters: {}'.format(highest_n_clusters))
