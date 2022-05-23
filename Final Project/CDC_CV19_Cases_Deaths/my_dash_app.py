from sodapy import Socrata
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import os.path
import sys
import json
import requests
import subprocess
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.express as px
import pycountry as pc

from requests.exceptions import RequestException
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from collections import namedtuple

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}
colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

# Reading The Dataset

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cdc.gov", None)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
Results = client.get("9mfq-cb36")

# Convert to pandas DataFrame
df = pd.DataFrame.from_records(Results)

# convert date time from string to date time type
df["submission_date"] = pd.to_datetime(df["submission_date"])
# sort the dataframe by dateTime
df = df.sort_values(by='submission_date', ascending=True)
# create a year column so we can use it in visualization by years
df['years'] = df.submission_date.map(lambda x: str(x)[0:4])
df['months'] = df.submission_date.map(lambda x: str(x)[5:7])

df['state_full_name'] = df['state'].replace(states)
df.tot_cases = df.tot_cases.astype('int64')
df.tot_death = df.tot_death.astype('int64')
# df.loc[(df['years'] == '2020') & (df['state'] == 'AL')
######


def filter_cases(year, state, df):
    if year == 'ALL' and state == 'ALL':
        return df
    if year != 'ALL' and state != 'ALL':
        return df.loc[(df['years'] == year) & (df['state'] == state)]
    if year != 'ALL':
        return df.loc[df['years'] == year]
    if state != 'ALL':
        return df.loc[df['state'] == state]

#######
# Defining App Layout


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Studying The Pandemic in USA states',
            style={'textAlign': 'center'}),
    dcc.Dropdown(
        # df['Indicator Name'].unique(),
        [{'label': 'Total Cases', 'value': 'tot_cases'}, {
            'label': 'Total_death', 'value': 'tot_death'}],
        'tot_cases',
        id='interest-variable'
    ),
    dcc.Graph(id='graph-with-options'),
    html.Div([
        html.Label('State options'),
        dcc.Dropdown(
            np.append(df['state'].unique(), 'ALL'),
            'ALL',
            id='state-column'
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
            # df['Indicator Name'].unique(),
            [{'label': 'All-years', 'value': 'ALL'},
             {'label': 'year-2020', 'value': '2020'},
                {'label': 'year-2021', 'value': '2021'},
                {'label': 'year-2022', 'value': '2022'},

             ],
            'ALL',
            id='years-dropdown'
        ),
        dcc.Dropdown(
            [{'label': 'Months', 'value': 'True'}, {
                'label': 'Years', 'value': 'False'}],
            'False',
            id='months-dropdown'
        ),
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    dcc.Graph(id='graph-with-dropdown'),
    html.Div([
        dcc.Dropdown(
            [{'label': 'Months', 'value': 'True'}, {
                'label': 'Years', 'value': 'False'}],
            'False',
            id='map-months-dropdown'
        ),
        dcc.Dropdown(
            # df['Indicator Name'].unique(),
            [{'label': 'All-years', 'value': 'ALL'},
             {'label': 'year-2020', 'value': '2020'},
             {'label': 'year-2021', 'value': '2021'},
             {'label': 'year-2022', 'value': '2022'},

             ],
            'ALL',
            id='map_years-dropdown'
        ),
    ], style={'width': '20%', 'float': 'center', 'display': 'inline-block'}),
    dcc.Graph(id='map-with-options'),
])


@app.callback(
    Output('graph-with-options', 'figure'),
    Input('interest-variable', 'value'),)
