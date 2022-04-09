import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
# import dash                           # conda install -c conda-forge dash
# import dash_core_components as dcc    # conda install -c conda-forge dash-core-components
# import dash_html_components as html   # conda install -c conda-forge dash-html-components

# conda install -c anaconda gunicorn    # needed for deployment to heroku


# read the data from the source
url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
#print(trees.head(10))

#print(trees.shape)


# define dataframe for question 1
trees_q1 = trees[['spc_common','boroname','health']]
trees_q1['spc_common'].fillna('Unknown',inplace = True)
trees_q1.dropna(inplace = True)
# print(trees_q1)

# define dataframe for question 2
trees_q2 = trees[['health','boroname','steward']]
trees_q2.dropna(inplace = True)
print(trees_q2)

# trees_q2[['steward','health']] = trees_q2[['steward','health']].apply(lambda x : pd.factorize(x)[0])
# trees_q2_cor = pd.DataFrame(trees_q2.groupby(['boroname','spc_common']).corr())
# print(trees_q2_cor)


# get list of unique tree species
species = list(set(trees_q1['spc_common']))
species.sort()
#print(species)

# get list of unique boroughs
boroughs = list(set(trees['boroname']))
boroughs.sort()
#print(boroughs)

# get list of unique health values
health_statuses = list(set(trees_q1['health']))
health_statuses.sort()
#print(health_statuses)

#print(trees_q1)


def percentage_plot(df, col, target, species):

    temp_df = df.copy(deep=True)
    temp_df = temp_df[temp_df['spc_common'] == species]
    print(temp_df.head())

    # Creates a temporary dataframe to get the percentages
    #temp_df = df.groupby(col)['health'].value_counts(normalize=True)
    temp_df = temp_df.groupby(col)['health'].value_counts(normalize=True)
    temp_df = temp_df.mul(100).rename('Percent').reset_index()
    temp_df['Percent'] = temp_df['Percent'].round(decimals=1)

    # Plot the percentages with the temporary dataframe
    fig = px.bar(temp_df, x=col, y='Percent', color=target, 
                    barmode="group", text='Percent', title=f"Percent {target} By {col}")

    return fig



#q1_fig = percentage_plot(df=trees_q1, col='boroname', target='health', species='American elm')

#q1_fig.show()


def stewardHealth_plot(df, col, target, borough):

    temp_df = df.copy(deep=True)
    temp_df = temp_df[temp_df['boroname'] == borough]
    print(temp_df.head())

    # Creates a temporary dataframe to get the percentages
    #temp_df = df.groupby(col)['health'].value_counts(normalize=True)
    temp_df = temp_df.groupby(col)['health'].value_counts(normalize=True)
    temp_df = temp_df.mul(100).rename('Percent').reset_index()
    temp_df['Percent'] = temp_df['Percent'].round(decimals=1)

    # Plot the percentages with the temporary dataframe
    fig = px.bar(temp_df, x=col, y='Percent', color=target, 
                    barmode="group", text='Percent', title=f"Percent {target} By {col}")

    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['None','1or2','3or4','4orMore']})
    #fig.update_layout(xaxis={'categoryorder':'category ascending'})

    return fig



###############################################################################################

app = Dash(__name__)

app.layout = html.Div([
    html.H2('Module 4'),
    html.P('In this module we’ll be looking at data from the New York City tree census:'),
    html.A(href='https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh'.replace(' ','%20'), title='2015 Street Tree Census - Tree Data'.replace(' ','%20')),
    html.P('This data is collected by volunteers across the city, and is meant to catalog information about every single tree in the city.'),
    html.P('Build a dash app for a arborist studying the health of various tree species (as defined by the variable "spc_common") across each borough (defined by the variable ‘borough’). This arborist would like to answer the following two questions for each species and in each borough:'),
  
    html.H3('Question 1: What proportion of trees are in good, fair, or poor health according to the "health" variable?'),
    html.H4('Select Tree Species:'),
    dcc.Dropdown(
        id="treeSpecies_dd",
        options=species,
        value=species[0],
        clearable=False,
    ),
    dcc.Graph(id="treeHealthGraph"),

    html.H3('Question 2: Are stewards (steward activity measured by the "steward" variable) having an impact on the health of trees?'),
    html.H4('Select Borough:'),
    dcc.Dropdown(
        id="boroughs_dd",
        options=boroughs,
        value=boroughs[0],
        clearable=False,
    ),
    dcc.Graph(id="stewardHealthGraph")
])

@app.callback(
    Output(component_id="treeHealthGraph", component_property="figure"), 
    Input(component_id="treeSpecies_dd", component_property="value"))
def update_bar_chart(treeSpeciesSelection):
    fig = percentage_plot(df=trees_q1, col='boroname', target='health', species = treeSpeciesSelection)
    return fig


@app.callback(
    Output(component_id="stewardHealthGraph", component_property="figure"), 
    Input(component_id="boroughs_dd", component_property="value"))
def update_stew_health_bar_chart(boroughSelection):
    fig = stewardHealth_plot(trees_q2, col = 'steward', target = 'health', borough = boroughSelection)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)



