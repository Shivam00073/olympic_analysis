import pandas as pd
import numpy as np


def preprocessor(df,region_df):

    # selecting the summer season
    df=df[df['Season']=='Summer']
    # merging both the dataset
    df=df.merge(region_df,on='NOC',how='left')
    #dropping the duplicate values
    df.drop_duplicates()
    #one hot encoding the medals columns as it has many NAN values
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df





