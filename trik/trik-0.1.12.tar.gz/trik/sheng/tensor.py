from functools import reduce
import numpy
#shape-----cs---------
def element_wise_shape(*shape_list):
	broadcast_map = {_shape: [] for _shape in shape_list}
	new_shape = []
	for shape in shape_list:
		if len(shape) > len(new_shape):
			new_shape = list(shape)
	for i in range(-len(new_shape), 0):
		index = len(new_shape) + i
		dimensions = {}
		for shape in shape_list:
			if -i > len(shape):
				broadcast_map[shape].append(-1)
			else:
				broadcast_map[shape].append(0)
				dimensions[shape] = shape[i]
		new_shape[index] = max([_d for _, _d in dimensions.items()])
		for shape, dimension in dimensions.items():
			if dimension != new_shape[index]:
				if dimension == 1:
					broadcast_map[shape][-1] = 1
				else:
					raise ValueError('Can not broadcast these shapes: {}'.format(shape_list))
	return (tuple(new_shape),) + tuple(tuple(broadcast_map[_shape]) for _shape in shape_list)

def matrix_multiply_shape(shape_a, shape_b):
	try:
		if len(shape_a) == 0 or len(shape_b) == 0:
			raise ValueError()
		if len(shape_a) == 1 and len(shape_b) == 1:
			if shape_a[0] == shape_b[0]:
				return (), (), ()
			else:
				raise ValueError()
		if len(shape_a) == 1:
			if shape_a[0] == shape_b[-2]:
				new_shape = list(shape_b)
				del new_shape[-2]
				return tuple(new_shape), (), ()
			else:
				raise ValueError()
		if len(shape_b) == 1:
			if shape_a[-1] == shape_b[0]:
				return shape_a[:-1], (), ()
			else:
				raise ValueError()
		if shape_a[-1] == shape_b[-2]:
			gap = abs(len(shape_a) - len(shape_b))
			if len(shape_a) > len(shape_b):
				if shape_a[gap:-2] != shape_b[:-2]:
					raise ValueError()
				new_shape = list(shape_a)
				broadcast_a = (0,) * len(shape_a)
				broadcast_b = shape_a[:gap] + (0, 0)
			else:
				if shape_b[gap:-2] != shape_a[:-2]:
					raise ValueError()
				new_shape = list(shape_b)
				broadcast_a = shape_b[:gap] + (0, 0)
				broadcast_b = (0,) * len(shape_b)
			new_shape[-1] = shape_b[-1]
			new_shape[-2] = shape_a[-2]
			return tuple(new_shape), broadcast_a, broadcast_b
		else:
			raise ValueError()
	except ValueError:
		raise ValueError('Can not execute matrix multiply with these two shapes: a={}, b={}'.format(shape_a, shape_b))

def reduce_shape(shape_a, axis, invariant):
	if axis is None:
		return (), ()
	else:
		new_shape = list(shape_a)
		if invariant:
			new_shape[axis] = 1
		else:
			del new_shape[axis]
		return tuple(new_shape), ()


def transpose_shape(shape_a, axes):
	if axes is None:
		return tuple(reversed(shape_a)), ()
	else:
		if len(set(axes)) == len(axes):
			if set(axes) == set(range(len(axes))) and len(axes) == len(shape_a):
				new_shape = [0] * len(shape_a)
				for i, d in zip(axes, shape_a):
					new_shape[i] = d
				return tuple(new_shape), ()
			else:
				raise ValueError('Invalid axes for this Shape: shape={}, axes={}'.format(shape_a, axes))
		else:
			raise ValueError('Repeated axis in axes: {}'.format(axes))

def concatenate_shape(axis, *shape_list):
	new_shape = list(shape_list[0])
	shape_len = len(new_shape)
	for shape in shape_list[1:]:
		if len(shape) == len(shape):
			for i in range(shape_len):
				if i == axis:
					new_shape[i] += shape[i]
				else:
					if new_shape[i] != shape[i]:
						raise ValueError('Concatenate shape not match: {}'.format(shape_list))
		else:
			raise ValueError('All shapes must have same dimensions')
	return (tuple(new_shape),) + () * len(shape_list)

def slice_shape(shape_a, slice_list):
	if not isinstance(slice_list, list):
		slice_list = [slice_list]
	new_shape = list(shape_a)
	delete_dimension = 0
	for i, s in enumerate(slice_list):
		index = i - delete_dimension
		if index < len(shape_a):
			if isinstance(s, slice):
				new_shape[index] = len(([0] * shape_a[index])[s])
			elif isinstance(s, int):
				del new_shape[index]
				delete_dimension += 1
			else:
				raise ValueError('Invalid slice type: {}'.format(type(s)))
		else:
			raise ValueError('Shape not match slice: shape={} slice={}'.format(shape_a, slice_list))
	return tuple(new_shape), ()

def rotate90_shape(shape_a, count, axes):
	new_shape = list(shape_a)
	if count % 2 == 0:
		return tuple(new_shape), ()
	else:
		new_shape[axes[0]], new_shape[axes[1]] = new_shape[axes[1]], new_shape[axes[0]]
		return tuple(new_shape), ()

#optim--------
class Optimizer:
	def optimize(self, engine,calculate_function):
		raise ValueError("this is abstract")
	def minimize(self, engine,steps: int=1):
		for _ in range(steps):
			self.optimize(engine,lambda v, g: v - g)
			
class SGD(Optimizer):
	def __init__(self, rate: float=0.01, factor: float=0.9,decay:float=0.0005,consistent: bool=True):
		self.__rate = rate
		self.__factor = factor
		self.__decay=decay
		self.__consistent = consistent
		self.__old_gradient_map = {}
		self.__gradient_engine = V()

	def __repr__(self):
		return '{}(rate={}, consistent={})'.format(self.__class__.__name__, self.__rate, self.__consistent)

	def optimize(self, engine, calculate_function):
		variables = engine.variables
		for variable in variables:
			value_cache = self.__gradient_engine.value_cache
			self.__gradient_engine = engine.bprop(variable)
			self.__gradient_engine.set_bind(engine.get_bind())
			if self.__consistent:
				self.__gradient_engine.value_cache = value_cache
			momentum = self.__gradient_engine.val() + self.__factor * self.__old_gradient_map.get(variable, 0)-self.__decay*variable.value
			self.__old_gradient_map[variable] = momentum
			variable.value = calculate_function(variable.value, self.__rate * momentum)
		engine.modified()
		self.__gradient_engine.modified()


