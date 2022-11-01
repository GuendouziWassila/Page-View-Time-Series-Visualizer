import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv ('fcc-forum-pageviews.csv',header=0)

#transfrom the date column to date so to be well fromated when we use set_major_formatter in the next lines 
df['date']=pd.to_datetime (df['date'])
df.index=df['date']


# Clean data
df =   df.loc[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
    ]

#print (df.size)

def draw_line_plot():
    # Draw line plot
       
    fig, ax = plt.subplots(1,1, figsize = (16, 6))
        
    ax.plot( df.index, df['value'], color = 'red')
   

    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
   
    locator = mdates.MonthLocator(bymonth = (1, 7))
    ax.xaxis.set_major_locator(locator)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby([df['date'].dt.year, df['date'].dt.month])['value'].mean().unstack()
  
    # Draw bar plot
    fig = plt.figure(figsize=(12, 8))
    width =0.03
    X_axis=np.arange(len(df_bar.index))
    space=0
    for i in range(df_bar.shape[1]): 
      plt.bar(X_axis+(space), df_bar[i+1], width=width)
      space=space+width
    
    plt.xticks(X_axis+0.2, df_bar.index, rotation=90)
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    MonthList=[ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    plt.legend(MonthList, loc='upper left', title='Months')
    

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    
    #df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]
    
    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(20, 6)) 
    
    
         
    orderMonth=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    g1=sns.boxplot(ax=axes[0], data=df_box, x='Year', y='value')
    g1.set_ylabel('Page Views')
    g1.set_title('Year-wise Box Plot (Trend)')
    
  
    g2=sns.boxplot(ax=axes[1], data=df_box, x='Month', y='value', order = orderMonth)
    g2.set_ylabel('Page Views')
    g2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
