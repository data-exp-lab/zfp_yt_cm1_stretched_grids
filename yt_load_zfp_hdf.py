import zfpy 
import h5py 
import hdf5plugin 
import numpy as np

ds = h5py.File('/home/chavlin/hdd/data/yt_data/yt_sample_sets/cm1_zfp_compressed/mkow075-ens-db620.00790800.nc')

print(np.mean(ds['dbz'][:]))



