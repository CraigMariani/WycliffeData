# interactive choropleth map 


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


# df = pd.read_csv('../../Data/OutsideData/smaller_data_for_Kmeans.csv')

# df = cln.parse_data(contents, filename)
df = None
selection = None
addresses = None

mapbox_accesstoken = 'pk.eyJ1IjoiY3JhaWdtYXJpYW5pIiwiYSI6ImNrNnk2bWQ0NjBxNmMzbG84OGpsa2IwMnQifQ.Hy10gEAc9eolUbu_lLgTMQ'
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

layout = None
class Map:
	

	def map_trace(layout):
	
		trace_map = []
		global df
		global selection
		global US_data

		global mapbox_accesstoken
		global pl_deep

		global addresses

		for attribute in selection:
			trace_map.append(go.Choroplethmapbox(
				geojson=US_data,
				locations=df['PostalCode_y'].tolist(),
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
		# print(trace_map[0]['locations'])
		# print(trace_map[0]['text'])
		print('Trace Map')
		# print(trace_map)
		return trace_map


	# initialize layout
	def layout_setup(df_imported):
		print('in setup')
		global US_data
		global pl_deep
		global mapbox_accesstoken
		
		global df
		global selection
		global layout
		global addresses

		df = df_imported
		# df = cln.full_cleaner(df_imported)
		df = pd.DataFrame(df)
		print('Showing contents::::')
		print(df.head())
		selection = list(df.columns)
		addresses = df['Address'].str.title().tolist()
		



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
