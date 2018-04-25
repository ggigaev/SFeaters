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
    mask_viol = df['violation_id'].isnull()
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
        Input : pass in a dataframe from Step 1
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
#  Step 3: Import zip codes from SF business location file
#####################################################################
def import_zipcode(df, df_b):
    '''
    Input: pass in dataframe from Step 2 and lookup df (SF business loc)
    Output: returns dataframe df with missing zipcodes imported
    '''
    # SF business location file uploading
    # df = idf (from Step 2)
    # df_b = pd.read_csv('data/Registered_Business_Locations_-_San_Francisco.csv')
    
    # Identify and import zip code from SF business loc.
    df_b_3cols = df_b[['Street Address', 'Source Zipcode', 'Business Start Date']]
    
    # let's identify missing zip code from df
    df2 = df[['business_postal_code', 'business_address', 'business_name']]
    
    # list of addresses without zip codes
    df_nozip = df2[df2['business_postal_code'].isnull()]
    list_nozip_address = df_nozip['business_address'].tolist()
    
    # Let's get the list of street address and zipcodes
    # df_b_matching_ones is the list of street addresses, zip codes, and business
    # start dates that are matching between business loc and SF inspection files.
    df_b_matching_ones = df_b_3cols[df_b_3cols['Street Address'].isin(list_nozip_address)]
    
    df_update_zipcode = df[:]
    
    # find matching addresses between SF inspection and SF business loc files and update 
    # the missing zip codes in SF inspection
    for address in list_nozip_address:
        for row in df_b_matching_ones.iterrows():
            if address == row[1][0]:
                idx = df_update_zipcode[df_update_zipcode['business_address'] == address].index
                df_update_zipcode.loc[idx,'business_postal_code'] = row[1][1]
    
    # Let's clean up df_update_zipcode
    m520 = df_update_zipcode['business_postal_code'].isnull()
    
    # Let's assign all the null zip codes to 'zzzzz'
    idx = df_update_zipcode[m520]['business_postal_code'].index
    df_update_zipcode.loc[idx, 'business_postal_code'] = 'zzzzz'
    
    # convert float (94102.0) to string ('94102')
    # Assign other junks like 'Ca' or '194' as 'zzzzz'
    for index, row in df_update_zipcode[['business_postal_code', 'business_id']].iterrows():
        n = row['business_postal_code']
        if isinstance(n, float):
            df_update_zipcode.loc[index, 'business_postal_code'] = str(int(n))
        elif len(n) < 4:
            df_update_zipcode.loc[index, 'business_postal_code'] = 'zzzzz'
        elif len(n) == 9:
            df_update_zipcode.loc[index, 'business_postal_code'] = str(n[:5])
    
    return df_update_zipcode

#####################################################################
#  Step 4: Zip code dummy columns created
#####################################################################
def get_zipcode_dummies(df):
    '''
        Input : pass in a dataframe from Step 3
        Output: returns a dataframe with zip code dummies.
        Comment: creates a text file called "col_names.txt" that will
                 be used to select features.
    '''
    # Using 9 months period as y label
    df['y_label'] = (df['p1_3'] + df['p4_6'] + df['p7_9']) > 0
    
    # pd.get_dummies(df['business_postal_code'])
    df = pd.concat([df, pd.get_dummies(df['business_postal_code'])], axis=1)
    # remove one redundant column
    df2 = df.drop(['zzzzz'], axis=1)
    
    # create a text file with column names, so that they can be used for feature 
    # selection. Remove 95105 and 92672, which do not belong to SF.
    s = ''
    for i in df2.columns.values:
        s += i + ', '
        
    with open('data/col_names.txt', 'w') as f:
        f.write(s)
    
    return df2

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
