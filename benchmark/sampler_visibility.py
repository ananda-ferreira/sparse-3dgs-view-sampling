import os

import numpy as np

from utils_sparse import maximize_point_cloud_coverage, read_cam_infos
from plot import highlight_sparse_views
from sampler import Sampler

# extr needed for points coverage
# cam_infos used for return
class VisibilitySampler(Sampler):

    extr: list
    unique_pts: list
    pts_shapes: np.ndarray

    def __init__(self, viewCount, cam_infos, extr):
        super().__init__(viewCount, cam_infos)
        
        # sort extr by img name to match cam_infox_ext         
        self.extr = sorted(extr.values(), key = lambda x: x.name)
        
        # get unique pts amd their shape per cam and add to cam_infos_ext
        self.unique_pts, self.pts_shapes = self._unique_pts(self.extr)
        for i,c in enumerate(self.cam_infos_ext):
            c["unique_pts"] = self.unique_pts[i]
            c["pts_shape"] = self.pts_shapes[i]

    def sample(self):
        if self.viewCount < 2:
            return None
        cam_best_cover = np.argmax(self.pts_shapes)
        sparse_view_idxs = maximize_point_cloud_coverage(self.viewCount, self.unique_pts, cam_best_cover)
        
        print(sparse_view_idxs)
        self.sparse_views = [tuple([self.cam_infos_ext[i]["img_name"] for i in sparse_view_idxs])]
        self.sparse_cs = self.get_sparse_cs()
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]
    
    def _unique_pts(self, extr):
        unique_pts, shapes = [], []
        for i, img in enumerate(extr):
            unique = np.unique([p for p in img.point3D_ids if p != -1])
            unique_pts.append(unique)
            shapes.append(unique.shape)
        return unique_pts, np.array(shapes)

if __name__ == "__main__":
    print("RUNNING RANDOM SAMPLER")
    # source_path = os.path.join("../data", "tandt", "train")
    # source_path = os.path.join("../data", "db", "playroom")
    source_path = os.path.join("../data", "dtu_corgs", "scan8")

    cam_infos, extr = read_cam_infos(source_path)
    sampler = VisibilitySampler(6, cam_infos, extr)
    sparse_cam_infos = sampler.sample()

    highlight_sparse_views(sampler.get_cs(), sampler.sparse_cs[0])