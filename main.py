
# application to simply compare covid dat between switzerland and Lombardy. Made for my mum

### main file that runs all the functions:
# 1- Update source data
# 2- Get differences
# 3- Calculate differences and plot
# 4- print or update output


# Imports
import os

# Main variables and parameters
ds_path = os.getcwd() + "/data_source"
out_path = os.getcwd() + "/output"
ita_url = "https://github.com/pcm-dpc/COVID-19/blob/master/dati-regioni/dpc-covid19-ita-regioni.csv"
ch_url = "https://github.com/openZH/covid_19/blob/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_FL_total.csv"


# startup check
# Check that files and folders are available
def check_folders():
    if not os.path.isdir(ds_path):
        print("no data source folder, creating one and downloading files")
        os.mkdir(ds_path)

    if not os.path.isdir(out_path):
        print("no output folder, creating one")
        os.mkdir(out_path)


# 1 download data_source file
def download_recent_data( country, date, url):
    data_path = ds_path+f"/{country}_{date}.csv"
    if not os.path.exists(data_path): 


# 2 clean and import data

if __name__ == "main"
