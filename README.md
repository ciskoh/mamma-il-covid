
# A dashboard for my mum:  
# COVID DATA COMPARISON  between Switzerland and Lombardy (ITA)    
Created by: matteo jucker riva   
Data sourced from:    
 https://covid19.who.int/WHO-COVID-19-global-data.csv (World Health Organisation)   
## Introduction
*Perception is strong and sight weak. In strategy it is important to see distant things as if they were close and to take a distanced view of close things.*
― Miyamoto Musashi

Like any son leaving in a different country from their parents, I have spent quite some time comparing with my Mum the developments of SARS-COVID-19 pandemic in our respective countries.
Like any other person the is not an epidemiologist, it has taken me some time to understand how to look at COVID data in a meaningful way
 

Deployed on Heroku at : *_[mamma-il-covid.herokuapp.com](mamma-il-covid.herokuapp.com)_*

### Files:  
|_main.py currently contains plots, dash app and deployment   
|_Procfile: required by heroku   
|_requirements.txt required by heroku, created using pipreqs pipreqs /path/to/project   
   see stackoverflow.com/questions/31684375/automatically-create-requirements-txt

### Requirements:

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


