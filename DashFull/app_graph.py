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

class Graph:

	# create layout for graph
	def layout_setup():

		layout = go.Layout(
			title = {'text':'Ministry Monthly Budget Amount vs End Date',
				'font': {'size':28, 
				'family':'Arial'}},
			width=1500,
			height=500,
			autosize = False,
			xaxis={
				'title':'EndDate',
				'zeroline': False,
				"showline": False,
				"showticklabels":True,
				'showgrid':True,
				'domain': [0, 1],
				'side': 'right',
				# 'anchor': 'x2',
				},
			yaxis={
				'title':'MinistryMonthlyBudgetAmount',
				'domain': [0, 1],
		        # 'anchor': 'y2',
				'autorange': 'reversed',
			},

		margin=dict(l=100, r=20, t=70, b=70),
			paper_bgcolor='rgb(204, 204, 204)',
	    	plot_bgcolor='rgb(204, 204, 204)',
            )
		return layout

	# return data to be traced
	def graph_trace(df):
		trace_graph = []
		x = []
		y = []
		df = df.sort_values(by=['EndDate'])
		x = df['EndDate']
		y = df['MinistryMonthlyBudgetAmount']

		trace_graph.append(go.Scatter( x=x, y=y , mode='markers',
			marker=dict(
	            	color='rgba(91, 207, 135, 0.3)',
	            	line=dict(
	                	color='rgba(91, 207, 135, 2.0)',
	                	width=0.5),
	        	),))


		return trace_graph


	