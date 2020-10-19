# application to simply compare covid dat between switzerland and Lombardy. Made for my mum

### main file that runs all the functions:
# 1- Update source data
# 2- Get differences
# 3- Calculate differences and plot
# 4- print or update output


# Imports
import os

print(os.environ)

import requests as rq
import pandas as pd
import os
import random
# --------------------------------- plotting libraries --------------------------------------
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
# --------------------------------- dash libraries --------------------------------------
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


# return app

# data preparation
def select_columns(country_name, source_raw):
    country_df = pd.DataFrame({
        'date': source_raw[source_raw[' Country'] == country_name]['Date_reported'],
        'new_cases': source_raw[source_raw[' Country'] == country_name][' New_cases'],
        'cum_deaths': source_raw[source_raw[' Country'] == country_name][' Cumulative_deaths'],
        'cum_cases': source_raw[source_raw[' Country'] == country_name][' Cumulative_cases'],
    })
    # turn date as date object
    country_df[['date']] = [pd.to_datetime(i, format="%Y-%m-%d") for i in source_raw['date']]
    return country_df


# merging together layers from ch and lombardy
def create_new_columns(country_df, window_size=7, ratio=100):
    country_df['new_cases_smooth'] = ['new_cases'].rolling(window=window_size).mean().fillna(0).astype(int)
    country_df['deaths_ratio'] = ratio * country_df['cum_deaths'] / country_df['cum_cases']
    return country_df


## --------------------------------------PLOTTING-------------------------------------------------
"""

Current plots:
1- New cases by month
2- Deaths per 1000 new cases and trend 
3- Recovered per 1000  new cases and trend # TODO
"""
# PARAMS
cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
         'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
         'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']


# FUNCTIONS

def create_country_palette(country_df):
    un_m = country_df.index.month.unique()
    # pick a color
    col = random.sample(cmaps)
    # create palette as hex
    palette = sns.color_palette(col, n_colors=len(un_m) + 2).as_hex()
    return palette, col


def plot_new_cases(country_df, country_name, color_palette):
    # create figure
    fig1 = make_subplots(rows=1, cols=2,
                         subplot_titles=('Lombardia', 'Svizzera'),
                         shared_yaxes=True
                         )
    un_m = country_df.index.month.unique()
    m_traces = []
    c_c = 0
    m_s = 2  # marker size
    m_o = 0.8  # marker opacity
    for m in un_m:
        # data selection
        temp = country_df[country_df.index.month == m]
        current = temp['new_cases']
        # prepare string and colour
        month_s = pd.to_datetime("2020-1-1").replace(month=int(m)).month_name()
        current_col = color_palette[c_c]
        monthly = go.Scatter(x=temp.index.day,
                             y=temp,
                             name=f"{month_s}",
                             marker_color=current_col,
                             line={'width': m_s},
                             opacity=m_o,
                             mode="lines",
                             hovertemplate=f"Lombardia: %{{x}} {month_s}<br>nuovi casi (media sett.): %{{y:.1f}}",
                             showlegend=True
                             )
        m_traces.append(monthly)
        if m == pd.to_datetime('today').month:
            # change viz param for current month
            m_o = 1  # marker opacity
            m_s = 3  # marker size
            current_col = color_palette[c_c + 1]

            # remove for filled area
            area_1 = go.Scatter(x=temp.index.day,
                                y=temp,
                                fill=None,
                                mode='lines',
                                line_color=current_col,
                                showlegend=False
                                )

            area_2 = go.Scatter(x=temp.index.day,
                                y=current,
                                fill='tonexty',  # fill area between trace0 and trace1
                                mode='lines',
                                line={'color': current_col, 'width': 1},
                                name=f"{country_name} current month",
                                hovertemplate=f"{country_name}: %{x}<br>new cases : %{y:.1f}",

                                )
            m_traces.extend([area_1, area_2])

        c_c = c_c + 1
    fig1.add_traces(m_traces)
    fig1.update_layout(plot_bgcolor="white", )
    fig1.update_yaxes(showgrid=True, gridwidth=0.2, gridcolor='lightgrey')
    return fig1


