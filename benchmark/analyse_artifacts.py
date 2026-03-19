# run samplers on one or multiple datasets. 
# -> sparse data
# run 3dgs on sparse data
# -> scene
# runs 3dgs.metrics on scene: how competitve is its perfromance?

import os

from plot import highlight_sparse_views
from utils_sparse import read_cam_infos
from sampler_baseline import BaselineSampler
from sampler_random import RandomSampler
from sampler_angular import AngularSampler
from sampler_visibility import VisibilitySampler

VIEWCOUNTS = [3,6,9]

def sample_cam_infos(viewCount, cam_infos, extr):

    randomS = RandomSampler(viewCount, cam_infos)
    rnd_c_infos = randomS.sample()
    rnd_cs = randomS.get_sparse_cs()
    
    baselineS = BaselineSampler(viewCount, cam_infos)
    bl_c_infos = baselineS.sample()
    bl_cs = baselineS.get_sparse_cs()
    
    angularS = AngularSampler(viewCount, cam_infos)
    ang_c_infos = angularS.sample()
    ang_cs = angularS.get_sparse_cs()
    
    visibilityS = VisibilitySampler(viewCount, cam_infos, extr)
    vis_c_infos = visibilityS.sample()
    vis_cs = visibilityS.get_sparse_cs()

    cs = {
        "all": randomS.get_cs(),
        "random": rnd_cs,
        "baseline": bl_cs,
        "angular": ang_cs,
        "visibility": vis_cs
    }

    cam_infos = {
        "random": rnd_c_infos,
        "baseline": bl_c_infos,
        "angular": ang_c_infos,
        "visibility": vis_c_infos
    }
    
    return (cam_infos, cs)

if __name__ == "__main__":

    # source_path = os.path.join("../data", "tandt", "train")
    # source_path = os.path.join("../data", "db", "playroom")
    source_path = os.path.join("../data", "dtu_corgs", "scan8")
    
    viewCount = VIEWCOUNTS[0]
    
    cam_infos, extr = read_cam_infos(source_path)
    sparse_cam_infos, cs = sample_cam_infos(viewCount, cam_infos, extr)

    sparse_cs = cs["random"][0]
    highlight_sparse_views(cs["all"], sparse_cs)