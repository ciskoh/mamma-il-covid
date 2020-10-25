# application to simply compare covid dat between switzerland and Lombardy. Made for my mum

### main file that runs all the functions:
# 1- Update source data
# 2- Get differences
# 3- Calculate differences and plot
# 4- print or update output


# Imports
import pandas as pd
import random
import datetime
# --------------------------------- plotting libraries --------------------------------------
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
# --------------------------------- dash libraries --------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ----- PARAMETERS -----------
source_url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'  # source of covid data
source_raw = pd.read_csv(source_url)
country_list = source_raw[' Country'].unique()

source_pop = 'assets/pop.csv'  # population data for normalisation
pop_df = pd.read_csv(source_pop)

cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
         'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
         'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']


# palettes
def create_country_palette(source_raw):
    palette_len = datetime.datetime.today().month - pd.to_datetime(source_raw['Date_reported'][0]).month
    # pick a color
    col = random.sample(cmaps, 1)[0]
    # create palette as hex
    palette = sns.color_palette(col, n_colors=palette_len + 2).as_hex()
    return palette, col


palette_c1, col1 = create_country_palette(source_raw)
col2 = col1
while col1 == col2:
    palette_c2, col2 = create_country_palette(source_raw)

# ----- DASH APP -----------

external_stylesheets = ['assets/stylesheet.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server  # important for heroku

# Define app layout
app.layout = html.Div([
    # Header
    html.H1(className='h1', children='Covid data for Mums'),
    html.Div(className="h1", children='A Dash web application framework to compare Covid data in 2 different countries'),
    html.Div(children=[dcc.Dropdown(id="selector1", options=[{'label': c, 'value': c} for c in country_list],
                                    value='Italy',
                                    placeholder="Select a country",
                                    multi=False,
                                    clearable=True,
                                    className='Selector'

                                    ),
                       dcc.Dropdown(id="selector2",
                                    options=[{'label': c, 'value': c} for c in country_list],
                                    value='Switzerland',
                                    placeholder="Select a country",
                                    multi=False,
                                    clearable=True,
                                    className='Selector'
                                    ), ]
             ),
    # separation line
    html.Hr(),

    # First plot
    html.Div([
        html.H3(className="h3", children="Hi Mum, here are today's new cases for (cases per 100'000 people):"),
        html.Div(children=[
            html.Div(id="country_name1", children=None),
            html.Div(id="c1_new_cases", children=None)
        ],
            className="pretty_container",
            style={'display': 'inline-block', 'background-color': palette_c1[-4],
                   'color': "white",
                   'font-weight': 'bold', 'font-size': '200%'}
        ),
        html.Div(children=[
            html.Div(id="country_name2", children=None),
            html.Div(id="c2_new_cases", children=None)
        ],
            className='pretty_container',
            style={'display': 'inline-block',
                   'background-color': palette_c2[-4],
                   'color': "white",
                   'font-weight': 'bold',
                   'font-size': '200%'}
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
        html.Div(id="Nc_plot_1", children=dcc.Graph(id="fig1_c1"),
                 className="pretty_container",
                 style={'display': 'inline-block'}),

        html.Div(children=dcc.Graph(id="fig1_c2"),
                 className="pretty_container",
                 style={'display': 'inline-block'})

        # add trace for each country

    ], className="h1"),

    # time series of deaths and ratio over cases
    html.Div(children=[
        html.H3(children="This is the cumulative trend of deaths", className='h3'),
        # html.H3(className="h3", children='Ciao mamma \n, ecco i nuovi casi di oggi:'),
        html.Div(children="Dot size gives you an idea of the relationship between new cases and deaths"),
        dcc.Graph(id="fig2" )
    ],
    ),
    html.Aside(className=".sidebar a",
               children="Made by Matteo Jucker Riva Thanks to propulsion Academy for all the skills", )
])

# ---- data preprations
"""these functions extract the data form the raw dataframe and create additional columns.  \
The data_prep_wrapper calls all other functions"""


# data preparation
def select_columns(country_name, source_raw):
    country_df = pd.DataFrame({
        'date': source_raw[source_raw[' Country'] == country_name]['Date_reported'],
        'new_cases': source_raw[source_raw[' Country'] == country_name][' New_cases'],
        'cum_deaths': source_raw[source_raw[' Country'] == country_name][' Cumulative_deaths'],
        'cum_cases': source_raw[source_raw[' Country'] == country_name][' Cumulative_cases'],
    })

    # turn date as date object & set as index
    country_df[['date']] = [pd.to_datetime(i, format="%Y-%m-%d") for i in country_df['date']]
    country_df = country_df.set_index('date')
    # replace nas
    country_df = country_df.fillna(0)
    return country_df


def make_pop_ratio(country_df, country_name, pop):
    pop_n = int(pop[pop['Country'] == country_name]['Pop_2020'])
    country_df = 100000 * country_df / pop_n
    return country_df.round(10)


# merging together layers from ch and lombardy
def create_new_columns(country_df, window_size=7, ratio=100):
    country_df['new_cases_smooth'] = country_df['new_cases'].rolling(window=window_size).mean().fillna(0).astype(int)
    country_df['deaths_ratio'] = ratio * country_df['cum_deaths'] / country_df['cum_cases']
    country_df = country_df.fillna(0)
    return country_df


# high level function
def data_prep_wrapper(country_name, source_raw=source_raw, pop=pop_df):
    country_df = select_columns(country_name, source_raw)
    country_df = make_pop_ratio(country_df, country_name, pop_df)
    country_df = create_new_columns(country_df)
    return country_df


# plotting FUNCTIONS
"""These functions create the interactive plots and figures for each plot. Are called by the update functions"""


def plot_new_cases(country_df, country_name, color_palette):
    # create figure
    fig1 = make_subplots()
    un_m = country_df.index.month.unique()
    m_traces = []
    c_c = 0
    for m in un_m:
        temp = country_df[country_df.index.month == m]
        month_s = pd.to_datetime("2020-1-1").replace(month=int(m)).month_name()
        current_col = color_palette[c_c]

        if m == pd.to_datetime('today').month:
            current = temp['new_cases']
            # change viz param for current month
            m_o = 1  # marker opacity
            m_s = 3  # marker size
            current_col = color_palette[c_c + 1]

            # remove for filled area
            area_1 = go.Scatter(x=temp.index.day,
                                y=temp['new_cases_smooth'],
                                fill=None,
                                mode='lines',
                                line_color=current_col,
                                marker_size=m_s,
                                hovertemplate=f"{country_name}" + ": %{x}" + "{month_s}<br>new cases (weekly avg):" + "%{y:.1f}",
                                showlegend=False
                                )

            area_2 = go.Scatter(x=temp.index.day,
                                y=current,
                                fill='tonexty',  # fill area between trace0 and trace1
                                mode='lines',
                                line={'color': current_col, 'width': 1},
                                name=f"current month",
                                hovertemplate=f"{country_name}" + ": %{x}<br>new cases : %{y:.1f}",
                                )
            m_traces.extend([area_1, area_2])
        else:
            m_s = 2  # marker size
            m_o = 0.8  # marker opacity
            monthly = go.Scatter(x=temp.index.day,
                                 y=temp['new_cases_smooth'],
                                 name=f"{month_s}",
                                 marker_color=current_col,
                                 line={'width': m_s},
                                 opacity=m_o,
                                 mode="lines",
                                 hovertemplate=f"{country_name}" + ": %{x}" + "{month_s}<br>new cases (weekly avg):" + "%{y:.1f}",
                                 showlegend=True
                                 )
            m_traces.append(monthly)
        c_c = c_c + 1
    fig1.add_traces(m_traces)
    fig1.update_layout(plot_bgcolor="white", )
    fig1.update_yaxes(type='log', showgrid=True, gridwidth=0.2, gridcolor='lightgrey')
    return fig1


def plot_deaths(country_df, country_name, palette):
    """returns trace only"""
    m_s = [(4 * a / max(country_df['deaths_ratio'])) ** 2 for a in country_df['deaths_ratio']]
    trace = go.Scatter(x=country_df.index,
                       y=country_df['cum_deaths'],
                       mode='markers',
                       name=country_name,
                       marker_size=[(4 * a / max(country_df['deaths_ratio'])) ** 2 for a in country_df['deaths_ratio']],
                       marker_color=[palette[int(i)] for i in country_df.index.month.values])
    return trace


# -------------- UPDATE FUNCTIONS
""" These function directly update the plots in the dashboard, using callbacks from the dropdown selector"""


@app.callback(
    [Output('country_name1', 'children'),
     Output('c1_new_cases', 'children')],
    Input('selector1', 'value')
)
def update_panel_c1(country_name):
    country_df = data_prep_wrapper(country_name)
    return country_name, round(country_df['new_cases'].iloc[-1], 2)


@app.callback(
    [Output('country_name2', 'children'),
     Output('c2_new_cases', 'children')],
    Input('selector2', 'value')
)
def update_panel_c2(country_name):
    country_df = data_prep_wrapper(country_name)
    return country_name, round(country_df['new_cases'].iloc[-1], 2)


@app.callback(Output('fig1_c1', 'figure'),
              Input('selector1', 'value'))
def update_plot_newcases_1(country_name_1, palette_c1=palette_c1, max_yrange=2):
    country_df1 = data_prep_wrapper(country_name_1)
    plot_c1 = plot_new_cases(country_df1, country_name_1, palette_c1)
    # set same y axis range to both plots
    plot_c1.update_yaxes(range=[0, max_yrange])
    return plot_c1


@app.callback(Output('fig1_c2', 'figure'),
              Input('selector2', 'value'))
def update_plot_newcases_2(country_name_2, palette_c2=palette_c2, max_yrange=2):
    country_df2 = data_prep_wrapper(country_name_2)
    plot_c2 = plot_new_cases(country_df2, country_name_2, palette_c2)
    # set same y axis range to both plots
    plot_c2.update_yaxes(range=[0, max_yrange])
    return plot_c2


@app.callback(Output('fig2', 'figure'),
              [Input('selector1', 'value'),
               Input('selector2', 'value')
               ])
def update_plot_deaths(country_name_1, country_name_2, palette_c1=palette_c1, palette_c2=palette_c2):
    country_df1 = data_prep_wrapper(country_name_1)
    country_df2 = data_prep_wrapper(country_name_2)
    fig2 = make_subplots(1, 1)
    fig2.update_layout(plot_bgcolor="white")
    fig2.update_yaxes(showgrid=True, gridwidth=0.2, gridcolor='lightgrey', title_text='cumulative deaths')
    # add trace from country 1
    trace_c1 = plot_deaths(country_df1, country_name_1, palette_c1)
    trace_c2 = plot_deaths(country_df2, country_name_2, palette_c2)
    fig2.add_traces([trace_c1, trace_c2])
    return fig2


if __name__ == '__main__':
    # run app
    app.run_server(debug=True)
