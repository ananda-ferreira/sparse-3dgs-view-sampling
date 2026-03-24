import os
import numpy as np

from samplers.utils_sparse import calc_pairwise_distances, farthest_point_sampling
from samplers import Sampler

# cam_infos needed for view dir calculation
# cam_infos used for return
class AngularSampler(Sampler):

    pw_dist_dirs: np.ndarray
    max_baselines: list[dict]

    def __init__(self, viewCount, cam_infos: list):
        super().__init__(viewCount, cam_infos)
        
        view_dirs = self.view_dirs()
        for i,c in enumerate(self.cam_infos_ext):
            c["view_dir"] = view_dirs[i]

        self.pw_dist_dirs = calc_pairwise_distances(view_dirs)
        self.max_baselines = self.get_max_baselines(self.pw_dist_dirs)

    def sample(self, sampleCount = 1):
        if self.viewCount < 2:
            return None
        
        self.sparse_views = self.get_sparse_view_pairs()
        self.sparse_cs = self.get_sparse_cs()

        if self.viewCount >= 3:
            print("greedy maximize minimum pairwise distance of view direction points")
            sparse_cs_init = list(self.sparse_cs[0])
            self.sparse_views = self.get_sparse_view_tuples(self.get_cs(), sparse_cs_init)
            self.sparse_cs = self.get_sparse_cs()
            print(f"angular sparse views: {self.sparse_views}")
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]
    
    def get_sparse_view_tuples(self, cs, top2_cs):
        sparse_cs = farthest_point_sampling(self.viewCount, cs, top2_cs)
        sparse_cs_set = {tuple(sc) for sc in sparse_cs}
        sparse_views = [c["img_name"] for c in self.cam_infos_ext if tuple(c["C"]) in sparse_cs_set]
        return [tuple(sparse_views)]
    
    def get_sparse_view_pairs(self, pairCount = 1):
        """
        Returns: a list of n tuples, where each tuple holds a pair of image names with a baseline among the top n. n == pairCount
        """
        if pairCount > 1:
            top_baselines = sorted(self.max_baselines, key= lambda x : x["score"], reverse=True)[:pairCount]
            return [(pair["view1"], pair["view2"]) for pair in top_baselines] 
        else: 
            best_baseline = max(self.max_baselines, key= lambda x : x["score"])
            return [(best_baseline["view1"], best_baseline["view2"])]
    
    def get_max_baselines(self, pairwise_dist: np.ndarray):
        max_baselines = list()
        for i, c in enumerate(self.cam_infos_ext):
            j = np.argmax(pairwise_dist[i])
            max_baselines.append({
                "view1": c["img_name"], 
                "view2": self.cam_infos_ext[j]["img_name"], 
                "score": pairwise_dist[i, j]
            })
        return max_baselines
    
    def view_dirs(self):
        forward_dir = np.array([0,0,-1])
        Rs = np.array([c.R for c in self.cam_infos])
        return Rs @ forward_dir
        