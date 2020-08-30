
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

print(f" cwd is {os.getcwd()}; ds path is {ds_path}")

# startup check
# Check that files and folders are available
if not os.path.isdir(ds_path):
    print("no data source folder, creating one and downloading files")
    os.mkdir(ds_path)

if not os.path.isdir(out_path):
    print("no output folder, creating one ")
    os.mkdir(out_path)


# 1 download data_source file

# 2 clean and import data

if __name__ == "main"
