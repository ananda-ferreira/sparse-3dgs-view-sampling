import os, sys
from random import sample
from sampler import Sampler
from plot import highlight_sparse_views
from utils_sparse import read_cam_infos

# cam_infos used for return
class RandomSampler(Sampler):

    def __init__(self, viewCount: int, cam_infos: list):
        super().__init__(viewCount, cam_infos)

    def sample(self):
        sparse_idxs = sorted(sample(range(len(self.cam_infos_ext)), self.viewCount))
        self.sparse_views = [tuple([self.cam_infos_ext[i]["img_name"] for i in sparse_idxs])]
    
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]

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