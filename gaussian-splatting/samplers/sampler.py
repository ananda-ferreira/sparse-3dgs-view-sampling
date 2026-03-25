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
    
    def save_sparse_views(self, model_path):
        if not os.path.exists(model_path):
            return None
        
        file_path = os.path.join(model_path, "sparse_views.txt")
        sparse_str, cs_str = "", "" 
        cs = self.get_sparse_cs()

        for i in range(0, self.viewCount):
            sparse_str += f"{str(self.sparse_views[i])} "
            cs_str += f"{str(cs[i])} "

        with open(file_path, 'w') as sparse_log_f:
            sparse_log_f.write(f"{sparse_str}'\n'"+ str(cs_str))
        return file_path
        
    # # note: "output" needs to be the output directory
    # def save_sparse_views(self, model_path):
    #     if not os.path.exists(model_path):
    #         return None
        
    #     output_path, id = model_path.split("output", 1)
    #     file_path = os.path.join(output_path, "sparse_views.txt")
    #     print(f"Path to sparse_views.txt: {file_path}")

    #     with open(file_path, 'a') as sparse_log_f:
    #         sparse_log_f.write(
    #             id + '\n'
    #             + f"{str(self.sparse_views[0])} {str(self.sparse_views[1])} {str(self.sparse_views[2])}'\n'"
    #             + str(self.get_sparse_cs()))
    #     return file_path