#Creating the command line
import argparse
import pandas as pd
import numpy as np
import plotly.express as px
import sys
sys.path.append("/Users/coraline/Desktop")

# Importing the library created
from PrometheusLib.wildfire import clean_data, count_fires, sum_burnt_area, burnt_area_statistics, pie_chart_burnt_area, evolution_graph

def main():
    parser = argparse.ArgumentParser(description="Wildfire Data Analysis Command Line Tool")
    parser.add_argument("--file_path", type=str, required=True, help="Path to the wildfire data CSV file")
    parser.add_argument("--year", type=int, help="Specify the year for analysis")
    parser.add_argument("--department", type=str, default="all", help="Specify the department for analysis (or 'all' for all departments)")
    parser.add_argument("--output_folder", type=str, default="output", help="Specify the output folder for saving graphs")

    args = parser.parse_args()

    # Cleaning the dataset
    wildfire_data = clean_data(args.file_path)

    # Computing key indicators and generate graphs based on user inputs
    if args.year is not None:
        # Counting fires
        fire_counts = count_fires(wildfire_data, args.department, args.year)
        print("Fire Counts:")
        print(fire_counts)

        # Sum burnt area
        burnt_area_sum = sum_burnt_area(wildfire_data, args.department, args.year)
        print("Burnt Area Sum:")
        print(burnt_area_sum)

        # Burnt area statistics
        burnt_area_stats = burnt_area_statistics(wildfire_data, args.department, args.year)
        print("Burnt Area Statistics:")
        print(burnt_area_stats)

        # Evolution graph
        evolution_graph(wildfire_data, args.output_folder)

        # Pie chart
        pie_chart_burnt_area(wildfire_data, args.year, args.output_folder)

if __name__ == "__main__":
    main()
