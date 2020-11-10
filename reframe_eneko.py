"""
Title: Mapper of given map for optimiser interpretation.
Description: Mapper of given map for optimiser interpretation.
Author: Pietro Campolucci
"""

# import packages
import numpy as np
from math import *
import pandas as pd
import os

V_wind = 5  # set V_wind to be 5 m/s from North to South

# get files and path information
cwd = os.getcwd()
database = "\database\\start.xlsx"
target = "\database\\pvr.xlsx"

# build start and end data frames
map_df = pd.read_excel(cwd + database)
distance_df = pd.DataFrame(columns=['From', 'To', 'Distance', 'DeltaV'])

# compute all possible arcs and respective distance in km
for i in range(len(map_df)):
    for j in range(len(map_df)):
        if i != j:
            from_node = map_df['id'][i]
            to_node = map_df['id'][j]
            x_distance = abs(map_df["lat"][i] - map_df["lat"][j]) * 111
            y_distance = abs(map_df["long"][i] - map_df["long"][j]) * 111
            tot_distance = (x_distance ** 2 + y_distance ** 2) ** (1 / 2)

            # compute change in distance (not abs so that we know in relative terms)
            delta_lat = map_df["lat"][j] - map_df["lat"][i]
            delta_long = map_df["long"][j] - map_df["long"][i]
            angle = np.arctan((delta_lat / delta_long)) * 360 / 2 / pi
            angle_wind = angle + 90
            factor = np.cos(angle_wind * 2 * pi / 360)
            Delta_V = V_wind * factor
            # print(map_df["lat"][i], map_df["lat"][j], map_df["long"][i], map_df["long"][j], angle, angle_wind, Delta_V)

            distance_df.loc[-1] = [from_node, to_node, tot_distance, Delta_V]
            distance_df.index += 1
            distance_df = distance_df.sort_index()
            distance_df = distance_df.iloc[::-1]

distance_df.to_excel(cwd + target, 'data')

print("Excel file ready")