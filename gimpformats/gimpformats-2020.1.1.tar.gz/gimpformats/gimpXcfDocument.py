#!/usr/bin/env python3
"""
Pure python implementation of the gimp xcf file format

Currently supports:
	Loading xcf files
	Getting image hierarchy and info
	Getting image for each layer (PIL image)
Currently not supporting:
	Saving
	Programatically alter documents (add layer, etc)
	Rendering a final, compositied image
"""
import argparse
import copy

import PIL.ImageGrab
from PIL import Image
from blendmodes.blend import blendLayers, BlendType
from .binaryIO import IO
from .gimpIOBase import GimpIOBase
from .gimpImageInternals import GimpChannel, GimpImageHierarchy


class GimpLayer(GimpIOBase):
	"""
	Represents a single layer in a gimp image
	"""

	COLOR_MODES = [
	'RGB color without alpha', 'RGB color with alpha', 'Grayscale without alpha',
	'Grayscale with alpha', 'Indexed without alpha', 'Indexed with alpha']
	PIL_MODE_TO_LAYER_MODE = {'L': 2, 'LA': 3, 'RGB': 0, 'RGBA': 1}

	def __init__(self, parent, name=None, image=None):
		GimpIOBase.__init__(self, parent)
		self.width = 0
		self.height = 0
		self.colorMode = 0
		self.name = name
		self._imageHierarchy = None
		self._imageHierarchyPtr = None
		self._mask = None
		self._maskPtr = None
		self._data = None
		if image is not None:
			self.image = image # done last as it resets some of the above defaults

	def _decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		io = IO(data, index)
		#print 'Decoding Layer at',index
		self.width = io.u32
		self.height = io.u32
		self.colorMode = io.u32 # one of self.COLOR_MODES
		self.name = io.sz754
		self._propertiesDecode_(io)
		self._imageHierarchyPtr = self._pointerDecode_(io)
		self._maskPtr = self._pointerDecode_(io)
		self._mask = None
		self._data = data
		return io.index

	def toBytes(self):
		"""
		encode to byte array
		"""
		dataAreaIO = IO()
		io = IO()
		io.u32 = self.width
		io.u32 = self.height
		io.u32 = self.colorMode
		io.sz754 = self.name
		dataAreaIndex = io.index + self._POINTER_SIZE_ * 2
		io.addBytes(self._pointerEncode_(dataAreaIndex))
		dataAreaIO.addBytes(self._propertiesEncode_())
		io.addBytes(self._pointerEncode_(dataAreaIndex))
		if self.mask is not None:
			dataAreaIO.addBytes(self.mask.toBytes())
		io.addBytes(self._pointerEncode_(dataAreaIndex + dataAreaIO.index))
		io.addBytes(dataAreaIO)
		return io.data

	@property
	def mask(self):
		"""
		Get the layer mask
		"""
		if self._mask is None and self._maskPtr is not None and self._maskPtr != 0:
			self._mask = GimpChannel(self)
			self._mask.fromBytes(self._data, self._maskPtr)
		return self._mask

	@property
	def image(self):
		"""
		get the layer image

		NOTE: can return None!
		"""
		if self.imageHierarchy is None:
			return None
		return self.imageHierarchy.image

	@image.setter
	def image(self, image):
		"""
		set the layer image

		NOTE: resets layer width, height, and colorMode
		"""
		self.height = image.height
		self.width = image.width
		if image.mode not in self.PIL_MODE_TO_LAYER_MODE:
			raise NotImplementedError('No way of handlng PIL image mode "' + image.mode + '"')
		self.colorMode = self.PIL_MODE_TO_LAYER_MODE[image.mode]
		if not self.name and isinstance(image, str):
			# try to use a filename as the name
			self.name = image.rsplit('\\', 1)[-1].rsplit('/', 1)[-1]
		self.imageHierarchy = GimpImageHierarchy(self)
		self.imageHierarchy.image = image

	@property
	def imageHierarchy(self):
		"""
		Get the image hierarchy objects

		This is mainly needed for deciphering image, and therefore,
		of little use to you, the user.

		NOTE: can return None if it has been fully read into an image
		"""
		if self._imageHierarchy is None and self._imageHierarchyPtr > 0:
			self._imageHierarchy = GimpImageHierarchy(self)
			self._imageHierarchy.fromBytes(self._data, self._imageHierarchyPtr)
		return self._imageHierarchy

	def _forceFullyLoaded(self):
		"""
		make sure everything is fully loaded from the file
		"""
		if self.mask is not None:
			self.mask._forceFullyLoaded()
		_ = self.image # make sure the image is loaded so we can delete the hierarchy nonsense
		self._imageHierarchy = None
		self._data = None

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Name: ' + str(self.name))
		ret.append('Size: ' + str(self.width) + ' x ' + str(self.height))
		ret.append('colorMode: ' + self.COLOR_MODES[self.colorMode])
		ret.append(GimpIOBase.__repr__(self, indent))
		m = self.mask
		if m is not None:
			ret.append('Mask:')
			ret.append(m.__repr__(indent + '\t'))
		return indent + (('\n' + indent).join(ret))


