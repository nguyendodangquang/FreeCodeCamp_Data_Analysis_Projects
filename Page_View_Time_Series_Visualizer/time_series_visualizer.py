import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    
    fig, ax = plt.subplots(figsize=(15,9))
    ax.plot(df.reset_index()['date'], df['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Months'] = pd.DatetimeIndex(df_bar.reset_index()['date']).month
    df_bar['Years'] = pd.DatetimeIndex(df_bar.reset_index()['date']).year
    df_bar = df_bar.groupby(['Years','Months'])['value'].mean().reset_index(name ='average')
    df_bar['average'] = df_bar['average'].round().astype('int')
    def changemonth(row):
        return datetime.datetime.strptime(str(row['Months']), "%m").strftime("%B")
    df_bar['Months'] = df_bar.apply(changemonth, axis=1)


    # Draw bar plot
    month_label = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    fig, ax = plt.subplots(figsize=(15,9))
    ax = sns.barplot(data=df_bar, x='Years', y='average', hue='Months', hue_order=month_label)
    ax.set(ylabel='Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2, figsize=(18,9))

    axes[0] = sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel='Page Views')
    axes[1] = sns.boxplot(data=df_box, x='month', y='value',ax=axes[1] ,order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel='Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
