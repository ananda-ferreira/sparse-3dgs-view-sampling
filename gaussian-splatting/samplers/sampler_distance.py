import numpy as np
from samplers.utils_sampler import farthest_point_sampling
from samplers import Sampler

# cam_infos used for return
class DistanceSampler(Sampler):

    pw_dist: np.ndarray
    # max_baselines: list[dict] # sorted by score! # not needed anymore

    def __init__(self, viewCount: int, cam_infos: list):
        super().__init__(viewCount, cam_infos)

    def sample(self, sampleCount = 1):
        if self.viewCount < 2:
            return None
        
        self.sparse_views = self.calc_furthest2_sparse_views(self.pw_dist)
        print(f"best 2 views: {self.sparse_views}")
        if self.viewCount >= 3:
            sparse_cs_init = self.get_sparse_cs()
            sparse_idxs = self.calc_sparse_views(self.get_cs(), sparse_cs_init)
            new_sparse_views = [self.cam_infos_ext[i]["img_name"] for i in sparse_idxs]
            self.sparse_views.extend(new_sparse_views)
        print(f"distance sparse views:")
        for i in self.sparse_views: print(f"{i}")
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]
    
    def calc_sparse_views(self, cs, top2_cs):
        return farthest_point_sampling(self.viewCount, cs, top2_cs)
        # sparse_cs_set = {tuple(sc) for sc in sparse_cs} # tuples are hashable, lists not; set is faster for lookup
        # return [c["img_name"] for c in self.cam_infos_ext if tuple(c["C"]) in sparse_cs_set]

    # max_baselines property not needed
    # refactor dict maybe not necessary
    def calc_furthest2_sparse_views(self, pairwise_dist: np.ndarray):
        max_baselines = list()
        for i, c in enumerate(self.cam_infos_ext):
            j = np.argmax(pairwise_dist[i])
            max_baselines.append({
                "view1": c["img_name"], 
                "view2": self.cam_infos_ext[j]["img_name"], 
                "score": pairwise_dist[i, j]
            })
        best_baseline = max(max_baselines, key= lambda x : x["score"])
        return [best_baseline["view1"], best_baseline["view2"]]
    
## if not interested in just the best option but pairCount best options which might have similar value but diffenret impact on result
    def get_sparse_view_pairs(self, pairCount = 1):
        """
        Returns: a list of n tuples, where each tuple holds a pair of image names with a baseline among the top n. n == pairCount
        """
        # if pairCount > 1:
        #     top_baselines = sorted(self.max_baselines, key= lambda x : x["score"], reverse=True)[:pairCount]
        #     return [(pair["view1"], pair["view2"]) for pair in top_baselines] 
        # else: 
        best_baseline = max(self.max_baselines, key= lambda x : x["score"])
        return [best_baseline["view1"], best_baseline["view2"]]
    
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
    