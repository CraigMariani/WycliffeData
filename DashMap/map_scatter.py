# interactive choropleth map of the analytics dashboard

import dash
import dash_core_components as dcc # for accessing interactive data visualization with plotly.js
import dash_html_components as html # for accessing html elements h1 h2
import plotly
import plotly.graph_objs as go # for designing Chloropleth map
import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
from production_cleaner import Cleaner as cln
from clustering import MeansLatLong as ml
# creating dash object for server
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app=dash.Dash(__name__)


# reading the dataset for now going to create an uploader and have it converted into pandas dataframe
df = pd.read_csv('../../Data/ICTO_Datasets/ICTO_Datasets.csv')

# initial cleaner
df = cln.full_cleaner(df)
# create a copy for k means scatter plot
df_scatter = df.copy(deep=True)

# format the data for k means clustering scatterplot
df_scatter = cln.geocoder(df_scatter)
df_scatter = cln.k_minimizer(df_scatter)

selection_scatter = list(df_scatter.columns)

# format the data for map plot
df = cln.feature_engineering(df)
df = cln.map_minimizer(df)

selection = list(df.columns)

mapbox_accesstoken = 'pk.eyJ1IjoiY3JhaWdtYXJpYW5pIiwiYSI6ImNrNnk2bWQ0NjBxNmMzbG84OGpsa2IwMnQifQ.Hy10gEAc9eolUbu_lLgTMQ'

addresses = df['Address'].str.title().tolist()

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
	US_data = json.load(response)

pl_deep=[[0.0, 'rgb(253, 253, 204)'],
         [0.1, 'rgb(201, 235, 177)'],
         [0.2, 'rgb(145, 216, 163)'],
         [0.3, 'rgb(102, 194, 163)'],
         [0.4, 'rgb(81, 168, 162)'],
         [0.5, 'rgb(72, 141, 157)'],
         [0.6, 'rgb(64, 117, 152)'],
         [0.7, 'rgb(61, 90, 146)'],
         [0.8, 'rgb(65, 64, 123)'],
         [0.9, 'rgb(55, 44, 80)'],
         [1.0, 'rgb(39, 26, 44)']]

def scatter_trace_k(layout):
	trace_k_scatter = []
	global df_scatter
	global app

	df_centroids = ml.start(df_scatter, 5)
	lat_mean = df_scatter[['Latitude']].mean(axis=1)
	long_mean = df_scatter[['Longitude']].mean(axis=1)
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

# lat long grid for k means clustering
def scatter_trace(layout):
	trace_scatter = []

	global df_scatter
	global app

	trace_scatter.append(go.Scatter(
			x=df_scatter['Latitude'],
			y=df_scatter['Longitude'],
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


# trace for the choropleth map
def map_trace(layout):
	
	trace_map = []

	global mapbox_accesstoken
	global df
	global selection
	global US_data
	global pl_deep
	global app
	
	for attribute in selection:
		trace_map.append(go.Choroplethmapbox(
			geojson=US_data,
			locations=df['PostalCode'].tolist(),
			z = df[attribute].tolist(),
			colorscale=pl_deep,
			text=addresses,
			colorbar=dict(
				thickness=20,
				ticklen=3),
			marker_line_width=0,
			marker_opacity=0.7,
			visible=False,
			subplot='mapbox1'
			))

	trace_map[0]['visible'] = True
	return trace_map 



# change layout based on drop down menu selection
def layout_update(layout):
	global selection
	size = len(selection)
	# boolean_menu = np.zeros((size), dtype=bool)
	menu = np.array([])

	for index, attribute in enumerate(selection):
		boolean_menu = np.zeros((size), dtype=bool)
		boolean_menu[index] = True
		item = dict(
			args=['visible', boolean_menu],
			label='Column Value: {}'.format(attribute),
			method='restyle'
		)
		menu = np.append(menu, item)
		# print(attribute)
		# print(index)

	menu = menu.tolist()
	# print(menu)

	# add a dropdown menu in the layout
	layout.update(updatemenus=list([
	    dict(x=0,
	         y=1,
	         xanchor='left',
	         yanchor='middle',
	         buttons=menu,
	        )]))
	return layout

def layout_setup2():
	global df_scatter
	global app
	global selection_scatter

	layout2 = go.Layout(
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
	return layout2
# initialize layout
def layout_setup():
	global mapbox_accesstoken
	global df
	global selection
	global US_data
	global pl_deep
	global app
	# global layout


	layout= go.Layout(
		title = {'text':'Financial vs Geospatial Data 2008-2019',
			'font': {'size':28, 
           	'family':'Arial'}},
    	autosize = True,

    	mapbox1 = dict(
			domain = {'x': [0, 1],'y': [0, 1]},
			center = dict(lat=38, lon=-97),
			zoom = 3,
	        accesstoken = mapbox_accesstoken, 
	      	),

		xaxis={
			'zeroline': False,
	        "showline": False,
	        "showticklabels":True,
	        'showgrid':True,
	        'domain': [0, 0.25],
	        'side': 'right',
	        'anchor': 'x2',
	        },
	    yaxis={
	    	'domain': [0.4, 0.9],
	        'anchor': 'y2',
	        'autorange': 'reversed',
	     	},
	    margin=dict(l=100, r=20, t=70, b=70),
    	paper_bgcolor='rgb(204, 204, 204)',
    	plot_bgcolor='rgb(204, 204, 204)',
		)

	return layout
# main function/ make all function calls from here
def main():
	global app
	# global layout
	layout = layout_setup()
	layout2 = layout_setup2()

	trace_map = map_trace(layout)
	trace_scatter = scatter_trace(layout2)
	trace_k_scatter = scatter_trace_k(layout2)
	layout = layout_update(layout)

	fig=go.Figure(data=trace_map, layout=layout)
	# fig=go.Figure(data=trace_map + trace_scatter, layout=layout)
	fig2=go.Figure(data=trace_scatter + trace_k_scatter, layout=layout2)
	app.layout = html.Div([
		html.H1(children=''),

		html.Div([
			dcc.Graph(
	        id='graph_1',
	        figure=fig
	    	),
			]),

		# plot for the k means clustering graph
		# 1) plot all lat long points on graph with color coded z label and x and y axis labels
		# 2) create clustering class that finds most optimal number of clusters and creates them
		# 3) display your clusters on the scatter plot
		# 4) OPTIONAL - create an input of type text for the number of k's for the user to select
		# 5) Try adding labels so they see other data besides lats and longs
	    html.Div([
	    	dcc.Graph(
			id='graph_2',
			figure=fig2
			)
	    	])
	    
	])

	print('Loading Server...')
	app.run_server(debug=False)
	
if __name__ == '__main__':	
	main()