from .tensor import V,as_symbols,element_wise_shape,numpy,reduce,Flip,Rotate90,ReduceMean,Expand,Operator
from ..yu import array_index_traversal, multi_range
from enum import Enum
#compute-------------
class ConvolutionMode(Enum):
	valid = 0
	full = 1
	
convolution_map = {
	'valid': ConvolutionMode.valid,
	'full': ConvolutionMode.full,
}

def __get_convolution_mode_string(mode):
	if isinstance(mode, str):
		if mode in convolution_map:
			return mode
		else:
			raise ValueError('No such convolution mode: {}'.format(mode))
	elif isinstance(mode, ConvolutionMode):
		return mode.name
	else:
		raise ValueError('Invalid mode type: {}'.format(type(mode)))


def basic_convolution_shape(shape_data, shape_kernel, dimension: int, mode: str):
	if mode == 'valid':
		return tuple(shape_data[i] - shape_kernel[i] + 1 for i in range(-dimension, 0))
	elif mode == 'full':
		return tuple(shape_data[i] + shape_kernel[i] - 1 for i in range(-dimension, 0))
	else:
		raise ValueError('Invalid convolution mode: {}'.format(mode))

def __compute_valid_convolution_nd(data, kernel, dimension: int):
	convolution_shape = tuple(data.shape[i] - kernel.shape[i] + 1 for i in range(-1, -dimension - 1, -1))
	list_dimension = reduce(lambda a, b: a * b, convolution_shape)
	data_prefix = data.shape[:-dimension]
	kernel_flat = kernel.ravel()
	data_flat = numpy.zeros(data_prefix + (list_dimension, len(kernel_flat)))
	for i in range(list_dimension):
		tensor_slice_start = [0] * len(kernel.shape)
		tensor_slice = [slice(None)] * len(data.shape)
		tensor_slice_start[-1] = i
		for r in range(-1, -len(kernel.shape) - 1, -1):
			dimension_scale = data.shape[r] - kernel.shape[r] + 1
			if tensor_slice_start[r] >= dimension_scale:
				tensor_slice_start[r + 1] = tensor_slice_start[r] // dimension_scale
				tensor_slice_start[r] %= dimension_scale
			tensor_slice[r] = slice(tensor_slice_start[r], tensor_slice_start[r] + kernel.shape[r])
		sub_convolution_index = (slice(None),) * (len(data.shape) - dimension) + tuple([i, slice(None)])
		data_flat[tuple(sub_convolution_index)] = data[tuple(tensor_slice)].reshape(data_prefix + (reduce(lambda a, b: a * b, kernel.shape),))
	convolution_flat = numpy.matmul(data_flat, numpy.flip(kernel_flat, axis=0))
	convolution_nd = convolution_flat.reshape(data_prefix + convolution_shape)
	return convolution_nd

def __compute_convolution_nd(data, kernel, dimension: int, mode: str):
	mode_string = __get_convolution_mode_string(mode)
	for i in range(dimension):
		if data.shape[i] < kernel.shape[i]:
			raise ValueError('Data shape smaller than kernel shape: {} {}'.format(data.shape, kernel.shape))
	if mode_string == 'valid':
		return __compute_valid_convolution_nd(data, kernel, dimension)
	elif mode_string == 'full':
		data_prefix = data.shape[:-dimension]
		expand_data = numpy.zeros(data_prefix + tuple(data.shape[i] + (kernel.shape[i] - 1) * 2 for i in range(dimension)))
		padding = tuple(kernel.shape[i] - 1 for i in range(dimension))
		expand_data[tuple(slice(None) for _ in data_prefix) + tuple(slice(padding[i], padding[i] + data.shape[i]) for i in range(dimension))] = data
		return __compute_valid_convolution_nd(expand_data, kernel, dimension)
	else:
		raise ValueError('Never reached.')