class Adam(Optimizer):
	def __init__(self, rate: float, decay: float=0.9, square_decay: float=0.999, consistent: bool=True):
		self.__rate = rate
		self.__decay = decay
		self.__square_decay = square_decay
		self.__consistent = consistent
		self.__gradient_engine = V()
		self.__estimation_map = {}
		self.__square_estimation_map = {}
		self.__step = 1

	def __repr__(self):
		return '{}(rate={}, decay={}, square_decay={}, consistent={})'.format(self.__class__.__name__, self.__rate, self.__decay, self.__square_decay, self.__consistent)

	def optimize(self, engine, calculate_function):
		
		variables = engine.variables
		for variable in variables:
			
			value_cache = self.__gradient_engine.value_cache
			self.__gradient_engine = engine.bprop(variable)
			self.__gradient_engine.bind=engine.bind
			if self.__consistent:
				self.__gradient_engine.value_cache = value_cache
			current_gradient = self.__gradient_engine.val()
			self.__estimation_map.setdefault(variable, 0)
			self.__square_estimation_map.setdefault(variable, 0)
			self.__estimation_map[variable] = self.__decay * self.__estimation_map[variable] + (1 - self.__decay) * current_gradient
			self.__square_estimation_map[variable] = self.__square_decay * self.__square_estimation_map[variable] + (1 - self.__square_decay) * current_gradient ** 2
			estimation = self.__estimation_map[variable] / (1 - self.__decay ** self.__step)
			square_estimation = self.__square_estimation_map[variable] / (1 - self.__square_decay ** self.__step)
			self.__step += 1
			regularization_value = estimation / (square_estimation + 1e-8) ** 0.5
			variable.value = calculate_function(variable.value, self.__rate * regularization_value)
		engine.modified()
		self.__gradient_engine.modified()


#tensor------------
class VCategory:
	variable = 0
	constant = 1
	placeholder = 2
	operator = 3
	
class V:
	def __init__(self, value=None, shape: tuple=None, name: str=None, operator=None, inputs=None, category: VCategory=None):
		self.__name = None
		self.__input = []
		self.__operator = None
		self.__output = []
		self.__value = None
		self.__shape = None
		self.__scalar = False
		self.__category = None
		# for engin
		self.__variables = set()
		self.__grad_table = {}
		self.__shape2 = {}
		self.__broadcast = {}
		self.__bind ={}
		self.__value_cache = {}
		if isinstance(value, V):
			self.__set_name(value.name)
			self.__set_value(value.value)
			self.__set_shape(value.shape)
			for _input in value.input:
				self.__add_input(_input.clone())
			self.__set_operator(value.__operator)
			for _output in value.output:
				self.__add_output(_output.clone())
			self.__set_category(value.category)
		else:
			self.symbolic_compute(operator, inputs)
			self.__set_value(value)
			self.__set_category(category)
			self.__set_shape(shape)
			self.__set_name(name)
	def __call__(self,op,*arg):
		arg=[self,]+list(arg)
		res=V(operator=op,inputs=as_symbols(arg))
		simp.simplify(res)
		return res
	def __repr__(self):
		if self.__operator is None:
			return self.__name
		else:
			if self.__operator.operator_sign is None:
				arguments = list(map(str, self.input))
				arguments += ['{}={}'.format(k, '\'' + v + '\'' if isinstance(v, str) else v) for k, v in self.__operator.arguments.items()]
				return '{}({})'.format(self.__operator.__class__.__name__, ', '.join(arguments))
			else:
				if len(self.input) < 2:
					return '{}{}'.format(self.__operator.operator_sign, self.input[0])
				else:
					return '({} {} {})'.format(self.input[0], self.__operator.operator_sign, self.input[1])

	def __get_name(self):
		return self.__name

	def __set_name(self, name: str):
		if name is None:
			if self.__value is None:
				self.__name = self.__class__.__name__
			else:
				if self.is_scalar():
					self.__name = str(self.__value)
				else:
					self.__name = '{}{}'.format(self.__class__.__name__, self.__value.shape)
		else:
			self.__name = name

	name = property(__get_name, __set_name)

	def __get_category(self):
		return self.__category

	def __set_category(self, category: VCategory):
		if category is None:
			if self.__category is None:
				self.__category = VCategory.variable
		else:
			if self.__category == VCategory.operator:
				if category != VCategory.operator:
					raise ValueError('Can not change category of Operator V.')
			if category == VCategory.variable:
				self.__category = category
			elif category == VCategory.constant:
				self.__category = category
				if self.__value is None:
					raise ValueError('constant V must have value.')
			elif category == VCategory.placeholder:
				self.__category = category
				if self.__value is not None:
					self.__set_shape(self.__value.shape)
			elif category == VCategory.operator:
				if self.operator is not None:
					self.__category = category
				else:
					raise ValueError('Can not convert other V to Operator V.')
			else:
				raise ValueError('Invalid category: {}'.format(category))

	category = property(__get_category, __set_category)

	def __get_value(self):
		return self.__value

	def __set_value(self, tensor):
		if tensor is not None:
			if self.__category == VCategory.constant:
				raise ValueError('Can not change value for constant.')
			else:
				if self.__operator is None:
					self.__value = numpy.array(tensor, dtype=float)
					self.__scalar = len(self.value.shape) == 0
					self.__set_category(VCategory.variable)
				else:
					raise ValueError('Can not assign value for Operator V.')

	value = property(__get_value, __set_value)

	def __get_shape(self):
		if self.__category == VCategory.placeholder:
			return self.__shape
		else:
			if self.__operator is None:
				return self.__value.shape
			else:
				return self.shape2(self)
