from sklearn.metrics import accuracy_score, confusion_matrix, precision_score
from sklearn.metrics import recall_score, roc_curve, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd
import utility
import sys

if len(sys.argv) >1:
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
    '''
    feature_names = ['p7_9','p10_12', 'p13_18', 'p19_24', 'p25_36', '94013', 
                     '94014', '94080', '94101', '94102', '94103', '94104',
       '94105', '94107', '94108', '94109', '94110', '94111', '94112', '94114',
       '94115', '94116', '94117', '94118', '94120', '94121', '94122', '94123',
       '94124', '94127', '94129', '94130', '94131', '94132', '94133', '94134',
       '94143', '94158']
    df = pd.read_pickle('../data/sf_inspection.pkl')

    y = df['y_label']
    X = df[feature_names]
    X_tr, X_test, y_tr, y_test = train_test_split(X, y, test_size=0.20, random_state=38)
    X_train, X_validation, y_train, y_validation = train_test_split(X_tr, y_tr, 
                                                        test_size=0.25, random_state=28)
    
    gb = GradientBoostingClassifier(n_estimators=20, learning_rate = 0.5, max_features=2, 
                                    max_depth = 2, random_state = 0)
    gb.fit(X_train, y_train)
    
    model = gb
    prediction = model.predict(X_test)
    
    # prediction
    accuracy = "%.3f" % accuracy_score(y_test, prediction)
    accuracy = float(accuracy) * 100
    
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