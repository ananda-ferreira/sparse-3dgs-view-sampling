import os

import numpy as np
from dataset_readers_helper import read_extr_and_intr, readColmapCameras

# should take (train) cam_infos as input, making dataset_path and read_cam_infos() redundant
# cs should be mapped to cam_infos in sampler, as params will be from og 3dgs without cs
class Sampler:
    
    viewCount : int
    cam_infos : list
    cam_infos_cd : list
    sparse_views: list[tuple[str]]

    def __init__(self, viewCount: int, cam_infos: list[dict]):
        self.viewCount = viewCount
        self.cam_infos = cam_infos
        self.cam_infos_cd = [{"C":self._cam_cs(c.R, c.T), "img_name":c.image_name} for c in cam_infos]

    def _cam_cs(self, R: np.ndarray, T:np.ndarray):
        """Returns: camera centers based on rotation and translation matrices. See Colmap documentation."""
        return - R @ T # new transpose again?

    def get_cs(self):
        """ Returns: a list of camera centers (3D np arrays) """
        return [c["C"] for c in self.cam_infos_cd]
    
    def get_sparse_cs(self):
        """ Returns: a list of tuples, where each tuple holds 2 camera centers (3D np arrays) corresponding to the pairs of images in views. """
        return [tuple([c["C"] for c in self.cam_infos_cd if c["img_name"] in vs]) for vs in self.sparse_views]
        
    # def get_sparse_cs(self, views:list[tuple]):
    #     """ Returns: a list of tuples, where each tuple holds 2 camera centers (3D np arrays) corresponding to the pairs of images in views. """
    #     return [tuple([c["C"] for c in self.cam_infos_cd if c["img_name"] in vs]) for vs in views]

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
    sampler = Sampler(4, cam_infos)