class Precision:
	"""
	Since the precision code is so unusual, I decided to create a class
	to parse it.
	"""
	def __init__(self):
		self.bits = 8
		self.gamma = True
		self.numberFormat = int

	def decode(self, gimpVersion, io):
		"""
		decode the precision code from the file
		"""
		if gimpVersion < 4:
			self.bits = 8
			self.gamma = True
			self.numberFormat = int
		else:
			code = io.u32
			if gimpVersion == 4:
				self.gamma = (True, True, False, False, False)[code]
				self.bits = (8, 16, 32, 16, 32)[code]
				self.numberFormat = (int, int, int, float, float)[code]
			elif gimpVersion in (5, 6):
				self.gamma = (code % 100 != 0)
				code = int(code / 100)
				self.bits = (8, 16, 32, 16, 32)[code]
				self.numberFormat = (int, int, int, float, float)[code]
			else: # gimpVersion 7 or above
				self.gamma = (code % 100 != 0)
				code = int(code / 100)
				self.bits = (8, 16, 32, 16, 32, 64)[code]
				self.numberFormat = (int, int, int, float, float, float)[code]

	def encode(self, gimpVersion, io):
		"""
		encode this to the file

		NOTE: will not mess with development versions 5 or 6
		"""
		if gimpVersion < 4:
			if self.bits != 8 or not (self.gamma) or self.numberFormat != int:
				raise Exception('Illegal precision (' + str(self) + ') for gimp version ' +
				str(gimpVersion))
		else:
			if gimpVersion == 4:
				if self.bits == 64:
					raise Exception('Illegal precision (' + str(self) + ') for gimp version ' +
					str(gimpVersion))
				if self.numberFormat == int:
					code = (8, 16, 32).index(self.bits)
				else:
					code = (16, 32).index(self.bits) + 2
				code = code * 100
				if self.gamma:
					code += 50
			elif gimpVersion in (5, 6):
				raise NotImplementedError('Cannot save to gimp developer version ' +
				str(gimpVersion))
			else: # version 7 or above
				if self.numberFormat == int:
					code = (8, 16, 32).index(self.bits)
				else:
					code = (16, 32, 64).index(self.bits) + 2
				code = code * 100
				if self.gamma:
					code += 50
			io.u32 = code

	def requiredGimpVersion(self):
		"""
		return the lowest gimp version that supports this precision
		"""
		if self.bits == 8 and self.gamma and self.numberFormat == int:
			return 0
		if self.bits == 64:
			return 7
		return 4

	def __repr__(self):
		ret = []
		ret.append(str(self.bits) + "-bit")
		ret.append('gamma' if self.gamma else 'linear')
		ret.append('integer' if self.numberFormat is int else float)
		return ' '.join(ret)


