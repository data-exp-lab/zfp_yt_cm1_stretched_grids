import h5py 
import yt 
import hdf5plugin
from yt.sample_data.api import lookup_on_disk_data
from yt.utilities.decompose import decompose_array, get_psize
from yt.utilities.logger import ytLogger as mylog
from typing import Optional, Union, List 
import numpy as np
import sys

def load_cm1_zfp(
    fn: Union[str, "os.PathLike[str]"],
    root_node: Optional[str] = "/",
    fields: Optional[List[str]] = None,
    bbox: np.ndarray = None,
    nchunks: int = 0,
    dataset_arguments: Optional[dict] = None,
):
    
    dataset_arguments = dataset_arguments or {}    

    def _read_data(handle, root_node):
        def _reader(grid, field_name):
            ftype, fname = field_name
            si = grid.get_global_startindex()
            ei = si + grid.ActiveDimensions
            return handle[root_node][fname][0, si[0] : ei[0], si[1] : ei[1], si[2] : ei[2]]

        return _reader

    fn = str(lookup_on_disk_data(fn))
    handle = h5py.File(fn, "r")
    
    if bbox is None:
        bbox = []
        dbz_shape = []
        for dim in ["zh", "yh", "xh"]: 
            bbox.append([np.min(handle[dim]), np.max(handle[dim])])
        bbox = np.array(bbox)
        mylog.info(f"calculated bounding box, {bbox}")
        # bbox = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
        # mylog.info("Assuming unitary (0..1) bounding box.")
    
    reader = _read_data(handle, root_node)
    if fields is None:
        fields = list(handle[root_node].keys())
        mylog.debug("Identified fields %s", fields)
    shape = handle[root_node][fields[0]].shape[1:]
    if nchunks <= 0:
        # We apply a pretty simple heuristic here.  We don't want more than
        # about 64^3 zones per chunk.  So ...
        full_size = np.prod(shape)
        nchunks = full_size // (64**3)
        mylog.info("Auto-guessing %s chunks from a size of %s", nchunks, full_size)
    grid_data = []
    psize = get_psize(np.array(shape), nchunks)
    left_edges, right_edges, shapes, _ = decompose_array(shape, psize, bbox)
    for le, re, s in zip(left_edges, right_edges, shapes):
        data = {_: reader for _ in fields}
        data.update({"left_edge": le, "right_edge": re, "dimensions": s, "level": 0})
        grid_data.append(data)
    return yt.load_amr_grids(grid_data, shape, bbox=bbox, **dataset_arguments)



def test_callable(fname, nchunks=0):
    ds_args = dict(geometry=("cartesian", ("z", "y", "x")),
                   length_unit="km")
    ds = load_cm1_zfp(fname,
                  fields=["dbz", "vortmag"],
                  dataset_arguments = ds_args, 
                  nchunks = nchunks)

    slc = yt.SlicePlot(ds, "z", ("stream", "dbz"), origin="native")
    slc.set_log(("stream", "dbz"), False)
    slc.save(f"dbz_slice_from_callable_{nchunks}.png")
    

def test_frontend(fname):
    ds = yt.load(fname)
    slc = yt.SlicePlot(ds, "z", ("cm1", "dbz"), origin="native")
    slc.set_log(("cm1", "dbz"), False)
    slc.save("dbz_slice_from_frontend.png")


if __name__ == "__main__":
    fname = "cm1_zfp_compressed/mkow075-ens-db620.00790800.nc"
    print(sys.argv)
    test_type = int(sys.argv[1])
    print(test_type)
    if test_type == 0:
        if len(sys.argv) == 3:
            nchunks = int(sys.argv[2])
        else:
            nchunks = 0
        print(f"testing callable with nchunks={nchunks}")
        test_callable(fname, nchunks=nchunks)
    else:
        print("testing frontend")
        test_frontend(fname)