def compute_convolution_nd(data, kernel, dimension: int, mode=ConvolutionMode.valid, element_wise: bool=False):
	mode_string = __get_convolution_mode_string(mode)
	result = []
	data_prefix_shape = data.shape[:-dimension]
	kernel_prefix_shape = kernel.shape[:-dimension]
	if element_wise:
		final_shape = element_wise_shape(data_prefix_shape, kernel_prefix_shape)[0]
		data = numpy.broadcast_to(data, final_shape + data.shape[-2:])
		kernel = numpy.broadcast_to(kernel, final_shape + kernel.shape[-2:])
		if final_shape:
			for index in array_index_traversal(final_shape):
				result.append(__compute_convolution_nd(data[index], kernel[index], dimension, mode_string))
			return numpy.array(result).reshape(final_shape + result[0].shape)
		else:
			return __compute_convolution_nd(data, kernel, dimension, mode_string)
	else:
		if kernel_prefix_shape:
			final_shape = data_prefix_shape + kernel_prefix_shape + basic_convolution_shape(data.shape[-dimension:], kernel.shape[-dimension:], dimension, mode_string)
			result = numpy.zeros(final_shape)
			for kernel_index in array_index_traversal(kernel_prefix_shape):
				sub_result_index = tuple(slice(None) for _ in data_prefix_shape) + kernel_index + tuple(slice(None) for _ in range(dimension))
				result[sub_result_index] = __compute_convolution_nd(data, kernel[kernel_index], dimension, mode_string)
			return result
		else:
			return __compute_convolution_nd(data, kernel, dimension, mode_string)

def __compute_max_pooling_nd(data, size, step, dimension: int, reference=None):
	for i in range(dimension):
		if data.shape[i] < size[i]:
			raise ValueError('Data shape smaller than size: {} {}'.format(data.shape, size))
	pooling_array = []
	pooling_grid = [range(0, data.shape[i] - size[i] + 1, step[i]) for i in range(dimension)]
	for index in multi_range(pooling_grid):
		sub_slice = [slice(index[i], index[i] + size[i]) for i in range(dimension)]
		if reference is None:
			pooling_array.append(numpy.max(data[tuple(sub_slice)]))
		else:
			max_index = numpy.argmax(reference[sub_slice])
			sub_data = data[sub_slice]
			pooling_array.append(sub_data[numpy.unravel_index(max_index, sub_data.shape)])
	
	return numpy.array(pooling_array).reshape([len(g) for g in pooling_grid])

def compute_max_pooling_nd(data, size, step, dimension: int, reference=None):
	result = []
	data_prefix_shape = data.shape[:-dimension]
	if data_prefix_shape:
		for key in array_index_traversal(data_prefix_shape):
			if reference is None:
				result.append(__compute_max_pooling_nd(data[key], size, step, dimension))
			else:
				result.append(__compute_max_pooling_nd(data[key], size, step, dimension, reference[key]))
		return numpy.array(result).reshape(data_prefix_shape + result[0].shape)
	else:
		return __compute_max_pooling_nd(data, size, step, dimension)


def __compute_max_unpooling_nd(data, pooling, size, step, dimension: int):
	for i in range(dimension):
		if data.shape[i] < size[i]:
			raise ValueError('Data shape smaller than size: {} {}'.format(data.shape, size))
	unpooling_array = numpy.zeros(data.shape)
	unpooling_grid = [range(0, data.shape[i] - size[i] + 1, step[i]) for i in range(dimension)]
	for n, index in enumerate(multi_range(unpooling_grid)):
		sub_slice = tuple([slice(index[i], index[i] + size[i]) for i in range(dimension)])
		max_index = numpy.argmax(data[sub_slice])
		sub_unpooling_array = unpooling_array[sub_slice]
		sub_unpooling_array[numpy.unravel_index(max_index, sub_unpooling_array.shape)] = pooling[numpy.unravel_index(n, pooling.shape)]
	return unpooling_array


def compute_max_unpooling_nd(data, pooling, size, step, dimension: int):
	result = []
	data_prefix_shape = data.shape[:-dimension]
	kernel_prefix_shape = pooling.shape[:-dimension]
	final_shape = element_wise_shape(data_prefix_shape, kernel_prefix_shape)[0]
	data = numpy.broadcast_to(data, final_shape + data.shape[-dimension:])
	pooling = numpy.broadcast_to(pooling, final_shape + pooling.shape[-dimension:])
	if final_shape:
		for key in array_index_traversal(final_shape):
			result.append(__compute_max_unpooling_nd(data[key], pooling[key], size, step, dimension))
		return numpy.array(result).reshape(final_shape + result[0].shape)
	else:
		return __compute_max_unpooling_nd(data, pooling, size, step, dimension)


def __compute_average_pooling_nd(data, size, step, dimension: int):
	for i in range(dimension):
		if data.shape[i] < size[i]:
			raise ValueError('Data shape smaller than size: {} {}'.format(data.shape, size))
	pooling_array = []
	pooling_grid = [range(0, data.shape[i] - size[i] + 1, step[i]) for i in range(dimension)]
	for index in multi_range(pooling_grid):
		pooling_array.append(numpy.mean(data[tuple([slice(index[i], index[i] + size[i]) for i in range(dimension)])]))
	return numpy.array(pooling_array).reshape([len(g) for g in pooling_grid])


