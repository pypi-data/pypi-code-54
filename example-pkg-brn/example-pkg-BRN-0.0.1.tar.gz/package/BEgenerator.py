########################################################################################################
# BE Generator: Make all relevant variants of BE's (1: #CE/BE  2: Length x Width x Height of BE)
# Distinction between Collo and Fusts
########################################################################################################

###########################
# Collo
###########################
## 0. Read relevant data from NASA (1: # CE/BE  2: Length, Width, Height of BE  3: Length, Width, Height of CE)
## 1. Determine how current BE is built up to determine:
##    - If article can be stacked ("Mag je twee CE op elkaar in de doos plaatsen?")
##    - Current orientation of article ("Hoe staat het artikel in de doos?")
##    - Current margins of the box ("Hoeveel extra ruimte neemt de doos nog in?")
## 2. Determine all possible variants of BE's per # CE/BE (e.g. 12 CE/BE)
##    - Certain variants are not possible (TODO: Determine rules for BE-size)
## 3. Calculate the size of the BE and NettVolume and GrossVolume (NettVolume x VCF ("LuchtVolumeCorrectieFactor"))
## 4. Determine for every # CE/BE the variant with the minimal GrossVolume
## 5. So the output of this procedure is a table like below
##   - 1 CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr)
##   - 2 CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr)
##   - 3 CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr)
##   - ...
##   - N CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr) (e.g. N = 2 x ASIS # CE/BE)
## Note: For the Length, Width, Height two things are given as output
##   1. Length, Width, Height in mm
##   2. How the Length, Width, Height are built up (e.g. Length of BE = 3 x Length of CE) 
##   - this is used for graphical representation in the tool
##   - TODO: To determine how to make graphical representation


###########################
# Fusts
###########################
## 0. Read relevant data from NASA (1: # CE/Fust  2: Fust as currently used  3: Length, Width, Height of CE)
## 1. Read a table with all possible fusts (Per fusttype: 1: Innersize of fust (LxWxH) 2: Outersize of fust (LxWxH)
## 1. Determine how current fust is filled to determine:
##    - If article can be stacked ("Mag je twee CE op elkaar in de fust plaatsen?")
##    - Current orientation of article ("Hoe staat het artikel in de fust?")
## 2. Determine for each fusttype all possible variants of #CE/BE
## 3. So the output of this procedure is a table which gives the maximum number of CE for that fusttype (see example below):
##   - CBL 7 : 12
##   - CBL 8 : 6
##   - CBL 11: 12
##   - CBL 15: 12
##   - CBL 17: 24
##   - CBL 23: 36


########################################################################################################
# BE Generator: Make all relevant variants of BE's (1: #CE/BE  2: Length x Width x Height of BE)
# Distinction between Collo and Fusts
########################################################################################################

###########################
# Collo
###########################
## 0. Read relevant data from NASA (1: # CE/BE  2: Length, Width, Height of BE  3: Length, Width, Height of CE)
## 1. Determine how current BE is built up to determine:
##    - If article can be stacked ("Mag je twee CE op elkaar in de doos plaatsen?")
##    - Current orientation of article ("Hoe staat het artikel in de doos?")
##    - Current margins of the box ("Hoeveel extra ruimte neemt de doos nog in?")
## 2. Determine all possible variants of BE's per # CE/BE (e.g. 12 CE/BE)
##    - Certain variants are not possible (TODO: Determine rules for BE-size)
## 3. Calculate the size of the BE and NettVolume and GrossVolume (NettVolume x VCF ("LuchtVolumeCorrectieFactor"))
## 4. Determine for every # CE/BE the variant with the minimal GrossVolume
## 5. So the output of this procedure is a table like below
##   - 1 CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr)
##   - 2 CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr)
##   - 3 CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr)
##   - ...
##   - N CE/BE: Length BE, Width BE, Height BE, NettVolume BE (ltr), GrossVolume BE (ltr) (e.g. N = 2 x ASIS # CE/BE)
## Note: For the Length, Width, Height two things are given as output
##   1. Length, Width, Height in mm
##   2. How the Length, Width, Height are built up (e.g. Length of BE = 3 x Length of CE) 
##   - this is used for graphical representation in the tool
##   - TODO: To determine how to make graphical representation


