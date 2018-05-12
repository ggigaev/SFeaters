import numpy as np
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import csv
import scrubbing

#ready4model_v2.csv file is from step1 and step2 in scrubbing.py
#df = pd.read_csv('../data/ready4model_v2.csv')
df2 = pd.read_csv('../data/Restaurant_Scores_-_LIVES_Standard.csv')
df3 = scrubbing.remove_missing_vid(df2)
df = scrubbing.group_bid_idate(df3)

# find out addresses without geo coords
address_no_geocoord = df.loc[df['business_latitude'].isnull(), 'business_address']
address_nogeo_lst = address_no_geocoord.values

num_vars = ['Off the Grid', 'Off The Grid', 'OFF The Grid', 'OFF THE GRID', 'Approved private locations', 'Approved Private Locations','Approved Locations']
L_nogeo = []
for address in address_nogeo_lst:
    if ~(address in num_vars):
        L_nogeo.append(address)
        
# take care of St
L_nogeo_St = []
for street in L_nogeo:
    st2 = street.split(' St ')
    L_nogeo_St.append(st2[0])
    
# take care of Ave
L_nogeo_Ave = []
for avenue in L_nogeo_St:
    st2 = avenue.split(' Ave ')
    L_nogeo_Ave.append(st2[0])
    
# take care of Blvd
L_nogeo_Blvd = []
for blvd in L_nogeo_Ave:
    st2 = blvd.split(' Blvd ')
    L_nogeo_Blvd.append(st2[0])
    
# take care of 0 in front of a street name like in 09th St
#L_nogeo_Blvd2 = ['2449 23rd St', '498 09th', '909 Grant Ave']
L_nogeo_Zero = []
for zero in L_nogeo_Blvd:
    st2 = zero.split(' 0')
    if len(st2) < 2:
        L_nogeo_Zero.append(st2[0])
    else:
        st1 = st2[0] + ' ' + st2[1]
        L_nogeo_Zero.append(st1)
        
# Go thru the list and collect the list of not getting addresses
geolocator = Nominatim(timeout = 20)

# add SF CA to addresses
L_nogeo_SFCA = []
for address in L_nogeo_Zero:
    L_nogeo_SFCA.append(address + ' SF CA')
    
def do_geocode2(address):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        time.sleep(1)
        return do_geocode(address)
    
# This code takes about 40 mins to finish. It is named as ..._dropme.csv to protect  
# geo_coords_sf.csv file already created. If you want to run this code again, drop 
# "dropme" part after the run.
write_file = "../data/geo_coords_sf_dropme.csv"
with open(write_file, "w") as output:
    for address in L_nogeo_SFCA[0:2231]:  #0:2231
        location = do_geocode2(address)
        if location != None:
            output.write( address + ',' + str(location.longitude) + ',' + 
                         str(location.latitude) +  '\n')