import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn import metrics

import numpy as np
import pandas as pd

class MeansLatLong():
	highest_score = 0

	# for running the actual clustering in production
	# only normalizes data and performs clustering, no checking/calculating scores
	def start(df, n_clusters):
		X = MeansLatLong.normalize_data(df)
		y_out, k_means, model = MeansLatLong.cluster(n_clusters, X, df.shape[0])
		centroids = model.cluster_centers_
		
		# df_centroids = format(df.columns, centroids)
		df_centroids = MeansLatLong.to_coordinates(df.columns, centroids)
		return df_centroids

	# format the centroids into a dataframe
	# def format(clmns, centroids):
	def to_coordinates(clmns, centroids):
		col_names = list(clmns)
		col_names.append('prediction')
		
		# zip columns
		Z = [np.append(A, index) for index, A in enumerate(centroids)]

		# convert to dataframe
		df_centroids = pd.DataFrame(Z, columns=col_names)
		# df_centroids = pd.DataFrame(centroids, columns=col_names)
		df_centroids['prediction'] = df_centroids['prediction'].astype(int)

		return df_centroids 

	# call events with one method
	# for testing the number of clusters in the scatter plot
	def test_start(df, n_clusters):
		X = MeansLatLong.normalize_data(df)

		y_out, k_means, model = MeansLatLong.cluster(n_clusters, X, df.shape[0])

		sil_score, ch_score, n_clusters, sum_squared_distances = MeansLatLong.calculate_scores(y_out,X , k_means, model)

		# return sil_score, ch_score, n_clusters, sum_squared_distances, model # experimental
		return sil_score, ch_score, sum_squared_distances # for testting
		


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
		# print(k_means)
		# run clustering algorithm and produce a model
		model = k_means.fit(X)
		# print(model.cluster_centers_)
		# print('*******************')
		# print(model.cluster_centers_[:,4])
		# print('*******************')
		# print(model.cluster_centers_[:,5])
		
		# create cluster predictions store in y_out
		y_out = k_means.predict(X)
		# print(y_out)

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