class GimpDocument(GimpIOBase):
	"""
	Pure python implementation of the gimp file format

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/xcf.txt
	"""
	def __init__(self, fileName=None):
		GimpIOBase.__init__(self, self)
		self.dirty = False # a file-changed indicator.  # TODO: Not fully implemented.
		self._layers = None
		self._layerPtr = []
		self.channels = []
		self._channelPtr = []
		self.version = None
		self.width = 0
		self.height = 0
		self.baseColorMode = 0
		self.precision = None # Precision object
		self._data = None
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName):
		"""
		load a gimp file

		:param filename: can be a file name or a file-like object
		"""
		if hasattr(fileName, 'read'):
			self.filename = fileName.name
			f = fileName
		else:
			self.filename = fileName
			f = open(fileName, 'rb')
		data = f.read()
		f.close()
		self._decode_(data)

	def _decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		io = IO(data, index)
		if io.getBytes(9) != "gimp xcf ".encode('ascii'):
			raise Exception('Not a valid GIMP file')
		version = io.cString
		if version == 'file':
			self.version = 0
		else:
			self.version = int(version[1:])
		self.width = io.u32
		self.height = io.u32
		self.baseColorMode = io.u32
		self.precision = Precision()
		self.precision.decode(self.version, io)
		self._propertiesDecode_(io)
		self._layerPtr = []
		self._layers = []
		while True:
			ptr = self._pointerDecode_(io)
			if ptr == 0:
				break
			self._layerPtr.append(ptr)
			l = GimpLayer(self)
			l._decode_(io.data, ptr)
			self._layers.append(l)
		self._channelPtr = []
		self.channels = []
		while True:
			ptr = self._pointerDecode_(io)
			if ptr == 0:
				break
			self._channelPtr.append(ptr)
			c = GimpChannel(self)
			c.fromBytes(io.data, ptr)
			self.channels.append(c)
		return io.index

	def toBytes(self):
		"""
		encode to a byte array
		"""
		io = IO()
		io.addBytes("gimp xcf ")
		io.addBytes(str(self.version) + '\0')
		io.u32 = self.width
		io.u32 = self.height
		io.u32 = self.baseColorMode
		if self.precision is None:
			self.precision = Precision()
		self.precision.encode(self.version, io)
		io.addBytes(self._propertiesEncode_())
		dataAreaIdx = io.index + self._POINTER_SIZE_ * (len(self.layers) + len(self.channels))
		dataAreaIo = IO()
		for l in self.layers:
			io.pointer = dataAreaIdx + dataAreaIo.index
			dataAreaIo.addBytes(l.toBytes())
		for channel in self.channels:
			io.pointer = dataAreaIdx + dataAreaIo.index
			dataAreaIo.addBytes(channel.toBytes())
		return io.data

	def _forceFullyLoaded(self):
		"""
		make sure everything is fully loaded from the file
		"""
		for l in self.layers:
			l._forceFullyLoaded()
		for chan in self.channels:
			chan._forceFullyLoaded()
		# no longer try to get the data from file
		self._layerPtr = None
		self._channelPtr = None
		self._data = None

	@property
	def layers(self):
		"""
		Decode the image's layers if necessary

		TODO: need to do the same thing with self.Channels
		"""
		if self._layers is None:
			self._layers = []
			for _ptr in self._layerPtr:
				l = GimpLayer(self)
				#l.fromBytes(self._data, ptr)
				self._layers.append(l)
			# add a reference back to this object so it doesn't go away while array is in use
			self._layers.parent = self
			# override some internal methods so we can do more with them
			self._layers._actualDelitem_ = self._layers.__delitem__
			self._layers.__delitem__ = self.deleteLayer
			self._layers._actualSetitem_ = self._layers.__delitem__
			self._layers.__setitem__ = self.setLayer
		return self._layers

	def getLayer(self, index):
		"""
		return a given layer
		"""
		return self.layers[index]

	def setLayer(self, _index, _l):
		"""
		assign to a given layer
		"""
		self._forceFullyLoaded()
		self.dirty = True
		self._layerPtr = None # no longer try to use the pointers to get data
		#self.layers._actualSetitem(index, l)

	def newLayer(self, name, image, index=-1):
		"""
		create a new layer based on a PIL image

		:param name: a name for the new layer
		:param index: where to insert the new layer (default=top)
		:return: newly created GimpLayer object
		"""
		l = GimpLayer(self, name, image)
		self.insertLayer(l, index)
		return layer

	def newLayerFromClipboard(self, name='pasted', index=-1):
		"""
		Create a new image from the system clipboard.

		:param name: a name for the new layer (default="pasted")
		:param index: where to insert the new layer (default=top)
		:return: newly created GimpLayer object

		NOTE: requires pillow PIL implementation
		NOTE: only works on OSX and Windows
		"""
		image = PIL.ImageGrab.grabclipboard()
		return self.newLayer(name, image, index)

	def addLayer(self, l):
		"""
		append a layer object to the document

		:param layer: the new layer to append
		"""
		self.insertLayer(l, -1)

	def appendLayer(self, l):
		"""
		append a layer object to the document

		:param layer: the new layer to append
		"""
		self.insertLayer(l, -1)

	def insertLayer(self, l, index=-1):
		"""
		insert a layer object at a specific position

		:param layer: the new layer to insert
		:param index: where to insert the new layer (default=top)
		"""
		self.layers.insert(index, l)

	def deleteLayer(self, index):
		"""
		delete a layer
		"""
		self.__delitem__(index)

	# make this class act like this class is an array of layers
	def __len__(self):
		return len(self.layers)

	def __getitem__(self, index):
		return self.layers[index]

	def __setitem__(self, index, l):
		self.setLayer(index, l)

	def __delitem__(self, index):
		self.deleteLayer(index)

	def __inc__(self, amt):
		self.appendLayer(amt)
		return self

	@property
	def image(self):
		"""
		get a final, compiled image
		"""
		# We need to preprocess the layers to sort them into a list of layers
		# and groups. Where a group is a list of layers

		# Example Layers [layer, layer, group, layer]
		# Example Group [Layer(Group), [layer, layer, ...]]
		layers = self.layers[:] # Copy the attribute rather than write to it
		layersOut = []
		index = 0
		while index < len(layers):
			layerOrGroup = layers[index]
			if layerOrGroup.isGroup:
				elem = [layerOrGroup, []]
				index += 1
				while layers[index].itemPath is not None:
					layerCopy = copy.deepcopy(layers[index])
					layerCopy.xOffset -= layerOrGroup.xOffset
					layerCopy.yOffset -= layerOrGroup.yOffset
					elem[1].append(layerCopy)
					layers.pop(index)
				layersOut.append(elem)
			else:
				layersOut.append(layerOrGroup)
				index += 1
		return flattenAll(layersOut, (self.width, self.height))

	def save(self, toFilename=None):
		"""
		save this gimp image to a file
		"""
		self._forceFullyLoaded()
		if toFilename is None:
			toFilename = self.filename
		if not hasattr(toFilename, 'write'):
			f = open(toFilename, 'wb')
		f.write(self.toBytes())
		self.dirty = False

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		if self.filename is not None:
			ret.append('Filename: ' + self.filename)
		ret.append('Version: ' + str(self.version))
		ret.append('Size: ' + str(self.width) + ' x ' + str(self.height))
		ret.append('Base Color Mode: ' + self.COLOR_MODES[self.baseColorMode])
		ret.append('Precision: ' + str(self.precision))
		ret.append(GimpIOBase.__repr__(self))
		if self._layerPtr:
			ret.append('Layers: ')
			for l in self.layers:
				ret.append(l.__repr__('\t'))
		if self._channelPtr:
			ret.append('Channels: ')
			for ch in self.channels:
				ret.append(ch.__repr__('\t'))
		return '\n'.join(ret)

