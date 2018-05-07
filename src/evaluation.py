from sklearn.metrics import accuracy_score, confusion_matrix, precision_score
from sklearn.metrics import recall_score, roc_curve, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd
import utility
import sys
import pickle
import scrubbing


if len(sys.argv) > 1:
    input_pkl = sys.argv[1]
    # data_sample_size = int(sys.argv[2])
else:
    print("No arguments")

class Scores(object):

    """
    Class for evaluating various model performance metrics.
    """

    def __init__(self, model, X_test, y_test):

        """
        Input: Model, X test split, y test split
        """

        self.model = model
        self.X_test = X_test
        self.y_test = y_test

        self.prediction = self.model.predict(X_test)

    def scores(self):

        """
        Prints various model scores
        """

        accuracy = accuracy_score(self.y_test, self.prediction)
        precision = precision_score(self.y_test, self.prediction)
        recall = recall_score(self.y_test, self.prediction)
        f1 = f1_score(self.y_test, self.prediction)

        acc_str = "Accuracy: {}".format(accuracy)
        prec_str = "Precision {}".format(precision)
        rec_str = "Recall {}".format(recall)
        f1_str = "F1 {}".format(f1)

        print ("\n".join([acc_str, prec_str, rec_str, f1_str]))

    def profit_curve(self, num_points, profit_matrix=[[0,-10],[0,190]]):

        """
            Input :
                Number to thresholds to test
                Profit Matrix
                    Format:
                        [[TN, FP],
                        [FN, TP]]
            Output:
                List of thresholds
                Profit at each threshold
        """

        prob_true = self.model.predict_proba(self.X_test)[:,1]

        x_thresh = []
        y_profit = []

        for thresh in np.linspace(0, 1, num_points):
            x_thresh.append(thresh)
            predictions = prob_true > thresh
            con_mat = confusion_matrix(self.y_test, predictions)
            profit = (con_mat * profit_matrix).sum()
            y_profit.append(profit)

        return x_thresh, y_profit

#####################################################################
#  Run model
#####################################################################
if __name__ == "__main__":
    '''
        Input : pass in a path to a pickle file ('../data/sf_...pkl')
        Output: 
            1. print out confusion matrix
            2. print out precision, recall, F1, and accuracy
        Comment: At the command line, go to src folder and type 
                 src$ python evaluation.py "../data/sf_clean_data.pkl" 
                 This will give scores and confusion matrix.
                 This also saves a final model file, finalized_model.sav
                 at data folder. This file will be used by prediction.
    '''
    feature_names = ['p7_9','p10_12', 'p13_18', 'p19_24', 'p25_36', '94013', 
                     '94014', '94080', '94101', '94102', '94103', '94104',
       '94105', '94107', '94108', '94109', '94110', '94111', '94112', '94114',
       '94115', '94116', '94117', '94118', '94120', '94121', '94122', '94123',
       '94124', '94127', '94129', '94130', '94131', '94132', '94133', '94134',
       '94143', '94158']
    df2 = pd.read_pickle(input_pkl)
    df = scrubbing.remove_rows_zero_violation2(df2) 

    y = df['y_label']
    X = df[feature_names]
    X_tr, X_test, y_tr, y_test = train_test_split(X, y, test_size=0.20, random_state=38)
    X_train, X_validation, y_train, y_validation = train_test_split(X_tr, y_tr, 
                                                        test_size=0.25, random_state=28)
    
    gb = GradientBoostingClassifier(n_estimators=40, learning_rate = 0.075, max_features=4, 
                                    max_depth = 8, subsample=0.4, random_state = 0)
    gb.fit(X_train, y_train)
    
    model = gb
    
    # save the model to disk
    filename = '../data/finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))
    
    prediction = model.predict(X_test)
    
    # scores
    accuracy = accuracy_score(y_test, prediction)
    precision = precision_score(y_test, prediction)
    recall = recall_score(y_test, prediction)
    f1 = f1_score(y_test, prediction)
    
    acc_str = "Accuracy: {0:.3f}".format(accuracy)
    prec_str = "Precision {0:.3f}".format(precision)
    rec_str = "Recall {0:.3f}".format(recall)
    f1_str = "F1 {0:.3f}".format(f1)
    
    print ("\n".join([acc_str, prec_str, rec_str, f1_str]))
    
    # confusion matrix
    y_predictions = gb.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_test, y_predictions).ravel()
    print("True Positive: {}".format(tp))
    print("False Negative: {}".format(fn))
    print("False Positive: {}".format(fp))
    print("True Negative: {}".format(tn))