#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import tempfile
import os
import subprocess
import glob
from collections import OrderedDict


# # Helper Functions

# In[2]:


get_ipython().run_cell_magic('javascript', '', 'var nb = IPython.notebook;\nvar kernel = IPython.notebook.kernel;\nvar command = "file_name = \'" + nb.notebook_path + "\'";\nkernel.execute(command);')


# In[3]:


def isnotebook():
    try:
        return get_ipython().__class__.__name__ == 'ZMQInteractiveShell'
    except:
        pass
    return False


# In[4]:


def is_testing():
    try:
        return file_name == 'lx.ipynb'
    except:
        pass
    return False


# In[5]:


def jprint(*args):
    if is_testing():
        print(*args)


# # Requiremtns

# In[6]:


requirements = []

requirements.append('numpy')
import numpy as np

requirements.append('natsort')
import natsort

requirements.append('opencv-python')
import cv2

requirements.append('Pillow')
from PIL import Image

requirements.append('urllib3')
from urllib.request import urlopen


# # Lists

# In[7]:


def listsGetPairsFromTwoLists(list1, list2):
    return list(zip(list1, list2))


# In[8]:


if is_testing:
    listAbcd = ['A', 'B', 'C', 'D']
    list1234 = ['1', '2', '3', '4']

    print(listsGetPairsFromTwoLists(listAbcd, list1234))


# In[9]:


def listSequentialOverlappingPairs(l):
    return list(zip(l[:-1], l[1:]))


# In[10]:


if is_testing:
    list1234 = ['1', '2', '3', '4']
    print(listSequentialOverlappingPairs(list1234))


# # List of Strings

# In[11]:


regex_cache = {}
def sListFilter(l, re_include=".*", re_exclude='^\b$'):
    regex_cache[re_include] = regex_cache.get(re_include, re.compile(re_include))
    regex_cache[re_exclude] = regex_cache.get(re_exclude, re.compile(re_exclude))
    return [e for e in l if regex_cache[re_include].search(e) and not regex_cache[re_exclude].search(e)]


# In[12]:


jprint(sListFilter(['good x', 'other good x', 'without the letter before y']))


# In[13]:


jprint(sListFilter(['good x', 'other good x', 'without the letter before y'], re_include='x'))


# In[14]:


