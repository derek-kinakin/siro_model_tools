# -*- coding: utf-8 -*-
""" Generate OPS parameter file for faults

Read a CSV file of fault centroids, orienations, and size information then
reformat the data into an OPS parameter file for faults in real world
coordinates for loading in SiroModel. 

"""


__author__ = "Derek Kinakin"
__email__ = "dkinakin@gmail.com"
__copyright__ = "Copyright 2021, Derek Kinakin"
__license__ = "GPL3"
__status__ = "Development"


import pandas as pd
import numpy as np


# Globals
IN_CSV_FILE_PATH_NAME = r"C:\Users\dkinakin\Desktop\fault_discs.csv"
OUT_FILE_PATH_NAME = r"C:\Users\dkinakin\Desktop\fault_parameter_file.txt"
FAULT_FRICTION_ANGLE = 18 # Degrees
FAULT_COHESION = 0 # kPa

FILE_TEMPLATE = """*Fault Parameter File   
*   
* Comment lines start with '*' symbol  
* Please do not alter the order of the parameters!  
*   
Total number of sets: {0}   
*Activated? (0/1):
{1}   
*Dip (degs): 
{2}   
*Dip Direction (degs):
{3}   
*Phi (degs):  
{4}   
*Cohesion (kpa):   
{5}  
*Persistence (m):   
{6}   
*Density above plane (currently unused so set all to 0):  
{7}   
*Density below plane (currently unused so set all to 0):  
{8}   
*Bench Number (set to zero for world coordinates):    
{9}   
*Easting or horizontal distance along face (m):    
{10}   
*Northing or vertical distance along face (m):    
{11}   
*Elevation or set to zero for bench coordinates (m):    
{12}"""


def csv_to_df(flp):
    """Load a CSV file with the following expected columns:
    "x","y","z","dip","dip_dir","diameter","name"

    Return a dataframe.
    """
    flts = pd.read_csv(flp)
    return flts


def series_to_string(srs):
    """Transform a series of parameters into a string for insert into the
    template.
    """
    tmplt_str = srs.to_string(index=False).replace("\n"," ")
    return tmplt_str


if __name__ == "__main__":
    faults_dataframe = csv_to_df(IN_CSV_FILE_PATH_NAME)
    flt_numb = len(faults_dataframe)

    # Geometry series
    flt_dips = faults_dataframe["dip"]
    flt_ddrs = faults_dataframe["dip_dir"]
    flt_eastings = faults_dataframe["x"]
    flt_northings = faults_dataframe["y"]
    flt_elevs = faults_dataframe["z"]
    flt_persist = faults_dataframe["diameter"]

    # Parameter series
    activated = pd.Series(1, index=np.arange(flt_numb))
    phi = pd.Series(FAULT_FRICTION_ANGLE, index=np.arange(flt_numb))
    cohesion = pd.Series(0, index=np.arange(flt_numb))
    density = pd.Series(0, index=np.arange(flt_numb))
    bench_numb = pd.Series(0, index=np.arange(flt_numb))

    # Strings
    str_dips = series_to_string(flt_dips)
    str_ddrs = series_to_string(flt_ddrs)
    str_east = series_to_string(flt_eastings)
    str_north = series_to_string(flt_northings)
    str_elev = series_to_string(flt_elevs)
    str_persist = series_to_string(flt_persist)
    str_act = series_to_string(activated)
    str_phi = series_to_string(phi)
    str_co = series_to_string(cohesion)
    str_dens = series_to_string(density)
    str_bn = series_to_string(bench_numb)

    # Create final file
    fault_file = FILE_TEMPLATE.format(flt_numb,
                                      str_act,
                                      str_dips,
                                      str_ddrs,
                                      str_phi,
                                      str_co,
                                      str_persist,
                                      str_dens,
                                      str_dens,
                                      str_bn,
                                      str_east,
                                      str_north,
                                      str_elev)

    with open(OUT_FILE_PATH_NAME, "w") as text_file:
        print(fault_file, file=text_file)
