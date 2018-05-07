from sklearn.metrics import accuracy_score, confusion_matrix, precision_score
from sklearn.metrics import recall_score, roc_curve, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd
import utility
import sys
import pickle

if len(sys.argv) >0:
    print("Write the restaurant's name: ")
    input_name = input()
else:
    print("No arguments")


#####################################################################
#  Run prediction
#####################################################################
if __name__ == "__main__":
    '''
        Input : pass in a restaurant name
        Output: 
            1. print out restaurant name and address
            2. print out prediction
        Comment: At the command line, go to src folder and type 
                 src$ python prediction.py.
                 This will prompt you for a restaurant name.
                 Once it receives the restaurant name, it will automaticall 
                 import sf_inspection.pkl from data folder. It will use the 
                 entire data set (without removing the ones with zero violations 
                 before 7 months ago) and rearrange the time periods
                 by including 1 - 6 months into test set (not targets anymore).
                 See the change in feature_names.
                 This program uses the model already developed at evaluation.py.
                 The model file name is "finalized_model.sav", a pickle file.
    '''
    accuracy = 71.2
    feature_names = ['p1_3','p4_6', 'p7_12', 'p13_18', 'p19_36', '94013', 
                     '94014', '94080', '94101', '94102', '94103', '94104',
       '94105', '94107', '94108', '94109', '94110', '94111', '94112', '94114',
       '94115', '94116', '94117', '94118', '94120', '94121', '94122', '94123',
       '94124', '94127', '94129', '94130', '94131', '94132', '94133', '94134',
       '94143', '94158']
    df = pd.read_pickle('../data/sf_clean_data.pkl')

    # create new columns for p7_12 and p19_36
    df['p7_12'] = df['p7_9'] + df['p10_12']
    df['p19_36'] = df['p19_24'] + df['p25_36']
    
    y = df['y_label']
    X = df[feature_names]
    
    # import saved model from data/finalized_model.sav
    filename = '../data/finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    
    prediction = loaded_model.predict(X)
    
    names_addresses = df[['business_name', 'business_address', 'y_label']]
    n = len(names_addresses)
    flag = 0    # to find out any restaurant not in the list
    for i in range(n):
        if input_name.lower() == names_addresses.iloc[i,0].lower():
            restaurant_name = names_addresses.iloc[i][0]
            restaurant_address = names_addresses.iloc[i][1]
            print('Restaurant name: {} \nAddress: {}'.format(restaurant_name, restaurant_address))
            if names_addresses.iloc[i][2]:  # check if y_label is True
                print('This place is predicted as risky, with accuracy of {}% \n'.format(accuracy))
            else: 
                print('This place is safe, with accuracy of {}% \n'.format(accuracy))
            flag = 1
    
    if flag == 0:
        print('This place is not rated. \n')