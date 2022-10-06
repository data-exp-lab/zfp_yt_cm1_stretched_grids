This repo contains some explatory work on using yt to load zfp-compressed lofs-cm1 netcdf files, with and without some of yt's new (as of 4.1.0) functionality.

The notebooks contain info on all the other files: 

* [zfp_cm1_yt_demo.ipynb](https://github.com/data-exp-lab/zfp_yt_cm1_stretched_grids/blob/main/zfp_cm1_yt_demo.ipynb)  -- using yt's existing nc_cm1 frontend, and using yt's new (as of 4.1.0) callable functionality to map data directly to an open hdf handle
* [zfp_cm1_stretched_grids.ipynb](https://github.com/data-exp-lab/zfp_yt_cm1_stretched_grids/blob/main/zfp_cm1_stretched_grids.ipynb) -- using yt's new (as of 4.1.0) stretched grid functionality. involves some in-memory trilinear interpolation on the user side 
* [stretched_from_node_points.ipynb](https://github.com/data-exp-lab/zfp_yt_cm1_stretched_grids/blob/main/stretched_from_node_points.ipynb) -- toy problem for considering how to build cells from vertex-centered data.