###########################
# Fusts
###########################
## 0. Read relevant data from NASA (1: # CE/Fust  2: Fust as currently used  3: Length, Width, Height of CE)
## 1. Read a table with all possible fusts (Per fusttype: 1: Innersize of fust (LxWxH) 2: Outersize of fust (LxWxH)
## 1. Determine how current fust is filled to determine:
##    - If article can be stacked ("Mag je twee CE op elkaar in de fust plaatsen?")
##    - Current orientation of article ("Hoe staat het artikel in de fust?")
## 2. Determine for each fusttype all possible variants of #CE/BE
## 3. So the output of this procedure is a table which gives the maximum number of CE for that fusttype (see example below):
##   - CBL 7 : 12
##   - CBL 8 : 6
##   - CBL 11: 12
##   - CBL 15: 12
##   - CBL 17: 24
##   - CBL 23: 36

# %md ## Setup
# Load standard packages and the bin packing package


# import necessary modules
import pandas as pd
import numpy as np
import itertools
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType, FloatType
import math

!pip install rectpack
from rectpack import newPacker # For code, installation and explanation see https://github.com/secnot/rectpack.
import rectpack.guillotine as guillotine
import rectpack.maxrects as maxrects

# Collo
# %md # 0. Read relevant data

# 0. Read relevant data
def readdata():
    df_nasa = table('ketenoptimalisatie.nasa').toPandas();#pd.read_csv('export_nasa.csv')
    df_result = df_nasa[['NASANbr', 'DepthCEinMM', 'WidthCEinMM', 'HeightCEinMM', 'PalletType', 'BE', 'LengthBEinMM', 'WidthBEinMM', 'HeightBEinMM', 'WeightColloInKG', 'QuantityPerLayerPallet', 'NbrLayersPallet', 'PackageType', 'WidthPalletInMM', 'LengthPalletInMM', 'HeightPalletInMM', 'Tiltable', 'Stream']]
    cols = {'DepthCEinMM': 'LengthCEinMM', 'BE': 'NbrCEinBE'}
    df_result = df_result.rename(columns = cols);
    df_result.HeightPalletInMM = df_result['NbrLayersPallet']*df_result['HeightBEinMM'];
    return df_result;


# %md # 1. Determine how the current BE is built

# 1. Determine how the current BE is built
# Derive the orientation and margins of the BE
# LxW = LengthxWidth on DepthxWidth BE
# WxL = WidthxLength CE on DepthxWidth BE
# LxH = LengthxHeight CE on DepthxWidth BE (assumed not in scope)
# HxL = HeightxLength CE on DepthxWidth BE (assumed not in scope)
# WxH = WidthxHeight CE on DepthxWidth BE (assumed not in scope)
# HxW = HeightxWidth CE on DepthxWidth BE (assumed not in scope)

def get_orientation(NASANbr, lengthCE, widthCE, heightCE, lengthBE, widthBE, heightBE ):
    # first determine how much space is left in each dimension if 
    # - for example -  in the length (l) direction of the BE, 
    # the length (l), width (w) or height (h) of the CE is used
    ll = lengthBE%lengthCE
    lw = lengthBE%widthCE
    lh = lengthBE%heightCE
    wl = widthBE%lengthCE
    ww = widthBE%widthCE
    wh = widthBE%heightCE
    hl = heightBE%lengthCE
    hw = heightBE%widthCE
    hh = heightBE%heightCE
    # calculate the open space for all options, then choose the best one
    options = [('L*W*H', ll*ww*hh), ('W*L*H', lw*wl*hh), ('LxH*W', ll*wh*hw), ('HxL*W', lh*wl*hw), ('WxH*L', lw*wh*hl), ('HxW*L', lh*ww*hl)];
    length_margin = dict([ ('L', ll), ('W', lw), ('H',ll)]);
    width_margin = dict([ ('L', wl), ('W', ww),('H', wh)]);
    height_margin = dict([('L', hl), ('W', hw),('H', hh)])
    dict_options = dict(options)
    # TODO: What do we do in case of multiple options? 
    # (I think this works fine, because the order of options is exactly the preference we would expect)
    key_min = min(dict_options.keys(), key=(lambda k: dict_options[k]))
    key_length = key_min[0:1];
    key_width = key_min[2:3];
    # get the height dimension byremoving the length and widht dimension
    dimensions = (['L', 'W', 'H']);
    dimensions.remove(key_length);
    dimensions.remove(key_width);
    key_height = dimensions[0];
    return {'NASANbr': NASANbr,
            'Orientation': key_min[0:5], 
            'MarginLengthInMM':length_margin[key_length], 
            'MarginWidthInMM': width_margin[key_width], 
            'MarginHeightInMM': height_margin[key_height] }

