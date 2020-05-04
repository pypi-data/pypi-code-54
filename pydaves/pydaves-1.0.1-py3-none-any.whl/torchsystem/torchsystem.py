import os
import torch
import torchnet
import traceback
import numpy as np
from pydaves.utils import PyLogger
from pydaves.utils import touch_dir
from pydaves.torchsystem.torchutils import TorchConfig


class TorchExperiment(object):
    def __init__(self,
                 config: TorchConfig,
                 loader_fun, model_class,
                 loader_args=(), model_args=()):
        # validating inputs
        self.__config, \
        self.__loader_fun, self.__model_class, \
        self.__loader_args, self.__model_args = \
            self._validate_inputs(
                config,
                loader_fun, model_class,
                loader_args, model_args
            )

        # managing paths
        touch_dir(self.work_dir)
        touch_dir(self.this_dir)

        # creating a logger instance
        self.__logger = PyLogger(
            log_path=self.log_path,
            console_only_flag=self.console_only_flag,
            print_timestamp_flag=self.print_timestamp_flag
        )

        # creating a device instance
        self.__device = self._validate_gpu()

        # creating loaders
        self.__train_loader, self.__valid_loader, \
        self.__input_shape, self.__classes = self.loader_fun(
            experiment=self, *loader_args)

        # creating activation and loss
        self.__activation = self._get_torch_activation()
        self.__loss = self._get_torch_loss()

        # creating a model instance
        self.__model = self.model_class(
            experiment=self, *model_args)

        # creating optimizer and lr_scheduler
        self.__optimizer = self._get_torch_optimizer()
        self.__lr_scheduler = self._get_torch_lr_scheduler()

        # creating a trainer and a tester instance
        self.__trainer = TorchTrainer(experiment=self)
        self.__tester = TorchTester(experiment=self)

    @staticmethod
    def _validate_inputs(config: TorchConfig,
                         loader_fun, model_class,
                         loader_args: tuple, model_args: tuple):
        if not isinstance(config, TorchConfig):
            raise TypeError("Input 'config' must be of type 'TorchConfig', "
                            f"got {type(config)} instead.")
        if not callable(loader_fun):
            raise TypeError("Input 'loader_fun' must be callable.")
        if not callable(model_class):
            raise TypeError("Input 'model_class' must be callable.")
        if not isinstance(loader_args, tuple):
            raise TypeError("Input 'loader_args' must be of type 'tuple', "
                            f"got {type(loader_args)} instead.")
        if not isinstance(model_args, tuple):
            raise TypeError("Input 'model_args' must be of type 'tuple', "
                            f"got {type(model_args)} instead.")
        return config, loader_fun, model_class, loader_args, model_args

    def _validate_gpu(self):
        # checking if the selected gpu is available
        if self.use_gpu_flag:
            if torch.cuda.is_available():
                if self.gpu_index < torch.cuda.device_count():
                    # enabling the chosen gpu
                    os.environ["CUDA_VISIBLE_DEVICES"] = str(self.gpu_index)

                    # creating a torch.device instance for the chosen gpu
                    device = torch.device(f"cuda:{self.gpu_index}")
                else:
                    raise ValueError(f"Invalid gpu index ({self.gpu_index}).")
            else:
                raise ValueError("CUDA not available.")
        else:
            # creating device for cpu
            device = torch.device("cpu")
        return device

    def _get_torch_activation(self):
        # getting activation_name
        activation_name = self.activation_name.lower()

        # selecting activation
        # TODO: add here a routine for each Torch activation
        if activation_name == "tanh":
            return torch.nn.Tanh()
        elif activation_name == "elu":
            if "alpha" not in self.activation_settings:
                self.set(
                    keys=("activation_settings", "alpha"),
                    value=1.0
                )
            if "inplace" not in self.activation_settings:
                self.set(
                    keys=("activation_settings", "inplace"),
                    value=False
                )
            return torch.nn.ELU(
                alpha=self.activation_settings["alpha"],
                inplace=self.activation_settings["inplace"]
            )
        else:
            raise ValueError(f"Unrecognized activation_name "
                             f"{self.activation_name}.")

    def _get_torch_loss(self):
        # getting loss_name
        loss_name = self.loss_name.lower()

        # selecting loss
        # TODO: add here a routine for each Torch loss
        if loss_name == "crossentropyloss":
            if "ignore_index" not in self.loss_settings:
                self.set(
                    keys=("loss_settings", "ignore_index"),
                    value=-100
                )
            if "reduction" not in self.loss_settings:
                self.set(
                    keys=("loss_settings", "reduction"),
                    value="mean"
                )
            return torch.nn.CrossEntropyLoss(
                ignore_index=self.loss_settings["ignore_index"],
                reduction=self.loss_settings["reduction"]
            )
        elif loss_name == "mseloss":
            if "reduction" not in self.loss_settings:
                self.set(
                    keys=("loss_settings", "reduction"),
                    value="mean"
                )
            return torch.nn.MSELoss(
                reduction=self.loss_settings["reduction"]
            )
        else:
            raise ValueError(f"Unrecognized loss_name "
                             f"{self.loss_name}.")

    # noinspection DuplicatedCode
    def _get_torch_optimizer(self):
        # getting optimizer_name
        optimizer_name = self.optimizer_name.lower()

        # selecting optimizer
        # TODO: add here a routine for each Torch optimizer
        if optimizer_name == "adam":
            if "lr" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "lr"),
                    value=0.001
                )
            if "betas" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "betas"),
                    value=(0.9, 0.999)
                )
            if "eps" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "eps"),
                    value=1e-08
                )
            if "weight_decay" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "weight_decay"),
                    value=0
                )
            if "amsgrad" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "amsgrad"),
                    value=False
                )
            return torch.optim.Adam(
                params=self.model.parameters(),
                lr=self.optimizer_settings["lr"],
                betas=self.optimizer_settings["betas"],
                eps=self.optimizer_settings["eps"],
                weight_decay=self.optimizer_settings["weight_decay"],
                amsgrad=self.optimizer_settings["amsgrad"]
            )
        elif optimizer_name == "adamax":
            if "lr" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "lr"),
                    value=0.002
                )
            if "betas" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "betas"),
                    value=(0.9, 0.999)
                )
            if "eps" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "eps"),
                    value=1e-08
                )
            if "weight_decay" not in self.optimizer_settings:
                self.set(
                    keys=("optimizer_settings", "weight_decay"),
                    value=0
                )
            # noinspection PyUnresolvedReferences
            return torch.optim.Adamax(
                params=self.model.parameters(),
                lr=self.optimizer_settings["lr"],
                betas=self.optimizer_settings["betas"],
                eps=self.optimizer_settings["eps"],
                weight_decay=self.optimizer_settings["weight_decay"],
            )
        else:
            raise ValueError(f"Unrecognized optimizer_name "
                             f"{self.optimizer_name}.")

    def _get_torch_lr_scheduler(self):
        # getting lr_scheduler_name
        lr_scheduler_name = self.lr_scheduler_name.lower()

        # selecting lr_scheduler
        # TODO: add here a routine for each Torch lr_scheduler
        if lr_scheduler_name == "reducelronplateau":
            if "mode" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "mode"),
                    value="min"
                )
            if "factor" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "factor"),
                    value=0.1
                )
            if "patience" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "patience"),
                    value=10
                )
            if "verbose" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "verbose"),
                    value=False
                )
            if "threshold" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "threshold"),
                    value=1e-4
                )
            if "threshold_mode" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "threshold_mode"),
                    value="rel"
                )
            if "cooldown" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "cooldown"),
                    value=0
                )
            if "min_lr" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "min_lr"),
                    value=0
                )
            if "eps" not in self.lr_scheduler_settings:
                self.set(
                    keys=("lr_scheduler_settings", "eps"),
                    value=1e-8
                )
            return torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer=self.optimizer,
                mode=self.lr_scheduler_settings["mode"],
                factor=self.lr_scheduler_settings["factor"],
                patience=self.lr_scheduler_settings["patience"],
                verbose=self.lr_scheduler_settings["verbose"],
                threshold=self.lr_scheduler_settings["threshold"],
                threshold_mode=self.lr_scheduler_settings["threshold_mode"],
                cooldown=self.lr_scheduler_settings["cooldown"],
                min_lr=self.lr_scheduler_settings["min_lr"],
                eps=self.lr_scheduler_settings["eps"]
            )
        else:
            raise ValueError(
                "<< {} >> lr_scheduler is not a valid one.".format(
                    self.lr_scheduler))

    @property
    def config(self) -> TorchConfig:
        return self.__config

    @property
    def loader_fun(self):
        return self.__loader_fun

    @property
    def model_class(self):
        return self.__model_class

    @property
    def loader_args(self) -> tuple:
        return self.__loader_args

    @property
    def model_args(self) -> tuple:
        return self.__model_args

    @property
    def logger(self) -> PyLogger:
        return self.__logger

    @property
    def device(self) -> torch.device:
        return self.__device

    # noinspection PyUnresolvedReferences
    @property
    def train_loader(self) -> torch.utils.data.DataLoader:
        return self.__train_loader

    # noinspection PyUnresolvedReferences
    @property
    def valid_loader(self) -> torch.utils.data.DataLoader:
        return self.__valid_loader

    @property
    def n_batches_train(self) -> int:
        return len(self.train_loader)

    @property
    def n_batches_valid(self) -> int:
        return len(self.valid_loader)

    @property
    def input_shape(self) -> tuple:
        return self.__input_shape

    @property
    def input_height(self) -> int:
        return self.input_shape[0]

    @property
    def input_width(self) -> int:
        return self.input_shape[1]

    @property
    def input_depth(self) -> int:
        return self.input_shape[2]

    @property
    def input_n_rows(self) -> int:
        return self.input_shape[0]

    @property
    def input_n_cols(self) -> int:
        return self.input_shape[1]

    @property
    def input_n_channels(self) -> int:
        return self.input_shape[2]

    @property
    def classes(self) -> tuple:
        return self.__classes

    @property
    def n_classes(self) -> int:
        return len(self.classes)

    @property
    def model(self):
        return self.__model

    @property
    def model_name(self) -> str:
        return type(self.model).__name__

    @property
    def activation(self):
        return self.__activation

    @property
    def loss(self):
        return self.__loss

    @property
    def optimizer(self):
        return self.__optimizer

    @property
    def lr_scheduler(self):
        return self.__lr_scheduler

    @property
    def trainer(self):
        return self.__trainer

    @property
    def tester(self):
        return self.__tester

    @property
    def path_settings(self) -> dict:
        return self.__config.path_settings

    @property
    def main_dir(self) -> str:
        return self.__config.main_dir

    @property
    def version(self) -> str:
        return self.__config.version

    @property
    def work_dir(self) -> str:
        return self.__config.work_dir

    @property
    def this_dir(self) -> str:
        return self.__config.this_dir

    @property
    def log_path(self) -> str:
        return self.__config.log_path

    @property
    def logger_settings(self) -> dict:
        return self.__config.logger_settings

    @property
    def console_only_flag(self) -> bool:
        return self.__config.console_only_flag

    @property
    def print_timestamp_flag(self) -> bool:
        return self.__config.print_timestamp_flag

    @property
    def loader_settings(self) -> dict:
        return self.__config.loader_settings

    @property
    def model_settings(self):
        return self.__config.model_settings

    @property
    def activation_settings(self):
        return self.__config.activation_settings

    @property
    def activation_name(self) -> str:
        return self.__config.activation_name

    @property
    def loss_settings(self) -> dict:
        return self.__config.loss_settings

    @property
    def loss_name(self) -> str:
        return self.__config.loss_name

    @property
    def optimizer_settings(self) -> dict:
        return self.__config.optimizer_settings

    @property
    def optimizer_name(self) -> str:
        return self.__config.optimizer_name

    @property
    def lr_scheduler_settings(self) -> dict:
        return self.__config.lr_scheduler_settings

    @property
    def lr_scheduler_name(self) -> str:
        return self.__config.lr_scheduler_name

    @property
    def training_settings(self) -> dict:
        return self.__config.training_settings

    @property
    def n_epochs(self) -> int:
        return self.__config.n_epochs

    @property
    def batch_size(self) -> int:
        return self.__config.batch_size

    @property
    def save_net_every_epochs(self) -> int:
        return self.__config.save_net_every_epochs

    @property
    def resume_flag(self) -> bool:
        return self.__config.resume_flag

    @property
    def use_gpu_flag(self) -> bool:
        return self.__config.use_gpu_flag

    @property
    def gpu_index(self) -> int:
        return self.__config.gpu_index

    @property
    def testing_settings(self) -> dict:
        return self.__config.testing_settings

    # noinspection PyProtectedMember
    def set(self, keys, value):
        if not isinstance(keys, tuple):
            raise TypeError("Input 'keys' must be of type 'tuple', "
                            f"got {type(keys)} instead.")
        elif len(keys) != 2:
            raise ValueError("Lenght of input 'keys' must be 2.")

        # checking the super_key existance
        if keys[0] not in self.config.data:
            self.config._data[keys[0]] = {}

        # assigning the key value
        self.config._data[keys[0]][keys[1]] = value

        # running again _validating_config routine
        self.config._validate_config()

    def print_summary(self):
        # summary preamble
        self.logger.print("EXPERIMENT SETTINGS:", style="d", timestamp=False)

        # getting properties list
        prop_list = dir(self)

        # removing some properties from the list
        prop_list.remove("print_summary")
        prop_list.remove("run")
        prop_list.remove("set")

        for current_prop in prop_list:
            if current_prop[0] is not "_":
                self.logger.print("{} = {}".format(
                    current_prop, getattr(self, current_prop)),
                    timestamp=False)

    def run(self):
        # the following try clause contains all the algorithm
        # noinspection PyBroadException
        try:
            # printing the start
            self.logger.print("TORCHEXPERIMENT STARTED", style="ud",
                              timestamp=False)

            # printing a summary on the experiment
            self.print_summary()

            # sending model to the right device
            self.model.to(self.device)

            # training!!
            self.trainer.train()
        except Exception:
            self.logger.print(traceback.format_exc())

        # stopping the logger object
        self.logger.stop()

    def __repr__(self):
        return f"TorchExperiment to train {self.model_name}"


