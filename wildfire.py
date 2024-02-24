#Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

# Creating the function that cleans the dataset
def clean_data(file_path):
    # Loading the CSV file
    wildfire = pd.read_csv(file_path, delimiter=';', encoding='utf-8', skiprows=2)

    # Renaming variables and set the right type
    wildfire.rename(columns={
        "Année": "year",
        "Numéro": "number",
        "Type de feu": "type_of_fire",
        "Département": "department",
        "Code INSEE": "INSEE_code",
        "Commune": "cities",
        "Lieu-dit": "location",
        "Code du carreau DFCI": "DFCI_code",
        "Alerte":"alert",
        "Origine de l'alerte": "alert_origine",
        "Surface parcourue (m2)": "surface",
    }, inplace=True)

    # Converting m2 to hectares
    wildfire["surface_ha"] = wildfire["surface"] / 10000

    # Using the "Numero" column as the index
    wildfire.set_index("number", inplace=True)

    # Cleaning text variables
    wildfire["cities"].dropna(inplace=True)
    wildfire["location"].dropna(inplace=True)
    wildfire["cities"] = wildfire["cities"].str.title()
    wildfire["location"] = wildfire["location"].str.title()

    # Spliting date into two columns (date and hours)
    wildfire[["date", "time"]] = wildfire["alert"].str.split(" ", 1, expand=True)
 
    # Dropping the original "Date and Time" column
    wildfire.drop("alert", axis=1, inplace=True)

    return wildfire


#Function that counts the number of fires per year and by department
def count_fires(data_wildfire, selected_department=None, selected_year=None):
    """
    Count the number of fires by year and by department.

    Parameters:
    - data_wildfire: DataFrame containing fire data with 'year' and 'department' columns.
    - selected_department: Optional, the department to filter by. If None, all departments are considered.
    - selected_year: Optional, the year to filter by. If None, all years are considered.

    Returns:
    - A DataFrame with counts of fires by year and department.
    """

    # Applying filters based on selected_department and selected_year
    if selected_department is not None:
        data_wildfire = data_wildfire[data_wildfire['department'] == selected_department]
    if selected_year is not None:
        data_wildfire = data_wildfire[data_wildfire['year'] == selected_year]

    # Group the data by 'year' and 'department' and count the occurrences
    fire_counts = data_wildfire.groupby(['year', 'department']).size().reset_index(name='FireCount')

    return fire_counts

# Example usage:
# Assuming you have a DataFrame 'wildfire_data' containing your wildfire data
# You can call the function like this:
# fire_counts = count_fires(data_wildfire, selected_department='06', selected_year=2022)
# To count all fires, omit the selected_department and selected_year arguments.


#Function that sums the burnt area by year and department
def sum_burnt_area(data_wildfire, selected_department=None, selected_year=None):
    """
    Sum the burnt area by year and by department.

    Parameters:
    - data_wildfire: DataFrame containing wild fire data with 'year', 'department', and 'BurntArea' columns.
    - selected_department: Optional, the department to filter by. If None, all departments are considered.
    - selected_year: Optional, the year to filter by. If None, all years are considered.

    Returns:
    - A DataFrame with sums of burnt area by year and department.
    """

    # Applying filters based on selected_department and selected_year
    if selected_department is not None:
        data_wildfire = data_wildfire[data_wildfire['department'] == selected_department]
    if selected_year is not None:
        data_wildfire = data_wildfire[data_wildfire['year'] == selected_year]

    # Grouping the data by 'year' and 'department' and sum the burnt areas
    burnt_area_sum = data_wildfire.groupby(['year', 'department'])['surface_ha'].sum().reset_index(name='TotalBurntArea')

    return burnt_area_sum

# Example usage:
# Assuming you have a DataFrame 'wildfire_data' containing your fire data
# You can call the function like this:
# burnt_area_sum = sum_burnt_area(wildfire_data, selected_department='06', selected_year=2022)
# To sum burnt area for all fires, omit the selected_department and selected_year arguments.


