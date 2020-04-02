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
import cufflinks as cf
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


# print('before layout set up')
# df = parse_data(contents, filename)
# df = pd.read_csv('../../Data/OutsideData/smaller_data_for_Kmeans.csv')
# layout = mp.layout_setup(df)	
# trace_map = mp.map_trace(layout)
fig = None
# fig=go.Figure(data=trace_map, layout=layout)

app.layout = html.Div([

		html.H1(children=''),

		# uploader
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

		dcc.Graph(
			id = 'graph_1'
			# id='graph_1',
			# figure=fig
			),
		html.Div(id='output-data-upload')
		])

def parse_data(contents, filename):
	print('parsing data')
	print('filename: {}'.format(filename))
	print(type(contents))
	contents = str(contents)
	print(type(contents))
	# print(contents)
	print('contents^^^^')
	# contents = list(content)

	# the address column has a , that seperates the values
	# this split is what is confusing it
	# it is seperating the dataframe into a list but since address has more 
	# commas it thinks that this needs to be seperated as well
	# content_type, content_string = contents.split(',')
	content_list = []
	content_list = contents.split(',')
	print(content_list)
	print('CONTENT_LIST^^^^^^^^^^^^')
	# exit()
	print('Zip: {}'.format(content_list[8]))
	print('Num_People: {}'.format(content_list[5]))
	print('Budget: {}'.format(content_list[1]))
	print('Mnths_Passed: {}'.format(content_list[17]))
	# exit()
	# print(content_string)
	# print(content_type)
	print(content_list)

	# there is an error here when we decode the content
	# try using \\ to escape commas in the text with the original "formatted_lat_long_for_Kmeans.csv"
	# example: df = pd.read_csv('temp.csv', header=0, escapechar='\\')

	decoded = base64.b64decode(content_string)
	try:
		if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
			print('formatting csv')
			df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), error_bad_lines=False).sample(frac=0.25)
			print(df.head())

		elif 'xls' in filename:
            # Assume that the user uploaded an excel file
			df = pd.read_excel(io.BytesIO(decoded))
		elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
			df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')

	except Exception as e:
		print(e)
		return html.Div([
            'There was an error processing this file.'
		])
	print('df data type is:')
	print(type(df))
	df.to_csv('../../Data/OutsideData/output.csv')
	return df

@app.callback(Output('graph_1', 'figure'),
	[
		Input('upload-data', 'contents'),
		Input('upload-data', 'filename')
	])

# is tied to the callback, the input comes from the user uploads 
def update_map(contents, filename):
	print('updating map')
	global trace_map
	global fig

	# if contents:
	# 	# parse the data uploaded into a pandas dataframe
	# 	df = parse_data(contents, filename)
	# 	# set up a layout based on the dataframe
	# 	# df = pd.read_csv('../../Data/OutsideData/smaller_data_for_Kmeans.csv')
	# 	layout = mp.layout_setup(df)
	# 	# return a new list based on a layout	
	# 	trace_map = mp.map_trace(layout)
	# 	# return a new figure based on the layout and the data created 
	# 	fig=go.Figure(data=trace_map, layout=layout)

	# else:
		# fig=go.Figure(
		# 	data=None,
		# 	layout=None)

		
	df = pd.read_csv('../../Data/OutsideData/smaller_data_for_Kmeans_copy.csv')
	layout = mp.layout_setup(df)
	# return a new list based on a layout	
	trace_map = mp.map_trace(layout)
	# return a new figure based on the layout and the data created 
	fig=go.Figure(data=trace_map, layout=layout)

	return fig

if __name__ == '__main__':
	app.run_server(debug=False)
	# app.run_server(debug=True)