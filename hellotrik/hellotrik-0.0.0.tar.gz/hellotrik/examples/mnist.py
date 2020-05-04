from ..kernel import *
import os

def cifar_net():
    l = [   make_convolutional_layer(32, 32, 3, 8, 3, 1, LRELU,1),
            make_maxpool_layer(32, 32, 8, 3, 2),
            make_convolutional_layer(16, 16, 8, 16, 3, 1, LRELU,1),
            make_maxpool_layer(16, 16, 16, 3, 2),
            make_convolutional_layer(8, 8, 16, 32, 3, 1, LRELU,1),
            make_maxpool_layer(8, 8, 32, 3, 2),
            make_convolutional_layer(4, 4, 32, 64, 3, 1, LRELU,1),
            make_maxpool_layer(4, 4, 64, 3, 2),
            make_connected_layer(256, 10, SOFTMAX,1)]
    return make_net(l)

def softmax_model():
    l = [make_connected_layer(784, 10, SOFTMAX)]
    return make_net(l)

def neural_net():
    l = [   make_connected_layer(784, 32, LRELU,1),
            make_connected_layer(32, 10, SOFTMAX,1)]
    return make_net(l)

def convnet():
    l = [   make_convolutional_layer(28, 28,  1,  8, 3, 1, LRELU),
            make_maxpool_layer(28, 28, 8, 3, 2),
            make_convolutional_layer(14, 14,  8, 16, 3, 1, LRELU),
            make_maxpool_layer(14, 14, 16, 3, 2),
            make_convolutional_layer( 7,  7, 16, 32, 3, 1, LRELU),
            make_maxpool_layer(7, 7, 32, 3, 2),
            make_convolutional_layer( 4,  4, 32, 32, 3, 1, LRELU),
            make_connected_layer(512, 10, SOFTMAX)]
    return make_net(l)

def le_net():
    l = [   make_convolutional_layer(28, 28,  1,  8, 3, 1, LRELU,1),
            make_convolutional_layer(28, 28,  8, 16, 3, 2, LRELU,1),
            make_convolutional_layer(14, 14, 16, 32, 3, 2, LRELU,1),
            make_convolutional_layer( 7,  7, 32, 32, 3, 2, LRELU,1),
            make_connected_layer(512, 10, SOFTMAX,1)]
    return make_net(l)
def my_net():
    l = [   make_convolutional_layer(28, 28,  1,  16,5, 1, LRELU,1),
            make_maxpool_layer(28, 28,16,2, 2),
            make_convolutional_layer(14, 14,  16,32, 3, 1, LRELU,1),
            make_maxpool_layer(14,14,32,2, 2),
            make_connected_layer(32*7*7, 10, SOFTMAX,1)]
    return make_net(l)


def train_mnist(iters=92):
	print("loading data...")
	train = load_image_classification_data("mnist/mnist.train", "mnist/mnist.labels")
	test  = load_image_classification_data("mnist/mnist.test", "mnist/mnist.labels")
	print("done")
	print("making model...")
	batch = 128
	rate = .01
	momentum = .9
	decay = .0005

	m = my_net()
	if(os.path.exists("my_net")):
		load_weights(m,"my_net")
	print("training...")
	train_image_classifier(m, train, batch, iters, rate, momentum, decay)
	train_image_classifier(m, train, batch, iters, rate*0.1, momentum, decay)
	train_image_classifier(m, train, batch, iters, rate*0.01, momentum, decay)
	save_weights(m,"my_net")
	print("done")
	print("evaluating model...")
	print("training accuracy: %f", accuracy_net(m, train))
	print("test accuracy:     %f", accuracy_net(m, test))
	free_net(m)
	os.system("@pause")
	
def train_cifar(iters=92):
	print("loading data...")
	train = load_image_classification_data("cifar/cifar.train", "cifar/cifar.labels")
	test  = load_image_classification_data("cifar/cifar.test",  "cifar/cifar.labels")
	print("done")
	
	print("making model...")
	batch = 32
	rate = .01
	momentum = .9
	decay = .005
	m = cifar_net()
	if(os.path.exists("cifa.weights")):
		load_weights(m,"cifa.weights")
	print("training...")
	train_image_classifier(m, train, batch, iters, rate, momentum, decay)
	save_weights(m,"cifa.weights")
	train_image_classifier(m, train, batch, iters, rate*0.1, momentum, decay)
	save_weights(m,"cifa.weights")
	train_image_classifier(m, train, batch, iters, rate*0.01, momentum, decay)
	save_weights(m,"cifa.weights")
	print("done")	
	print("evaluating model...")
	print("training accuracy: %f", accuracy_net(m, train))
	print("test accuracy:     %f", accuracy_net(m, test))

	# How accurate is the fully connected network vs the convnet when they use similar number of operations?
	# Why are you seeing these results? Speculate based on the information you've gathered and what you know about DL and ML.
	# Your answer:
	# 8*27*1024 + 16*72*256 + 32*144*64 + 64*288*16 + 256*10
	# 1108480
	# 221696
	# 3072 input
	# 72 out
	free_net(m)
	os.system("@pause")
