from sklearn.metrics import accuracy_score, confusion_matrix, precision_score
from sklearn.metrics import recall_score, roc_curve, f1_score
import numpy as np

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


    def roc(self):

        """
        Output: True Positive Rate, False Positive Rate
        """

        probs = self.model.predict_proba(self.X_test)[:,1]

        roc = roc_curve(self.y_test, probs)

        return roc[0], roc[1], roc[2]

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
