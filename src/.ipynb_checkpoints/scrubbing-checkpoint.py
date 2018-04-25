import numpy as np
import pandas as pd


#####################################################################
#  Step 1: remove missing violation id's
#####################################################################
def remove_missing_vid(df):
    '''
        Input : pass in a dataframe
        Output: returns a dataframe with clean violation id's
    '''
    mask = df['violation_id'].isnull()
    df_viol = df[~mask_viol]
    
    # clean up violation id's
    a = df_viol['violation_id']
    a[0].split('_')[2]
    
    L_vid = []
    for id in a:
        id_split = id.split('_')
        vid = id_split[2]
        L_vid.append(vid)
        
    df_viol['short_violation_id'] = L_vid
    return df_viol


#####################################################################
#  Step 2: get the number of violations per business at a given 
#          inspection date
#####################################################################
def group_bid_idate(df):
    '''
        Input : pass in a dataframe
        Output: returns a new dataframe with number of viloations per 
                business at a given inspection date
    '''
    # create a datetime column for inspection date
    df['inspect_date'] = pd.to_datetime(df.inspection_date)
    df['short_violation_id'] = df['short_violation_id'].apply(np.int64)
    
    # create a pandas series with groupby
    m1100 = df.groupby(['business_id', 'inspect_date'])['short_violation_id'].unique()
    df_grouped = pd.DataFrame(m1100)
    
    # Create a frame for data filling in
    ndf = df.drop_duplicates('business_id')
    # idf is just a frame to be filled with data from df_grouped 
    idf = ndf.reset_index(drop=True)
    
    # initialize idf
    idf.at[:, 'p1_3'] = 0
    idf.at[:, 'p4_6'] = 0
    idf.at[:, 'p7_9'] = 0
    idf.at[:, 'p10_12'] = 0
    idf.at[:, 'p13_18'] = 0
    idf.at[:, 'p19_24'] = 0
    idf.at[:, 'p25_36'] = 0
    
    # Filling up the number of violations per business per inspection date
    for row in df_grouped.iterrows():
        latest_enddate = pd.to_datetime('2018-03-31')
        bid = row[0][0]
        date = row[0][1]
        date1 = latest_enddate 
        date2 = latest_enddate - pd.DateOffset(months=3)
        date3 = latest_enddate - pd.DateOffset(months=6)
        date4 = latest_enddate - pd.DateOffset(months=9)
        date5 = latest_enddate - pd.DateOffset(months=12)
        date6 = latest_enddate - pd.DateOffset(months=18)
        date7 = latest_enddate - pd.DateOffset(months=24)
        date8 = latest_enddate - pd.DateOffset(months=36)

        if date2 < date <= date1:
            num_viols = len(row[1]['short_violation_id'])
            idx = idf.business_id[idf.business_id ==bid].index.tolist()
            idf.at[idx, 'p1_3'] = num_viols
        elif date3 < date <= date2:
            num_viols = len(row[1]['short_violation_id'])
            idx = idf.business_id[idf.business_id ==bid].index.tolist()
            idf.at[idx, 'p4_6'] = num_viols
        elif date4 < date <= date3:
            num_viols = len(row[1]['short_violation_id'])
            idx = idf.business_id[idf.business_id ==bid].index.tolist()
            idf.at[idx, 'p7_9'] = num_viols
        elif date5 < date <= date4:
            num_viols = len(row[1]['short_violation_id'])
            idx = idf.business_id[idf.business_id ==bid].index.tolist()
            idf.at[idx, 'p10_12'] = num_viols
        elif date6 < date <= date5:
            num_viols = len(row[1]['short_violation_id'])
            idx = idf.business_id[idf.business_id ==bid].index.tolist()
            idf.at[idx, 'p13_18'] = num_viols
        elif date7 < date <= date6:
            num_viols = len(row[1]['short_violation_id'])
            idx = idf.business_id[idf.business_id ==bid].index.tolist()
            idf.at[idx, 'p19_24'] = num_viols
        elif date8 < date <= date7: 
            num_viols = len(row[1]['short_violation_id'])
            idx = idf.business_id[idf.business_id ==bid].index.tolist()
            idf.at[idx, 'p25_36'] = num_viols
    
        return idf

#####################################################################
#  Step 3: Import zip codes from SF business lo
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