def plot_deaths(country_df, country_name, palette):
    """returns trace only"""
    trace = go.Scatter(x=country_df.index,
                       y=country_df['cum_deaths'],
                       mode='markers',
                       name=country_name,
                       marker_size=[(4 * a / max(country_df['deaths_ratio'])) ** 2 for a in
                                    country_df['deaths_ratio']],
                       marker_color=[country_df[int(i)] for i in country_df.index.month.values])
    return trace


# -----

def main():
    source_url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'

    source_raw = pd.read_csv(source_url)

    # TODO: add interactive app
    # for testing:
    country_name1 = "Italy"
    country_name2 = "Switzerland"

    # prepare data
    country1_df = select_columns(country_name1, source_raw)
    country1_df = create_new_columns(country1_df)

    country2_df = select_columns(country_name2)
    country2_df = create_new_columns(country2_df)

    print("data_prepared : ")
    print(country1_df.tail())
    print(country2_df.tail())

    # ------ PLOTS -------------

    # create palette
    palette_c1, col1 = create_country_palette(country1_df)
    palette_c2, col2 = create_country_palette(country2_df)
    while col1 == col2:
        print("colors picked are the same. finding new palette")
        palette_c2, col2 = create_country_palette(country2_df)
    # plot 1
    fig1_c1=plot_new_cases(country1_df,country_name1,palette_c1)
    fig1_c2=plot_new_cases(country2_df,country_name2,palette_c2)
    # plot 2
    # create figure
    fig2 = make_subplots(1, 1)
    fig2.update_layout(plot_bgcolor="white")
    fig2.update_yaxes(showgrid=True, gridwidth=0.2, gridcolor='lightgrey', title_text='cumulative deaths')
    # add trace from country 1
    fig2.add_trace(plot_deaths(country1_df, country_name1, palette_c1))
    # add trace from country 2
    fig2.add_trace(plot_deaths(country2_df, country_name2, palette_c2))
    # ----- DASH APP -----------
    external_stylesheets = ['assets/stylesheet.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    server = app.server  # important for heroku

    # Define app layout
    app.layout = html.Div([
        # Header
        html.H1(className='h1', children='Covid for Mums',

                ),

        html.Div(className="h1", children='A Dash web application framework for COVID analysis',

                 ),

        # separation line
        html.Hr(),

        # 3rd header
        html.Div([
            html.H3(className="h3", children="Hi Mum, here are today's new cases:"),
            html.Div(children=[
                html.Div(children=country_name1),
                html.Div(country1_df['new_cases'].iloc[-1])
            ],
                className="pretty_container",
                style={'display': 'inline-block', 'background-color': '#9FA4F5',
                       'color': "white",
                       'font-weight': 'bold', 'font-size': '200%'}

            ),
            html.Div(children=[
                html.Div(children=country_name2),
                html.Div(country2_df['new_cases'].iloc[-1])
            ],
                className='pretty_container',
                style={'display': 'inline-block', 'display': 'inline-block', 'background-color': '#ffa6b9',
                       'color': "white",
                       'font-weight': 'bold', 'font-size': '200%'}
            ),
        ],
            style={'padding-left': '40%'}
        ),
        # Time series plot of global confirmed cases
        html.Div(children=[
            html.H3(children="This is the monthly trend of new cases"),
            html.Div(
                children="New cases have been translated in weekly average, except for the last month.\
                 The lighter the colors the further away in the past"),
                    html.Div(children=dcc.Graph(figure=fig1_c1),
                             className="pretty_container",
                             style={'display': 'inline-block'} ),
                    html.Div(children=dcc.Graph(figure=fig1_c1),
                             className="pretty_container",
                            style={'display': 'inline-block'})

            # add trace for each country

        ], className="h1"),

        # time series of deaths and ratio over cases
        html.Div(children=[
            html.H3(children="This is the cumulative trend of deaths", className='h3'),
            # html.H3(className="h3", children='Ciao mamma \n, ecco i nuovi casi di oggi:'),
            html.Div(children="Dot size gives you an idea of the relationship between new cases and deaths"),
            dcc.Graph(figure=fig2)
        ],
        ),
        html.Aside(className=".sidebar a",
                   children="Made by Matteo Jucker Riva Thanks to propulsion Academy for all the skills", )
    ])
    return app

app = main()

if __name__ == '__main__':
    # run app
    app.run_server(debug=False)

"""

# plot 2 cumulative deaths
fig2 = make_subplots(rows=1, cols=1,
                     shared_yaxes=True
                     )
fig2.add_trace(go.Scatter(x=combined.index,
                          y=combined['cum_deaths_lom'],
                          mode='markers',
                          name='Lombardia',
                          marker_size=[(4 * a / max(combined['deaths_ratio_lom'])) ** 2 for a in
                                       combined['deaths_ratio_lom']],
                          marker_color=[pal_lom[int(i)] for i in combined.index.month.values]
                          ))

fig2.add_trace(go.Scatter(x=combined.index,
                          y=combined['cum_deaths_ch'],
                          mode='markers',
                          name="Svizzera",
                          marker_size=[(4 * a / max(combined['deaths_ratio_ch'])) ** 2 for a in
                                       combined['deaths_ratio_ch']],
                          marker_color=[pal_ch[int(i)] for i in combined.index.month.values]
                          ))

fig2.update_layout(plot_bgcolor="white")
fig2.update_yaxes(showgrid=True, gridwidth=0.2, gridcolor='lightgrey', title_text='cumulative deaths')
# fig2.show()

## --------------------------------------DASHBOARD-------------------------------------------------
colors = {
    'background': '#0',
    'text': 'rgb(135,206,250)',
    'text2': 'black',
    'text3': 'orange'
}

# we use a pre-defined css file. feel free to try others!
external_stylesheets = ['assets/stylesheet.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets )
server = app.server

# Define app layout
app.layout = html.Div([
    # Header
    html.H1(className='h1', children='Mamma il Covid',


            ),

    html.Div(className="h1", children='Visualization: A Dash web application framework for COVID analysis',

             ),

    # separation line
    html.Hr(),

    # 3rd header
    html.Div([
            html.H3(className="h3", children='Ciao mamma \n, ecco i nuovi casi di oggi:'),
            html.Div(children=[
                     html.Div(children="Lombardia"),
                     html.Div(combined['new_cases_lom'].iloc[-1])
                     ],
                className="pretty_container",
                style={'display': 'inline-block', 'display': 'inline-block', 'background-color':'#9FA4F5',
                       'color': "white",
                       'font-weight': 'bold', 'font-size': '200%'}


            ),
            html.Div(children=[
                     html.Div(children="Svizzera"),
                     html.Div(combined['new_cases_ch'].iloc[-1] )
                     ],
            className='pretty_container',
            style={'display': 'inline-block', 'display': 'inline-block', 'background-color':'#ffa6b9','color': "white",
                  'font-weight': 'bold', 'font-size': '200%' }
                  ),
        ],
    style={'padding-left': '40%'}
),
    # Time series plot of global confirmed cases
    html.Div(children=[
            html.H3(children="Questo è l'andamento mensile dei nuovi contagiati"),
            html.Div(children="I nuovi casi giornalieri sono stati trasformarti in media settimnale, tranne che per l'ultimo mese."),
            dcc.Graph(figure=fig1)
            ], className="h1"),




    # time series of deaths and ratio over cases
    html.Div(children=[
            html.H3(children="Questo è l'andamento delle morti.", className='h3'),
            #html.H3(className="h3", children='Ciao mamma \n, ecco i nuovi casi di oggi:'),
            html.Div(children="Il diametro dei punti rappresenta la proporzione tra morti e nuovi casi"),
            dcc.Graph(figure=fig2)
],
     ),
    html.Aside(className=".sidebar a", children="Made by Matteo Jucker Riva Thanks to propulsion Academy for all the skills", )
])
"""
