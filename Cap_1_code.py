import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statistics as sts
plt.style.use('ggplot')


def date_time(df):
    """This function seperates the sale date column into a month day and year column
    
    Arguments: df
    """
    df['SALE DATE'] = pd.to_datetime(df['SALE DATE'])
    df['YEAR'] = df['SALE DATE'].apply(lambda x: x.year)
    df['MONTH'] = df['SALE DATE'].apply(lambda x: x.month)
    df['DAY'] = df['SALE DATE'].apply(lambda x: x.day)
    return df

def clean_sales(df):
    """This function gets rid of the dashes in the Sale Price column and replaces them with NaN values
    It then drops those NaN values
    Arguments: df
    """
    df['SALE PRICE'] = df['SALE PRICE'].replace(' -  ', np.NaN).astype(np.float)
    df = df.dropna(axis=0).reset_index(drop=True)
    return df

def drop_cols(df):
    """This function drops unwanted columns
    
    Arguments: df
    """
    df = df.drop(['Unnamed: 0','EASE-MENT','APARTMENT NUMBER'],axis =1)
    return df

def transition(df):
    """ This function takes the Borough column and turns in to a integer type
    
    Arguments: df
    """
    for column in ['BOROUGH']:
        df[column] = df[column].astype(int)
    return df
def clean_feet(df):
    """This cleans the gross square feet and sale price column

    Arguments: df
    """
    df['GROSS SQUARE FEET'] = df['GROSS SQUARE FEET'].replace(' -  ', np.NaN)
    df['GROSS SQUARE FEET'] = pd.to_numeric(df['GROSS SQUARE FEET'] )
    df = df.dropna(axis=0).reset_index(drop=True)
    for column in ['GROSS SQUARE FEET','SALE PRICE']:
        df[column] = df[column].replace(0,np.NaN)
        df[column] = pd.to_numeric(df[column])
        df = df.dropna(axis=0).reset_index(drop=True)
    return df

def cat_boro(df):
    """This function turns the Borough columns from integers to Borough names
    
    Arguments: df
    """
    boroughs ={1:'Manhattan' , 2:'Bronx' , 3:'Brooklyn', 4:'Queens' , 5:'Staten Island'}
    df['BOROUGH'].replace(boroughs,inplace=True)
    return df

def add_price_per_square_feet(df):
    """This function adds the Price per square foot column
    
    Arguments: df
    """
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

def strd_dev(df):
    s = df.groupby(['BOROUGH']).std()
    return s

def strd_dev_class(df):
    h = df.groupby(['BUILDING CLASS AT TIME OF SALE']).std()
    plt.plot(h['BUILDING CLASS AT TIME OF SALE'])
    plt.title('Standard Deviation per building class')
    plt.xlabel('Building Class')
    plt.ylabel('Stadard Deviation')
    plt.show(block=False)
    return plt.show
    


if __name__ =="__main__":
    df = pd.read_csv('./data/nyc-rolling-sales.csv')

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
    s = strd_dev(df)
    strd_dev_class(df)
    print(s)

    # print(df_time(new_york))


    