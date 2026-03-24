import os

import numpy as np

# should take (train) cam_infos as input, making dataset_path and read_cam_infos() redundant
# cs should be mapped to cam_infos in sampler, as params will be from og 3dgs without cs
# cam_infos needed for C calculation and creation of cam_infos_ext
class Sampler:
    
    viewCount : int
    cam_infos : list
    cam_infos_ext : list
    sparse_views: list[str]

    def __init__(self, viewCount: int, cam_infos: list[dict]):
        self.viewCount = viewCount
        self.cam_infos = cam_infos

        self.cam_infos_ext = [{"img_name":c.image_name, "C":self._cam_cs(c.R, c.T), } for c in cam_infos]

    def _cam_cs(self, R: np.ndarray, T:np.ndarray):
        """Returns: camera centers based on rotation and translation matrices. See Colmap documentation."""
        return - R @ T # new transpose again?

    def get_cs(self):
        """ Returns: a list of camera centers (3D np arrays) """
        return [c["C"] for c in self.cam_infos_ext]
    
    def get_sparse_cs(self, views:list[tuple] = None):
        """ Returns: a list of tuples, where each tuple holds 2 camera centers (3D np arrays) corresponding to the pairs of images in views. """
        if views == None:
            views = self.sparse_views
        return [tuple([c["C"] for c in self.cam_infos_ext if c["img_name"] in vs]) for vs in views]
    
    def save_sparse_views(self, views, model_path):
        if not os.path.exists(model_path):
            return None
        file_path = os.path.join(model_path, "sparse_views")
        with open(file_path, 'w') as sparse_log_f:
            sparse_log_f.write(str(views))
            return file_path