#Function which computes the mean, median, Q1, and Q3 
def burnt_area_statistics(data_wildfire, selected_department=None, selected_year=None):
    """
    Compute statistics (mean, median, Q1, and Q3) of the burnt area by year and by department.

    Parameters:
    - data_wildfire: DataFrame containing fire data with 'year', 'department', and 'BurntArea' columns.
    - selected_department: Optional, the department to filter by. If None, all departments are considered.
    - selected_year: Optional, the year to filter by. If None, all years are considered.

    Returns:
    - A DataFrame with computed statistics by year and department.
    """

    # Applying filters based on selected_department and selected_year
    if selected_department is not None:
        data_wildfire = data_wildfire[data_wildfire['department'] == selected_department]
    if selected_year is not None:
        data_wildfire = data_wildfire[data_wildfire['year'] == selected_year]

    # Grouping the data by 'year' and 'department' and compute statistics
    burnt_area_stats = data_wildfire.groupby(['year', 'department'])['surface_ha'].agg(['mean', 'median', lambda x:np.percentile(x,25), lambda x:np.percentile(x,75)]).reset_index()
    burnt_area_stats.rename(columns={'<lambda_0>': 'Q1', '<lambda_1>': 'Q3'}, inplace=True)

    return burnt_area_stats

# Example usage:
# Assuming you have a DataFrame 'wildfire_data' containing your fire data
# You can call the function like this:
# burnt_area_stats = compute_burnt_area_statistics(fire_data, selected_department='Paris', selected_year=2022)
# To compute statistics for all fires, omit the selected_department and selected_year arguments.



#Graph of the evolution of the total burnt area by department over years

def evolution_graph(data_wildfire, output_folder):
    """
    Create an interactive line graph of the evolution of total burnt area by department over years.

    Parameters:
    - data: DataFrame containing fire data with 'Year', 'Department', and 'BurntArea' columns.
    - output_folder: Path to the folder where the graph will be saved.

    Returns:
    - None (saves the interactive graph as an HTML file).
    """
    # Grouping the data by 'year' and 'department' and sum the burnt areas
    burnt_area_by_year_dept = data_wildfire.groupby(['year', 'department'])['surface_ha'].sum().unstack()
    
    # Creating the interactive line graph using Plotly
    fig = px.line(burnt_area_by_year_dept, x=burnt_area_by_year_dept.index, y=burnt_area_by_year_dept.columns, title='Evolution of Total Burnt Area by Department Over Years')
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Total Burnt Area')
    
    # Save the interactive graph as an HTML file
    fig.write_html(f'{output_folder}/burnt_area_evolution_graph.html')



    #Pie chart of the total burnt area
def pie_chart_burnt_area(data_wildfire, year, output_folder):
    """
    Create an interactive pie chart of the total burnt area for one year with all departments.

    Parameters:
    - data: DataFrame containing fire data with 'Year', 'Department', and 'BurntArea' columns.
    - year: The year for which to create the pie chart.
    - output_folder: Path to the folder where the pie chart will be saved.

    Returns:
    - None (saves the interactive pie chart as an HTML file).
    """
    # Filter the data for the selected year
    data_year = data_wildfire[data_wildfire['year'] == year]
    
    # Calculate the total burnt area for the selected year
    total_burnt_area = data_year['surface_ha'].sum()
    
    # Group the data by 'Department' and sum the burnt areas
    burnt_area_by_dept = data_year.groupby('department')['surface_ha'].sum().reset_index()
    
    # Create the interactive pie chart using Plotly
    fig = px.pie(burnt_area_by_dept, values='surface_ha', names='department', title=f'Total Burnt Area for Year {year}')
    
    # Save the interactive pie chart as an HTML file
    fig.write_html(f'{output_folder}/pie_chart_total_burnt_area_{year}.html')