def compute_average_pooling_nd(data, size, step, dimension: int):
	result = []
	data_prefix_shape = data.shape[:-dimension]
	if data_prefix_shape:
		for key in array_index_traversal(data_prefix_shape):
			result.append(__compute_average_pooling_nd(data[key], size, step, dimension))
		return numpy.array(result).reshape(data_prefix_shape + result[0].shape)
	else:
		return __compute_average_pooling_nd(data, size, step, dimension)


def __compute_average_unpooling_nd(pooling, size, step, dimension: int, unpooling_size=None):
	if unpooling_size is None:
		unpooling_array = numpy.zeros([size[i] + (pooling.shape[i] - 1) * step[i] for i in range(dimension)])
	else:
		unpooling_array = numpy.zeros(unpooling_size)
	unpooling_grid = [range(0, unpooling_array.shape[i] - size[i] + 1, step[i]) for i in range(dimension)]
	for n, index in enumerate(multi_range(unpooling_grid)):
		sub_slice = tuple(slice(index[i], index[i] + size[i]) for i in range(dimension))
		unpooling_array[sub_slice] += pooling[numpy.unravel_index(n, pooling.shape)]
	return unpooling_array


def compute_average_unpooling_nd(pooling, size, step, dimension: int, unpooling_size=None):
	result = []
	data_prefix_shape = pooling.shape[:-dimension]
	if data_prefix_shape:
		for key in array_index_traversal(data_prefix_shape):
			result.append(__compute_average_unpooling_nd(pooling[key], size, step, dimension, unpooling_size))
		return numpy.array(result).reshape(data_prefix_shape + result[0].shape)
	else:
		return __compute_average_unpooling_nd(pooling, size, step, dimension, unpooling_size)

#function----------

def convolution_nd(data, kernel, dimension: int, mode, element_wise: bool=False):
	return V(operator=ConvolutionND(dimension, mode, element_wise), inputs=as_symbols([data, kernel]))


def convolution_1d(data, kernel, mode, element_wise: bool=False):
	return convolution_nd(data, kernel, 1, mode, element_wise)


def convolution_2d(data, kernel, mode, element_wise: bool=False):
	return convolution_nd(data, kernel, 2, mode, element_wise)


def convolution_3d(data, kernel, mode, element_wise: bool=False):
	return convolution_nd(data, kernel, 3, mode, element_wise)


def max_pooling_nd(data, size: tuple, step: tuple, dimension: int, reference=None):
	if reference is None:
		return V(operator=MaxPoolingND(dimension, size, step), inputs=as_symbols([data]))
	else:
		return V(operator=MaxReferencePoolingND(dimension, size, step), inputs=as_symbols([data, reference]))


def max_pooling_1d(data, size: tuple, step: tuple, reference=None):
	return max_pooling_nd(data, size, step, 1, reference)


def max_pooling_2d(data, size: tuple, step: tuple, reference=None):
	return max_pooling_nd(data, size, step, 2, reference)


def max_pooling_3d(data, size: tuple, step: tuple, reference=None):
	return max_pooling_nd(data, size, step, 3, reference)


def max_unpooling_nd(data, pooling, size: tuple, step: tuple, dimension: int):
	return V(operator=MaxUnpoolingND(dimension, size, step), inputs=as_symbols([data, pooling]))


def max_unpooling_1d(data, pooling, size: tuple, step: tuple):
	return max_unpooling_nd(data, pooling, size, step, 1)


def max_unpooling_2d(data, pooling, size: tuple, step: tuple):
	return max_unpooling_nd(data, pooling, size, step, 2)


def max_unpooling_3d(data, pooling, size: tuple, step: tuple):
	return max_unpooling_nd(data, pooling, size, step, 3)


def average_pooling_nd(data, size: tuple, step: tuple, dimension: int):
	return V(operator=AveragePoolingND(dimension, size, step), inputs=as_symbols([data]))


def average_pooling_1d(data, size: tuple, step: tuple):
	return average_pooling_nd(data, size, step, 1)


def average_pooling_2d(data, size: tuple, step: tuple):
	return average_pooling_nd(data, size, step, 2)


def average_pooling_3d(data, size: tuple, step: tuple):
	return average_pooling_nd(data, size, step, 3)


