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

#--------------------------------- plotting libraries --------------------------------------
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
#--------------------------------- dash libraries --------------------------------------
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


# 0. startup check
# Check that files and folders are available and make them if needed
def check_folders(ds_path, out_path):
    if not os.path.isdir(ds_path):
        print("no data source folder, creating one")
        os.mkdir(ds_path)

    if not os.path.isdir(out_path):
        print("no output folder, creating one")
        os.mkdir(out_path)


# 1. download data_source file
def download_recent_data(data_path, url):
    print(f'downloading {data_path}')
    req = rq.get(url, allow_redirects=True)
    csv_file = open(data_path, 'wb')
    csv_file.write(req.content)
    csv_file.close()

#  create cards for dashboard
def card_content_function( case, data ):
    card_content  = [
        dbc.CardHeader(html.H5(case, className="card-title")),
        dbc.CardBody([
                html.P(data[case].sum(),
                className="card-text")])]
    return card_content



# main function to run

# Main variables and parameters
ds_path = os.path.join(os.getcwd(), "data_source")
out_path = os.path.join(os.getcwd(), "output")

ita_url = 'http://raw.github.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
ch_url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
    
ita_raw = pd.read_csv(ita_url)
ch_raw = pd.read_csv(ch_url)


# DATA CLEANING FOR LOMBARDY
ita_selected = pd.DataFrame({
    'date' : ita_raw[ita_raw['denominazione_regione'] == 'Lombardia']['data'],
    'cum_cases_lom' : ita_raw[ita_raw['denominazione_regione'] == 'Lombardia']['totale_positivi'],
    'new_cases_lom' : ita_raw[ita_raw['denominazione_regione'] == 'Lombardia']['nuovi_positivi'],
    'deaths_lom' : ita_raw[ita_raw['denominazione_regione'] == 'Lombardia']['deceduti']
    })
    # turn time stamp to pandas data format
ita_selected['date'] =[ pd.to_datetime(i.split("T")[0], format = "%Y-%m-%d" ) for i in ita_selected['date'] ]

# DATA CLEANING FOR SWITZERLAND
# ch_cumul=ch_raw[ ['date', 'ncumul_conf']# selected layer
ch_cumul = pd.DataFrame({
    'date': ch_raw[ch_raw[' Country'] == 'Switzerland']['Date_reported'],
    'cum_cases_ch': ch_raw[ch_raw[' Country'] == 'Switzerland'][' Cumulative_cases'],
    'new_cases_ch': ch_raw[ch_raw[' Country'] == 'Switzerland'][' New_cases'],
    'deaths_ch' : ch_raw[ch_raw[' Country'] == 'Switzerland'][' New_deaths'],
})

# turn date as date object
ch_cumul[['date']] = [pd.to_datetime(i, format="%Y-%m-%d") for i in ch_cumul['date']]

# merging together layers from ch and lombardy

combined = ita_selected.merge(ch_cumul, on = 'date').set_index("date")

# smooth new cases by moving window 7 days
combined['new_ch_smooth'] = combined['new_cases_ch'].rolling(window=5).mean().fillna(0).astype(int)
combined['new_lom_smooth'] = combined['new_cases_lom'].rolling(window=5).mean().fillna(0).astype(int)

## --------------------------------------PLOTTING-------------------------------------------------
"""
Current plots:
1- New cases by month
2- Deaths per 1000 new cases and trend # TODO
3- Recovered per 1000  new cases and trend # TODO
"""
# plotting 1- new cases month by month
un_m = combined.index.month.unique()
# colour palettes
pal_lom = sns.color_palette("Blues", n_colors=len(un_m) + 2).as_hex()
pal_ch = sns.color_palette("Reds", n_colors=len(un_m) + 2).as_hex()

fig1 = make_subplots(rows=1, cols=2,
                         subplot_titles=('Lombardia', 'Svizzera'),
                         shared_yaxes=True
                         )

m_traces = []
c_c = 0  # color counter
for m in un_m:
# data selection
    temp = combined[combined.index.month == m]
    temp_lom = temp['new_lom_smooth']
    temp_ch = temp['new_ch_smooth']
    current_lom = temp['new_cases_lom']
    current_ch = temp['new_cases_ch']

# prepare string and colour
    month_s = pd.to_datetime("2020-1-1").replace(month=int(m)).month_name()
    col_lom = pal_lom[c_c]
    col_ch = pal_ch[c_c]
    m_s = 2
    m_o = 0.8  # marker opacity

    # create monthly traces
    if m == pd.to_datetime('today').month:
    # change viz param for current month
        m_o = 1
        col_lom = pal_lom[c_c + 1]
        col_ch = pal_ch[c_c + 1]
        m_s = 3
