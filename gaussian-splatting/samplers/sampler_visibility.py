import numpy as np
from samplers.utils_sampler import maximize_point_cloud_coverage
from samplers import Sampler

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
        # for i,c in enumerate(self.cam_infos_ext):
        #     c["unique_pts"] = self.unique_pts[i]
        #     c["pts_shape"] = self.pts_shapes[i]

    def sample(self):
        if self.viewCount < 2:
            return None
        
        best_cam_idx = np.argmax(self.pts_shapes)
        sparse_view_idxs = maximize_point_cloud_coverage(self.viewCount, self.unique_pts, best_cam_idx)
        print(f"length cam_infos_ext: {len(self.cam_infos_ext)}")
        print(f"sparse_view_idxs: {sparse_view_idxs}")
        self.sparse_views = [self.cam_infos_ext[i]["img_name"] for i in sparse_view_idxs]

        print(f"visibility sparse views: {self.sparse_views}")
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]
    
    def _unique_pts(self, extr):
        print(f"length of extrinsics: {len(extr)}. Should match length of cam_infos_ext")
        unique_pts, shapes = [], []
        for i, img in enumerate(extr):
            unique = np.unique([p for p in img.point3D_ids if p != -1])
            unique_pts.append(unique)
            shapes.append(unique.shape)
        return unique_pts, np.array(shapes)
