from samplers.utils_sampler import calc_pairwise_distances
from samplers.sampler_distance import DistanceSampler

# cam_infos used for return
class BaselineSampler(DistanceSampler):

    def __init__(self, viewCount: int, cam_infos: list):
        super().__init__(viewCount, cam_infos)
        
        self.pw_dist = calc_pairwise_distances(self.get_cs())
        # self.max_baselines = self.get_max_baselines(self.pw_dist)