class TorchTrainer(object):
    def __init__(self, experiment: TorchExperiment):
        self.experiment = experiment

        # creating training lists
        self.los_list_train = None
        self.acc_list_train = None
        self.los_list_valid = None
        self.acc_list_valid = None
        self.lr_list = None
        self.cm_list = None

        # creating last loss and accuracy
        self.last_los_train = None
        self.last_acc_train = None
        self.last_los_valid = None
        self.last_acc_valid = None

        # creating best loss and accuracy
        self.best_los_train = None
        self.best_acc_train = None
        self.best_los_valid = None
        self.best_acc_valid = None

        # creating epoch of bests
        self.best_los_epoch_train = None
        self.best_acc_epoch_train = None
        self.best_los_epoch_valid = None
        self.best_acc_epoch_valid = None

    def init_training(self):
        # pre-allocating training lists
        self.los_list_train = []
        self.acc_list_train = []
        self.los_list_valid = []
        self.acc_list_valid = []
        self.lr_list = []
        self.cm_list = []

        # pre-allocating last loss and accuracy
        self.last_los_train = float("inf")
        self.last_acc_train = 0.
        self.last_los_valid = float("inf")
        self.last_acc_valid = 0.

        # pre-allocating best loss and accuracy
        self.best_los_train = float("inf")
        self.best_acc_train = 0.
        self.best_los_valid = float("inf")
        self.best_acc_valid = 0.

        # pre-allocating epoch of bests
        self.best_los_epoch_train = 0
        self.best_acc_epoch_train = 0
        self.best_los_epoch_valid = 0
        self.best_acc_epoch_valid = 0

    # noinspection PyArgumentList
    def loop(self, validation_flag=False):
        # if we are in validation mode
        if validation_flag:
            # printing validation
            self.experiment.logger.print("VALIDATION",
                                         style="ud",
                                         up_extra_lines=1)

            # setting model in validation mode
            self.experiment.model.eval()

            # getting / settings validation variables
            dataset_loader = self.experiment.valid_loader
            n_batches = self.experiment.n_batches_valid
            current_mode = "VALIDATION"
        else:
            # printing training
            self.experiment.logger.print("TRAINING", style="d")

            # setting model in training mode
            self.experiment.model.train()

            # getting / settings training variables
            dataset_loader = self.experiment.train_loader
            n_batches = self.experiment.n_batches_train
            current_mode = "TRAINING"

        # pre-allocating batch_los_list
        batch_los_list = []

        # creating a confusion matrix instance
        confusion_matrix = torchnet.meter.ConfusionMeter(
            self.experiment.n_classes)

        # batch loop
        for batch_index, batch_samples in enumerate(dataset_loader):
            # getting current data and labels
            inputs = batch_samples[0].float()
            labels = batch_samples[1]

            # sending inputs and labels to the right device
            inputs = inputs.to(self.experiment.device)
            labels = labels.to(self.experiment.device)

            # running optimizer
            self.experiment.optimizer.zero_grad()

            # computing output
            outputs = self.experiment.model(inputs)

            # deleting inputs from memory (if on gpu, releasing memory)
            del inputs

            # computing loss
            batch_los = self.experiment.loss(outputs, labels.long())

            # updating batch loss list
            # noinspection PyTypeChecker
            batch_los_list.append(float(batch_los))

            # computing labels_pred
            _, labels_pred = torch.max(outputs, 1)

            # now, both y0 and y_pred are tensors 1 x batch_size.
            # So, we can compute accuracy
            batch_acc = (labels_pred == labels).sum().item() / len(labels)

            # updating confusion matrix
            confusion_matrix.add(labels_pred.int(), labels)

            # backward + optimize if training
            if not validation_flag:
                # back propagating loss
                batch_los.backward()

                # making a step with optimizer
                self.experiment.optimizer.step()

            # printing batch information
            # noinspection PyTypeChecker
            self.experiment.logger.print(
                ">> {} Batch {}/{} | loss: {:.4f}, acc: {:.4f}".format(
                    current_mode,
                    str(batch_index + 1).zfill(len(str(n_batches))),
                    n_batches,
                    float(batch_los),
                    batch_acc
                )
            )

        # running lr_scheduler if in validation
        if validation_flag:
            if type(self.experiment.lr_scheduler).__name__ == \
                    "ReduceLROnPlateau":
                self.experiment.lr_scheduler.step(np.mean(batch_los_list))
            else:
                self.experiment.lr_scheduler.step()

        # getting lr
        lr = None
        for param_group in self.experiment.optimizer.param_groups:
            lr = param_group['lr']

        # getting confusion matrix
        cm = confusion_matrix.conf

        # getting loss
        los = np.mean(batch_los_list)

        # getting accuracy
        acc = sum(cm.diagonal()) / np.sum(cm)

        # filling class attributes
        if validation_flag:
            self.last_los_valid = los
            self.last_acc_valid = acc
            self.los_list_valid.append(los)
            self.acc_list_valid.append(acc)
            self.lr_list.append(lr)
            self.cm_list.append(cm)
        else:
            self.last_los_train = los
            self.last_acc_train = acc
            self.los_list_train.append(los)
            self.acc_list_train.append(acc)

    def train(self):
        # inizializing training
        self.init_training()

        # main loop
        for epoch in range(self.experiment.n_epochs):
            # printing this epoch
            self.experiment.logger.print(
                'EPOCH {}/{}'.format(epoch + 1, self.experiment.n_epochs),
                style="ud", up_extra_lines=1, timestamp=True)

            # running training
            self.loop(validation_flag=False)

            # running validation
            self.loop(validation_flag=True)

            # saving last values for train if best loss
            if self.last_los_train >= self.best_los_train:
                self.best_los_train = self.last_los_train
                self.best_los_epoch_train = epoch

            # saving last values for train if best accuracy
            if self.last_acc_train >= self.best_acc_train:
                self.best_acc_train = self.last_acc_train
                self.best_acc_epoch_train = epoch

            # saving last net
            torch.save(
                self.experiment.model.state_dict(),
                os.path.join(self.experiment.this_dir, 'Net_last_update.pt'))

            # saving net if the epoch X has come
            if (epoch + 1) % self.experiment.save_net_every_epochs == 0:
                torch.save(
                    self.experiment.model.state_dict(),
                    os.path.join(self.experiment.this_dir,
                                 "Net_at_epoch_{}".format(epoch)))

            # saving last net if best loss during validation
            if self.last_los_valid <= self.best_los_valid:
                torch.save(
                    self.experiment.model.state_dict(),
                    os.path.join(self.experiment.this_dir, 'Net_best_loss'))
                self.best_los_valid = self.last_los_valid
                self.best_los_epoch_valid = epoch

            # saving last net if best accuracy during validation
            if self.last_acc_valid >= self.best_acc_valid:
                torch.save(
                    self.experiment.model.state_dict(),
                    os.path.join(self.experiment.this_dir, 'Net_best_acc'))
                self.best_acc_valid = self.last_acc_valid
                self.best_acc_epoch_valid = epoch

            # saving plot
            # self.save_loss_fig(losses_train, 'loss_val',
            # losses_val=losses_val)
            # self.save_loss_fig(accs_train, 'acc_val', losses_val=accs_val)
            # self.save_loss_fig(lr_epoch, 'learning_rate')

            # self.experiment.logger("")
            # print('== TRAIN ==')
            # print('LOSS: {:.4f}'.format(loss_tr))
            # print('ACC:  {:.4f}'.format(acc_tr))
            # print('CM: \n%s' % cm_tr)
            # print('== VALIDATION ==')
            # print('LOSS: {:.4f}'.format(loss_val))
            # print('ACC:  {:.4f}'.format(acc_val))
            # print('CM: \n%s' % cm_val)
            # print(f'Epoch best loss: {epoch_best}')
            # print(f'Epoch best acc:  {epoch_best_acc}')
            # print('\n')

    def __repr__(self):
        return f"TorchTrainer instance to train {self.experiment.model_name}"

    def __str__(self):
        return self.__repr__()


class TorchTester(object):
    def __init__(self, experiment: TorchExperiment):
        self.experiment = experiment

    # TODO: TorchTester

    def __repr__(self):
        return f"TorchTester instance to test {self.experiment.model_name}"

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    # importing MNIST loader and model
    from pydaves.torchsystem.torchloaders import mnist
    from pydaves.torchsystem.torchmodels import Net3Conv1MP2Lin

    # creating a TorchConfig instance
    config = TorchConfig("config_example.yml")

    # creating a TorchExperiment instance
    experiment = TorchExperiment(
        config=config,
        loader_fun=mnist,
        model_class=Net3Conv1MP2Lin
    )

    # running the experiment
    experiment.run()
