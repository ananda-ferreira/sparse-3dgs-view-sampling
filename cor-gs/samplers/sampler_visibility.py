import numpy as np
from samplers.utils_sampler import maximize_point_cloud_visibility
from samplers import Sampler

# extr needed for points coverage
# cam_infos used for return
class VisibilitySampler(Sampler):

    extr: list
    unique_pts: list
    pts_shapes: np.ndarray

    def __init__(self, viewCount, cam_infos, extr: list):
        super().__init__(viewCount, cam_infos)
        
        # sort extr by img name to match cam_infox_ext         
        self.extr = sorted(extr, key = lambda x: x.name)

        # get unique pts amd their shape per cam 
        self.unique_pts, self.pts_shapes = self._unique_pts(self.extr)

    def sample(self):
        if self.viewCount < 2:
            return None
        
        best_cam_idx = np.argmax(self.pts_shapes)
        sparse_view_idxs = maximize_point_cloud_visibility(self.viewCount, self.unique_pts, best_cam_idx)
        self.sparse_views = [self.cam_infos_ext[i]["img_name"] for i in sparse_view_idxs]

        print(f"visibility sparse views: {self.sparse_views}")
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]
    
    def _unique_pts(self, extr):
        unique_pts, shapes = [], []
        for _, img in enumerate(extr):
            unique = np.unique([p for p in img.point3D_ids if p != -1])
            unique_pts.append(unique)
            shapes.append(unique.shape)
        return unique_pts, np.array(shapes)