#                 raise ValueError('Operator V has no shape.')

	def __set_shape(self, shape: tuple):
		if shape is not None:
			if self.__category == VCategory.placeholder:
				self.__shape = shape
			else:
				raise ValueError('Only Placeholder can set shape.')

	shape = property(__get_shape, __set_shape)

	def __get_operator(self):
		return self.__operator

	def __set_operator(self, operator):
		if operator is not None:
			if isinstance(operator, Operator):
				self.__operator = operator
			else:
				raise ValueError('Operator must be Operator.')

	operator = property(__get_operator, __set_operator)

	def __get_input(self):
		return self.__input

	input = property(__get_input)

	def __add_input(self, symbol):
		if isinstance(symbol, V):
			self.__input.append(symbol)
		else:
			raise ValueError('Input must be V.')

	def __get_output(self):
		return self.__output

	output = property(__get_output)

	def __add_output(self, symbol):
		if isinstance(symbol, V):
			self.__output.append(symbol)
		else:
			raise ValueError('Output must be V.')

	def symbolic_compute(self, operator, inputs):
		if operator is not None and inputs:
			self.__set_operator(operator)
			inputs_count = operator.inputs_count
			if inputs_count is None:
				inputs_count = len(inputs)
			self.__input = []
			self.__scalar = True
			for symbol in inputs[:inputs_count]:
				if isinstance(symbol, V):
					if not symbol.is_scalar():
						self.__scalar = False
					self.__add_input(symbol)
					symbol.__add_output(self)
				else:
					raise ValueError('Input must be V.')
			self.__set_category(VCategory.operator)

	def remove_input(self, symbol):
		new_input = []
		find_input = None
		for each_input in self.__input:
			if hash(each_input) != hash(symbol):
				new_input.append(each_input)
			else:
				find_input = each_input
		self.__input = new_input
		if find_input is not None:
			find_input.remove_output(self)

	def remove_output(self, symbol):
		new_output = []
		find_output = None
		for each_output in self.__output:
			if hash(each_output) != hash(symbol):
				new_output.append(each_output)
			else:
				find_output = each_output
		self.__output = new_output
		if find_output is not None:
			find_output.remove_input(self)

	def clear_input(self):
		for symbol in set(self.__input):
			symbol.remove_output(self)
		self.__input = []

	def clear_output(self):
		for symbol in set(self.__output):
			symbol.remove_input(self)
		self.__output = []

	def clear_operator(self):
		self.clear_input()
		self.__operator = None
		self.__category = VCategory.variable

	def destroy(self):
		self.clear_input()
		self.clear_output()
		self.__value = None
		self.__operator = None

	def is_scalar(self):
		return self.__scalar
	def is_constant(self):
		return self.__category == VCategory.constant
	def is_variable(self):
		return self.__category == VCategory.variable
	def is_placeholder(self):
		return self.__category == VCategory.placeholder
	def is_operator(self):
		return self.__category == VCategory.operator

	def symbolic_hash(self):
		if self.is_operator():
			inputs_symbolic_hash = [each_input.symbolic_hash() for each_input in self.input]
			return '{}({})'.format(self.operator.__class__.__name__, ','.join(inputs_symbolic_hash))
		else:
			return str(hash(self))

	def __hash__(self):
		return id(self)
	def __getitem__(self, item):
		return slice_select(self, item)
	def __setitem__(self, key, value):
		return slice_assign(self, value, key)
	
	def clear(self):
		self.__grad_table = {}
		self.__shape2 = {}
		self.__broadcast = {}
		self.__value_cache = {}
	def get_variables(self):
		return self.__variables

	def set_variables(self, symbol):
		if symbol is None:
			symbol = set()
			symbol_set ={self} 
			while len(symbol_set):
				any_symbol = symbol_set.pop()
				if any_symbol.is_variable():
					symbol.add(any_symbol)
				elif any_symbol.is_operator():
					symbol_set |= set(any_symbol.input)
		old_variables = set(self.__variables)
		if isinstance(symbol, V):
			symbols = {symbol}
		else:
			symbols = set(symbol)
		for symbol in symbols:
			if isinstance(symbol, V) and not symbol.is_operator():
				self.__variables.add(symbol)
			else:
				raise ValueError('Variable must be V.')
		unused_variables = old_variables - self.__variables
		for variable in unused_variables:
			if variable in self.__grad_table:
				del self.__grad_table[variable]

	variables = property(get_variables, set_variables)

	def get_bind(self,):
		return self.__bind

	def set_bind(self,bind_data: dict):
		old_bind = self.__bind
		self.__bind ={}
		need_clear = False
		for s, d in bind_data.items():
			if s.category == VCategory.constant:
				raise ValueError('Can not bind data for constant.')
			d_array = numpy.array(d)
			if s in old_bind:
				if old_bind[s].shape != d_array.shape:
					need_clear = True
			else:
				need_clear = True
			self.__bind[s] = d_array
		if need_clear:
			self.clear()
	bind=property(get_bind,set_bind)
	def get_value_cache(self):
		return self.__value_cache

	def set_value_cache(self, value_cache: dict):
		self.__value_cache = value_cache

	value_cache = property(get_value_cache, set_value_cache)

	def modified(self):
		self.__value_cache = {}

	def __compute_value(self,symbol):
		if not isinstance(symbol,V):raise ValueError('symbol Must be V')
		if not symbol.is_operator():
			if symbol in self.__bind:
				return numpy.array(self.__bind[symbol])
			else:
				if symbol.value is None or symbol.is_placeholder():
					raise ValueError('V must bind data: {}'.format(symbol))
				else:
					return symbol.value
		else:
			if symbol in self.__value_cache:
				return self.__value_cache[symbol]
			else:
				compute_inputs =[self.__compute_value(_s) for _s in symbol.input]
				symbol_value = symbol.operator.f(*compute_inputs)
				self.__value_cache[symbol] =symbol_value
				return symbol_value

	def __build_grad(self, variable):
		if not isinstance(variable,V):
			raise ValueError('variable must be V')
		if hash(self) == hash(variable):
			self.__grad_table[variable] = constant(1)(Broadcast(self.shape2(self)))
			return
		current_operator = None
		index = -1
		for forward in variable.output:
			if forward.is_constant():continue
			if self.bprop(forward) is not None:
				if current_operator != forward.operator:
					current_operator = forward.operator
					index = -1
				gradients = forward.operator.bprop(self, forward, *forward.input)
				for i, _variable in enumerate(forward.input, start=index + 1):
					if hash(_variable) == hash(variable):
						index = i
						break
				if gradients:current_gradient=gradients[index]()
				else:current_gradient=constant(0)
				if forward.operator.auto_reduce:
					invariant = 0
					for i, d in enumerate(self.broadcast(variable, forward)):
						if d > 0:
							current_gradient = current_gradient(ReduceSum(axis=i + invariant, invariant=True))
						elif d < 0:
							current_gradient = current_gradient(ReduceSum(axis=i + invariant, invariant=False))
							invariant -= 1
				if variable not in self.__grad_table:
					self.__grad_table[variable] = current_gradient
				else:
					self.__grad_table[variable] = self.__grad_table[variable](Plus(),current_gradient)
		if variable in self.__grad_table:
			simp.simplify(self.__grad_table[variable])

	def __compute_shape(self, symbol):
		if not isinstance(symbol,V):
			raise ValueError('symbol must be V')
		if not symbol.is_operator():
			if symbol in self.__bind:
				self.__shape2[symbol] = self.__bind[symbol].shape
			else:
				if symbol.shape is None:
					raise ValueError('Placeholder must bind data or set shape: {}'.format(symbol))
				else:
					self.__shape2[symbol] = symbol.shape
		else:
			shape_broadcasts = symbol.operator.shape(*[self.shape2(s) for s in symbol.input])
			shape = shape_broadcasts[0]
			broadcasts = shape_broadcasts[1:]
			self.__shape2[symbol] = shape
			for input_symbol, input_broadcast in zip(symbol.input, broadcasts):
				if sum([abs(d) for d in input_broadcast]) > 0:
					self.__broadcast.setdefault(input_symbol, {})
					self.__broadcast[input_symbol].setdefault(symbol, {})
					self.__broadcast[input_symbol][symbol] = input_broadcast

	def val(self):
		return self.__compute_value(self)

	def differentiate(self):
		for variable in self.__variables:
			if variable not in self.__grad_table:
				self.__build_grad(variable)

	def bprop(self, variable):
		if not isinstance(variable,V):
			raise ValueError('variable must be V')
		if variable not in self.__grad_table:
			self.__build_grad(variable)
		return self.__grad_table.get(variable, None)

	def shape2(self, variable):
		if not isinstance(variable,V):
			raise ValueError('variable must be V')
		if variable not in self.__shape2:
			self.__compute_shape(variable)
		return self.__shape2.get(variable, None)

	def broadcast(self, from_variable, to_variable):
		if not isinstance(from_variable,V) or not isinstance(to_variable,V):
			raise ValueError('variable must be V')
		if from_variable not in self.__broadcast:
			self.__compute_shape(from_variable)
		if from_variable not in self.__broadcast:
			return ()
		else:
			if to_variable not in self.__broadcast[from_variable]:
				return ()
			else:
				return self.__broadcast[from_variable][to_variable]
	
