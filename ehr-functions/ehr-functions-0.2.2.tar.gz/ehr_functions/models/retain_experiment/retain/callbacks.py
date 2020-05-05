from ehr_functions.models.retain_experiment.retain.sequence_builder import SequenceBuilder
from keras.callbacks import Callback, ModelCheckpoint
from sklearn.metrics import average_precision_score, roc_auc_score
import os


def create_callbacks(model, data, ARGS):
    """Create the checkpoint and logging callbacks"""

    class LogEval(Callback):
        """Logging Callback"""

        def __init__(self, filepath, model, data, ARGS, interval=1):

            super(Callback, self).__init__()
            self.filepath = filepath
            self.interval = interval
            self.data_test, self.y_test = data
            self.generator = SequenceBuilder(data=self.data_test, target=self.y_test,
                                             batch_size=ARGS.batch_size, ARGS=ARGS,
                                             target_out=False)
            self.model = model

        def on_epoch_end(self, epoch, logs={}):
            # Compute ROC-AUC and average precision the validation data every interval epochs
            if epoch % self.interval == 0:
                # Compute predictions of the model
                y_pred = [x[-1] for x in
                          self.model.predict_generator(self.generator,
                                                       verbose=0,
                                                       use_multiprocessing=True,
                                                       workers=5,
                                                       max_queue_size=5)]
                score_roc = roc_auc_score(self.y_test, y_pred)
                score_pr = average_precision_score(self.y_test, y_pred)
                # Create log files if it doesn't exist, otherwise write to it
                if os.path.exists(self.filepath):
                    append_write = 'a'
                else:
                    append_write = 'w'
                with open(self.filepath, append_write) as file_output:
                    file_output.write("\nEpoch: {:d}- ROC-AUC: {:.6f} ; PR-AUC: {:.6f}" \
                                      .format(epoch, score_roc, score_pr))

                print("\nEpoch: {:d} - ROC-AUC: {:.6f} PR-AUC: {:.6f}" \
                      .format(epoch, score_roc, score_pr))

    # Create callbacks
    checkpoint = ModelCheckpoint(filepath=ARGS.directory + '/weights.{epoch:02d}.hdf5')
    log = LogEval(ARGS.directory + '/log.txt', model, data, ARGS)
    return checkpoint, log