def get_row_orientation( row ):
    NASANbr = row.NASANbr
    lengthCE = row['LengthCEinMM']
    widthCE = row['WidthCEinMM']
    heightCE = row['HeightCEinMM']
    lengthBE = row['LengthBEinMM']
    widthBE = row['WidthBEinMM']
    heightBE = row['HeightBEinMM']
    result = get_orientation( NASANbr, lengthCE, widthCE, heightCE, lengthBE, widthBE, heightBE)
    return result



def getdimensions(df):
    df_result = df;
    df_result['length_dimension'] = df_result.Orientation.apply( lambda x: x[0:1])
    df_result['width_dimension'] = df_result.Orientation.apply( lambda x: x[2:3])
    df_result['height_dimension'] = df_result.Orientation.apply( lambda x: x[4:5])
    return df_result;


# Derive the stackability
def get_stackability( heightCE, heightBE):
    result = heightBE/heightCE >= 2
    return result
def get_row_stackability(row):
    heightCEinMM = row['LengthCEinMM']*(row['height_dimension'] == "L") + \
                                row['WidthCEinMM']*(row['height_dimension'] == "W") + \
                                row['HeightCEinMM']*(row['height_dimension'] == "H")
    heightBEinMM = row['HeightBEinMM']
    return get_stackability(heightCEinMM, heightBEinMM)

# %md #2. Determine all possible BE variants

# define functions to calculate all BE options
def prime_factors(n):
    # Get prime numbers of nr BE's
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def diff_list(basis, l):
    # remove all elements in list basis that are in list l, 
    # but only once per element
    result = basis.copy();
    for el in l:
        result.remove(el);
    return result;

def get_BE_options(BEsize):
    # get the prime factors and add 1 twice, 
    # so that we can also look at options like 1x1xBEsize
    factors = [1,1] + prime_factors(BEsize);
    # start with an empty df with three columns for the nr of CE in 3 dimensions
    options = pd.DataFrame(columns=['LengthInNbrCE', 'WidthInNbrCE', 'HeightInNbrCE']);
    # we will now split the factors into three sets: One set for each dimension
    # the product of the factors in each set will be the length in CE

    # we start with the factors for LengthInNrCE

    # select a subset of at most len(factors)-2 numbers from the factors, 
    # so that we have at least two left for the width and height
    for i in range(1, len(factors)-1):
        lst_length = list(itertools.combinations(factors,i));
        for l_length in lst_length:
            # for each possible set of factors, we also determine the remaining set
            # and we do the same trick: we make a list of possible set of factors for WidthInNrCE
            remaining = diff_list(factors, l_length);
            for i in range(1, len(remaining)):
                # for the remaining
                lst_width = list(itertools.combinations(remaining, i))
                for l_width in lst_width:
                    # get the remaining factors, these are left for HeightInNrCE
                    l_height =  diff_list(remaining,l_width)

                    options = options.append( {'LengthInNbrCE':np.prod(l_length), 
                                               'WidthInNbrCE': np.prod(l_width), 
                                               'HeightInNbrCE':np.prod(l_height)}, 
                                             ignore_index = True )
    options = options.drop_duplicates()
    options = options.reset_index(drop = True)
    return options;

# apply get_BE_options to get a df with all BE options for one NASANbr
# then calculate the number of CE in the different dimensions for the ASIS situation
# and put that option on top (index 0)
def get_dimensions_asis_row(row):
    result = pd.Series();#dtype='String');
    result['LengthInNbrCE'] = round( row['LengthBEinMM'] / ( row['LengthCEinMM']*(row['length_dimension']=="L" ) + \
                                                             row['WidthCEinMM']*(row['length_dimension']=="W" ) + \
                                                             row['HeightCEinMM']*(row['length_dimension']=="H" ) ) )
    result['WidthInNbrCE'] = round( row['WidthBEinMM']  / ( row['LengthCEinMM']*(row['width_dimension']=="L") + \
                                                            row['WidthCEinMM']*(row['width_dimension']=="W" ) + \
                                                            row['HeightCEinMM']*(row['width_dimension']=="H" ) ) )
    result['HeightInNbrCE'] = round( row['HeightBEinMM'] / ( row['LengthCEinMM']*(row['height_dimension']=="L" ) + \
                                                             row['WidthCEinMM']*(row['height_dimension']=="W" ) + \
                                                             row['HeightCEinMM']*(row['height_dimension']=="H" ) ) )
    return result;

