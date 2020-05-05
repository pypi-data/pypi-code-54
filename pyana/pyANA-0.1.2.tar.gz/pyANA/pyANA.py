# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 09:47:41 2020

@author: Edward
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
import sklearn.mixture
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import re


class ANA():
    def __init__(self, directory):
        self.directory = directory
        self.files = glob(self.directory + '\\scalar*.h5')
        self.files.sort(key=self._natural_keys)

        self.parameters()

    def spec_map(self):
        tree = ET.parse(self.directory + '//spec_maps')
        root = tree.getroot()

        maps = root.findall('element')

        im = Image.open(self.directory + '//experiment.png')
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("arial", 16)
        sz = 10

        for i, m in enumerate(maps):
            cx = int(m.find('center_x_on_image').text)
            cy = int(m.find('center_y_on_image').text)

            draw.rectangle([cx - sz, cy - sz, cx + sz, cy + sz], fill='orange')

            w, h = draw.textsize(str(i + 1))
            draw.text((cx - w/2, cy - h/2), str(i + 1), font=font, anchor='SE')

        im.save(self.directory + '//exp_loc.png')
        self.spec_image = im

    def parameters(self):
        tree = ET.parse(self.directory + '//spec_maps')
        root = tree.getroot()

        maps = root.findall('element')

        sz = []
        dP = []
        xStart = []
        xEnd = []
        maxF = []
        rampL = []
        rampS = []
        for m in maps:
            sz.append(int(m.find('spec_map_').find('x_point_count').text))
            xStart.append(float(m.find('spec_map_').find('x_start').text))
            xEnd.append(float(m.find('spec_map_').find('x_end').text))
            dP.append(int(m.find('forward_').find('datapoints_').text))
            rampL.append(float(m.find('forward_').find('ramp_length_').text))
            rampS.append(float(m.find('forward_').find('ramp_speed_').text))
            maxF.append(float(m.find('forward_').find('maximum_force_').text))

        tree = ET.parse(self.directory + '//measurement')
        root = tree.getroot()

        maps = root.findall('measurement')

        filename = [x.text for x in root.find('spec_nid_files_').findall('element')]
        springK = [float(x.text) for x in root.find('spring_constants_').findall('element')]
        deflection = [float(x.text) * 1e9/10 for x in root.find('deflection_sensitivities_').findall('element')]

        mapSz = (np.array(xEnd) - np.array(xStart)) * 1e6

        self.param = pd.DataFrame(data={'FileName': filename,
                                        'SpringConstant': springK,
                                        'DeflSens': deflection,
                                        'MapSize': mapSz,
                                        'MapPixSize': sz,
                                        'DataPoints': dP,
                                        'RampLength': rampL,
                                        'RampSpeed': rampS,
                                        'MaxForce': maxF})

    def read(self, index=[]):

        data_list = []
        file_list = []
        
        if not isinstance(index, list):
            print('File index must be list')
            return
            
        idx = np.arange(len(self.files))

        if not index:
            index = idx
        
        idx = [i for i in index if i in idx]
        if len(idx) == 1:
            idx = (idx[0],)
    
        for i in idx:
            df = pd.read_hdf(self.files[i])
            
            data_list.append(df)
            file_list.append(self.files[i])
        file_list = np.array([f.split('\\') for f in file_list])
        spot_num = [int(f[:-3].split('_')[-1]) + 1 for f in file_list[:, 1]]

        self.data = pd.DataFrame(data={'Experiment': file_list[:, 0],
                                       'Files': file_list[:, 1],
                                       'Spot': spot_num,
                                       'Data': data_list})

    def stats(self, spots):
        d = self.spotData(spots)
                        
        return d.groupby(['Channel', 'Backward']).Value.describe()

    def hist(self, spots, channel, backward, *args, **kwargs):
        dd = self.channelData(spots, channel, backward).Value.dropna().values
        plt.hist(dd, **kwargs)
        plt.xlabel(channel)
        plt.ylabel('Counts')

    def image(self, spot, channel, backward, *args, **kwargs):
        if isinstance(spot, list):
            print('Can only show map of one spot at a time')
            return

        ar = self.channelData(spot, channel, backward, fill_empty=True).Value.values
        
        sz = self.param.MapPixSize[spot]
        ar = ar.reshape((sz, sz)).copy()
        ar[::2] = np.fliplr(ar[::2])

        mSize = self.param.MapSize[spot]
        plt.imshow(ar, origin='bottomleft', extent=(0, mSize, 0, mSize), **kwargs)
        plt.xlabel('[um]')
        plt.ylabel('[um]')
        plt.title(channel)
        plt.colorbar()
        return ar
    
    def xml2hdf(self):
        f1 = glob(self.directory + '//scalar*')
        f2 = glob(self.directory + '//scalar*.h5')
        
        files = [f for f in f1 if f not in f2]
        
        for f in files:
            tree = ET.parse(f)
            root = tree.getroot()
            
            name = []
            line = []
            value = []
            backward = []
            for element in root[0].findall('element'):
                line.append(int(element.find('line_').text))
                name.append(element.find('calc_name_').text)
                value.append(float(element.find('value_').text))
                backward.append(int(element.find('p_').text))
                
            df = pd.DataFrame({'Line': line,
                               'Channel': name,
                               'Value': value,
                               'Backward': backward})
            
            df.to_hdf(f + '.h5', key='df')
    
    def gaussianMix(self, spots, channel, backward, number=1):
        gmm = sklearn.mixture.GaussianMixture(n_components=number, covariance_type='diag')
        d = self.channelData(spots, channel, backward).Value.values
        r = gmm.fit(d[:, np.newaxis])
        m = r.means_.flatten()
        w = r.weights_.flatten()
        # c = r.covariances_.flatten()
        fits = pd.DataFrame({'mean': m, 'weight': w})
        fits = fits.sort_values('mean').reindex()
        return fits
    
    def channelData(self, spots, channel, backward, fill_empty=False):
        d = self.spotData(spots)
        dd = d[(d['Channel'] == channel) & (d['Backward'] == backward)]
        if fill_empty:
            sz = self.param.MapPixSize[spots]
        
            ar = np.zeros(sz*sz) * np.nan
            ar[dd.Line.values] = dd.Value.values
            dd = pd.DataFrame({'Value': ar})
        return dd
    
    # sorts list numerically
    def _atoi(self, text):
        return int(text) if text.isdigit() else text
    
    def _natural_keys(self, text):
        return [self._atoi(c) for c in re.split(r'(\d+)', text)]

    def spotData(self, spots):
        if isinstance(spots, list):
            if len(spots) > 1:
                spots = self.data.Spot.isin(spots)
                d = pd.concat([x for x in self.data[spots].Data], axis=0)
            else:
                spots = self.data.Spot.isin(spots)
                d = self.data[spots]
        else:
            spots = self.data.Spot.isin([spots])
            d = self.data[spots].Data.iloc[0]
        return d


if __name__ == "__main__":
    from matplotlib import cm
    directory = 'data_1mgmL'
    ana = ANA(directory)
    # ana.xml2hdf()
    ana.read()
    ana.hist(7, 'E-Modul', True, bins=100)
    ana.image(7, 'E-Modul', True, cmap=cm.afmhot)
    r = ana.gaussianMix(7, 'E-Modul', True, 2)
