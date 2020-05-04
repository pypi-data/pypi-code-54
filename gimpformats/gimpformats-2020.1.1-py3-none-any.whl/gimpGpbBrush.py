#!/usr/bin/env python3
"""
Pure python implementation of the OLD gimp gpb brush format
"""
import argparse
from .binaryIO import IO
from .gimpGbrBrush import GimpGbrBrush
from .gimpPatPattern import GimpPatPattern


class GimpGpbBrush:
	"""
	Pure python implementation of the OLD gimp gpb brush format

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/vbr.txt
	"""
	def __init__(self, filename):
		self.brush = GimpGbrBrush()
		self.pattern = GimpPatPattern()
		if hasattr(filename, 'read'):
			self.filename = filename.name
		else:
			self.filename = filename

	def load(self, filename):
		"""
		load a gimp file

		:param filename: can be a file name or a file-like object
		"""
		if hasattr(filename, 'read'):
			self.filename = filename.name
			f = filename
		else:
			self.filename = filename
			f = open(filename, 'rb')
		data = f.read()
		f.close()
		self._decode_(data)

	def _decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		index = self.brush._decode_(data, index)
		#index = self.pattern._decode_(data, index)
		return index

	def toBytes(self):
		""" encode this object to a byte array """
		io = IO()
		io.addBytes(self.brush.toBytes())
		io.addBytes(self.pattern.toBytes())
		return io.data

	def save(self, toFilename=None):
		""" save this gimp image to a file """
		if not hasattr(toFilename, 'write'):
			f = open(toFilename, 'wb')
		f.write(self.toBytes())

	def __repr__(self, indent=''):
		""" Get a textual representation of this object """
		ret = []
		if self.filename is not None:
			ret.append('Filename: ' + self.filename)
		ret.append(self.brush.__repr__(indent + '\t'))
		ret.append(self.pattern.__repr__(indent + '\t'))
		return ('\n' + indent).join(ret)


if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("gimpGbrBrush.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	parser.add_argument("--dump", action="store_true",
	help="dump info about this file")
	args = parser.parse_args()

	gimpDocument = GimpGbrBrush(args.xcfdocument)

	if args.dump:
		print(gimpDocument)