def get_BE_options_and_dimensions_asis_row(row, newNbrCEinBE):
    row_with_dimensions_asis = get_dimensions_asis_row(row);
    df_options = get_BE_options(newNbrCEinBE);
    # make sure the asis situation is on top
    # first copy the current first to the end
    df_options.append(df_options.iloc[0]);
    # then put the asis on top
    df_options.iloc[0] = get_dimensions_asis_row(row);
    # and remove the asis from its old position
    df_options = df_options.drop_duplicates()
    return df_options


def getnewBEdimensions(df):
    # Get the new BE dimensions for all BE variants
    df_result = df;
    
    df_result['LengthBEinMM'] = df_result['LengthCEinMM']*df_result['LengthInNbrCE']*(df_result['length_dimension']=="L")
    df_result['LengthBEinMM'] = df_result['LengthBEinMM'] + \
                                df_result['WidthCEinMM']*df_result['LengthInNbrCE']*(df_result['length_dimension']=='W')
    df_result['LengthBEinMM'] = df_result['LengthBEinMM'] + \
                                df_result['HeightCEinMM']*df_result['LengthInNbrCE']*(df_result['length_dimension']=='H')
    
    df_result['WidthBEinMM'] = df_result['LengthCEinMM'] * df_result['WidthInNbrCE']*(df_result['width_dimension']=='L')
    df_result['WidthBEinMM'] = df_result['WidthBEinMM'] + \
                               df_result['WidthCEinMM']*df_result['WidthInNbrCE']*(df_result['width_dimension']=='W')
    df_result['WidthBEinMM'] = df_result['WidthBEinMM'] + \
                               df_result['HeightCEinMM']*df_result['WidthInNbrCE']*(df_result['width_dimension']=='H')
    
    df_result['HeightBEinMM'] = df_result['LengthCEinMM']*df_result['HeightInNbrCE']*(df_result['height_dimension']=='L')
    df_result['HeightBEinMM'] = df_result['HeightBEinMM'] + \
                                df_result['WidthCEinMM']*df_result['HeightInNbrCE']*(df_result['height_dimension']=='W')
    df_result['HeightBEinMM'] = df_result['HeightBEinMM'] + \
                                df_result['HeightCEinMM']*df_result['HeightInNbrCE']*(df_result['height_dimension']=='H')
    
    df_result['LengthBEinMM'] = df_result['LengthBEinMM'] + df['MarginLengthInMM']
    df_result['WidthBEinMM'] = df_result['WidthBEinMM'] + df['MarginWidthInMM']
    df_result['HeightBEinMM'] = df_result['HeightBEinMM'] + df['MarginHeightInMM']
    return df_result


# Get the possible orientations
def get_orientations(row):
    list_result = [{'length_dimension':'L', 'width_dimension': 'W', 'height_dimension': 'H'}, \
              {'length_dimension':'W', 'width_dimension': 'L', 'height_dimension': 'H'} ]
    if( row['Tiltable'] ):
        list_result = list_result + \
                [{'length_dimension':'L', 'width_dimension': 'H', 'height_dimension': 'W'}, \
                 {'length_dimension':'W', 'width_dimension': 'H', 'height_dimension': 'L'}, \
                 {'length_dimension':'H', 'width_dimension': 'L', 'height_dimension': 'W'},
                 {'length_dimension':'H', 'width_dimension': 'W', 'height_dimension': 'L'} ]
    # make sure asis dimensions go first
    asis_dimensions = {'length_dimension': row['length_dimension'], \
                       'width_dimension': row['width_dimension'],
                       'height_dimension': row['height_dimension']};
    list_result.remove(asis_dimensions);
    list_result.insert(0, asis_dimensions);
    return list_result;
# combine the orientations and BE options
def get_all_options(row, newNbrCEinBE):
    list_orientations = get_orientations(row);
    df_orientations = pd.DataFrame(list_orientations);
    df_orientations['NASANbr'] = row['NASANbr'];
    df_orientations['Orientation'] = (df_orientations['length_dimension']) + 'x' \
                                    + (df_orientations['width_dimension']) + 'x' \
                                    + (df_orientations['height_dimension']);
    df_start = pd.DataFrame([row]).drop(['length_dimension', 'width_dimension', 'height_dimension', 'Orientation'], 1)
    df_orientations = df_start.merge(df_orientations, left_on = 'NASANbr', right_on = 'NASANbr', how = 'outer')

    df_options = get_BE_options_and_dimensions_asis_row(row, newNbrCEinBE);
    df_options['NASANbr'] = row['NASANbr'];
    df_options = df_orientations.merge(df_options, left_on = 'NASANbr', right_on = 'NASANbr', how = 'inner')
    return df_options;

#%md # 3. Do some simple checks to find out if the different BE variants are allowed


def get_reason_not_valid_row(df_row, maxPalletHeightInMM, maxWeightBEinKG):
    # here we do all the checks on the input data, 
    # so all checks that do not depend on the new BE dimensions
    df_row['ReasonNotValid'] = '';
    if(df_row['WidthCEinMM'] == 0):
        df_row['ReasonNotValid'] = 'Width of CE is 0.';
    if(df_row['LengthCEinMM'] == 0):
        df_row['ReasonNotValid'] = 'Length of CE is 0.';
    if(df_row['HeightCEinMM'] == 0):
        df_row['ReasonNotValid'] = 'Height of CE is 0.';
    if(df_row['LengthInNbrCE']*df_row['WidthInNbrCE']*df_row['HeightInNbrCE'] != df_row['NbrCEinBE']):
        df_row['ReasonNotValid'] = 'Number of CE asis '+ str(df_row['NbrCEinBE']) + ' does not fit in BE.';
    if( df_row['HeightBEinMM'] > maxPalletHeightInMM or \
        df_row['LengthBEinMM'] > df_row['LengthPalletInMM'] or \
        df_row['WidthBEinMM'] > df_row['WidthPalletInMM']):
        df_row['ReasonNotValid'] = 'Dimensions of BE exceed dimensions of pallet.'
    if( df_row['WeightColloInKG'] > maxWeightBEinKG):
        df_row['ReasonNotValid'] = "Weight of BE "+ str(df_row['WeightColloInKG']) +" kg) exceeds the max. collo weight (" + str(maxWeightBEinKG)+ " kg )."
    
    return df_row;

def get_reason_not_valid(df, maxPalletHeightInMM, maxWeightBEinKG):
    df_result = df.apply( lambda row: get_reason_not_valid_row(row, maxPalletHeightInMM, maxWeightBEinKG), axis = 1)
    return df_result;


def get_reason_not_allowed_row(df_row):
    # here we check if the new BE dimensions are allowed
    df_row['ReasonNotAllowed'] = '';
    if(df_row['LengthBEinMM'] < df_row['WidthBEinMM']):
        df_row['ReasonNotAllowed'] = 'Length of BE is ' + str(df_row['LengthBEinMM']) + ' mm, which is ' + \
        str(df_row['WidthBEinMM']-df_row['LengthBEinMM']) + ' mm smaller than the width of the BE ('  + \
        str(df_row['WidthBEinMM']) + ' mm).';
    df_row['HeightWidthRatioBE'] = df_row['HeightBEinMM']/df_row['WidthBEinMM'];
    if( df_row['HeightWidthRatioBE'] > 2.5):
        df_row['ReasonNotAllowed'] = 'Height of BE is ' + str(df_row['HeightWidthRatioBE']) + ' times the width of the BE.';
    if(df_row['LengthBEinMM'] < 120):
        df_row['ReasonNotAllowed'] = 'Length of BE ('+ str(df_row['LengthBEinMM']) + ' mm) is smaller than 120 mm.';
    if(df_row['WidthBEinMM'] < 80):
        df_row['ReasonNotAllowed'] = 'Width of BE ('+ str(df_row['WidthBEinMM']) + ' mm) is smaller than 80 mm.';
    if(df_row['LengthBEinMM'] > df_row['LengthPalletInMM']):
        df_row['ReasonNotAllowed'] = 'Length BE ('+ str(df_row['LengthBEinMM']) + ' mm) exceeds length pallet ('+ str(df_row['LengthPalletInMM']) + 'mm).'
    if(df_row['WidthBEinMM'] > df_row['WidthPalletInMM']):
        df_row['ReasonNotAllowed'] = 'Width BE ('+ str(df_row['WidthBEinMM']) + ' mm) exceeds width pallet ('+ str(df_row['WidthPalletInMM']) + 'mm).'
    return df_row
 
def get_reason_not_allowed(df):
    df_result = df.apply( lambda row: get_reason_not_allowed_row(row), axis = 1)
    return df_result

    

%md # Pallet placer
# This code takes as input a BE (besteleenheid) with the corresponding sizes. The output consists of:
# - the number of BE on the 2D top sight of a pallet
# - the location and orientation of each item on the pallet

# The main usage of this script is by calling the function 'pallet_stacker(...)'.

# *created by Frans de Ruiter (CQM, March 30, 2020)*

# For algorithms used, download the pdf: http://pds25.egloos.com/pds/201504/21/98/RectangleBinPack.pdf


%md ## The bin pack function

#     (BE_count, coverage, locations) = bin_packer(  BE_width, 
#                                                     BE_length, 
#                                                     pallet_width, 
#                                                     pallet_length, 
#                                                     rotation_allowed = True, 
#                                                     guillotine_cut_required = True,
#                                                     fulleffort = True)

# **Input**:
# - `BE_width` (width of BE)
# - `BE_length` (length of BE)
# - `pallet_width`
# - `pallet_length` (
# - `rotation_allowed`
# - `guillotine_cut_required`
# - `fulleffort`

# The first four are self-explanatory. The only thing is that for sake of consistency we assume that length > width for both the BE and the pallet. `rotation_allowed` indicates whether it is allowed to rotate the BE, `guillotine_cut_required` sets whether the 2D Bin packing pattern should require a guillotine cut ([click here for wiki explanation](https://en.wikipedia.org/wiki/Guillotine_problem)). Lastly, if `fulleffort` is true, then many 2D binpacking algorithms are called, and the best result among them is picked.

# **Output**
# - `BE_count` (integer) number of BE on pallet
# - `coverage` (float in \[0,1\]) describing the coverage of the pallet surface
# - `locations` (list) each entry in the list contains in order:
#     - x_coordinate
#     - y_coordinate
#     - orientation (0 = original, 1 = 90 degrees rotated)

# Python implementation of bin packing algorithm with homogeneous item.
def bin_packer(BE_width: float,
              BE_length: float,
              pallet_width: float,
              pallet_length: float,
              rotation_allowed: bool = True,
              guillotine_cut_required: bool = True,
              fulleffort: bool = True):
    
    # Some basic input checks
#     if BE_length < BE_width:
#         raise Exception("BE_length is wider than BE_width. Please give items such that BE_width >= BE_length.")
    if pallet_length <  pallet_width:
        raise Exception("pallet_length is wider than pallet_width. Please give items such that pallet_width >= pallet_length.")        
    if BE_length > pallet_length or BE_width > pallet_width:
        raise Exception("BE dimensions exceed pallet dimensions.")
        
    # Determine maximum number of rectangles possible
    area_pallet = int(pallet_length * pallet_width)
    area_BE = int(BE_length * BE_width)
    max_BE,min_area_uncovered = divmod(area_pallet,area_BE)
    
    # create potential algorithm list
    binpacking_algo_list = [maxrects.MaxRectsBssf,
                       maxrects.MaxRectsBl,
                       maxrects.MaxRectsBaf,
                       maxrects.MaxRectsBlsf]
    
    if guillotine_cut_required == True:   
        # list all binpacking algorithms with guillotine cut
        binpacking_algo_list = [guillotine.GuillotineBssfSas,
                           guillotine.GuillotineBssfLas,
                           guillotine.GuillotineBssfSlas,
                           guillotine.GuillotineBssfLlas,
                           guillotine.GuillotineBssfMaxas,
                           guillotine.GuillotineBssfMinas,
                           guillotine.GuillotineBlsfSas,
                           guillotine.GuillotineBlsfLas,
                           guillotine.GuillotineBlsfSlas,
                           guillotine.GuillotineBlsfLlas,
                           guillotine.GuillotineBlsfMaxas,
                           guillotine.GuillotineBlsfMinas,
                           guillotine.GuillotineBafSas,
                           guillotine.GuillotineBafLas,
                           guillotine.GuillotineBafSlas,
                           guillotine.GuillotineBafLlas,
                           guillotine.GuillotineBafMaxas,
                           guillotine.GuillotineBafMinas]
    
    # Consider two possible starting positions: rotated or not
    rect_options = [(BE_width,BE_length), (BE_length,BE_width)]
    
    # Consider only on algorithm if you do not do a full effort
    if fulleffort == False:
        binpacking_algo_list = [binpacking_algo_list[0]]
    
    # Initialize best count
    BE_count_best = 0
    coverage = 0
    locations = []
    
    for rect in rect_options:
        for binpacking_algo in binpacking_algo_list:
    
            # add packer object
            # class newPacker([, mode][, bin_algo][, pack_algo][, sort_algo][, rotation])
            packer = newPacker(pack_algo=binpacking_algo,
                                rotation=rotation_allowed
                              )

            # Add the rectangles to packing queue
            for i in range(0,max_BE):
                packer.add_rect(*rect)

            # Add the bin (i.e. pallet) where the rectangles will be placed
            packer.add_bin(*(pallet_width, pallet_length))

            # Start packing (see github doc link on top of file for explanation)  
            packer.pack()

            # Extract results
            BE_count  = len(packer[0])
            
            # update best if algorithm is better
            if BE_count == max_BE or BE_count > BE_count_best:
                BE_count_best = BE_count
                
                # update coverage: area covered by BE items divided by total area of pallet
                coverage  = ( BE_count * BE_length * BE_width ) / area_pallet
                
                # Save locations for visualization purposes and include whether or not the packag is rotated
                locations = [(rect.x,rect.y,(rect.width == BE_width)) for rect in packer[0]]

    return (BE_count_best, coverage, locations)
    

def bin_packer_row(row):
    result = bin_packer(row['WidthBEinMM'], row['LengthBEinMM'], row['WidthPalletInMM'], row['LengthPalletInMM'], row['Tiltable'], True, True)
    return result;
def bin_packer_df(df):
    result = df.apply(lambda row: pd.Series(bin_packer_row(row)), axis = 1);
    return result;


def palletDimensions(BE_width: float,
                     BE_length: float,
                     BE_height: float, 
                     BE_weight: float,
                     BE_per_layer: int,
                     max_pallet_height: float,
                     max_pallet_weight: float
                      ):
    # max layers according to height restrictions:
    max_layers_height = divmod(max_pallet_height * 1000,BE_height)[0]
    
    # max layers according to weight restrictions:
    max_layers_weight = divmod(max_pallet_weight,(BE_weight * BE_per_layer))[0]
        
    # return minimum of both    
    layers = min(max_layers_height, max_layers_weight)
    weight = BE_per_layer * layers * BE_weight
    height = layers * BE_height / 1000
    netVolume   = BE_width * BE_length * BE_height * 10**(-9)
    stackVolume = 0 #TODO!
    grossVolume = netVolume + stackVolume
    return (int(layers), weight, height, netVolume, stackVolume, grossVolume)

def pallet_dimensions_row(row, MaxPalletHeightInMM, MaxPalletWeightInKG):
  result = palletDimensions( row['LengthBEinMM'],
                             row['WidthBEinMM'],
                             row['HeightBEinMM'],
                             row['WeightColloInKG'],
                             row['QuantityUsedPerLayerPallet'],
                             MaxPalletHeightInMM, 
                             MaxPalletWeightInKG )
  
  return result;
def pallet_dimensions_df(df, MaxPalletHeightInMM, MaxPalletWeightInKG):
    result = df.apply(lambda row: pd.Series(pallet_dimensions_row(row, MaxPalletHeightInMM, MaxPalletWeightInKG)), axis = 1);
    return result;


def prepareData():
    df_input = readdata();
    df_orientation = df_input.apply(lambda row: pd.Series(get_row_orientation(row)), axis = 1)
    df_be_input_orientation = df_input.merge(df_orientation, left_on = 'NASANbr', right_on = 'NASANbr')
    df_result = getdimensions(df_be_input_orientation)
    df_result['Stackability'] = df_result.apply( lambda row: get_row_stackability(row), axis = 1);  
    return df_result


def VCF(delivery_stream, col_length, col_width, col_height):
  '''  
  function calculates the volume correction factor (VCF)
  extra percentage of air when building a rolcage with non modulair cases
  '''  
  
  # size rolcage
  rclength=800 
  rcwidth=620  
  
  ColloModPosLength = min( (rclength / col_length) - math.floor( rclength / col_length ), (rcwidth / col_length) - math.floor( rcwidth / col_length) ) 
  ColloModPosWidth  = min( (rclength / col_width ) - math.floor( rclength / col_width  ), (rcwidth / col_width)  - math.floor( rcwidth / col_width ) )
  ColloModNegLength = min( math.ceil(rclength / col_length) - (rclength  / col_length), math.ceil( rcwidth / col_length ) - rcwidth / col_length )
  ColloModNegWidth  = min( math.ceil(rclength / col_width)  - (rclength  / col_width) , math.ceil( rcwidth / col_width )  - rcwidth / col_width  )
  
  ColloModLength = 1 - min( ColloModPosLength , ColloModNegLength)
  ColloModWidth  = 1 - min( ColloModPosWidth  , ColloModNegWidth)
  
  VolumeFactor = 0.55 
  # nog aan te passen per assortimentsgroep
         
  if delivery_stream  == 1 : Intercept=0.68 # houdbaar RDC
  elif delivery_stream  == 9 : Intercept=0.54 # houdbaar LDC
  elif delivery_stream  in (2,11,96) : Intercept=0.34 # Vers RVC, Zeewolde en XPO Nieuwegein
  else: Intercept=0.68
  
  NettoVolume = col_length * col_width * col_height /1000000
  
  StackVolume = Intercept + NettoVolume * (VolumeFactor - (0.34 * ColloModLength) - (0.15*ColloModWidth)) 
    
  VCF = min(1 + max(0,StackVolume / NettoVolume ), 1.35)
  
  return round(VCF, 3)


def get_nasanbrs(path_assortment, format_assortment_group, format_assortment_group19):
  '''
  This function returns a dataframe that contains all relevant nasanumbers for a specific formatassortmentgroup in formatnumber 6 and 20 and a specific formatassortmentgroup in formatnumber 19.
  output is dataframe with 1 column: NASANbr
  '''
  df_nasa = (spark.read.format('delta').load(path_assortment)
            .where(((F.col('FormatAssortmentGroupNbr')==format_assortment_group) & (F.col('FormatNbr').isin(6, 20)))  |
                   ((F.col('FormatAssortmentGroupNbr')==format_assortment_group19) & (F.col('FormatNbr').isin(19)))
                  )
            .select('NASANbr')
            .drop_duplicates()
           )
  
  return df_nasa

udf_get_VCF = F.udf(VCF, FloatType())


def generateBEoptions(row, newBEsize, maxPalletHeightInMM, maxPalletWeightInKG, maxWeightBEinKG):   
    df_options = get_all_options(row, newBEsize)
    df_options.NrCEinBE = newBEsize
    df_options_and_dimensions = getnewBEdimensions(df_options)
    df_options_dimensions_valid = get_reason_not_valid(df_options_and_dimensions, maxPalletHeightInMM, maxWeightBEinKG)
    df_result = get_reason_not_allowed(df_options_dimensions_valid)
    df_result.index.names = ['option'];
    df_result = df_result[df_result.ReasonNotAllowed == ''];
    df_result = df_result[df_result.ReasonNotValid == ''];
    ds_binpacking = bin_packer_df(df_result);
    df_binpacking = pd.DataFrame(ds_binpacking);
    df_binpacking.columns = ['QuantityUsedPerLayerPallet', 'CoverageBEonPalletLayerInPct', 'locations'];
    df_binpacking.CoverageBEonPalletLayerInPct = 100*df_binpacking.CoverageBEonPalletLayerInPct;
    df_result = df_result.merge(df_binpacking, left_on = 'option', right_on = 'option', how = 'outer')
    
    ds_palletdimensions = pallet_dimensions_df(df_result, maxPalletHeightInMM, maxPalletWeightInKG);
    df_palletdimensions = pd.DataFrame(ds_palletdimensions);
    df_palletdimensions.columns = ['NbrUsedPalletLayers', 'PalletWeightInKG', 'UsedHeightPalletInMM', 'NettVolumeInM3', 'StackVolumeInM3', 'GrossVolumeInM3'];
    
    df_result.LengthBEinMM = df_result.LengthBEinMM.astype(float);
    df_result.WidthBEinMM = df_result.WidthBEinMM.astype(float);
    df_result.HeightBEinMM = df_result.HeightBEinMM.astype(float);
                 
    return df_result;