#!/usr/bin/env python3
"""
Pure python implementation of the gimp file formats
"""
import argparse
from .gimpXcfDocument import GimpDocument
register = False

class GimpFormatPlugin:
	"""
	Pure python implementation of the gimp file formats
	"""

# ========= automatically add format info for pyformatgenie =========
if register:
	try:
		# will run this every time this module is loaded
		import pyformatgenie
		pfg = pyformatgenie.PyFormatGenie()
		pfg.add(GimpFormatPlugin)
		# and the most important part...
		pfg.save()
	except ImportError as e:
		# pyformatgenie is not installed (yet?). Continue with whatever you came here for.
		pass


if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("gimpFormat.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true",
	help="dump info about this file")
	group.add_argument("--showLayer", action="store",
	help="show layer(s) (use * for all)")
	group.add_argument("--saveLayer", action="store",
	help="n,out.jpg save layer(s) out to file")
	args = parser.parse_args()

	gimpDocument = GimpDocument(args.xcfdocument)

	if args.dump:
		print(gimpDocument)
	if args.showLayer:
		if args.showLayer == '*':
			for layer in range(len(gimpDocument.layers)):
				iterationM = gimpDocument.layers[layer].image
				showLayer(iterationM, layer)
		else:
			iterationM = gimpDocument.layers[int(args.showLayer)].image
			showLayer(iterationM, int(args.showLayer))
	if args.saveLayer:
		layer = args.saveLayer.split(',', 1)
		if len(layer) > 1:
			filenameM = layer[1]
		else:
			filenameM = 'layer *.png'
		layer = args.saveLayer[0]
		if layer == '*':
			if filenameM.find('*') < 0:
				filenameM = '.'.join(filenameM.split('.', 1).insert(1, '*'))
			for layer in range(len(gimpDocument.layers)):
				saveLayer(gimpDocument, layer, filenameM)
		else:
			saveLayer(gimpDocument, layer, filenameM)


def showLayer(iteration, l):
	""" show a layer """
	if iteration is None:
		print('No image for layer', l)
	else:
		print('Showing layer', l)
		iteration.show()


def saveLayer(gimpDoc, l, filename):
	""" save a layer """
	iteration = gimpDoc.layers[l].image
	if iteration is None:
		print('No image for layer', l)
	else:
		fn2 = filename.replace('*', str(l))
		print('saving layer', fn2)
		iteration.save(fn2)
