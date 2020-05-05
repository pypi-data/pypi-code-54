from ehr_functions.models.retain_experiment.retain.freeze_padding import FreezePadding, FreezePaddingNonNegative
# from keras_exp.multigpu import get_available_gpus, make_parallel
from keras.constraints import non_neg
from keras.regularizers import l2
from keras.models import Model
from keras import backend as K
import keras.layers as L
import tensorflow as tf


def model_create(ARGS):
    """Create and Compile model and assign it to provided devices"""

    def retain(ARGS):
        """Create the model"""

        # Define the constant for model saving
        reshape_size = ARGS.emb_size + ARGS.numeric_size
        if ARGS.allow_negative:
            embeddings_constraint = FreezePadding()
            beta_activation = 'tanh'
            output_constraint = None
        else:
            embeddings_constraint = FreezePaddingNonNegative()
            beta_activation = 'sigmoid'
            output_constraint = non_neg()

        # Get available gpus , returns empty list if none
        glist = False  # get_available_gpus()

        def reshape(data):
            """Reshape the context vectors to 3D vector"""
            return K.reshape(x=data, shape=(K.shape(data)[0], 1, reshape_size))

        # Code Input
        codes = L.Input((None, None), name='codes_input')
        inputs_list = [codes]
        # Calculate embedding for each code and sum them to a visit level
        codes_embs_total = L.Embedding(ARGS.num_codes + 1,
                                       ARGS.emb_size,
                                       name='embedding',
                                       embeddings_constraint=embeddings_constraint)(codes)
        codes_embs = L.Lambda(lambda x: K.sum(x, axis=2))(codes_embs_total)
        # Numeric input if needed
        if ARGS.numeric_size:
            numerics = L.Input((None, ARGS.numeric_size), name='numeric_input')
            inputs_list.append(numerics)
            full_embs = L.concatenate([codes_embs, numerics], name='catInp')
        else:
            full_embs = codes_embs

        # Apply dropout on inputs
        full_embs = L.Dropout(ARGS.dropout_input)(full_embs)

        # Time input if needed
        if ARGS.use_time:
            time = L.Input((None, 1), name='time_input')
            inputs_list.append(time)
            time_embs = L.concatenate([full_embs, time], name='catInp2')
        else:
            time_embs = full_embs

        # Setup Layers
        # This implementation uses Bidirectional LSTM instead of reverse order
        #    (see https://github.com/mp2893/retain/issues/3 for more details)

        # If training on GPU and Tensorflow use CuDNNLSTM for much faster training
        if glist:
            alpha = L.Bidirectional(L.CuDNNLSTM(ARGS.recurrent_size, return_sequences=True),
                                    name='alpha')
            beta = L.Bidirectional(L.CuDNNLSTM(ARGS.recurrent_size, return_sequences=True),
                                   name='beta')
        else:
            alpha = L.Bidirectional(L.LSTM(ARGS.recurrent_size,
                                           return_sequences=True, implementation=2),
                                    name='alpha')
            beta = L.Bidirectional(L.LSTM(ARGS.recurrent_size,
                                          return_sequences=True, implementation=2),
                                   name='beta')

        alpha_dense = L.Dense(1, kernel_regularizer=l2(ARGS.l2))
        beta_dense = L.Dense(ARGS.emb_size + ARGS.numeric_size,
                             activation=beta_activation, kernel_regularizer=l2(ARGS.l2))

        # Compute alpha, visit attention
        alpha_out = alpha(time_embs)
        alpha_out = L.TimeDistributed(alpha_dense, name='alpha_dense_0')(alpha_out)
        alpha_out = L.Softmax(axis=1)(alpha_out)
        # Compute beta, codes attention
        beta_out = beta(time_embs)
        beta_out = L.TimeDistributed(beta_dense, name='beta_dense_0')(beta_out)
        # Compute context vector based on attentions and embeddings
        c_t = L.Multiply()([alpha_out, beta_out, full_embs])
        c_t = L.Lambda(lambda x: K.sum(x, axis=1))(c_t)
        # Reshape to 3d vector for consistency between Many to Many and Many to One implementations
        contexts = L.Lambda(reshape)(c_t)

        # Make a prediction
        contexts = L.Dropout(ARGS.dropout_context)(contexts)
        output_layer = L.Dense(1, activation='sigmoid', name='dOut',
                               kernel_regularizer=l2(ARGS.l2), kernel_constraint=output_constraint)

        # TimeDistributed is used for consistency
        # between Many to Many and Many to One implementations
        output = L.TimeDistributed(output_layer, name='time_distributed_out')(contexts)
        # Define the model with appropriate inputs
        model = Model(inputs=inputs_list, outputs=[output])

        return model

    # Set Tensorflow to grow GPU memory consumption instead of grabbing all of it at once
    K.clear_session()
    config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
    config.gpu_options.allow_growth = True
    tfsess = tf.Session(config=config)
    K.set_session(tfsess)
    # If there are multiple GPUs set up a multi-gpu model
    glist = []  # get_available_gpus()
    if len(glist) > 1:
        with tf.device('/cpu:0'):
            model = retain(ARGS)
        model_final = make_parallel(model, glist)
    else:
        model_final = retain(ARGS)

    # import tensorflow as tf
    # from keras import backend as K
    def auc(y_true, y_pred):
        auc = tf.metrics.auc(y_true, y_pred)[1]
        K.get_session().run(tf.local_variables_initializer())
        return auc

    # Compile the model - adamax has produced best results in our experiments
    model_final.compile(optimizer='adamax', loss='binary_crossentropy', metrics=['accuracy', auc],
                        sample_weight_mode="temporal")

    return model_final
