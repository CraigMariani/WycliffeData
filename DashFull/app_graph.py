# basic time vs financial data
import base64
import datetime
import io
import plotly.graph_objs as go
# import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

class Graph:

	# parsing data from uploader
	def parse_data(contents, filename):
	    content_type, content_string = contents.split(',')

	    decoded = base64.b64decode(content_string)
	    try:
	        if 'csv' in filename:
	            # Assume that the user uploaded a CSV or TXT file
	            df = pd.read_csv(
	                io.StringIO(decoded.decode('utf-8'))).sample(frac=0.25)
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

	    return df

	@app.callback(Output('Mygraph', 'figure'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])

	# update line graph
	def update_graph(contents, filename):
	    fig = {
	        'layout': go.Layout(
	            plot_bgcolor=colors["graphBackground"],
	            paper_bgcolor=colors["graphBackground"])
	    }

	    if contents:
	        contents = contents[0]
	        filename = filename[0]
	        df = parse_data(contents, filename)
	        df = df.set_index(df.columns[0])
	        fig['data'] = df.iplot(asFigure=True, kind='scatter', mode='lines+markers', size=1)


	    return fig

	@app.callback(Output('output-data-upload', 'children'),
        [
            Input('upload-data', 'contents'),
            Input('upload-data', 'filename')
        ])