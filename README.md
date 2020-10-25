
# A dashboard for my mum:  
# COVID DATA COMPARISON  between countries
Created by: matteo jucker riva   
Data sourced from [World Health Organisation](https://covid19.who.int/WHO-COVID-19-global-data.csv)    
   
# Deployed to [https://covid-data-for-mums.herokuapp.com/](https://covid-data-for-mums.herokuapp.com/)  
   
## Introduction
*Perception is strong and sight weak. In strategy it is important to see distant things as if they were close and to take a distanced view of close things.*
― Miyamoto Musashi

Like any son leaving in a different country from their parents, I spent quite some time in the recent times comparing with my Mum the developments of SARS-COVID-19 pandemic in our respective countries.
Like anyone who is not a skilled epidemiologist, it has taken me some time to understand how to look at COVID data in a meaningful way.    
Cumulative numbers are needed the overall evolution of the pandemic, allowing general comparison between places and giving us a frame to make predictions. However the fail miserably when we try to source from them the current situation, or to understand the impact of the prevention measures adopted in different countries. On the other head, daily changes are extremely sensitive to the changes and the measures adopted, but are also influenced by a whole range of other factors, which makes htem extremly noisy.   
   
In this dashboard I have tried to provide data with as little elaboration as possible, but displaying them in a way that would facilitate contextualisation and long term vs short term comparison. I first did it for my Mum on a separate release (*_[mamma-il-covid.herokuapp.com](mamma-il-covid.herokuapp.com)_*)

## How to read the plots

** Disclaimer 1: All data comes from the WHO official database, and is mnormalised to the population for 100'000 people**  
** Disclaimer 2: Data on new cases is strictly depndent on the amount of testing done and the testing strategy. ** Unfortunately such information is not yet collected in a consistent way at a global scale. I am following the evolution of this database: https://ourworldindata.org/coronavirus-testing. I will integrate it as soon as global coverage increases.

### Daily new cases
The first plot shows the new daily cases for each selected country, smoothed with a rolling average calculated over a window of 7 days. The closer to the present day, the darker the color of the line. Only for the current month daily new cases are displayed, allowing to infere the uncertainty of the data. Daily new cases can be compared as absolute numbers as well as in trends. THe colors, that fade the farther we are in the past, highlight the current (or recent) data.

### Cumulative deaths
Deaths from COVID are the result of long weeks of sickness, thus their daily change is less interesting, as no relevant inference can be done on daily, or even weekly changes. However, it in order to get a perception of the mortality, the marker site is proportional to the ratio between new cases and deaths.


## Files:  
|_main.py currently contains plots, dash app and deployment   
|_Procfile: required by heroku   
|_requirements.txt required by heroku, created using pipreqs pipreqs /path/to/project   
   see stackoverflow.com/questions/31684375/automatically-create-requirements-txt

## Requirements:

dash_table==4.4.1  
numpy==1.19.1  
dash_html_components==1.0.1  
plotly==4.10.0  
seaborn==0.10.1  
requests==2.24.0  
pandas==1.1.1   
dash_core_components==1.3.1  
dash==1.16.2  
dash_bootstrap_components==0.10.6  
gunicorn  
python-dotenv  