def average_unpooling_nd(pooling, size: tuple, step: tuple, dimension: int, unpooling_size: int=None):
	return V(operator=AverageUnpoolingND(dimension, size, step, unpooling_size), inputs=as_symbols([pooling]))


def average_unpooling_1d(pooling, size: tuple, step: tuple, unpooling_size: tuple=None):
	return average_unpooling_nd(pooling, size, step, 1, unpooling_size)


def average_unpooling_2d(pooling, size: tuple, step: tuple, unpooling_size: tuple=None):
	return average_unpooling_nd(pooling, size, step, 2, unpooling_size)


def average_unpooling_3d(pooling, size: tuple, step: tuple, unpooling_size: tuple=None):
	return average_unpooling_nd(pooling, size, step, 3, unpooling_size)

#operator---------------
def convolution_nd_shape(shape_data, shape_kernel, dimension, mode):
	prefix_shape = shape_data[:-dimension] + shape_kernel[:-dimension]
	if mode == 'valid' or mode == ConvolutionMode.valid:
		new_shape = prefix_shape + tuple(shape_data[i] - shape_kernel[i] + 1 for i in range(-dimension, 0))
	elif mode == 'full' or mode == ConvolutionMode.full:
		new_shape = prefix_shape + tuple(shape_data[i] + shape_kernel[i] - 1 for i in range(-dimension, 0))
	else:
		raise ValueError('Invalid convolution mode: {}'.format(mode))
	return new_shape, (), ()


def element_wise_convolution_nd_shape(shape_data, shape_kernel, dimension, mode):
	prefix_shape, prefix_broadcast_data, prefix_broadcast_kernel = element_wise_shape(shape_data[:-dimension], shape_kernel[:-dimension])
	if mode == 'valid' or mode == ConvolutionMode.valid:
		new_shape = prefix_shape + tuple(shape_data[i] - shape_kernel[i] + 1 for i in range(-dimension, 0))
	elif mode == 'full' or mode == ConvolutionMode.full:
		new_shape = prefix_shape + tuple(shape_data[i] + shape_kernel[i] - 1 for i in range(-dimension, 0))
	else:
		raise ValueError('Invalid convolution mode: {}'.format(mode))
	return new_shape, prefix_broadcast_data + (0,) * dimension, prefix_broadcast_kernel + (0,) * dimension


def pooling_nd_shape(shape_data, size, step, dimension):
	prefix_shape = shape_data[:-dimension]
	if not isinstance(size, tuple):
		size = (size,)
	if not isinstance(step, tuple):
		step = (step,)
	new_shape = prefix_shape + tuple(len(range(0, shape_data[i] - size[i] + 1, step[i])) for i in range(-dimension, 0))
	return new_shape, ()


def max_unpooling_nd_shape(shape_data, shape_pooling, dimension):
	prefix_shape, prefix_broadcast_data, prefix_broadcast_kernel = element_wise_shape(shape_data[:-dimension], shape_pooling[:-dimension])
	new_shape = prefix_shape + tuple(shape_data[i] for i in range(-dimension, 0))
	return new_shape, prefix_broadcast_data + (0,) * dimension, prefix_broadcast_kernel + (0,) * dimension


def unpooling_nd_shape(shape_pooling, size, step, unpooling_size, dimension):
	prefix_shape, prefix_broadcast_data, prefix_broadcast_kernel = element_wise_shape(shape_pooling[:-dimension], shape_pooling[:-dimension])
	new_shape = prefix_shape + tuple((size[i] + (shape_pooling[i] - 1) * step[i]) if unpooling_size is None else unpooling_size[i] for i in range(-dimension, 0))
	return new_shape, prefix_broadcast_data + (0,) * dimension, prefix_broadcast_kernel + (0,) * dimension


