
import os

from benchmark.plot import highlight_sparse_views
from benchmark.sampler import Sampler

from dataset_readers_helper import read_extr_and_intr, readColmapCameras

class CoverageSampler(Sampler):

    view_dirs: list

    def __init__(self, viewCount, cam_infos: list):
        super().__init__(viewCount, cam_infos)

    def sample():
        return # filtered cam_infos
    
    def calc_view_dirs(self):
        return ()


def read_cam_infos(dataset_path):
    extr, intr = read_extr_and_intr(dataset_path)
    depths=""
    cam_infos_unsorted = readColmapCameras(
        cam_extrinsics=extr, cam_intrinsics=intr, depths_params=None,
        images_folder=os.path.join(dataset_path, "images"), 
        depths_folder=os.path.join(dataset_path, depths) if depths != "" else "", test_cam_names_list=[])
    return sorted(cam_infos_unsorted.copy(), key = lambda x : x.image_name)
    
if __name__ == "__main__":
    print("RUNNING SAMPLER")
    source_path = os.path.join("..","data", "dtu_corgs", "scan8")

    cam_infos = read_cam_infos(source_path)
    sampler = CoverageSampler(4, cam_infos)

