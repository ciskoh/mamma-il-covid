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
import datetime as dt
import pandas as pd



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

# 2 import data



# main function to run
def main():
    # Main variables and parameters
    ds_path = os.path.join(os.getcwd(), "data_source")
    out_path = os.path.join(os.getcwd(), "output")

    ita_url = 'http://raw.github.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
    ch_url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
    

    print("data path: ", ds_path)
    print("output path : ", out_path)

    check_folders(ds_path, out_path)

    # download data for Italy
    data_path_ita = ds_path + f"/ita_{dt.date.today()}.csv"
    download_recent_data(data_path_ita, ita_url)

    # download data for ch
    data_path_ch = ds_path + f"/ch_{dt.date.today()}.csv"
    download_recent_data(data_path_ch, ch_url)

    # import and clean
    ita_raw = pd.read_csv(data_path_ita)
    ds_path = os.getcwd() + "/data_source"
    data_path_ita = ds_path + f"/ita_{dt.date.today()}.csv"
    ita_raw = pd.read_csv(data_path_ita)

    # change column names to remove special chars
    # short_name = {i: re.sub('[\W\_]', '', i) for i in ita_raw.columns}
    # ita_raw.rename(short_name)
    # print(ita_raw.columns)

   # print(ita_raw[['data', 'variazione_totale_positivi']])
  #  plt.plot(ita_raw.data, ita_raw.variazione_totale_positivi)



    


main()
if __name__ == "main":
    check_folders()

