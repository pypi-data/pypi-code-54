from keras_preprocessing import sequence
from keras.utils.data_utils import Sequence
import numpy as np


class SequenceBuilder(Sequence):
    """Generate Batches of data"""

    def __init__(self, data, target, batch_size, ARGS, target_out=True):
        # Receive all appropriate data
        self.codes = data[0]
        index = 1
        if ARGS.numeric_size:
            self.numeric = data[index]
            index += 1

        if ARGS.use_time:
            self.time = data[index]

        self.num_codes = ARGS.num_codes
        self.target = target
        self.batch_size = batch_size
        self.target_out = target_out
        self.numeric_size = ARGS.numeric_size
        self.use_time = ARGS.use_time
        self.n_steps = ARGS.n_steps
        # self.balance = (1-(float(sum(target))/len(target)))/(float(sum(target))/len(target))

    def __len__(self):
        """Compute number of batches.
        Add extra batch if the data doesn't exactly divide into batches
        """
        if len(self.codes) % self.batch_size == 0:
            return len(self.codes) // self.batch_size
        return len(self.codes) // self.batch_size + 1

    def __getitem__(self, idx):
        """Get batch of specific index"""

        def __is_weird_steps(a):
            # Rewrite to fix error
            # if steps != [[-1]]:
            if len(a) == 1 and isinstance(a, int) and a[0] == -1:
                return True

            return False

        def pad_data(data, length_visits, length_codes, pad_value=0):
            """Pad data to desired number of visits and codes inside each visit"""
            zeros = np.full((len(data), length_visits, length_codes), pad_value)
            for steps, mat in zip(data, zeros):
                # if steps != [[-1]]:
                if not __is_weird_steps(steps):
                    for step, mhot in zip(steps, mat[-len(steps):]):
                        # Populate the data into the appropriate visit
                        mhot[:len(step)] = step

            return zeros

        # Compute reusable batch slice
        batch_slice = slice(idx * self.batch_size, (idx + 1) * self.batch_size)
        x_codes = self.codes[batch_slice]
        # Max number of visits and codes inside the visit for this batch
        pad_length_visits = min(max(map(len, x_codes)), self.n_steps)
        pad_length_codes = max(map(lambda x: max(map(len, x)), x_codes))
        # Number of elements in a batch (useful in case of partial batches)
        length_batch = len(x_codes)
        # Pad data
        x_codes = pad_data(x_codes, pad_length_visits, pad_length_codes, self.num_codes)
        outputs = [x_codes]
        # Add numeric data if necessary
        if self.numeric_size:
            x_numeric = self.numeric[batch_slice]
            x_numeric = pad_data(x_numeric, pad_length_visits, self.numeric_size, -99.0)
            outputs.append(x_numeric)
        # Add time data if necessary
        if self.use_time:
            x_time = sequence.pad_sequences(self.time[batch_slice],
                                            dtype=np.float32, maxlen=pad_length_visits,
                                            value=+99).reshape(length_batch, pad_length_visits, 1)
            outputs.append(x_time)

        # Add target if necessary (training vs validation)
        if self.target_out:
            target = self.target[batch_slice].reshape(length_batch, 1, 1)
            # sample_weights = (target*(self.balance-1)+1).reshape(length_batch, 1)
            # In our experiments sample weights provided worse results
            return outputs, target

        return outputs