class ConvolutionND(Operator):
	def __init__(self, dimension: int, mode, element_wise: bool=False):
		self.inputs_count = 2
		self.arguments = {'dimension': dimension, 'mode': mode, 'element_wise': element_wise}
		assert dimension > 0

	def f(self, value_data, value_kernel):
		res=compute_convolution_nd(value_data, value_kernel, **self.arguments)
		return res

	def bprop(self, engine, symbol_forward, symbol_data, symbol_kernel):
		forward = engine.bprop(symbol_forward)
		dimension = self.arguments['dimension']
		mode = self.arguments['mode']
		if mode == 'valid' or mode == ConvolutionMode.valid:
			prefix_shape_kernel = engine.shape2(symbol_kernel)[:-dimension]
			prefix_shape_data = engine.shape2(symbol_data)[:-dimension]
			if dimension == 2:
				flip_kernel = symbol_kernel(Rotate90(count=2, axes=(-2, -1)))
			else:
				flip_kernel = symbol_kernel
				for i in range(dimension):
					flip_kernel = flip_kernel(Flip(-1 - i))
			gradient_data = convolution_nd(forward, flip_kernel, dimension, ConvolutionMode.full, True)
			for _ in prefix_shape_kernel:
				gradient_data = gradient_data(ReduceMean(axis=-dimension - 1))
				symbol_data = symbol_data(Expand(-dimension - 1))
			gradient_kernel = convolution_nd(symbol_data, forward, dimension, ConvolutionMode.valid, True)
			for _ in prefix_shape_data:
				gradient_kernel = gradient_kernel(ReduceMean(axis=-dimension - 1 - len(prefix_shape_kernel)))
			return [lambda: gradient_data,
					lambda: gradient_kernel]
		elif mode == 'full' or mode == ConvolutionMode.full:
			prefix_shape_kernel = engine.shape2(symbol_kernel)[:-dimension]
			prefix_shape_data = engine.shape2(symbol_data)[:-dimension]
			if dimension == 2:
				flip_kernel = symbol_kernel(Rotate90(count=2, axes=(-2, -1)))
			else:
				flip_kernel = symbol_kernel
				for i in range(dimension):
					flip_kernel = flip_kernel(Flip(-1 - i))
			gradient_data = convolution_nd(forward, flip_kernel, dimension, ConvolutionMode.valid, True)
			for _ in prefix_shape_kernel:
				gradient_data = gradient_data(ReduceMean(axis=-dimension - 1))
				symbol_data = symbol_data(Expand(-dimension - 1))
			flip_gradient = convolution_nd(forward, symbol_data, dimension, ConvolutionMode.valid, True)
			if dimension == 2:
				gradient_kernel = flip_gradient(Rotate90(count=2, axes=(-2, -1)))
			else:
				gradient_kernel = flip_gradient
				for i in range(dimension):
					gradient_kernel = gradient_kernel(Flip(-1 - i))
			for _ in prefix_shape_data:
				gradient_kernel = gradient_kernel(ReduceMean(axis=-dimension - 1 - len(prefix_shape_kernel)))
			return [lambda: gradient_data,
					lambda: gradient_kernel]
		else:
			raise ValueError('Invalid mode: {}'.format(mode))

	def shape(self, shape_data, shape_kernel):
		if self.arguments['element_wise']:
			return element_wise_convolution_nd_shape(shape_data, shape_kernel, self.arguments['dimension'], self.arguments['mode'])
		else:
			return convolution_nd_shape(shape_data, shape_kernel, self.arguments['dimension'], self.arguments['mode'])


class Convolution1D(ConvolutionND):
	def __init__(self, mode, element_wise: bool=False):
		ConvolutionND.__init__(self, 1, mode, element_wise)


class Convolution2D(ConvolutionND):
	def __init__(self, mode, element_wise: bool=False):
		ConvolutionND.__init__(self, 2, mode, element_wise)


class Convolution3D(ConvolutionND):
	def __init__(self, mode, element_wise: bool=False):
		ConvolutionND.__init__(self, 3, mode, element_wise)


class MaxPoolingND(Operator):
	def __init__(self, dimension: int, size: tuple, step: tuple):
		self.inputs_count = 1
		self.arguments = {'dimension': dimension, 'size': size, 'step': step}

	def f(self, value_data):
		res=compute_max_pooling_nd(value_data, **self.arguments)
		return res

	def bprop(self, engine, symbol_forward, symbol_data):
		forward = engine.bprop(symbol_forward)
		return [lambda: max_unpooling_nd(symbol_data, forward, **self.arguments)]

	def shape(self, shape_data):
		return pooling_nd_shape(shape_data, **self.arguments)


