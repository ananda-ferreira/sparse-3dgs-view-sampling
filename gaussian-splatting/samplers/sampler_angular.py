import numpy as np
from samplers.utils_sampler import calc_pairwise_distances
from samplers.sampler_distance import DistanceSampler

# cam_infos used for return
# cam_infos needed for view dir calculation
class AngularSampler(DistanceSampler):

    def __init__(self, viewCount: int, cam_infos: list):
        super().__init__(viewCount, cam_infos)
        
        view_dirs = self.view_dirs()
        for i,c in enumerate(self.cam_infos_ext):
            c["view_dir"] = view_dirs[i]

        self.pw_dist = calc_pairwise_distances(view_dirs)
        self.max_baselines = self.get_max_baselines(self.pw_dist)

    def view_dirs(self):
        forward_dir = np.array([0,0,-1])
        Rs = np.array([c.R for c in self.cam_infos])
        return Rs @ forward_dir   