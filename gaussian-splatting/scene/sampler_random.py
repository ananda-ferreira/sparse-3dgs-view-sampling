from random import sample

from scene.sampler import Sampler

# cam_infos used for return
class RandomSampler(Sampler):

    def __init__(self, viewCount: int, cam_infos: list):
        super().__init__(viewCount, cam_infos)

    def sample(self):
        sparse_idxs = sorted(sample(range(len(self.cam_infos_ext)), self.viewCount))
        self.sparse_views = [[self.cam_infos_ext[i]["img_name"] for i in sparse_idxs]]
        print(f"sparse views: {self.sparse_views}")
        return [c for c in self.cam_infos if c.image_name in self.sparse_views]