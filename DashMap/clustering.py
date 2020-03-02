import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn import metrics

import numpy as np
import pandas as pd

class MeansLatLong():
	highest_score = 0
	# call events with one method
	def start(df, n_clusters):
		X = MeansLatLong.normalize_data(df)
		y_out, k_means, model = MeansLatLong.cluster(n_clusters, X, df.shape[0])
		sil_score, ch_score, n_clusters, sum_squared_distances = MeansLatLong.calculate_scores(y_out,X , k_means, model)

		return sil_score, ch_score, n_clusters, sum_squared_distances


	# scale values so they are all equal importance
	def normalize_data(df):
		X = StandardScaler().fit_transform(df)
		return X


	# generate cluster predictions for analysis
	def cluster(n_clusters, X, max_clusters):
		if n_clusters == None or n_clusters >= max_clusters:
			n_clusters = 5

		# set number of clusters for algorithm
		k_means = KMeans(n_clusters=n_clusters)

		# run clustering algorithm and produce a model
		model = k_means.fit(X)

		# create cluster predictions store in y_out
		y_out = k_means.predict(X)

		return y_out, k_means, model

	# calinksi harabaski store determines the effectiveness of number of clusters
	def calculate_scores(y_out, X, k_means, model):
		# create labels for each of the clusters
		labels = k_means.labels_

		# calculate silhoutte coefficient
		# (how similar the object is to its own cluster compared to other clusters)
		sil_score = metrics.silhouette_score(X, labels, metric='euclidean')

		# calculate ch score or variance ratio criterion
		ch_score = metrics.calinski_harabasz_score(X, labels)
		n_clusters = model.n_clusters
		sum_squared_distances = k_means.inertia_
		return sil_score, ch_score, n_clusters, sum_squared_distances

	# test the number of cluster predictions to see if it is most optimal 
	def test_prediction(sil_score, ch_score, n_clusters):
		highest_n_clusters = 0
		highest_sil_score = 0
		highest_ch_score = 0

		optimal_n_clusters = False

		if ch_score > highest_ch_score and sil_score > highest_sil_score:
			highest_n_clusters = n_clusters
			highest_sil_score = sil_score
			highest_ch_score = ch_score
		else:
			optimal_n_clusters = True

		return highest_n_clusters, highest_sil_score, highest_ch_score, optimal_n_clusters


