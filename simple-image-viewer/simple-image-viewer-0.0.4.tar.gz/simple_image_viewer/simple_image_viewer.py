#!/usr/bin/env python
##############################################################################
#
# Copyright (c) 2020 Saeid Hosseinipoor <shossei1@stevens.edu>
# All rights reserved.
# Licensed under the MIT License
#
##############################################################################

from __future__ import absolute_import, division, print_function

MASKS = ('*.jpg', '*.png', '*.flo', '*.dpt', '*.pfm')
MASK_DESCRIPTION = ('jpeg files', 'png files', 'flow files', 'depth files', 'disparity files')
IMAGE_TYPES = list(zip(MASK_DESCRIPTION, MASKS))
ALL_TYPES = [('*.*', 'all files')] + IMAGE_TYPES
EXTENSIONS = [mask.split('.')[-1] for mask in MASKS]
EXTENSIONS += ['jpeg']

import PIL.Image

try:
	import clipboard
	CLIPBOARD_FLAG = False
except:
	CLIPBOARD_FLAG = False 

try:
	from sintel_io import *
	from flowlib import *
	import pfmutil as pfm
except:
	from simple_image_viewer.sintel_io import *
	from simple_image_viewer.flowlib import *
	import simple_image_viewer.pfmutil as pfm

try:
	from helpers import *
except:
	from simple_image_viewer.helpers import *

try:
	from Tkinter import *
	import tkFileDialog as filedialog
except ImportError:
	from tkinter import *
	from tkinter import filedialog
import PIL.ImageTk

class SimpleImageViewer(Frame):
	def chg_image(self, filename):
		self.original_image, self.display_image = self.open_image(filename)
		self.image_format = filename.split('.')[-1].lower()
		self.image_index = self.image_list.index(filename)
		sp = filename.split('/')
		path = '/'.join(sp[:2]+['...']+sp[-2:])
		self.master.title('Simple Image Viewer: '+path)
			
		self.display_image = PIL.Image.fromarray(self.display_image)
		self.img = PIL.ImageTk.PhotoImage(self.display_image)
		self.la.config(image=self.img, bg="#000000", width=self.img.width(), height=self.img.height())

	def open(self):
		filename = filedialog.askopenfilename(title = "Select file",filetypes = ALL_TYPES)
		
		if filename != "" and filename.split('.')[-1] in EXTENSIONS:
			dirName = '/'.join(filename.split('/')[:-1])+'/'
			self.image_list = getListOfFiles(dirName, masks=MASKS)
			self.chg_image(filename)
			self.image_list.sort()
		
	def save_as(self):
		if not hasattr(self, 'original_image'): 
			print ("Error: Select and open an image first.")
			return
		filename = filedialog.asksaveasfilename(filetypes = IMAGE_TYPES, defaultextension='.png') 
		if not filename: return
		print ('Saving '+filename)
		self.save_image (filename)
		
	def seek_prev(self):
		if self.image_index > 0:
			self.image_index -= 1
		else:
			self.image_index = len(self.image_list) - 1
		filename = self.image_list[self.image_index]
		if filename != "" and filename.split('.')[-1] in EXTENSIONS:
			self.chg_image(filename)
		print (self.image_index, filename)


	def seek_next(self):
		if self.image_index < len(self.image_list)-1:
			self.image_index += 1
		else:
			self.image_index = 0
		filename = self.image_list[self.image_index]
		if filename != "" and filename.split('.')[-1] in EXTENSIONS:
			self.chg_image(filename)
		print (self.image_index, filename)

	def ctrl_c(self):
		if not hasattr(self, 'display_image'): 
			print ("Error: Select and open an image first.")
			return
		# clipboard.set_image(self.im, format='png')
		clipboard.copy(self.im)

	def open_image (self, filename):
		extension = filename.split('.')[-1].lower()
		if extension in ['png', 'jpg', 'jpeg']:
			image = scipy.misc.imread(filename)
			disp_image = image
		elif extension == 'flo':
			image = read_flow(filename)
			disp_image = flow_to_image(image)
		elif extension == 'dpt':
			image = depth_read(filename)
			disp_image = 1. / image
			self.dpt_max = np.amax(disp_image)
			disp_image = disp_image / np.amax(disp_image) * 255
		elif extension == 'pfm':
			image = pfm.load(filename)[0]
			disp_image = image
		else:
			try:
				image = scipy.misc.imread(filename)
				disp_image = image
			except:
				image = np.ones([200,400]) * 255
				for i in range(200):
					image[i, 2*i] = 0
					image[199-i, 398-2*i] = 0
				disp_image = image
		
		return image, disp_image
	
	def save_image (self, filename):
		extension = filename.split('.')[-1].lower()
		if extension in ['png', 'jpg', 'jpeg']:
			scipy.misc.imsave(filename, self.display_image)
		elif extension == 'flo' and self.image_format == 'flo':
			write_flow(image, self.original_image)
		elif extension == 'dpt' and len(self.original_image.shape) == 2:
			if self.image_format == 'dpt':
				depth_write(filename, self.original_image)
			else:
				depth_write(filename, 1. / self.original_image)
		elif extension == 'pfm':
			if self.image_format == 'dpt':
				pfm.save(filename, 1. / (self.original_image / 255 * self.dpt_max))
			else:
				pfm.save(filename, self.original_image)
		else:
			try:
				scipy.misc.imsave(filename, self.display_image)
			except:
				Print ("Error: Cannot save.")


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master.title('Simple Image Viewer')

		self.image_list = list()
		self.caption = StringVar()

		frame_top = Frame(self)
		Button(frame_top, text="Open File ...", command=self.open).pack(side=LEFT)
		Button(frame_top, text="Save as ...", command=self.save_as).pack(side=LEFT)
		if CLIPBOARD_FLAG:
			Button(frame_top, text="Copy to clipboard", command=self.ctrl_c).pack(side=RIGHT)

		frame_bot = Frame(self)
		Button(frame_bot, text="Prev", command=self.seek_prev).pack(side=LEFT)
		Button(frame_bot, text="Next", command=self.seek_next).pack(side=RIGHT)
				
		Label(frame_top, textvariable=self.caption).pack(side=LEFT)
		self.la = Label(self)

		frame_top.pack(side=TOP, fill=BOTH)
		frame_bot.pack(side=BOTTOM, fill=BOTH)
		self.la.pack()
		self.pack()

if __name__ == "__main__":
	app = SimpleImageViewer()
	app.mainloop()