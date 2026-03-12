from typing import Literal

import numpy as np
import os
from sampler import Sampler
from plot import highlight_sparse_views
from scipy.spatial.distance import cdist

from dataset_readers_helper import read_extr_and_intr, readColmapCameras


class BaselineSampler(Sampler):

    cam_infos_cd : list # [CameraInfo]
    max_baselines: list[dict]
    min_baselines: list[dict]
    pw_dist_mat: np.ndarray

    def __init__(self, viewCount: int, cam_infos: list):
        super().__init__(viewCount, cam_infos)
        img_names = [c["img_name"] for c in self.cam_infos_cd]
        cam_cs = [c["C"] for c in self.cam_infos_cd]
        self.pw_dist_mat = calc_pairwise_distances(cam_cs)
        self.max_baselines = self.get_max_baselines(img_names, self.pw_dist_mat)
        self.min_baselines = self.get_min_baselines(img_names, self.pw_dist_mat)

    def sample(self, sampleCount = 1):
        print("SAMPLE VIEWS")        
        if self.viewCount >= 3:
            print("greedy maximize minimum pairwise distance")
            self.sparse_views = self.get_sparse_view_tuples()
            self.sparse_cs = self.get_sparse_cs()

        elif self.viewCount == 2:
            print("max 2 views: pick one or more pairs of imgs with max baseline")
            self.sparse_views = self.get_sparse_view_pairs(sampleCount)
            self.sparse_cs = self.get_sparse_cs()
        else:
            print("use all views")

        return [c for c in self.cam_infos if c[8] in self.sparse_views]

    def get_sparse_view_tuples(self):
        sparse_views = []
        cs = self.get_cs()

        top2 = self.get_sparse_view_pairs()
        # top2_cs = list(self.get_sparse_cs(top2)[0])
        top2_cs = [c["C"] for c in self.cam_infos_cd if c["img_name"] in top2]
        sparse_views = top2[0]
        sparse_cs = top2_cs.copy()
        print()

        for _ in range(2, self.viewCount):
            # dists = cdist(cs, sparse_cs) # distances from each cs to the already selected sparse views!
            
            # get min distances ; different than max dist based on current sparse cs not pairwise dist
            distances = []
            for c in self.cam_infos_cd: 
                dists = euclidean_dist(c["C"], sparse_cs) # distances from each cs to the already selected sparse views!
                distances.append(np.min(dists))
            print(distances)

            # get cs of max distance to current sparse
            max_idx = np.argmax(distances)
            sparse_cs.append(self.cam_infos_cd[max_idx]["C"])

            # get corresponding image names
            sparse_views += (self.cam_infos_cd[max_idx]["img_name"],)

        print(f"\nsparse cs: {sparse_cs}")
        print(f"sparse views: {sparse_views}")
        return tuple(sparse_views)
    
    def farthest_point_sampling(cam_cs, k):
        """
        Sample k cam_cs from input pointcloud data cam_cs using Farthest Point Sampling.

        Parameters:
        cam_cs: numpy.ndarray
            The input pointcloud data, a numpy array of shape (N, D) where N is the
            number of cam_cs and D is the dimensionality of each point.
        k: int
            The number of cam_cs to sample.

        Returns:
        sampled_cam_cs: numpy.ndarray
            The sampled pointcloud data, a numpy array of shape (k, D).
        """
        N, D = cam_cs.shape
        farthest_pts = np.zeros((k, D))
        distances = np.full(N, np.inf)
        farthest = np.random.randint(0, N)
        for i in range(k):
            farthest_pts[i] = cam_cs[farthest]
            centroid = cam_cs[farthest]
            dist = np.sum((cam_cs - centroid) ** 2, axis=1)
            distances = np.minimum(distances, dist)
            farthest = np.argmax(distances)
        return farthest_pts

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
    
    def get_max_baselines(self, img_names, pairwise_dist: np.ndarray):
        max_baselines = list()
        for i, img in enumerate(img_names):
            j = np.argmax(pairwise_dist[i])
            max_baselines.append({"view1": img, "view2": img_names[j], "score": pairwise_dist[i, j]})
        return max_baselines
    
    def get_min_baselines(self, img_names, pairwise_dist: np.ndarray):
        min_baselines = list()
        for i, img in enumerate(img_names):
            row = pairwise_dist[i].copy()
            row[i] = np.inf
            j = np.argmin(row)
            min_baselines.append({"view1": img, "view2": img_names[j], "score": pairwise_dist[i, j]})
        return min_baselines
    
def calc_pairwise_distances(cam_cs: list):
    # this can be improved by avoiding the squareroot computation of euclidean distance
    cs = np.array(cam_cs)
    return cdist(cs, cs, 'euclidean')

# chatgpt
def farthest_pair(pw_dist_mat):
    i, j = np.unravel_index(np.argmax(pw_dist_mat), pw_dist_mat.shape)
    return i, j

def euclidean_dist(c, sparse_cs):
    # sqrt computation unnecessary 
    return np.sum((c - sparse_cs) ** 2, axis=1)

def read_cam_infos(dataset_path):
    extr, intr = read_extr_and_intr(dataset_path)
    depths=""
    cam_infos_unsorted = readColmapCameras(
        cam_extrinsics=extr, cam_intrinsics=intr, depths_params=None,
        images_folder=os.path.join(dataset_path, "images"), 
        depths_folder=os.path.join(dataset_path, depths) if depths != "" else "", test_cam_names_list=[])
    return sorted(cam_infos_unsorted.copy(), key = lambda x : x.image_name)
    
if __name__ == "__main__":
    print("RUNNING BASELINE SAMPLER")
    # source_path = os.path.join("../data", "tandt", "train")
    # source_path = os.path.join("../data", "db", "playroom")
    source_path = os.path.join("../data", "dtu_corgs", "scan8")
    
    cam_infos = read_cam_infos(source_path)
    sampler = BaselineSampler(2, cam_infos)
    sampler.sample(4)

    # cs = sampler.get_cs()
    # highlight_sparse_views(cs, sampler.sparse_cs[2])