def blendModeLookup(blendmode, blendLookup, default=BlendType.NORMAL):
	""" Get the blendmode from a lookup table """
	if blendmode not in blendLookup:
		print("WARNING " + str(blendmode) + " is not currently supported!")
		return default
	return blendLookup[blendmode]

def rasterImageOffset(image, size, offsets=(0, 0)):
	""" Rasterise an image with offset to a given size"""
	imageOffset = Image.new("RGBA", size)
	imageOffset.paste(image.convert("RGBA"), offsets, image.convert("RGBA"))
	return imageOffset

def flattenLayerOrGroup(layerOrGroup, imageDimensions, flattenedSoFar=None,
ignoreHidden=True):
	"""Flatten a layer or group on to an image of what has already been
	flattened
	Args:
		layerOrGroup (Layer|Group): A layer or a group of layers
		imageDimensions ((int, int)): size of the image
		flattenedSoFar (PIL.Image, optional): the image of what has already
		been flattened. Defaults to None.
		ignoreHidden (bool, optional): ignore layers that are hidden. Defaults
		to True.
	Returns:
		PIL.Image: Flattened image
	"""
	blendLookup = {0: BlendType.NORMAL, 3: BlendType.MULTIPLY,
	4: BlendType.SCREEN, 5: BlendType.OVERLAY, 6: BlendType.DIFFERENCE,
	7: BlendType.ADDITIVE, 8: BlendType.NEGATION, 9: BlendType.DARKEN,
	10: BlendType.LIGHTEN, 11: BlendType.HUE, 12: BlendType.SATURATION,
	13: BlendType.COLOUR, 14: BlendType.LUMINOSITY, 15: BlendType.DIVIDE,
	16: BlendType.COLOURDODGE, 17: BlendType.COLOURBURN,
	18: BlendType.HARDLIGHT, 19: BlendType.SOFTLIGHT, 20: BlendType.GRAINEXTRACT,
	21: BlendType.GRAINMERGE, 23: BlendType.OVERLAY, 24: BlendType.HUE,
	25: BlendType.SATURATION, 26: BlendType.COLOUR, 27: BlendType.LUMINOSITY,
	28: BlendType.NORMAL, 30: BlendType.MULTIPLY, 31: BlendType.SCREEN,
	32: BlendType.DIFFERENCE, 33: BlendType.ADDITIVE, 34: BlendType.NEGATION,
	35: BlendType.DARKEN, 36: BlendType.LIGHTEN, 37: BlendType.HUE,
	38: BlendType.SATURATION, 39: BlendType.COLOUR, 40: BlendType.LUMINOSITY,
	41: BlendType.DIVIDE, 42: BlendType.COLOURDODGE,
	43: BlendType.COLOURBURN, 44: BlendType.HARDLIGHT, 45: BlendType.SOFTLIGHT,
	46: BlendType.GRAINEXTRACT, 47: BlendType.GRAINMERGE,
	48: BlendType.VIVIDLIGHT, 49: BlendType.PINLIGHT, 52: BlendType.EXCLUSION}

	if isinstance(layerOrGroup, list):
		if ignoreHidden and not layerOrGroup[0].visible:
			foregroundRaster = Image.new("RGBA", imageDimensions)
		else: # A group is a list of layers
			# (see flattenAll)
			foregroundRaster = rasterImageOffset(flattenAll(layerOrGroup[1],
			imageDimensions, ignoreHidden), imageDimensions, (layerOrGroup[0].xOffset,
			layerOrGroup[0].yOffset))
		if flattenedSoFar is None:
			return foregroundRaster
		return blendLayers(flattenedSoFar, foregroundRaster,
		blendModeLookup(layerOrGroup[0].blendMode, blendLookup),
		layerOrGroup[0].opacity)

	if ignoreHidden and not layerOrGroup.visible:
		foregroundRaster = Image.new("RGBA", imageDimensions)
	else:
		# Get a raster image and apply blending
		foregroundRaster = rasterImageOffset(layerOrGroup.image, imageDimensions,
		(layerOrGroup.xOffset, layerOrGroup.yOffset))
	if flattenedSoFar is None:
		return foregroundRaster
	return blendLayers(flattenedSoFar, foregroundRaster,
	blendModeLookup(layerOrGroup.blendMode, blendLookup),
	layerOrGroup.opacity)


