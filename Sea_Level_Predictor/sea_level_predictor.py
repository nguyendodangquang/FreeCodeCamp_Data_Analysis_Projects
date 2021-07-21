import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10,7))
    ax.scatter(x=df['Year'], y=df['CSIRO Adjusted Sea Level'])

    # Create first line of best fit
    x = [z for z in df['Year']]
    y = [i for i in df['CSIRO Adjusted Sea Level']]
    res = linregress(x, y)
    ax.set(xlim=(1850, 2075))
    years = pd.Series(list(range(1880, 2051)))
    ax.plot(years, res.intercept + res.slope*years, 'r')

    # Create second line of best fit
    x2 = [z for z in df[df['Year'] >= 2000]['Year']]
    y2 = [i for i in df[df['Year'] >= 2000]['CSIRO Adjusted Sea Level']]
    res2 = linregress(x2, y2)
    years2 = pd.Series(list(range(2000, 2051)))
    ax.plot(years2, res2.intercept + res2.slope*years2, 'r', label='fitted line', color='green')

    # Add labels and title
    ax.set(xlabel='Year', ylabel='Sea Level (inches)', title='Rise in Sea Level')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()