def update_scatter(interest_variable):
    fig = px.scatter(df,
                     x=interest_variable,
                     y=df.state,
                     size='tot_cases',
                     color='state_full_name',
                     hover_name='state_full_name',
                     template='plotly_white',
                     labels={'tot_cases': 'Total number of cases',
                             'y': 'State Name'},
                     title='Total Cases VS State Name')
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('graph-with-dropdown', 'figure'),
    Input('state-column', 'value'),
    Input('years-dropdown', 'value'),
    Input('months-dropdown', 'value'),
)
def update_scatter(state, year, month):
    if month == "True":
        fig = px.bar(filter_cases(year, state, df),
                     # the task is to create a function that filter the df based on state and year and month
                     #x=df.state[df['state'] == 'Texas'],
                     #y=df.tot_cases[df['state'] == 'Texas'],
                     x='state_full_name',
                     y='tot_cases',
                     color='months',
                     # color = df.years[df['state'] == 'Texas'],
                     template='plotly_white',
                     barmode='group',
                     labels={'state_full_name': 'State Name',
                              'tot_cases': 'Total cases',
                             },
                     title='Total Cases per State by year')
        fig.update_layout(transition_duration=500)

        return fig
    else:
        fig = px.bar(filter_cases(year, state, df),
                     # the task is to create a function that filter the df based on state and year and month
                     #x=df.state[df['state'] == 'Texas'],
                     #y=df.tot_cases[df['state'] == 'Texas'],
                     x='state_full_name',
                     y='tot_cases',
                     color='years',
                     # color = df.years[df['state'] == 'Texas'],
                     template='plotly_white',
                     barmode='group',
                     labels={'state_full_name': 'State Name',
                              'tot_cases': 'Total cases',
                             },
                     title='Total Cases per State by year')
        fig.update_layout(transition_duration=500)
        return fig

# @app.callback(
#     Output('graph-with-dropdown', 'figure'),
#     Input('state-column', 'value'),
#     Input('years-dropdown', 'value'),
#     Input('months-dropdown', 'value'),
#     )

# def update_scatter(state,year,month):

#     fig = px.bar(filter_cases(year , state , df),
#                   ## the task is to create a function that filter the df based on state and year and month
#                   #x=df.state[df['state'] == 'Texas'],
#                   #y=df.tot_cases[df['state'] == 'Texas'],
#                   x =  'state_full_name',
#                   y =  'tot_cases',
#                   color='months',
#                   # color = df.years[df['state'] == 'Texas'],
#                   template='plotly_white',
#                   barmode='group',
#                   labels={'state_full_name':'State Name',
#                           'tot_cases': 'Total cases',
#                 },
#                   title='Total Cases per State by year')
#     fig.update_layout(transition_duration=500)
#     return fig


@app.callback(
    Output('map-with-options', 'figure'),
    Input('map-months-dropdown', 'value'),
    Input('map_years-dropdown', 'value'),
)
def update_scatter(month, year):
    if month == "True":
        if year == "ALL":
            fig = px.choropleth(df,
                                locations='state',
                                color='tot_cases',
                                template='plotly_white',
                                color_continuous_scale="Viridis_r",
                                animation_frame="months",
                                locationmode="USA-states",
                                basemap_visible=True,
                                scope="usa",
                                height=600,
                                width=800,
                                title="Total cases per state in the US Map",
                                hover_name="state_full_name",
                                labels={"tot_cases": 'Total cases per State',
                                        'state_codes': 'State Code'})
            fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
            fig.show()

            return fig

        else:
            fig = px.choropleth(df[df['years'] == year],
                                locations='state',
                                color='tot_cases',
                                template='plotly_white',
                                color_continuous_scale="Viridis_r",
                                animation_frame="months",
                                locationmode="USA-states",
                                basemap_visible=True,
                                scope="usa",
                                height=600,
                                width=800,
                                title="Total cases per state in the US Map",
                                hover_name="state_full_name",
                                labels={"tot_cases": 'Total cases per State',
                                        'state_codes': 'State Code'})
            fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
            fig.show()

            return fig
    else:
        if year == "ALL":
            fig = px.choropleth(df,
                                locations='state',
                                color='tot_cases',
                                template='plotly_white',
                                color_continuous_scale="Viridis_r",
                                animation_frame="years",
                                locationmode="USA-states",
                                basemap_visible=True,
                                scope="usa",
                                height=600,
                                width=800,
                                title="Total cases per state in the US Map",
                                hover_name="state_full_name",
                                labels={"tot_cases": 'Total cases per State',
                                        'state_codes': 'State Code'})
            fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
            fig.show()

            return fig
        else:
            fig = px.choropleth(df[df['years'] == year],
                                locations='state',
                                color='tot_cases',
                                template='plotly_white',
                                color_continuous_scale="Viridis_r",
                                animation_frame="years",
                                locationmode="USA-states",
                                basemap_visible=True,
                                scope="usa",
                                height=600,
                                width=800,
                                title="Total cases per state in the US Map",
                                hover_name="state_full_name",
                                labels={"tot_cases": 'Total cases per State',
                                        'state_codes': 'State Code'})
            fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
            fig.show()

            return fig


if __name__ == '__main__':
    app.run_server(debug=True)