def constant(value=None, shape: tuple=None, name: str=None, operator=None, inputs=None):
	return V(value, shape, name, operator, inputs, VCategory.constant)
def variable(value=None, shape: tuple=None, name: str=None, operator=None, inputs=None):
	return V(value, shape, name, operator, inputs, VCategory.variable)
def placeholder(value=None, shape: tuple=None, name: str=None, operator=None, inputs=None):
	return V(value, shape, name, operator, inputs, VCategory.placeholder)

def as_symbol(thing):
	if isinstance(thing, V):
		return thing
	else:
		return constant(thing)
def as_symbols(things):
	return list(map(as_symbol, things))
def slice_assign(a, b, slice_tuple):
	return V(operator=SliceAssign(slice_tuple), inputs=as_symbols([a, b]))  
def slice_select(a, slice_tuple):
	return V(operator=SliceSelect(slice_tuple), inputs=as_symbols([a]))

#operator---------
class Operator:
	operator_sign = None
	inputs_count = None
	auto_reduce = True
	arguments = {}

	def __repr__(self):
		return '{}({})'.format(self.__class__.__name__, ', '.join(['{}={}'.format(key, value) for key, value in self.arguments.items()]))

	def f(self, *args, **kwargs):
		raise ValueError("this is abstract")

	def bprop(self, *args, **kwargs):
		raise ValueError("this is abstract")

	def shape(self, *args, **kwargs):
		raise ValueError("this is abstract")

class Neg(Operator):
	def __init__(self):
		self.operator_sign = '-'
		self.inputs_count = 1

	def f(self, value_a):
		return -value_a

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Neg())]

	def shape(self, shape_a):
		return shape_a, ()


class Abs(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.absolute(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),0), 1, -1])))]

	def shape(self, shape_a):
		return shape_a, ()


class Plus(Operator):
	def __init__(self):
		self.operator_sign = '+'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return value_a + value_b

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1),
				lambda: forward(Mul(),1)]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Sub(Operator):
	def __init__(self):
		self.operator_sign = '-'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return value_a - value_b

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1),
				lambda: forward(Mul(),-1)]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Mul(Operator):
	def __init__(self):
		self.operator_sign = '*'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return value_a * value_b

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),symbol_b),
				lambda: forward(Mul(),symbol_a)]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Div(Operator):
	def __init__(self):
		self.operator_sign = '/'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return value_a / value_b

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),symbol_b),
				lambda: forward(Mul(),-1)(Mul(),symbol_a)(Div(),symbol_b(Pow(),2))]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class MM(Operator):
	def __init__(self):
		self.operator_sign = '@'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		if len(value_a.shape) == 0 or len(value_b.shape) == 0:
			return value_a * value_b
		else:
			return value_a @ value_b

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		shape_a = engine.shape2(symbol_a)
		shape_b = engine.shape2(symbol_b)
		if len(shape_a) >= 2:
			axes_a = tuple(range(len(shape_a) - 2)) + (-1, -2)
		else:
			axes_a = None
		if len(shape_b) >= 2:
			axes_b = tuple(range(len(shape_b) - 2)) + (-1, -2)
		else:
			axes_b = None
		return [lambda: forward(MM(),symbol_b(T(axes=axes_a))),
				lambda: symbol_a(T(axes=axes_b))(MM(),forward)]

	def shape(self, shape_a, shape_b):
		return matrix_multiply_shape(shape_a, shape_b)


class T(Operator):
	def __init__(self, axes=None):
		self.inputs_count = 1
		self.arguments = {'axes': axes}

	def f(self, value_a):
		return numpy.transpose(value_a, axes=self.arguments['axes'])

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(T(axes=self.arguments['axes']))]

	def shape(self, shape_a):
		return transpose_shape(shape_a, self.arguments['axes'])


class ReduceSum(Operator):
	def __init__(self, axis: int=None, invariant: bool=False):
		self.inputs_count = 1
		self.arguments = {'axis': axis, 'invariant': invariant}

	def f(self, value_a):
		return numpy.sum(value_a, axis=self.arguments['axis'], keepdims=self.arguments['invariant'])

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		shape_a = engine.shape2(symbol_a)
		axis = self.arguments['axis']
		if axis:
			return [lambda: forward(Expand(axis))(Broadcast(shape_a))]
		else:
			return [lambda: forward(Broadcast(shape_a))]

	def shape(self, shape_a):
		return reduce_shape(shape_a, **self.arguments)


class ReduceMean(Operator):
	def __init__(self, axis: int=None, invariant: bool=False):
		self.inputs_count = 1
		self.arguments = {'axis': axis, 'invariant': invariant}

	def f(self, value_a):
		return numpy.mean(value_a, axis=self.arguments['axis'], keepdims=self.arguments['invariant'])

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		shape_a = engine.shape2(symbol_a)
		axis = self.arguments['axis']
		if axis:
			return [lambda: forward(Expand(axis))(Broadcast(shape_a))(Div(),shape_a[axis])]
		else:
			return [lambda: forward(Broadcast(shape_a))( Div(),reduce(lambda x, y: x * y, shape_a, 1))]

	def shape(self, shape_a):
		return reduce_shape(shape_a, **self.arguments)