# remove for filled area
        """ note the traces have to be created one for each country otherwise they are assigned 
        to the wrong subplot"""
        area_lom1 = go.Scatter(x=temp_lom.index.day,
                                   y=temp_lom,
                                   fill=None,
                                   mode='lines',
                                   line_color=col_lom,
                                   showlegend=False
                                   )
        area_ch1 = go.Scatter(x=temp_lom.index.day,
                                  y=temp_ch,
                                  fill=None,
                                  mode='lines',
                                  line_color=col_ch,
                                  showlegend=False
                                  )
        area_lom2 = go.Scatter(x=temp_lom.index.day,
                                   y=current_lom,
                                   fill='tonexty',  # fill area between trace0 and trace1
                                   mode='lines',
                                   line={'color': col_lom, 'width': 1},
                                   name="Lombardia mese corrente",
                                   hovertemplate="Lombardia: %{x}<br>nuovi casi : %{y:.1f}",

                                   )
        area_ch2 = go.Scatter(x=temp_lom.index.day,
                                  y=current_ch,
                                  fill='tonexty',  # fill area between trace0 and trace1
                                  mode='lines',
                                  line={'color': col_ch, 'width': 1},
                                  name="Svizzera mese corrente",
                                  hovertemplate="Svizzera: %{x}<br>nuovi casi : %{y:.1f}",
                                  )

        m_traces.extend([  # th_m_lom,
                # th_m_ch,
                area_lom1, area_ch1, area_lom2, area_ch2])

    m_lom = go.Scatter(x=temp_lom.index.day,
                           y=temp_lom,
                           name=f"{month_s}",
                           marker_color=col_lom,
                           line={'width': m_s},
                           opacity=m_o,
                           mode="lines",
                           hovertemplate=f"Lombardia: %{{x}} {month_s}<br>nuovi casi (media sett.): %{{y:.1f}}",
                           showlegend=True
                           )
    m_ch = go.Scatter(x=temp_ch.index.day,
                          y=temp_ch,
                          name=f" {month_s}",
                          marker_color=col_ch,
                          line={'width': m_s},
                          opacity=m_o,
                          text=month_s,
                          mode="lines",
                          hovertemplate=f"Lombardia: %{{x}} {month_s} <br>nuovi casi (media sett.): %{{y:.1f}}",
                          showlegend=True
                          )
    m_traces.append(m_lom)
    m_traces.append(m_ch)
    c_c = c_c + 1
    # define which subplot
row_pos = tuple([1] * (len(m_traces)))
col_pos = tuple([1, 2] * (int(len(m_traces) / 2)))
    # add traces
fig1.add_traces(m_traces, rows=row_pos, cols=col_pos)
    # update layout
fig1.update_layout(plot_bgcolor="white", title="Nuovi casi (media settimanale) per mese")
fig1.update_yaxes(showgrid=True, gridwidth=0.2, gridcolor='lightgrey')
    # fig1.show()


## --------------------------------------DASHBOARD-------------------------------------------------
colors = {
        'background': '#0',
        'text': 'rgb(135,206,250)',
        'text2' : 'black',
        'text3' : 'orange'
}

# we use a pre-defined css file. feel free to try others!

app = dash.Dash(__name__, )
server = app.server

# Define app layout
app.layout = html.Div([
    # Header
    html.H1(children='Mamma il Covid',
                style={
                    'textAlign': 'center',
                    'color': colors['text']}
                ),

    html.Div(children='Visualization: A Dash web application framework for COVID analysis',
                 style={
                     'textAlign': 'center',
                     'color': colors['text']}
                 ),

    # separation line
    html.Hr(),

    # 3rd header
    html.H3(children='Global COVID-19 cases',
                style={
                    'textAlign': 'center',
                    'color': colors['text3']}),
    dbc.Row([
            dbc.Col(dbc.Card(card_content_function('new_cases_lom', data=combined), color=col_lom[-1], outline=True)),
            dbc.Col(dbc.Card(card_content_function('new_cases_ch', data=combined), color=col_ch[-1], outline=True))],
            className="mb-4"),

    # Time series plot of global confirmed cases
    dcc.Graph(figure=fig1)
])

if __name__ == '__main__':

    # run app
    app.run_server(debug=True)
