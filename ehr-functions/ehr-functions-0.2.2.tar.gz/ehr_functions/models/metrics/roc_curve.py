from ._base import BaseMetric
import sklearn.metrics as metrics
import matplotlib.pyplot as plt


class ROCCurve(BaseMetric):
    def __init__(self):
        super().__init__()

    def post_train(self, train_data, val_data):
        print('Train AUC-ROC Curve')
        self.__plot_roc_curve(*train_data, data_type='Train')

        print('Val AUC-ROC Curve')
        self.__plot_roc_curve(*val_data, data_type='Val')

    # Source: https://stackoverflow.com/a/38467407/556935
    @staticmethod
    def __plot_roc_curve(y_true, y_pred, data_type):
        fpr, tpr, threshold = metrics.roc_curve(y_true, y_pred)
        roc_auc = metrics.auc(fpr, tpr)

        plt.figure(figsize=(20, 10))

        # Styling for NICoE presentation
        ax = plt.gca()
        ax.set_facecolor((223 / 255, 227 / 255, 235 / 255))
        ax.grid(color='white')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.title(data_type + ' Receiver Operating Characteristic', fontsize=16)
        plt.plot(fpr, tpr, '#002060', label='AUC = %0.2f' % roc_auc)
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], '#b50023', linestyle='--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')

        plt.show()
