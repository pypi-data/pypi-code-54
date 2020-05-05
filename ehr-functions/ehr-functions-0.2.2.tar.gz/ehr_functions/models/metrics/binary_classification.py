from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

from ._base import BaseMetric


class BinaryClassification(BaseMetric):
    def post_train(self, train_data, val_data):
        print('Train')
        self.print_report(*train_data)

        print('')

        print('Validation')
        self.print_report(*val_data)

    @staticmethod
    def print_report(y_true, y_pred):
        try:
            auc_score = roc_auc_score(y_true, y_pred, average='micro')
        except ValueError as e:
            auc_score = str(e)

        print('Accuracy: ' + str(accuracy_score(y_true, y_pred) * 100))
        print('AUC: ' + str(auc_score))
        print(classification_report(y_true, y_pred))
