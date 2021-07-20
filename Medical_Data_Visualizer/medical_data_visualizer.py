import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
def BMI(row):
    result = row['weight']/((row['height']/100)**2)
    if result > 25:
        return 1
    else:
        return 0
df['overweight'] = df.apply(BMI, axis=1)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

def nor_cho(row):
    if row['cholesterol'] == 1:
        return 0
    elif row['cholesterol'] > 1:
        return 1
df['cholesterol'] = df.apply(nor_cho, axis=1)

def nor_gluc(row):
    if row['gluc'] == 1:
        return 0
    elif row['gluc'] > 1:
        return 1
df['gluc'] = df.apply(nor_gluc, axis=1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(id_vars=['cardio'], # Column that is kept unchanged
                    value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], # Column that are melted
                    var_name='variable', # New column name
                    value_name='value') # New column name


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio','variable','value'])['value'].count().reset_index(name="total")

    # Draw the catplot with 'sns.catplot()
    g = sns.catplot(data=df_cat, x = 'variable', y='total', hue='value', col='cardio', kind='bar')
    fig = g.fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr().round(1)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(data=corr, mask=mask, annot=True, linewidths=.5, square=True, fmt='.1f')
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
