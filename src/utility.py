import numpy as np
import pandas as pd
import csv

#####################################################################
#  Add number of turnovers and latest business startdate (ipynb: 05b)
#####################################################################
def import_turnover_duration(df, df_b):
    '''
        Input : pass in a dataframe from Step 4 and lookup df (SF business loc)
        Output: returns a dataframe with number of turnovers and start dates
        Comment: missing data were filled with average of turnovers and 
                average startdate
    '''
    df_b_3cols = df_b[['Street Address', 'Source Zipcode', 'Business Start Date']]
    # Let's get all the addresses
    address_lst = df['business_address'].tolist()
    address_unique_lst = list(set(address_lst))
    
    # Using the unique addresses from SF inpect, identify the same addresses
    # at SF business loc. Find num of turnovers and startdates. Update SF inspect.
    for address in address_unique_lst:
        df_b_3unique = df_b_3cols[df_b_3cols['Street Address'] == address]
        if len(df_b_3unique) > 0:
            num_turnovers = len(df_b_3unique)
            latest_startdate = pd.to_datetime(max(df_b_3unique['Business Start Date'].values))
            # let's append these info onto df
            idx = df[df['business_address'] == address].index
            df.loc[idx,'number_turnovers'] = num_turnovers
            df.loc[idx,'start_date'] = latest_startdate
    
    # Let's replace average values of num turnovers and start dates for NaN
    mask_turnovers = df['number_turnovers'].isnull()
    
    # sum(~mask_turnovers) is the number of True in number_turnovers
    avg_turnover = sum(df['number_turnovers'][~mask_turnovers])/sum(~mask_turnovers)
    df.loc[mask_turnovers, 'number_turnovers'] = avg_turnover
    
    # convert datetime in start_date to integer to use it for modeling
    #df.loc[:,'start_date'] = df.loc[:,'start_date'].dt.strftime('%Y%m%d')
    #df.loc[~mask_turnovers,'start_date'] = df.loc[~mask_turnovers,'start_date'].astype(int)
    #avg_startdate = sum(df['start_date'][~mask_turnovers].values)/sum(~mask_turnovers)
    #df.loc[mask_turnovers, 'start_date'] = int(avg_startdate)
    
    # Find the years in business for each restaurant by subtracting their starting date 
    # from End of March 2018.
    end_of_march_2018 = latest_startdate = pd.to_datetime('03/31/2018')
    df['duration_business'] = (end_of_march_2018 - df['start_date'])/ np.timedelta64(1, 'M')
    avg_duration = sum(df['duration_business'][~mask_turnovers].values)/sum(~mask_turnovers)
    df.loc[mask_turnovers, 'duration_business'] = avg_duration
    
    return df

#####################################################################
#  import yelp ratings (ipynb: 08)
#####################################################################
def yelp_ratings(df, df_ratings):
    '''
        Input : pass in two dataframes
           df = pd.read_pickle('data/sf_inspection2.pkl') or last df
           df_ratings = pd.read_pickle('data/yelp_ratings.pkl').
           
        Output: returns a dataframe with a new column called 'rating'
    '''
    # read in business names
    ratings_lst = list(df_ratings.iloc[:,0])
    rnames = []
    for line in ratings_lst:
        #print(line[1:5])
        if line[1:5] == 'span':
            name = line.split('<span>')
            name2 = name[1].split('</span>')
            rnames.append(name2[0])
            
    # read in ratings
    r_ratings = []
    for line in ratings_lst:
        #print(line[1:5])
        if line[1:4] == 'img':
            name = line.split('<img alt="')
            name2 = name[1].split(' star')
            r_ratings.append(name2[0])
            
    r_ratings_f = list(map(float, r_ratings))
    # Join these two lists together
    yelp_ratings = dict(zip(rnames, r_ratings_f))
    
    # match restaurant names and input to ratings column. This process will 
    # run after step remove_rows_zero_violation function
    for yname, rating in yelp_ratings.items():
        for bname in df['business_name']:
            yname_c = yname.strip().lower()
            bname_c = bname.strip().lower()
            if yname_c[:10] == bname_c[:10]:
                idx = df.loc[df['business_name'] == bname].index
                #print(idx)
                df.loc[idx, 'rating'] = rating
                
    # Give un-rated restaurants the average value.
    mask = df['rating'].isnull()
    avg_rating = df.loc[~mask, 'rating'].sum()/len(df.loc[~mask, 'rating'])
    df.loc[mask,'rating'] = avg_rating
    
    return df

#####################################################################
#  import yelp food prices (ipynb: 09)
#####################################################################
def yelp_prices(df, df_ratings):
    '''
        Input : pass in two dataframes
           df = pd.read_pickle('data/sf_inspection2.pkl') or last df
           df_prices = pd.read_pickle('data/yelp_prices.pkl').
           
        Output: returns a dataframe with a new column called 'price'
    '''
    
    prices_lst = list(df_ratings.iloc[:,0])
    
    # extract restaurant names first
    rnames = []
    for line in prices_lst:
        #print(line[1:6])
        if line[1:6] == 'span>':
            name = line.split('<span>')
            name2 = name[1].split('</span>')
            rnames.append(name2[0])
    
    # extract food prices
    r_prices = []
    for line in prices_lst:
        if line[1:7] == 'span c':
            name = line.split('">')
            name2 = name[1].split('</span>')
            r_prices.append(name2[0])
            
    prices_lst = list(map(len, r_prices))
    
    # Join these two lists together
    yelp_prices = dict(zip(rnames, prices_lst))
    
    # match restaurant names and input to price column. This process 
    # runs after remove_rows_zero_violation function
    
    for yname, price in yelp_prices.items():
        for bname in df['business_name']:
            yname_c = yname.strip().lower()
            bname_c = bname.strip().lower()
            if yname_c[:10] == bname_c[:10]:
                idx = df.loc[df['business_name'] == bname].index
                #print(idx)
                df.loc[idx, 'price'] = price
                
    # let's give un-priced ones the average value.
    mask = df['price'].isnull()
    avg_price = df.loc[~mask, 'price'].sum()/len(df.loc[~mask, 'price'])
    df.loc[mask,'price'] = avg_price
    
    return df


#####################################################################
#  geo coords round values (ipynb: 08)
#####################################################################
def geo_round(df):
    '''
        Input : pass in a dataframe at the end of the pipeline
           
        Output: returns a dataframe with a new column called 'longitude
            _round' and 'latitude_round'.
    '''
    
    # round the longitude and latitude values to 2 decimal point.
    lati = df['business_latitude'].values
    lati = [round(elem, 2) for elem in lati ]
    longi = df['business_longitude'].values
    longi = [round(elem, 2) for elem in longi ]
    df['longitude_round'] = longi
    df['latitude_round'] = lati
    
    # give NaN's the average value to both geo coords
    mask = df['longitude_round'].isnull()
    avg_longi = df.loc[~mask, 'longitude_round'].sum()/len(df.loc[~mask, 'longitude_round'])
    df.loc[mask,'longitude_round'] = round(avg_longi, 2)
    
    mask = df['latitude_round'].isnull()
    avg_lati = df.loc[~mask, 'latitude_round'].sum()/len(df.loc[~mask, 'latitude_round'])
    df.loc[mask,'latitude_round'] = round(avg_lati, 2)
    
    return df