import numpy as np
import pandas as pd
import csv
import utility
import sys

if len(sys.argv) >1:
    input_csv = sys.argv[1]
    data_sample_size = int(sys.argv[2])
else:
    print("No arguments")

print(input_csv)

#####################################################################
#  Step 1: remove missing violation id's (ipynb: 01)
#####################################################################
def remove_missing_vid(df):
    '''
        Input : pass in a dataframe
        Output: returns a dataframe with clean violation id's
    '''
    print('hello')
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
#          inspection date (ipynb: 03-1)
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
#  Step 3: remove missing violation id's (ipynb: 42-1)
#####################################################################
def geo_coords_import(df, csv_file):
    '''
        Input : pass in a dataframe from the previous step and a csv file
                with geo coords
        Output: returns a dataframe with geo coords imported
    '''
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            address = row[0]
            longitude = row[1]
            latitude = row[2]
            n = len(df)
            for idx in range(n):
                df_address = df.loc[idx, 'business_address']
                # to remove ' SF CA' at the end of an address
                if df_address == address[:-6]: 
                    df.loc[idx, 'business_longitude'] = longitude
                    df.loc[idx, 'business_latitude'] = latitude
    
    # change longitude and latitude to float type
    df['business_longitude'] = df['business_longitude'].astype(float)
    df['business_latitude'] = df['business_latitude'].astype(float)
    
    # remove outliers
    mask333 = df['business_longitude'].values > -122.375
    df2 = df[~mask333]
    mask334 = df2['business_latitude'].values < 37.70
    df3 = df2[~mask334]
    
    return df3


#####################################################################
#  Step 4: Import zip codes from SF business location file (ipynb: 05)
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
    
    # Let's get the list of street address and zipcodes.
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
#  Step 6: Zip code dummy columns created (ipynb: 06)
#####################################################################
def get_zipcode_dummies(df):
    '''
        Input : pass in a dataframe from Step 4
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
        
    with open('../data/col_names.txt', 'w') as f:
        f.write(s)
    
    return df2

#####################################################################
#  Step 6-1: Zip code dummy columns created (ipynb: 06)
#####################################################################
def get_zipcode_dummies2(df):
    '''
        Input : pass in a dataframe from Step 4
        Output: returns a dataframe with zip code dummies.
        Comment: creates a text file called "col_names.txt" that will
                 be used to select features.
                 Use the latest 6 months period as y label.
    '''
    # Using 6 months period as y label
    df['y_label'] = (df['p1_3'] + df['p4_6'] ) > 0
    
    # pd.get_dummies(df['business_postal_code'])
    df = pd.concat([df, pd.get_dummies(df['business_postal_code'])], axis=1)
    # remove one redundant column
    df2 = df.drop(['zzzzz'], axis=1)
    
    # create a text file with column names, so that they can be used for feature 
    # selection. Remove 95105 and 92672, which do not belong to SF.
    s = ''
    for i in df2.columns.values:
        s += i + ', '
        
    with open('../data/col_names.txt', 'w') as f:
        f.write(s)
    
    return df2

#####################################################################
#  Step 7: Remove the rows with 0 violation between 10 and 36 months
#####################################################################
def remove_rows_zero_violation(df):
    '''
        Input : pass in a dataframe from Step 6
        Output: returns a dataframe without the rows with zero violation
                between 10 and 36 months. (Those rows are labeled as
                1, since this data set is from at least one violation.)
    '''
    # Using 9 months period as y label
    df['p10_36'] = df['p10_12'] + df['p13_18'] + df['p19_24'] + df['p25_36']
    
    # Let's remove the ones with df5['p10_36'] == 0
    df2 = df[df['p10_36'] != 0]
    
    return df2

#####################################################################
#  Step 7-1: Remove the rows with 0 violation between 7 and 36 months
#####################################################################
def remove_rows_zero_violation2(df):
    '''
        Input : pass in a dataframe from Step 6
        Output: returns a dataframe without the rows with zero violation
                between 7 and 36 months. (Those rows are labeled as
                1, since this data set is from at least one violation.)
    '''
    # Using 6 months period as y label
    df['p7_36'] = df['p7_9'] + df['p10_12'] + df['p13_18'] + df['p19_24'] + df['p25_36']
    
    # Let's remove the ones with df5['p7_36'] == 0
    df2 = df[df['p7_36'] != 0]
    
    return df2

#####################################################################
#  SCRUB EVERYTHING
#####################################################################
if __name__ == "__main__":
    '''
        Input : pass in a dataframe, and a list of wanted feature names
        Output: tuple of 3 items
            1. returns a new dataframe with all scrubbing steps done
            2. returns 'y' --> target column
            3. returns 'X' --> Feature Matrix
    '''
    df = pd.read_csv(input_csv)

    df2 = remove_missing_vid(df)
    df3 = group_bid_idate(df2)
    csv_file = '../data/geo_coords_sf.csv'
    df4 = geo_coords_import(df3, csv_file)
    df_b = pd.read_csv('../data/Registered_Business_Locations_-_San_Francisco.csv')
    
    #======================================================================
    # import_turnover_duration runs here if needed
    df4b = utility.import_turnover_duration(df4, df_b)
    #======================================================================
    
    df5 = import_zipcode(df4, df_b)
    df6 = get_zipcode_dummies2(df5)  # with new time periods
    df7 = remove_rows_zero_violation2(df6)  # with new time periods
    
    #======================================================================
    # yelp_ratings runs here if needed
    # yelp_prices runs here if needed
    # df_ratings = pd.read_pickle('../data/yelp_ratings.pkl')
    # df_prices = pd.read_pickle('../data/yelp_prices.pkl')    
    # df7a = utility.yelp_ratings(df7, df_ratings)
    # df7b = utility.yelp_prices(df7a, df_prices)
    # df7c = utility.geo_round(df7b)
    #======================================================================

    df.to_pickle('../data/sf_inspection.pkl')