jprint(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+'))


# In[15]:


jprint(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+', re_exclude='z'))


# # Text files

# In[16]:


def txtread(path):
    if 'http://' in path or 'https://' in path:
        return urlopen(path).read().decode()
    else:
        with open(path, 'r') as f:
            return f.read()

def txtwrite(path, txt):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        return f.write(txt)


# In[17]:


if is_testing():
    print(txtread('https://arxiv.org'))


# # Images

# # List of Strings

# In[18]:


regex_cache = {}
def sListFilter(l, re_include=".*", re_exclude='^\b$'):
    regex_cache[re_include] = regex_cache.get(re_include, re.compile(re_include))
    regex_cache[re_exclude] = regex_cache.get(re_exclude, re.compile(re_exclude))
    return [e for e in l if regex_cache[re_include].search(e) and not regex_cache[re_exclude].search(e)]


# In[19]:


jprint(sListFilter(['good x', 'other good x', 'without the letter before y']))


# In[20]:


jprint(sListFilter(['good x', 'other good x', 'without the letter before y'], re_include='x'))


# In[21]:


jprint(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+'))


# In[22]:


jprint(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+', re_exclude='z'))


# In[23]:


if is_testing():
    print(txtread('https://arxiv.org'))


# In[24]:


def imread(path):
    if isinstance(path, np.ndarray) and path.dtype == np.uint8:
        return path
    elif 'http://' in path or 'https://' in path:
        raw = np.asarray(bytearray(urlopen(path).read()), dtype="uint8")
        img = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    elif os.path.isfile(path):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img[:, :, [2, 1, 0]]

def imsread(paths):
    assert isinstance(paths, list) or isinstance(paths, tuple), type(paths)
    return [imread(path) for path in paths]

def imwrite(path, img):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, img[:, :, [2, 1, 0]])
    
def imjoin(imgs, axis=1):
    return np.concatenate(imgs, axis=axis)

def impad(img, top=0, bottom=0, left=0, right=0, color=255):
    return np.pad(img, [(top, bottom), (left, right), (0, 0)], 'constant', constant_values=color)


# In[ ]:





# In[25]:


def imshow(array):
    array = imread(array)
    if isnotebook():
        display(Image.fromarray(array))
    else:
        cv2.imshow('img', array[:, :, [2, 1, 0]])
        cv2.waitKey()


# In[26]:


if is_testing():
    imshow(imread('http://via.placeholder.com/70.png'))


# In[27]:


if is_testing():
    imshow('http://via.placeholder.com/70.png')


# In[28]:


def imscaleNN(img, s):
    return cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)

def imscaleBic(img, s):
    return cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)


# In[29]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        img = (255 * np.random.rand(20, 20, 3)).astype(np.uint8)
        img_path = os.path.join(d, 'test.png')
        imwrite(img_path, img)
        img_read = imread(img_path)
        out = imjoin([impad(img, right=5), img_read])

        out_large_pixaleted = imscaleNN(out, 8)
        imshow(out_large_pixaleted)

        out_large_interbic = imscaleBic(out, 8)
        imshow(out_large_interbic)


# In[30]:


def imNewWhite(height, width):
    return np.ones((height, width, 3)).astype(np.uint8) * 255


# In[31]:


if is_testing(): imshow(imNewWhite(10, 500) - 30)


# In[32]:


def imNewBlack(height, width):
    return np.zeros((height, width, 3)).astype(np.uint8)


# In[33]:


if is_testing(): imshow(imNewBlack(10, 500))


# In[34]:


def imAddNoiseGauss(img, std):
    assert img.dtype == np.uint8, img.dtype
    noise = np.random.randn(*img.shape) * std
    noisy = (np.clip(img.astype(np.float) + noise.astype(np.float), 0, 255)).astype(np.uint8)
    return noisy

if is_testing(): imshow(imAddNoiseGauss(imread('http://via.placeholder.com/150.png'), 10))


# In[35]:


def imJpgDegradation(img, quality):
    assert img.dtype == np.uint8, img.dtype
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode('.jpg', img, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    return decimg

if is_testing(): imshow(imJpgDegradation(imread('http://via.placeholder.com/150.png'), 15))


# In[36]:


def imCropCenter(img, size):
    h, w, c = img.shape

    h_start = max(h // 2 - size // 2, 0)
    h_end = min(h_start + size, h)

    w_start = max(w // 2 - size // 2, 0)
    w_end = min(w_start + size, w)

    return img[h_start:h_end, w_start:w_end]


# In[37]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 10))


# In[38]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 49))


# In[39]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 50))


# In[40]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 100))


# In[41]:


def imGallery(imgs, pad=0):
    n = len(imgs)
    nw = int(np.ceil(np.sqrt(n)))
    nh = int(np.ceil(n / nw))
    img_h, img_w, _ = imgs[0].shape
    w = nw * img_w + (nw - 1) * pad
    h = nh * img_h + (nh - 1) * pad

    assert imgs[0].dtype == np.uint8
    assert all([img.shape[0] == img_h for img in imgs])
    assert all([img.shape[1] == img_w for img in imgs])
    out = np.ones((h, w, 3), dtype=np.uint8) * 255

    idx = 0
    for ih in range(nh):
        for iw in range(nw):
            if idx + 1 > len(imgs):
                break
            w_beg = (iw + 0) * (img_w + pad)
            w_end = (iw + 1) * (img_w + pad) - pad
            h_beg = (ih + 0) * (img_h + pad)
            h_end = (ih + 1) * (img_h + pad) - pad
            out[h_beg:h_end, w_beg:w_end] = imgs[idx]
            idx += 1
    return out


# In[42]:


if is_testing():
    # List of images from back to white
    listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]


# In[43]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:1]))


# In[44]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:2]))


# In[45]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:2], pad=1))


# In[46]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:5], pad=1))


# In[47]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:9], pad=1))


# In[48]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:10], pad=1))


# In[49]:


if is_testing():
    img40x20 = imread('http://via.placeholder.com/40x20.png')
    imshow(imGallery([img40x20, img40x20, img40x20], pad=1))


# # Files

# In[50]:


def fiFindByWildcard(wildcard):
    return natsort.natsorted(glob.glob(wildcard, recursive=True))


# In[51]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]
        
        out_dir = os.path.join(d, "sub_dir")
        
        imgs_write = []
        for i in range(10):
            img = imNewBlack(10, 10) + 25 * i
            imwrite(os.path.join(out_dir, "{}.png".format(i)), img)
            imgs_write.append(img)
        
        print("written images:")
        imshow(imGallery(imgs_write))
        
        print("found images:")
        img_paths = fiFindByWildcard(os.path.join(out_dir, "*"))
        imgs = imsread(img_paths)
        imshow(imGallery(imgs))
        
        print("found images:")
        img_paths = fiFindByWildcard(os.path.join(d, "**/*.png"))
        imgs = imsread(img_paths)
        imshow(imGallery(imgs))


# In[52]:


# Jupyter


# In[53]:


def jnImageRenderingPixelated():
    """Do not interpolate images"""
    display(HTML('<style type = text/css> img { image-rendering: pixelated; } </style>'))
    
def jnImageRenderingAuto():
    """Interpolate images"""
    display(HTML('<style type = text/css> img { image-rendering: auto; } </style>'))


# In[ ]:





# # Shell

# In[54]:


def shell(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode()


# # Package Files

# In[55]:


if is_testing():
    package_files = {}


# In[56]:


def shell(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode()


# In[57]:


if is_testing():
    package_files['setup.py'] = r"""from distutils.core import setup
setup(
  name = 'lx',         # How you named your package folder (MyLib)
  packages = ['lx'],   # Chose the same as "name"
  version = '0.26',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'lx',   # Give a short description about your library
  author = 'lx',                   # Type in your name
  author_email = 'hx2983113@gmail.com',      # Type in your E-Mail
  #url = 'https://github.com/hx2983113/lx',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/hx2983113/lx/archive/0.20.tar.gz',    # I explain this later on
  keywords = [],   # Keywords that define your package best
  install_requires=[
      {requirements}
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)""".format(requirements=", ".join(["'" + r + "'" for r in requirements]))


# In[58]:


if is_testing():
    package_files['setup.cfg'] = r"""# Inside of setup.cfg
[metadata]
description-file = README.md
"""


# In[59]:


if is_testing():
    package_files['LICENSE.txt'] = r"""MIT License
Copyright (c) 2018 YOUR NAME
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


# In[60]:


if is_testing():
    package_files['README.md'] = ""


# In[61]:


if is_testing():
    get_ipython().system(' jupyter nbconvert --to script lx.ipynb')
    package_files['lx/__init__.py'] = txtread("lx.py")


# In[ ]:





# In[62]:


if is_testing():
    package_files['MANIFEST'] = r"""# file GENERATED by distutils, do NOT edit
setup.cfg
setup.py
lx/__init__.py
"""


# In[63]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        for key, value in package_files.items():
            txtwrite(os.path.join(d, key), value)

        print("\n".join(fiFindByWildcard(os.path.join(d, '**/*'))))

        #print(shell("cd {d} && git status && git config user.name 'lx' && git config user.email 'lx' && git commit -a -m 'Add' && git log && git push && python setup.py sdist && twine upload dist/* --verbose".format(d=d)))
        print(shell("cd {d} && python3 setup.py sdist && twine upload dist/* --verbose".format(d=d)))


# In[ ]:





# In[ ]:




