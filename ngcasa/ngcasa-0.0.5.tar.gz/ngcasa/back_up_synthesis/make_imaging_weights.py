#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#Allow setting of padding
#Setting to keep grid or correcting
#normalizarion parameters (flat sky, flat noise etc)
#mosaic parameters, etc

import numpy as np

#Usage, to_disk first iteration (data is subselected). For Subsequent calculations use append.
#If not needed delete subfolder folder
def make_imaging_weights(vis_dataset, user_imaging_weights_parms,user_storage_parms):
    """
    Grids visibilities from Visibility Dataset and returns dirty Image Dataset.
    If to_disk is set to true the data is saved to disk.
    Parameters
    ----------
    vis_xds : xarray.core.dataset.Dataset
        input Visibility Dataset
    user_imaging_weights_parms : dictionary
          keys ('chan_mode','imsize','cell','oversampling','support','to_disk','outfile')
    Returns
    -------
    dirty_image_xds : xarray.core.dataset.Dataset

    """
    import time
    import math
    import xarray as xr
    import dask.array as da
    import matplotlib.pylab as plt
    import dask.array.fft as dafft
    import dask
    import copy, os
    from numcodecs import Blosc
    from itertools import cycle
    import zarr
    
    from .synthesis_utils._cngi_check_parameters import _check_gridder_params
    from .synthesis_utils._standard_grid import _graph_standard_grid
    from .synthesis_utils._gridding_convolutional_kernels import _create_prolate_spheroidal_kernel, _create_prolate_spheroidal_kernel_1D
    from .synthesis_utils._cngi_funcs import _remove_padding, _add_data_variable_to_dataset, _to_storage
    
    #If per_chan_weight is True and grid_parms['chan_mode'] = 'continuum' then say per_chan_weight is no set to false
    #Add parameter checking and default settings
    #If append set outfile to file path specified in vis_dataset
    imaging_weights_parms =  copy.deepcopy(user_imaging_weights_parms)
    storage_parms =  copy.deepcopy(user_storage_parms)
    
    #Check if weight or weight spectrum present
    #If both default to weight spectrum
    #If none create new
    weight_present = 'WEIGHT' in vis_dataset.data_vars
    weight_spectrum_present = 'WEIGHT_SPECTRUM' in vis_dataset.data_vars
    all_dims_dict = vis_dataset.dims
    vis_data_dims = vis_dataset.DATA.dims
    vis_data_chunksize = vis_dataset.DATA.data.chunksize
    
    if weight_present and weight_spectrum_present:
        print('Both WEIGHT and WEIGHT_SPECTRUM data variables found, will use WEIGHT_SPECTRUM to calculate IMAGING_WEIGHT')
        imaging_weight = _match_array_shape(vis_dataset.WEIGHT_SPECTRUM,vis_dataset.DATA)
    elif weight_present:
        print('WEIGHT data variable found, will use WEIGHT to calculate IMAGING_WEIGHT')
        imaging_weight = _match_array_shape(vis_dataset.WEIGHT,vis_dataset.DATA)
    elif weight_spectrum_present:
        print('WEIGHT_SPECTRUM  data variable found, will use WEIGHT_SPECTRUM to calculate IMAGING_WEIGHT')
        imaging_weight = _match_array_shape(vis_dataset.WEIGHT_SPECTRUM,vis_dataset.DATA)
    else:
        print('No WEIGHT or WEIGHT_SPECTRUM data variable found,  will assume all weights are unity to calculate IMAGING_WEIGHT')
        imaging_weight = da.ones(vis_dataset.DATA.shape,chunks=vis_dataset.data.chunksize)
    
    if imaging_weights_parms['weighting'] == 'natural':
        print('natural,not a lot to do')
    elif imaging_weights_parms['weighting'] == 'uniform':
        print('uniform')
        print('$$$$$$$$$$$$$$$$$$')
        print(imaging_weight.compute())
        print('$$$$$$$$$$$$$$$$$$')
        vis_dataset['IMAGING_WEIGHT'] = xr.DataArray(imaging_weight, dims=vis_dataset.DATA.dims)
        calc_briggs_weights(vis_dataset,imaging_weights_parms)
        print(vis_dataset.IMAGING_WEIGHT.data.compute())
        print('$$$$$$$$$$$$$$$$$$')
        
    elif imaging_weights_parms['weighting'] == 'briggs':
        print('briggs')
        
        
    storage_parms['function_name'] = 'make_imaging_weights'
    
    if  storage_parms['to_disk']:
        if os.path.exists(storage_parms['outfile']) and not(storage_parms['overwrite']):
            print('Adding IMAGING_WEIGHT to ', storage_parms['outfile'])
            
            vis_group = zarr.open_group(storage_parms['outfile'],mode='r')
            storage_parms['array_dimensions'] = vis_group['DATA'].attrs["_ARRAY_DIMENSIONS"]
            return _add_data_variable_to_dataset(imaging_weight,storage_parms)
        else:
            if storage_parms['overwrite']:
                print('Overwriiting ', storage_parms['outfile'])
            vis_dataset['IMAGING_WEIGHT'] = xr.DataArray(imaging_weight, dims=vis_dataset.DATA.dims)
            return _to_storage(vis_dataset, storage_parms)
    
    #vis_dataset['IMAGING_WEIGHT'] = xr.DataArray(imaging_weight, dims=vis_dataset.DATA.dims)
    return vis_dataset
            
def _match_array_shape(array_to_reshape,array_to_match):
    # Reshape in_weight to match dimnetionality of vis_data (vis_dataset.DATA)
    # The order is assumed the same (there can be missing). array_to_reshape is a subset of array_to_match
    import dask.array as da
    import numpy as np
    
    match_array_chunksize = array_to_match.data.chunksize
    
    reshape_dims = np.ones(len(match_array_chunksize),dtype=int)  #Missing dimentions will be added using reshape command
    tile_dims = np.ones(len(match_array_chunksize),dtype=int) #Tiling is used so that number of elements in each dimention match
    
    
    array_to_match_dims = array_to_match.dims
    array_to_reshape_dims = array_to_reshape.dims
    
    for i in range(len(match_array_chunksize)):
        if array_to_match_dims[i] in array_to_reshape_dims:
            reshape_dims[i] = array_to_match.shape[i]
        else:
            tile_dims[i] = array_to_match.shape[i]
            
    print('reshape dim', reshape_dims)
    print('tile dim', tile_dims)
    return da.tile(da.reshape(array_to_reshape.data,reshape_dims),tile_dims).rechunk(match_array_chunksize)



def calc_briggs_weights(vis_dataset,imaging_weights_parms):
    import dask.array as da
    import xarray as xr
    from .synthesis_utils._standard_grid import _graph_standard_grid, _graph_standard_degrid
    from .synthesis_utils._standard_grid import _standard_imaging_weight_degrid_numpy_wrap
    
    print(imaging_weights_parms)
    
    dtr = np.pi / (3600 * 180)
    grid_parms = {}
    
    grid_parms['chan_mode'] = imaging_weights_parms['chan_mode']
    
    #Match CASA fortran
    #grid_parms['imsize_padded'] =  np.array([240,480]) #calculate using largest value
    #grid_parms['cell'] = dtr*np.array([-0.08, 0.08]) #signs match casa fortran
    
    #Match CASA C++
    grid_parms['imsize_padded'] =  imaging_weights_parms['imsize'] #np.array([200,400]) #calculate using largest value #do not need to pad since no fft
    grid_parms['cell'] = imaging_weights_parms['cell'] #dtr*np.array([0.08, -0.08]) #signs match casa weights
    grid_parms['do_imaging_weight'] = True
    
    grid_parms['oversampling'] = 0
    grid_parms['support'] = 1
    grid_parms['do_psf'] = True
    #implement grid_parms['complex_grid'] = False
    grid_parms['do_imaging_weight'] = True
    #grid_parms['per_chan_weight'] = gridding_weights_parms['per_chan_weight']
    
    cgk_1D = np.ones((1))
    
    print('cgk_1D is ',cgk_1D)
    vis_dataset
    
    
    grid_of_imaging_weights, sum_weight = _graph_standard_grid(vis_dataset, cgk_1D, grid_parms)
    print(grid_of_imaging_weights)
    
    imaging_weight = _graph_standard_degrid(vis_dataset, grid_of_imaging_weights, cgk_1D, grid_parms)
    
    vis_dataset['IMAGING_WEIGHT'] = xr.DataArray(imaging_weight, dims=vis_dataset.DATA.dims)
    
    
    #freq_chan = vis_dataset.coords['chan'].values
    #imaging_weight, sum_weight = _standard_imaging_weight_degrid_numpy_wrap(grid_of_weights[0].compute(), vis_dataset.UVW.data.compute(), grid_weight.compute(), vis_dataset.FLAG_ROW.data.compute(), vis_dataset.FLAG.data.compute(), freq_chan, grid_parms)
    
    #print(imaging_weight)
    '''
    import matplotlib.pylab as plt
    
    print(grid_of_weights[0])
    plt.figure()
    plt.imshow(np.real(grid_of_weights[0][:,:,0,0]))
    plt.colorbar()
    plt.show()
    
    casa_grid  = np.load('/Users/jsteeb/Dropbox/ngcasa/data/casa_data/a_gwt_p_noconj.npy')
    
    plt.figure()
    plt.imshow(casa_grid)
    plt.colorbar()
    plt.show()

    plt.figure()
    plt.imshow(casa_grid - np.real(grid_of_weights[0][:,:,0,0]))
    plt.colorbar()
    plt.show()
    '''
    