def flattenAll(layers, imageDimensions, ignoreHidden=True):
	"""Flatten a list of layers and groups

	Note the bottom layer is at the end of the list

	Args:
		layers ([Layer|Group]): A list of layers and groups
		imageDimensions ((int, int)): size of the image
		been flattened. Defaults to None.
		ignoreHidden (bool, optional): ignore layers that are hidden. Defaults
		to True.
	Returns:
		PIL.Image: Flattened image
	"""
	end = len(layers) - 1
	flattenedSoFar = flattenLayerOrGroup(layers[end], imageDimensions, ignoreHidden=ignoreHidden)
	for l in range(end - 1, -1, -1):
		flattenedSoFar = flattenLayerOrGroup(layers[l], imageDimensions,
		flattenedSoFar=flattenedSoFar, ignoreHidden=ignoreHidden)
	return flattenedSoFar


if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("gimpGbrBrush.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true",
	help="dump info about this file")
	group.add_argument("--showLayer", action="store_true",
	help="show layer(s) (use * for all)")
	group.add_argument("--saveLayer", action="store_true",
	help="save layer(s) out to file")
	group.add_argument("--save", action="store",
	help="save out the brush image")
	args = parser.parse_args()

	gimpDocument = GimpDocument(args.xcfdocument)

	if args.dump:
		print(gimpDocument)
	if args.showLayer:
		if args.showLayer == '*':
			for layer in range(len(gimpDocument.layers)):
				im = gimpDocument.layers[layer].image
				showLayer(im, layer)
		else:
			im = gimpDocument.layers[int(args.showLayer)].image
			showLayer(im, int(args.showLayer))
	if args.saveLayer:
		layer = args.saveLayer.split(',', 1)
		if len(layer) > 1:
			filename = layer[1]
		else:
			filename = 'layer *.png'
		layer = args.saveLayer[0]
		if layer == '*':
			if filename.find('*') < 0:
				filename = '.'.join(filename.split('.', 1).insert(1, '*'))
			for n in range(len(gimpDocument.layers)):
				saveLayer(gimpDocument, n, filename)
		else:
			saveLayer(gimpDocument, int(layer), filename)
	if args.save:
		gimpDocument.save(args.save)


def showLayer(image, l):
	""" show a layer """
	if image is None:
		print('No image for layer', l)
	else:
		print('Showing layer', l)
		image.show()


def saveLayer(gimpDoc, l, fileName):
	""" save a layer """
	iteration = gimpDoc.layers[l].image
	if iteration is None:
		print('No image for layer', l)
	else:
		fn2 = fileName.replace('*', str(l))
		print('saving layer', fn2)
		iteration.save(fn2)
