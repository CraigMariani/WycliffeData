# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.title = 'Dash Tutorial'

#Bootstrap CSS.
app=dash.Dash(__name__, external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css'])

app.layout = html.Div(
    html.Div([
        html.Div([
            html.Img(
                src="https://lakeforest.org/wp-content/uploads/2017/08/wycliffe-logo-colour.jpg",
                className='three columns',
                style={
                    'height': '25%',
                    'width': '25%',
                    'float': 'right',
                    'position': 'relative',
                    'margin-bottom': 100
                    # 'margin-right': 20
                },
            ),
            html.H1(children='Wycliffe Data Visualization Model',
                    className = "nine colums"),
            html.Div(children='''
                        Dash: A web application framework for Python.
                        ''',
                    className = 'nine columns')
        ], className="row"),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data':[
                            {'x': [1,2,3], 'y': [4,1,2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1,2,3], 'y': [2,4,5], 'type': 'bar', 'name': 'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization',
                            'xaxis' : dict(
                                title='x Axis',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='y Axis',
                                titlefont=dict(
                                family='Helvetica, monospace',
                                size=10,
                                color='#7f7f7f'
                            ))
                        }
                    }
                )
            ], className='six columns'),
        html.Div([
            dcc.Graph(
                id='example-graph-2',
                figure={
                    'data':[
                        {'x': [1,2,3], 'y': [4,1,2], 'type': 'line', 'name': 'SF'},
                        {'x': [1,2,3], 'y': [2,4,5], 'type': 'line', 'name': 'Montréal'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization',
                        'xaxis' : dict(
                            title='x Axis',
                            titlefont=dict(
                            family='Courier New, monospace',
                            size=20,
                            color='#7f7f7f'
                        )),
                        'yaxis' : dict(
                            title='y Axis',
                            titlefont=dict(
                            family='Helvetica, monospace',
                            size=10,
                            color='#7f7f7f'
                        ))
                    }
                }
            )
        ], className='six columns')
    ], className="row")
    ], className='ten columns offset-by-one')
)

if __name__ == '__main__':
    app.run_server(debug=True)
