# full app is run here
# will have table, map, and other graphs imported here and displayed through this file
# but will have an uploader that reaches all of these files

# import cufflinks as cf

# for dash
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# for data science libraries
import pandas as pd
import numpy as np

# for graphs
import plotly
import plotly.graph_objs as go 
import base64
import datetime
import io

# for geojson file in map
import json
from urllib.request import urlopen 

# local custom files
from production_cleaner import Cleaner as cln
# from app_table import Table as tbl
# from app_graph import Graph as grph
# from app_scatter import Scatter as scttr
from app_map import Map as mp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# returns a list of data and a layout for graph
def graph():
	pass

# returns a list of data and a layout for scatter
def scatter():
	pass

# returns a list of data and a layout for map
def map():
	print('layout setup')
	layout = mp.layout_setup()
	# layout_setup()
	
	trace_map = mp.map_trace(layout)
	return trace_map, layout
	


def main():
	global app

	trace_map, layout = map()
	layout = mp.layout_update(layout)

	fig=go.Figure(data=trace_map, layout=layout)
	app.layout = html.Div([

		html.H1(children=''),

		# uploader
		html.Div([
			dcc.Upload(
	        	id='upload-data',
	        	children=html.Div([
	            	'Drag and Drop or ',
	            	html.A('Select Files')
	        	]),
	        	style={
		            'width': '100%',
		            'height': '60px',
		            'lineHeight': '60px',
		            'borderWidth': '1px',
		            'borderStyle': 'dashed',
		            'borderRadius': '5px',
		            'textAlign': 'center',
		            'margin': '10px'
	        	},
		        # Allow multiple files to be uploaded
		        multiple=True
    		),
		])
		
		html.Div([
			dcc.Graph(
				id='graph_1',
				figure=fig
			),
		])
		
		html.Div(id='output-data-upload')
		])

	print('loading server')
	app.run_server(debug=True)

if __name__ == '__main__':
    main()