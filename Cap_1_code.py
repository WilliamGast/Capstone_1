import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
plt.style.use('ggplot')


def date_time(df):
    df['SALE DATE'] = pd.to_datetime(df['SALE DATE'])
    df['YEAR'] = df['SALE DATE'].apply(lambda x: x.year)
    df['MONTH'] = df['SALE DATE'].apply(lambda x: x.month)
    df['DAY'] = df['SALE DATE'].apply(lambda x: x.day)
    return df

def clean_sales(df):
    df['SALE PRICE'] = df['SALE PRICE'].replace(' -  ', np.NaN).astype(np.float)
    df = df.dropna(axis=0).reset_index(drop=True)
    return df

def drop_cols(df):
    df = df.drop(['Unnamed: 0','EASE-MENT','APARTMENT NUMBER'],axis =1)
    return df
def transition(df):
    for column in ['BOROUGH']:
        df[column] = df[column].astype(int)
    return df
def clean_feet(df):
    df['GROSS SQUARE FEET'] = df['GROSS SQUARE FEET'].replace(' -  ', np.NaN)
    df['GROSS SQUARE FEET'] = pd.to_numeric(df['GROSS SQUARE FEET'] )
    df = df.dropna(axis=0).reset_index(drop=True)
    for column in ['GROSS SQUARE FEET','SALE PRICE']:
        df[column] = df[column].replace(0,np.NaN)
        df[column] = pd.to_numeric(df[column])
        df = df.dropna(axis=0).reset_index(drop=True)
    
    # for column in df['GROSS SQUARE FEET']:  
    #     df[column].replace(' -  ', np.NaN,inplace=True).astype(np.float)
    #     df = df.dropna(axis=0).reset_index(drop=True)
    # for column in df['GROSS SQUARE FEET']:
    #     df[column] = df[column].astype(int)
    # for column in df['GROSS SQUARE FEET','SALE PRICE']:
    #     df[column] = df[column].replace(0,np.NaN,inplace=True).astype(np.float)
    #     df = df.dropna(axis=0,inplace=True).reset_index(drop=True)
    return df
def cat_boro(df):
    boroughs ={1:'Manhattan' , 2:'Bronx' , 3:'Brooklyn', 4:'Queens' , 5:'Staten Island'}
    df['BOROUGH'].replace(boroughs,inplace=True)
    return df

def add_price_per_square_feet(df):
    df['PRICE PER SQR FOOT'] = df['SALE PRICE'] / df['GROSS SQUARE FEET']
    return df

def Boro_compare(df):
    boro = df.groupby(['BOROUGH']).mean()
    plt.plot('PRICE PER SQR FOOT')
    plt.title('Price per Square Foot in each Borough ')
    plt.xlabel('Boroughs')
    plt.ylabel('Price per Square Foot')
    plt.show(block=False)
    return plt.show()

def all_sales_SQRF(df):
    plt.plot(df['PRICE PER SQR FOOT'])
    plt.title('Price per Square in NYC')
    plt.xlabel('Individual Sales')
    plt.ylabel('Price per Square Foot')
    plt.show(block=False)
    return plt.show
    
    
def get_rid_of_outliers(df):
    #df_bar_1 = df[['BOROUGH', 'PRICE PER SQR FOOT']]
    df['z_scores']= stats.zscore(df['PRICE PER SQR FOOT'])
    df_without_out = df.copy()
    df_without_out = df_without_out.loc[df_without_out['z_scores'].abs()<=3]
    return df_without_out

#df_bar =df[['BOROUGH', 'PRICE PER SQR FOOT']].groupby(by='BOROUGH').mean().sort_values(by='PRICE PER SQR FOOT', ascending=True).reset_index()
def box_plot_wo_out(df_without_out):
    plt.figure(figsize=(12,6))
    g = sns.boxplot(x = 'BOROUGH',y = 'PRICE PER SQR FOOT',data = df_without_out)
    plt.title('Price per square foot per borough')
    g.set(ylim=(0,2500))
    return plt.show()


if __name__ =="__main__":
    df = pd.read_csv('nyc-rolling-sales.csv')

    df = date_time(df)
    df = clean_sales(df)
    df = drop_cols(df)
    df = transition(df)
    df = clean_feet(df)
    
    df = cat_boro(df)
    df = add_price_per_square_feet(df)
    Boro_compare(df)
    all_sales_SQRF(df)
    df_without_out = get_rid_of_outliers(df)
    box_plot_wo_out(df_without_out)
    # save(df)

    # print(df_time(new_york))


    