class Expand(Operator):
	def __init__(self, axis: int):
		self.inputs_count = 1
		self.arguments = {'axis': axis}

	def f(self, value_a):
		return numpy.expand_dims(value_a, **self.arguments)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(ReduceMean(**self.arguments))]

	def shape(self, shape_a):
		new_shape = list(shape_a)
		new_shape.insert(self.arguments['axis'], 1)
		broadcast_a = [0] * len(shape_a)
		broadcast_a.insert(self.arguments['axis'], 1)
		return tuple(new_shape), tuple(broadcast_a)


class Broadcast(Operator):
	def __init__(self, shape):
		self.inputs_count = 1
		self.arguments = {'shape': shape}

	def f(self, value_a):
		if len(value_a.shape) == 1 and len(self.arguments['shape']) > 1:
			if value_a.shape[0] == self.arguments['shape'][0]:
				value_a = value_a.reshape((value_a.shape[0], 1))
		return numpy.broadcast_to(value_a, **self.arguments)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward]

	def shape(self, shape_a):
		return element_wise_shape(shape_a, self.arguments['shape'])[:2]


class Pow(Operator):
	def __init__(self):
		self.operator_sign = '**'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.power(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),symbol_b)(Mul(),symbol_a(Pow(),symbol_b(Sub(),1))),
				lambda: forward(Mul(),symbol_a(Pow(),symbol_b))(Mul(),symbol_a(Log()))]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Log(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.log(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),symbol_a)]

	def shape(self, shape_a):
		return shape_a, ()


class Where(Operator):
	def __init__(self):
		self.inputs_count = 3

	def f(self, value_condition, value_a, value_b):
		return numpy.array(numpy.where(value_condition, value_a, value_b), dtype=float)

	def bprop(self, engine, symbol_forward, symbol_condition, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		
		return [lambda: constant(0),
				lambda: forward(Mul(),V(oprator=Where(),inputs=as_symbols([symbol_condition, forward, 0]))),
				lambda: forward(Mul(),V(oprator=Where(),inputs=as_symbols([symbol_condition, 0,forward])))]

	def shape(self, shape_condition, shape_a, shape_b):
		return element_wise_shape(shape_condition, shape_a, shape_b)


class Eq(Operator):
	def __init__(self):
		self.operator_sign = '=='
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.equal(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda: V(operator=Where(),inputs=as_symbols([symbol_a(Eq(),symbol_b), forward, 0])),
				lambda: V(operator=Where(),inputs=as_symbols([symbol_a(Eq(),symbol_b), forward, 0]))]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class NEq(Operator):
	def __init__(self):
		self.operator_sign = '!='
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.not_equal(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(NEq(),symbol_b), forward,0])),
				lambda:V(operator=Where(),inputs=as_symbols([symbol_a(NEq(),symbol_b), forward,0])),]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Lt(Operator):
	def __init__(self):
		self.operator_sign = '<'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.less(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),
				lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class LEq(Operator):
	def __init__(self):
		self.operator_sign = '<='
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.less_equal(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(LEq(),symbol_b), forward, 0])),
				lambda:V(operator=Where(),inputs=as_symbols([symbol_a(LEq(),symbol_b), forward, 0])),]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Gt(Operator):
	def __init__(self):
		self.operator_sign = '>'
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.greater(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),
				lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class GEq(Operator):
	def __init__(self):
		self.operator_sign = '>='
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.greater_equal(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(GEq(),symbol_b), forward, 0])),
				lambda:V(operator=Where(),inputs=as_symbols([symbol_a(GEq(),symbol_b), forward, 0])),]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Max(Operator):
	def __init__(self):
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.maximum(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),
				lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Min(Operator):
	def __init__(self):
		self.inputs_count = 2

	def f(self, value_a, value_b):
		return numpy.minimum(value_a, value_b)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),
				lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),]

	def shape(self, shape_a, shape_b):
		return element_wise_shape(shape_a, shape_b)


class Sin(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.sin(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),symbol_a(Cos()))]

	def shape(self, shape_a):
		return shape_a, ()


class Cos(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.cos(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),symbol_a(Sin())(Neg()))]

	def shape(self, shape_a):
		return shape_a, ()


class Tan(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.tan(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),symbol_a(Cos())(Pow(),2))]

	def shape(self, shape_a):
		return shape_a, ()


class ArcSin(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.arcsin(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),constant(1)(Sub(),symbol_a(Pow(),2))(Pow(),0.5))]

	def shape(self, shape_a):
		return shape_a, ()


class ArcCos(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.arccos(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),-1)(Div(),constant(1)(Sub(),symbol_a(Pow(),constant(2)))(Pow(),0.5))]

	def shape(self, shape_a):
		return shape_a, ()


class ArcTan(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.arctan(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),constant(1)(Plus(),symbol_a(Pow(),2)))]

	def shape(self, shape_a):
		return shape_a, ()


class Sinh(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.sinh(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),symbol_a(Cosh()))]

	def shape(self, shape_a):
		return shape_a, ()


class Cosh(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.cosh(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),symbol_a(Sinh()))]

	def shape(self, shape_a):
		return shape_a, ()


class Tanh(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.tanh(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),constant(1)(Sub(),symbol_a(Tanh())(Pow(),2)))]

	def shape(self, shape_a):
		return shape_a, ()


class ArcSinh(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.arcsinh(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),symbol_a(Pow(),2)(Plus(),1)(Pow(),0.5))]

	def shape(self, shape_a):
		return shape_a, ()


class ArcCosh(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.arccosh(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),symbol_a(Pow(),2)(Sub(),1)(Pow(),0.5))]

	def shape(self, shape_a):
		return shape_a, ()


class ArcTanh(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.arctanh(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),1)(Div(),constant(1)(Sub(),symbol_a(Pow(),2)))]

	def shape(self, shape_a):
		return shape_a, ()


class Exp(Operator):
	def __init__(self):
		self.inputs_count = 1

	def f(self, value_a):
		return numpy.exp(value_a)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Mul(),symbol_a(Exp()))]

	def shape(self, shape_a):
		return shape_a, ()


