import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Functions for creating visuals
def barChart(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    df.sort_values(by='NumberOfUpdates', ascending=False).plot(kind='bar', x='Attribute', y='NumberOfUpdates', ax=ax, color='skyblue')

    ax.set_title('Frequency of Updates per Attribute')
    ax.set_xlabel('Attribute')
    ax.set_ylabel('Number of Updates')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def stackedBarChart(df):
    pivot_df = df.pivot_table(index='Table', columns='Attribute', values='NumberOfUpdates', aggfunc='sum', fill_value=0)
    pivot_df.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab20c')

    plt.title('Stacked Bar Chart of Update Frequencies by Table and Attribute')
    plt.xlabel('Table')
    plt.ylabel('Number of Updates')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def pieChart(df):
    plt.figure(figsize=(8, 8))
    plt.pie(df['NumberOfUpdates'], labels=df['Attribute'], autopct='%1.1f%%', startangle=140)
    plt.title(f'Update Frequency Distribution across all tables')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def pieChartPerTable(df): 
    for table in df['Table'].unique():
        table_df = df[df['Table'] == table]
        plt.figure(figsize=(8, 8))
        plt.pie(table_df['NumberOfUpdates'], labels=table_df['Attribute'], autopct='%1.1f%%', startangle=140)
        plt.title(f'Update Frequency Distribution for {table}')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

def histogram(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df['NumberOfUpdates'], bins=10, color='skyblue', edgecolor='black')
    plt.title('Distribution of Update Frequencies Across Attributes')
    plt.xlabel('Number of Updates')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def heatmap(df):
    heatmap_data = df.pivot_table(index='Table', columns='Attribute', values='NumberOfUpdates', aggfunc='sum', fill_value=0)
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap='YlGnBu', linewidths=.5)
    plt.title('Heatmap of Update Frequencies')
    plt.xlabel('Attribute')
    plt.ylabel('Table')
    plt.tight_layout()
    plt.show()