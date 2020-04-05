# scatter plot of latitudes and longitudes from k means clustering
import dash
import dash_core_components as dcc # for accessing interactive data visualization with plotly.js
import dash_html_components as html # for accessing html elements h1 h2
import plotly
import plotly.graph_objs as go # for designing Chloropleth map
import pandas as pd
import numpy as np
from clustering import MeansLatLong as ml


class Scatter:

	def layout_setup():
		
		layout = go.Layout(
		title={'text':'Latitude vs Longitude',
			'font': {'size':28,
			'family':'Arial'}},
		width=1500,
		height=500,
		autosize = False,
		xaxis={
			'title':'Latitude',
			'zeroline': False,
			"showline": False,
			"showticklabels":True,
			'showgrid':True,
			'domain': [0, 1],
			'side': 'right',
			# 'anchor': 'x2',
			},
			yaxis={
			'title':'Longitude',
			'domain': [0, 1],
	        # 'anchor': 'y2',
			'autorange': 'reversed',
			},

		margin=dict(l=100, r=20, t=70, b=70),
		paper_bgcolor='rgb(204, 204, 204)',
		plot_bgcolor='rgb(204, 204, 204)',

		)

		return layout

	# lat long grid for k means clustering
	def scatter_trace(df):
		trace_scatter = []

		trace_scatter.append(go.Scatter(
				x=df['Latitude'],
				y=df['Longitude'],
				mode='markers',
				# text=df_scatter,
				marker=dict(
	            	color='rgba(91, 207, 135, 0.3)',
	            	line=dict(
	                	color='rgba(91, 207, 135, 2.0)',
	                	width=0.5),
	        	),
				name='Latitude vs. Longitude',
				))

		return trace_scatter

	def scatter_trace_k(df):
		trace_k_scatter = []


		df_centroids = ml.start(df, 5)
		lat_mean = df[['Latitude']].mean(axis=1)
		long_mean = df[['Longitude']].mean(axis=1)
		df_centroids['Latitude'] += lat_mean
		df_centroids['Longitude'] += long_mean

		trace_k_scatter.append(go.Scatter(
			x=df_centroids['Latitude'], #latitudes
			y=df_centroids['Longitude'], #longitudes
			name='Centroids',
			mode='markers',
			marker=dict(symbol='x',
						size=12,
						# color=range(n_clusters))
						color='rgba(255,20,20)')
			))

		return trace_k_scatter