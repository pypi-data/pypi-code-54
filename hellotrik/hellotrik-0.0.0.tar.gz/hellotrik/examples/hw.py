from ..kernel import *
from math import *

def imdog():
	return load_image(dog)
	
def funnyimage(savedir:str,imgdir:str=dog,theta=0.53,x=100,y=0):
	im=load_image(imgdir)
	h=MATRIX()
	h.rows=h.cols=3;
	h.data=(c_float*9)()
	h.data[0]=h.data[4]=cos(theta)
	h.data[2]=x
	h.data[5]=y
	h.data[1]=-sin(theta)
	h.data[3]=-h.data[1]
	h.data[8]=1
	im=funny(im,h)
	save_image(im,savedir)

def dog_no_red(savedir:str):
	im = imdog()
	for row in range(im.h):
		for col in range(im.w):
			set_pixel(im, col, row, 0, 0)
	save_image(im,savedir)
def dog_gray(savedir:str):
	im = load_image(dog)
	graybar = rgb_to_grayscale(im)
	save_image(graybar,savedir)
def dog_shift(savedir:str,v=.4):
	im = imdog()
	for i in range(3):shift_image(im,i,v)
	save_image(im,savedir)
def dog_clamp(savedir:str):
	im = imdog()
	for i in range(3):shift_image(im,i,.4)
	clamp_image(im)
	save_image(im,savedir)
### 6-7. Colorspace and saturation
def dog_hsv_change(savedir:str):
	im = imdog()
	rgb_to_hsv(im)
	shift_image(im, 1, .2)
	clamp_image(im)
	hsv_to_rgb(im)
	save_image(im,savedir)
def dog_difgauss(savedir:str,a=1,b=0.1):
	im =imdog()
	f=make_filter(GAUSS,1)
	f2=make_filter(GAUSS,0.1)
	f=add_image(f,f2,0)
	im=convolve_image(im,f,1)
	clamp_image(im)
	#~ lib.feature_normalize(im)
	save_image(im,savedir)
def dog_resize(savedir:str,size,model=1):
	model=0 if model==0 else 1
	im =imdog()
	a = resize(im,int(im.w*size),int(im.h*size),model)
	save_image(a,savedir)

def dog_box_filter(savedir:str):
	im = imdog()
	f = make_filter(BOX,7)
	blur = convolve_image(im, f, 1)
	save_image(blur,savedir)
	
##---------hw3----------
def dog_corners(savedir:str):
	im = imdog()
	detect_and_draw_corners(im, 2, 50, 3)
	save_image(im,savedir)

def dog_matches(savedir:str):
	a = imdog()
	b = resize(a, a.w>>1, a.h>>1,1)
	m = find_and_draw_matches(a, b, 2, 50, 3)
	save_image(m,savedir)

def panorama(a:str,b:str,c:str,savedir:str):
	im1 = load_image(a)
	im2 = load_image(b)
	im3 = load_image(c)
	pan = panorama_image(im1, im2, thresh=5)
	pan2 = panorama_image(pan, im3, thresh=5)
	save_image(pan2,savedir)


def field_panorama(a:str,b:str,c:str,savedir:str):
	im1 = load_image(a)
	im2 = load_image(b)
	im3 = load_image(c)
	im1 = cylindrical_project(im1, 1200)
	im2 = cylindrical_project(im2, 1200)
	im3 = cylindrical_project(im3, 1200)
	pan = panorama_image(im1, im2, thresh=2, iters=50000, inlier_thresh=3)
	pan2 = panorama_image(pan, im3, thresh=2, iters=50000, inlier_thresh=3)
	save_image(pan2,savedir)

def flow_image(a:str,b:str,savedir:str):
	a = load_image(a)
	b = load_image(b)
	flow = optical_flow_images(b, a, 15, 8)
	draw_flow(a, flow, 8)
	save_image(a,savedir)