class MaxPooling1D(MaxPoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxPoolingND.__init__(self, 1, size, step)


class MaxPooling2D(MaxPoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxPoolingND.__init__(self, 2, size, step)


class MaxPooling3D(MaxPoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxPoolingND.__init__(self, 3, size, step)


class MaxReferencePoolingND(Operator):
	def __init__(self, dimension: int, size: tuple, step: tuple):
		self.inputs_count = 2
		self.arguments = {'dimension': dimension, 'size': size, 'step': step}

	def f(self, value_data, reference_data):
		res=compute_max_pooling_nd(value_data, reference=reference_data, **self.arguments)
		return res

	def bprop(self, engine, symbol_forward, symbol_data, symbol_reference):
		forward = engine.bprop(symbol_forward)
		return [lambda: max_unpooling_nd(symbol_reference, forward, **self.arguments),
				lambda: max_unpooling_nd(symbol_reference, numpy.ones(engine.shape2(forward)), **self.arguments)]

	def shape(self, shape_data):
		return pooling_nd_shape(shape_data, **self.arguments)


class MaxReferencePooling1D(MaxReferencePoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxReferencePoolingND.__init__(self, 1, size, step)


class MaxReferencePooling2D(MaxReferencePoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxReferencePoolingND.__init__(self, 2, size, step)


class MaxReferencePooling3D(MaxReferencePoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxReferencePoolingND.__init__(self, 3, size, step)


class MaxUnpoolingND(Operator):
	def __init__(self, dimension: int, size: tuple, step: tuple):
		self.inputs_count = 2
		self.arguments = {'dimension': dimension, 'size': size, 'step': step}

	def f(self, value_data, value_pooling):
		res=compute_max_unpooling_nd(value_data, value_pooling, **self.arguments)
		return res

	def bprop(self, engine, symbol_forward, symbol_data, symbol_pooling):
		forward = engine.bprop(symbol_forward)
		return [lambda: max_unpooling_nd(symbol_data, numpy.ones(engine.shape2(symbol_pooling)), **self.arguments),
				lambda: max_pooling_nd(forward, reference=symbol_data, **self.arguments)]

	def shape(self, shape_data, shape_pooling):
		return max_unpooling_nd_shape(shape_data, shape_pooling, self.arguments['dimension'])


class MaxUnpooling1D(MaxUnpoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxUnpoolingND.__init__(self, 1, size, step)


class MaxUnpooling2D(MaxUnpoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxUnpoolingND.__init__(self, 2, size, step)


class MaxUnpooling3D(MaxUnpoolingND):
	def __init__(self, size: tuple, step: tuple):
		MaxUnpoolingND.__init__(self, 3, size, step)


class AveragePoolingND(Operator):
	def __init__(self, dimension: int, size: tuple, step: tuple):
		self.inputs_count = 1
		self.arguments = {'dimension': dimension, 'size': size, 'step': step}

	def f(self, value_data):
		return compute_average_pooling_nd(value_data, **self.arguments)

	def bprop(self, engine, symbol_forward, symbol_data):
		forward = engine.bprop(symbol_forward)
		return [lambda: average_unpooling_nd(forward, unpooling_size=engine.shape2(symbol_data)[-self.arguments['dimension']:], **self.arguments)]

	def shape(self, shape_data):
		return pooling_nd_shape(shape_data, **self.arguments)


class AveragePooling1D(AveragePoolingND):
	def __init__(self, size: tuple, step: tuple):
		AveragePoolingND.__init__(self, 1, size, step)


class AveragePooling2D(AveragePoolingND):
	def __init__(self, size: tuple, step: tuple):
		AveragePoolingND.__init__(self, 2, size, step)


class AveragePooling3D(AveragePoolingND):
	def __init__(self, size: tuple, step: tuple):
		AveragePoolingND.__init__(self, 3, size, step)


class AverageUnpoolingND(Operator):
	def __init__(self, dimension: int, size: tuple, step: tuple, unpooling_size: tuple=None):
		self.inputs_count = 1
		self.arguments = {'dimension': dimension, 'size': size, 'step': step, 'unpooling_size': unpooling_size}

	def f(self, value_pooling):
		return compute_average_unpooling_nd(value_pooling, **self.arguments)

	def bprop(self, engine, symbol_forward, symbol_pooling):
		forward = engine.bprop(symbol_forward)
		return [lambda: average_pooling_nd(forward, **self.arguments)]

	def shape(self, shape_data):
		return unpooling_nd_shape(shape_data, **self.arguments)


class AverageUnpooling1D(AverageUnpoolingND):
	def __init__(self, size: tuple, step: tuple, unpooling_size: tuple=None):
		AverageUnpoolingND.__init__(self, 1, size, step, unpooling_size)


class AverageUnpooling2D(AverageUnpoolingND):
	def __init__(self, size: tuple, step: tuple, unpooling_size: tuple=None):
		AverageUnpoolingND.__init__(self, 2, size, step, unpooling_size)


class AverageUnpooling3D(AverageUnpoolingND):
	def __init__(self, size: tuple, step: tuple, unpooling_size: tuple=None):
		AverageUnpoolingND.__init__(self, 3, size, step, unpooling_size)
