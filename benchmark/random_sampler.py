import os, sys
from random import sample
import numpy as np
from sampler import Sampler
from plot import highlight_sparse_views

from dataset_readers_helper import read_extr_and_intr, readColmapCameras

class RandomSampler(Sampler):

    def __init__(self, viewCount: int, cam_infos: list):
        super().__init__(viewCount, cam_infos)

    def sample(self):
        sparse_idxs = sorted(sample(range(len(self.cam_infos)), self.viewCount))
        self.sparse_views = [tuple([self.cam_infos[i].image_name for i in sparse_idxs])]
        
        # if not self.recalibrate: 
        #     print("not recalibrating...")
        #     # rewrite images.txt, see sparseGS
        #     # rerun triangulation, see sparseGS; might break due to lack of corresp 
        # else: 
        #     print("recalibrating...")
        #     # colmap feature_extractor # 3dgs, sparsegs
        #     # colmap exhaustive_matcher # 3dgs, sparsegs
        #     # colmap mapper # 3dgs, 
        #     # colmap model_converter # cenverts between txt and bin # corgs, sparsegs
        #     # colmap point_triangulator # sparsegs
        #     # colmap image_undistorter # 3dgs, sparsegs
        
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]

def read_cam_infos(dataset_path):
    extr, intr = read_extr_and_intr(dataset_path)
    depths=""
    cam_infos_unsorted = readColmapCameras(
        cam_extrinsics=extr, cam_intrinsics=intr, depths_params=None,
        images_folder=os.path.join(dataset_path, "images"), 
        depths_folder=os.path.join(dataset_path, depths) if depths != "" else "", test_cam_names_list=[])
    return sorted(cam_infos_unsorted.copy(), key = lambda x : x.image_name)
    
if __name__ == "__main__":
    print("RUNNING RANDOM SAMPLER")
    # fix wokring directory later
    # source_path = os.path.join("../data", "tandt", "train")
    # source_path = os.path.join("../data", "db", "playroom")
    source_path = os.path.join("../data", "dtu_corgs", "scan8")

    cam_infos = read_cam_infos(source_path)
    sampler = RandomSampler(4, cam_infos)
    sparse_cam_infos = sampler.sample()

    highlight_sparse_views(sampler.get_cs(), sampler.get_sparse_cs()[0])