class SliceAssign(Operator):
	def __init__(self, slice_tuple):
		self.inputs_count = 2
		self.arguments = {'slice_tuple': slice_tuple}

	def f(self, value_a, value_b):
		value_a[self.arguments['slice_tuple']] = value_b
		return value_a

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		slice_tuple = self.arguments['slice_tuple']
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(SliceAssign(slice_tuple),numpy.zeros(engine.shape2(symbol_b))),
				lambda: forward[slice_tuple]]

	def shape(self, shape_a, shape_b):
		shape_select = slice_shape(shape_a, self.arguments['slice_tuple'])[0]
		shape_package = element_wise_shape(shape_select, shape_b)
		if shape_package[0] != shape_select:
			raise ValueError('Can not assign: {} to {} with {}'.format(shape_b, shape_a, self.arguments['slice_tuple']))
		return shape_a, (), shape_package[2]


class SliceSelect(Operator):
	def __init__(self, slice_tuple):
		self.inputs_count = 1
		self.arguments = {'slice_tuple': slice_tuple}

	def f(self, value_a):
		return value_a[self.arguments['slice_tuple']]

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		symbol_zero = constant(numpy.zeros(engine.shape2(symbol_a)))
		return [lambda: symbol_zero(SliceAssign(forward), self.arguments['slice_tuple'])]

	def shape(self, shape_a):
		return slice_shape(shape_a, self.arguments['slice_tuple'])


class Concatenate(Operator):
	def __init__(self, axis: int=0):
		self.inputs_count = 2
		self.arguments = {'axis': axis}

	def f(self, value_a, value_b):
		return numpy.concatenate((value_a, value_b), **self.arguments)

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		split_dimension = engine.shape2(symbol_a)[self.arguments['axis']]
		total_dimension = engine.shape2(symbol_forward)[self.arguments['axis']]
		return [lambda: forward[[slice(None)] * self.arguments['axis'] + [slice(0, split_dimension)]],
				lambda: forward[[slice(None)] * self.arguments['axis'] + [slice(split_dimension, total_dimension)]]]

	def shape(self, *shapes):
		return concatenate_shape(self.arguments['axis'], *shapes)


class Rotate90(Operator):
	def __init__(self, count: int=1, axes: tuple=None):
		self.inputs_count = 1
		self.arguments = {'count': count, 'axes': axes}

	def f(self, value_a):
		return numpy.rot90(value_a, k=self.arguments['count'], axes=self.arguments['axes'])

	def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Rotate90(-self.arguments['count'] & 3, self.arguments['axes']))]

	def shape(self, shape_a):
		return rotate90_shape(shape_a, **self.arguments)


class Flip(Operator):
	def __init__(self, axis: int):
		self.inputs_count = 1
		self.arguments = {'axis': axis}

	def f(self, value_a):
		return numpy.flip(value_a, self.arguments['axis'])

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Flip(self.arguments['axis']))]

	def shape(self, shape_a):
		return shape_a, ()


class Reshape(Operator):
	def __init__(self, shape):
		self.inputs_count = 1
		self.arguments = {'shape': shape}

	def f(self, value_a):
		return numpy.reshape(value_a, self.arguments['shape'])

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Reshape(engine.shape2(symbol_a)))]

	def shape(self, shape_a):
		return self.arguments['shape'], ()


class Spread(Operator):
	def __init__(self, position):
		self.inputs_count = 1
		self.arguments = {'position': position}

	def f(self, value_a):
		shape_a = value_a.shape
		spread_dimension = numpy.prod(shape_a[self.arguments['position']:])#reduce(lambda a, b: a * b, shape_a[self.arguments['position']:])
		new_shape = shape_a[:self.arguments['position']] + (spread_dimension,)
		return numpy.reshape(value_a, new_shape)

	def bprop(self, engine, symbol_forward, symbol_a):
		forward = engine.bprop(symbol_forward)
		return [lambda: forward(Reshape(engine.shape2(symbol_a)))]

	def shape(self, shape_a):
		spread_dimension = reduce(lambda a, b: a * b, shape_a[self.arguments['position']:])
		new_shape = shape_a[:self.arguments['position']] + (spread_dimension,)
		return new_shape, ()


# def negative(a):
#     return V(operator=Neg(), inputs=as_symbols([a]))
#  
#  
# def absolute(a):
#     return V(operator=Abs(), inputs=as_symbols([a]))
#  
#  
# def plus(a, b):
#     return V(operator=Plus(), inputs=as_symbols([a, b]))
#  
#  
# def subtract(a, b):
#     return V(operator=Sub(), inputs=as_symbols([a, b]))
#  
#  
# def multiply(a, b):
#     return V(operator=Mul(), inputs=as_symbols([a, b]))
#  
#  
# def divide(a, b):
#     return V(operator=Div(), inputs=as_symbols([a, b]))
#  
#  
# def matrix_multiply(a, b):
#     return V(operator=MM(), inputs=as_symbols([a, b]))
#  
#  
# def power(a, b):
#     return V(operator=Pow(), inputs=as_symbols([a, b]))
#  
#  
# def log(a):
#     return V(operator=Log(), inputs=as_symbols([a]))
#  
#  
# def transpose(a, axes: tuple=None):
#     return V(operator=T(axes), inputs=as_symbols([a]))
#  
#  
# def reduce_sum(a, axis: int=None, invariant=False):
#     return V(operator=ReduceSum(axis, invariant), inputs=as_symbols([a]))
#  
#  
# def reduce_mean(a, axis: int=None, invariant=False):
#     return V(operator=ReduceMean(axis, invariant), inputs=as_symbols([a]))
#  
#  
# def expand(a, axis: int):
#     return V(operator=Expand(axis), inputs=as_symbols([a]))
#  
#  
# def broadcast(a, shape):
#     return V(operator=Broadcast(shape), inputs=as_symbols([a]))
#  
#  
# def where(condition, a, b):
#     return V(operator=Where(), inputs=as_symbols([condition, a, b]))
#  
#  
# def equal(a, b):
#     return V(operator=Eq(), inputs=as_symbols([a, b]))
#  
#  
# def not_equal(a, b):
#     return V(operator=NEq(), inputs=as_symbols([a, b]))
#  
#  
# def less(a, b):
#     return V(operator=Lt(), inputs=as_symbols([a, b]))
#  
#  
# def less_equal(a, b):
#     return V(operator=LEq(), inputs=as_symbols([a, b]))
#  
#  
# def greater(a, b):
#     return V(operator=Gt(), inputs=as_symbols([a, b]))
#  
#  
# def greater_equal(a, b):
#     return V(operator=GEq(), inputs=as_symbols([a, b]))
#  
#  
# def maximum(a, b):
#     return V(operator=Max(), inputs=as_symbols([a, b]))
#  
#  
# def minimum(a, b):
#     return V(operator=Min(), inputs=as_symbols([a, b]))
#  
#  
# def sin(a):
#     return V(operator=Sin(), inputs=as_symbols([a]))
#  
#  
# def cos(a):
#     return V(operator=Cos(), inputs=as_symbols([a]))
#  
#  
# def tan(a):
#     return V(operator=Tan(), inputs=as_symbols([a]))
#  
#  
# def arcsin(a):
#     return V(operator=ArcSin(), inputs=as_symbols([a]))
#  
#  
# def arccos(a):
#     return V(operator=ArcCos(), inputs=as_symbols([a]))
#  
#  
# def arctan(a):
#     return V(operator=ArcTan(), inputs=as_symbols([a]))
#  
#  
# def sinh(a):
#     return V(operator=Sinh(), inputs=as_symbols([a]))
#  
#  
# def cosh(a):
#     return V(operator=Cosh(), inputs=as_symbols([a]))
#  
#  
# def tanh(a):
#     return V(operator=Tanh(), inputs=as_symbols([a]))
#  
#  
# def arcsinh(a):
#     return V(operator=ArcSinh(), inputs=as_symbols([a]))
#  
#  
# def arccosh(a):
#     return V(operator=ArcCosh(), inputs=as_symbols([a]))
#  
#  
# def arctanh(a):
#     return V(operator=ArcTanh(), inputs=as_symbols([a]))
#  
#  
# def exp(a):
#     return V(operator=Exp(), inputs=as_symbols([a]))
#  
#  
# def slice_assign(a, b, slice_tuple):
#     return V(operator=SliceAssign(slice_tuple), inputs=as_symbols([a, b]))
#  
#  
# def assign(a, b):
#     return slice_assign(a, b, slice(None))
#  
#  
# def slice_select(a, slice_tuple):
#     return V(operator=SliceSelect(slice_tuple), inputs=as_symbols([a]))
#  
#  
# def concatenate(a, b):
#     return V(operator=Concatenate(), inputs=as_symbols([a, b]))
#  
#  
# def rotate90(a, count, axes):
#     return V(operator=Rotate90(count, axes), inputs=as_symbols([a]))
#  
#  
# def flip(a, axis):
#     return V(operator=Flip(axis), inputs=as_symbols([a]))
#  
# def reshape(a, shape):
#     return V(operator=Reshape(shape), inputs=as_symbols([a]))
#  
#  
# def spread(a, position):
#     return V(operator=Spread(position), inputs=as_symbols([a]))
def where(a,b,c):
	return V(operator=Where(),inputs=as_symbols([a,b,c]))

