#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Author: Li Fajin
@Date: 2019-08-21 22:03:59
@LastEditors: Li Fajin
@LastEditTime: 2019-08-30 16:42:25
@Description: This script is used for plotting the GC content generated by GCContent.py
'''


import pandas as pd
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from optparse import OptionParser
from .__init__ import __version__

def create_parse_for_plot_GC_content():
	'''argument parser'''
	usage="usage: python %prog [options]"
	parser=OptionParser(usage=usage,version=__version__)
	parser.add_option('-i','--input',action="store",type="string",dest="GC_content",help="Input file generated by GCContent.py.[required]")
	parser.add_option('-o',"--otput_prefix",action="store",type="string",dest="output_prefix",help="Prefix of output files.[required]")
	parser.add_option("--mode",action="store",type="string",dest="mode",default="normal",help="The type of GC content you want to statistic. Either the normal type or GC content from each reading frame. [normal or frames]. defaul=%default")
	return parser

def plot_GC_content_for_different_frames(GC_content_melt,output_prefix,text_font={"size":20,"family":"Arial","weight":"bold"}):
	''' plot GC content for different frames'''
	plt.rc('font',weight='bold')
	fig=plt.figure(figsize=(8,6))
	ax=fig.add_subplot(111)
	ax=sns.violinplot(x='variable',y='value',data=GC_content_melt)
	ax.set_xlabel("Different reading frames",fontdict=text_font)
	ax.set_ylabel("GC%",fontdict=text_font)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines["bottom"].set_linewidth(2)
	ax.spines["left"].set_linewidth(2)
	ax.tick_params(which="both",width=2,labelsize=10)
	plt.savefig(output_prefix+"_frames_GC_contents.pdf")
	plt.close()

def plot_normal_GC_content(GC_content,output_prefix,text_font={"size":20,"family":"Arial","weight":"bold"}):
	plt.rc('font',weight='bold')
	fig=plt.figure(figsize=(8,6))
	ax=fig.add_subplot(111)
	ax=sns.distplot(GC_content['GC%'],bins=100,kde_kws={"color": "r", "lw": 3},hist_kws={"linewidth": 3,"alpha": 0.5, "color": "b"})
	ax.set_xlabel("GC%",fontdict=text_font)
	ax.set_ylabel("Frequency",fontdict=text_font)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines["bottom"].set_linewidth(2)
	ax.spines["left"].set_linewidth(2)
	ax.tick_params(which="both",width=2,labelsize=10)
	plt.savefig(output_prefix+"_GC_contents.pdf")
	plt.close()

def main():
	parser=create_parse_for_plot_GC_content()
	(options,args)=parser.parse_args()
	if not options.GC_content or not options.output_prefix:
		raise IOError("Please your input GC_content file and prefix of your output files.")
	GC_content=pd.read_csv(options.GC_content,sep="\t")
	if options.mode == 'normal':
		print("Start plot GC content...",file=sys.stderr)
		plot_normal_GC_content(GC_content,options.output_prefix,text_font={"size":20,"family":"Arial","weight":"bold"})
		print("Finish the step of plot GC content!",file=sys.stderr)
	elif options.mode == 'frames':
		GC_content_melt=pd.melt(GC_content,id_vars="transcripts")
		print("Start plot GC content...",file=sys.stderr)
		plot_GC_content_for_different_frames(GC_content_melt,options.output_prefix,text_font={"size":20,"family":"Arial","weight":"bold"})
		print("Finish the step of plot GC content!",file=sys.stderr)
	else:
		raise IOError("Please reset your --mode parameter [normal/frames]")

if __name__=="__main__":
	main()