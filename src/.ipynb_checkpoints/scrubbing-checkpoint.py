import numpy as np
import pandas as pd


#####################################################################
#  Step 1: create 'fraud_no_fraud'
#####################################################################
def scrub_fraud_no_fraud(df):
    '''
        Input : pass in a dataframe
        Output: returns a series of Booleans based on 'acct_type'
    '''
    df['fraud_no_fraud'] = df['acct_type'].astype(str).str[:5] == 'fraud'
    return df['fraud_no_fraud']



#####################################################################
#  Step 2: update time based columns to datetime
#####################################################################
def scrub_datetime(df):
    '''
        Input : pass in a dataframe
        Output: returns a new dataframe with updated datetime
    '''
    df['approx_payout_date']=df['approx_payout_date'].astype("datetime64[s]")
    df['event_created']=df['event_created'].astype("datetime64[s]")
    df['event_end']=df['event_end'].astype("datetime64[s]")
    df['event_published']=df['event_published'].astype("datetime64[s]")
    df['event_start']=df['event_start'].astype("datetime64[s]")
    df['user_created']=df['user_created'].astype("datetime64[s]")
    return df

#####################################################################
#  Step 3: Create column for events with no organization name
#####################################################################

def add_bool_name(df):
    '''
    Input: DataFram df
    Output: DataFrame df with boolean column attached
    '''
    length = len(df['org_name'])
    L_flag = []
    for i in range(length):
        flag = len(df['org_name'][i]) == 0
        L_flag.append(flag)

    df['org_name_bool'] = L_flag

    return df

#####################################################################
#  Step 4: Create column user_delta with difference of event_created and user_created
#####################################################################
def add_user_delta_min(df):
    '''
        Input : pass in a dataframe
        Output: DataFrame df with user_delta attached
        user_delta is the difference in time when event was created and published
    '''
    df['user_delta'] = df['event_created']-df['user_created']
    df['user_hour_delta']=df['user_delta'] / np.timedelta64(1, 'h')
    df['user_min_delta']=df['user_hour_delta']*60
    return df

#####################################################################
#  Step 5: Create column event_delta with difference of event_created and event_published
#####################################################################
def add_event_delta_min(df):
    '''
        Input : pass in a dataframe
        Output: DataFrame df with user_delta attached
        user_delta is the difference in time when event was created and published
    '''
    df['event_delta'] = df['event_published'] - df['event_created']
    df['event_hour_delta']=df['event_delta'] / np.timedelta64(1, 'h')
    df['event_min_delta']=df['event_hour_delta']*60
    return df

#####################################################################
#  SCRUB EVERYTHING
#####################################################################
def scrub_everything(df, feature_names):
    '''
        Input : pass in a dataframe, and a list of wanted feature names
        Output: tuple of 3 items
            1. returns a new dataframe with all scrubbing steps done
            2. returns 'y' --> target column
            3. returns 'X' --> Feature Matrix
    '''
    df['fraud_no_fraud'] = scrub_fraud_no_fraud(df)
    df2 = scrub_datetime(df)
    df3 = add_bool_name(df2)
    df4 = add_user_delta_min(df3)
    df5 = add_event_delta_min(df4)
    X = df5[feature_names].values
    y = df5['fraud_no_fraud'].values
    return (df, y, X)