#algbra---------
class Template:
	active_operator = None
	def __init__(self):
		if self.active_operator is None:
			self.active_sign = None
		else:
			self.active_sign = self.active_operator.__name__

	@staticmethod
	def reduce_symbol(symbol, index: int):
		if not isinstance(symbol,V):raise ValueError("symbol Must be V")
		input_list = symbol.input
		reduce_to_symbol = input_list[index]
		symbol.clear_operator()
		symbol.value = reduce_to_symbol.value
		symbol.name = reduce_to_symbol.name
		if reduce_to_symbol.is_operator():
			symbol.symbolic_compute(reduce_to_symbol.operator, reduce_to_symbol.input)
		else:
			symbol.category = reduce_to_symbol.category

	@staticmethod
	def value_equal(a, b):
		result = a == b
		if isinstance(result, bool) or isinstance(result, numpy.bool_):
			return result
		elif isinstance(result, numpy.ndarray):
			return result.all()
		else:
			raise Exception('Never reached.')

	@staticmethod
	def symbol_equal(a, b):
		if not isinstance(a,V) or not isinstance(b,V):raise ValueError("symbol Must be V")
		return a.symbolic_hash() == b.symbolic_hash()

	def simplify(self, symbol):
		raise ValueError("this is abstract")

class Simplification:
	def __init__(self,templates:list):
		self.__templates = {}
		for template in templates:
			self.register(template())
	def operator_trigger(self, operator: Operator):
		operator_sign = operator.__class__.__name__
		if operator_sign in self.__templates:
			return self.__templates[operator_sign]
		else:
			return set()

	def register(self, template: Template):
		active_operator = template.active_sign
		self.__templates.setdefault(active_operator, set())
		self.__templates[active_operator].add(template)

	def simplify(self, symbol):
		if not isinstance(symbol,V):raise ValueError("symbol Must be V")
		while self.simplify_cycle(symbol):
			pass
	def simplify_cycle(self, symbol):
		if not isinstance(symbol,V):raise ValueError("symbol Must be V")
		effective = False
		templates = list(self.operator_trigger(symbol.operator)) + list(self.__templates[None])
		if templates:
			for template in templates:
				if template.simplify(symbol):
					effective |= True
					break
		for next_symbol in symbol.input:
			if next_symbol.operator is not None:
				effective |= self.simplify_cycle(next_symbol)
		return effective

class TemplateConstant(Template):
	active_operator = None

	def simplify(self, symbol: V):
		if symbol.is_operator():
			for s in symbol.input:
				if not s.is_constant():
					return False
			compute_inputs = [_s.value for _s in symbol.input]
			value = symbol.operator.f(*compute_inputs)
			symbol.clear_operator()
			symbol.value = value
			symbol.category = VCategory.constant
			symbol.name=None
			return True
		else:
			return False


class TemplatePlus(Template):
	active_operator = Plus

	def simplify(self, symbol: V):
		left_symbol, right_symbol = symbol.input
		if left_symbol.is_constant() and self.value_equal(left_symbol.value, 0):
			self.reduce_symbol(symbol, 1)
			return True
		elif right_symbol.is_constant() and self.value_equal(right_symbol.value, 0):
			self.reduce_symbol(symbol, 0)
			return True
		elif self.symbol_equal(left_symbol, right_symbol):
			symbol.clear_operator()
			symbol.symbolic_compute(Mul(), [left_symbol, constant(2)])
			symbol.name=None
			return True
		elif left_symbol.operator!=None: 
			if left_symbol.operator.operator_sign=='-' and left_symbol.operator.inputs_count==1 and self.symbol_equal(left_symbol.input[0],right_symbol):
				symbol.clear_operator()
				symbol.symbolic_compute(Broadcast(()),[constant(0)])
				symbol.name=None
				return True
		elif right_symbol.operator!=None: 
			if right_symbol.operator.operator_sign=='-' and left_symbol.operator.inputs_count==1 and self.symbol_equal(right_symbol.input[0],left_symbol):
				symbol.clear_operator()
				symbol.symbolic_compute(Broadcast(()),[constant(0)])
				symbol.name=None
				return True
		else:
			return False


class TemplateSubtract(Template):
	active_operator = Sub

	def simplify(self, symbol: V):
		left_symbol, right_symbol = symbol.input
		if right_symbol.is_constant() and self.value_equal(left_symbol.value, 0):
			symbol.clear_operator()
			symbol.clear_input()
			symbol.symbolic_compute(Neg(), [right_symbol])
			symbol.name=None
			return True
		elif right_symbol.is_constant() and self.value_equal(right_symbol.value, 0):
			self.reduce_symbol(symbol, 0)
			return True
		elif self.symbol_equal(left_symbol, right_symbol):
			symbol.clear_operator()
			symbol.symbolic_compute(Broadcast(()), [left_symbol, constant(0)])
			symbol.name=None
			return True
		else:
			return False


class TemplateDivide(Template):
	active_operator = Div

	def simplify(self, symbol: V):
		left_symbol, right_symbol = symbol.input
		if right_symbol.is_constant() and self.value_equal(right_symbol.value, 1):
			self.reduce_symbol(symbol, 0)
			return True
		elif left_symbol.is_constant() and self.value_equal(left_symbol.value, 0):
			symbol.clear_operator()
			symbol.symbolic_compute(SliceAssign(slice(None)), [left_symbol, constant(0)])
			symbol.name=None
			return True
		elif self.symbol_equal(left_symbol, right_symbol):
			symbol.clear_operator()
			symbol.symbolic_compute(SliceAssign(slice(None)), [left_symbol, constant(1)])
			symbol.name=None
			return True
		else:
			return False


class TemplateMultiply(Template):
	active_operator = Mul

	def simplify(self, symbol: V):
		left_symbol, right_symbol = symbol.input
		if left_symbol.is_constant() and self.value_equal(left_symbol.value, 1):
			self.reduce_symbol(symbol, 1)
			return True
		elif right_symbol.is_constant() and self.value_equal(right_symbol.value, 1):
			self.reduce_symbol(symbol, 0)
			return True
		elif (left_symbol.is_constant() and self.value_equal(left_symbol.value, 0)) or(right_symbol.is_constant() and self.value_equal(right_symbol.value, 0)) :
			symbol.clear_operator()
			symbol.symbolic_compute(Broadcast(()),[constant(0)])
			symbol.name=None
			return True
		elif self.symbol_equal(left_symbol, right_symbol):
			symbol.clear_operator()
			symbol.symbolic_compute(Pow(), [left_symbol, constant(2)])
			symbol.name=None
			return True
		elif left_symbol.operator!=None: 
			if left_symbol.operator.operator_sign=='/' and left_symbol.input[0].is_constant() and self.symbol_equal(left_symbol.input[1],right_symbol):
				if left_symbol.input[0].value==1:
					symbol.clear_operator()
					symbol.symbolic_compute(Broadcast(()),[constant(1)])
					symbol.name=None
					return True
		elif right_symbol.operator!=None: 
			if right_symbol.operator.operator_sign=='/' and right_symbol.input[0].is_constant() and self.symbol_equal(right_symbol.input[1],left_symbol):
				if right_symbol.input[0].value==1:
					symbol.clear_operator()
					symbol.symbolic_compute(Broadcast(()),[constant(1)])
					symbol.name=None
					return True
		else:
			return False


class TemplatePower(Template):
	active_operator = Pow
	def simplify(self, symbol: V):
		left_symbol, right_symbol = symbol.input
		if (self.value_equal(left_symbol.value, 1) and left_symbol.is_constant() and right_symbol.is_constant()) or (self.value_equal(right_symbol.value, 1) and right_symbol.is_constant()):
			self.reduce_symbol(symbol, 0)
			return True
		elif self.value_equal(left_symbol.value, 1) and left_symbol.is_constant() :
			symbol.clear_operator()
			symbol.symbolic_compute(Broadcast(right_symbol.shape),[constant(1)])    
			symbol.name=None
			return True
		elif self.value_equal(right_symbol.value, 0) and right_symbol.is_constant():
			symbol.clear_operator()
			symbol.symbolic_compute(Broadcast(()),[constant(1)])    
			symbol.name=None
			return True
		else:
			return False

class TemplateMM(Template):
	active_operator = MM
	maxlen=4;
	def simplify(self, symbol:V):
		ls=g(symbol)
		if len(ls)>self.maxlen:
			self.maxlen=len(ls)
#             print(ls)
			symbol2=rebuildChain(ls)            
			symbol.clear_operator()
			symbol.symbolic_compute(SliceSelect(slice(None,None,None)),[symbol2])    
			symbol.name=None
			return False


def chainTrace(i,j,s):
	if i==j:
		return []
	ls=[]
	ls+=(chainTrace(i,s[(i,j)],s))
	ls+=(chainTrace(s[(i,j)]+1,j,s))
	ls.append(s[(i,j)])
	return ls    
def matChain(p:list):
	n=len(p)-1
	m,s={},{}
	for i in range(1,n+1):m[(i,i)]=0
	for r in range(2,n+1):
		for i in range(1,n-r+2):
			j=i+r-1
			m[(i,j)]=m[(i+1,j)]+p[i-1]*p[i]*p[j]
			s[(i,j)]=i;
			for k in range(i+1,j):
				t=m[(i,k)]+m[(k+1,j)]+p[i-1]*p[k]*p[j]
				if t<m[(i,j)]:
					m[(i,j)]=t;s[(i,j)]=k    
	return chainTrace(1, n, s)
def rebuildChain(ls):
	if len(ls)<3:return
	ls1=[ls[0].shape[0]]+[i.shape[1] for i in ls]
	m=matChain(ls1)
	nls=ls[m[0]-1](MM(),ls[m[0]])
	ls[m[0]-1]=nls
	ls[m[0]]=None
	for i in m[1:]:
		j=0
		k=1
		while ls[i+j]==None:j+=1
		while ls[i-k]==None:k+=1
		nls=ls[i-k](MM(),ls[i+j])
		ls[i-k]=nls
		ls[i+j]=None
	return nls

def g(l):
	if l.operator==None or l.operator.operator_sign!='@':
		return [l]
	ls =[]
	for i in range(l.operator.inputs_count):
		ls+=g(l.input[i])
	return ls

default_templates = [
	TemplateConstant,
	TemplatePlus,
	TemplateSubtract,
	TemplateMultiply,
	TemplateDivide,
	TemplatePower,
	TemplateMM,
]
simp=Simplification(default_templates)


