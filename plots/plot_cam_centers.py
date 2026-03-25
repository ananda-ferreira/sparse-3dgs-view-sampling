import os

from plot import highlight_sparse_views
from scene.dataset_readers_ext import read_extr_and_intr, readColmapCameras
import samplers

VIEWCOUNTS = [3,6,9]
SAMPLERS = ["random", "baseline", "angular", "visibility"]
DATASETS = ["db", "dtu", "tandt"]

def read_cam_infos(dataset_path):
    extr, intr = read_extr_and_intr(dataset_path)
    depths=""
    cam_infos_unsorted = readColmapCameras(
        cam_extrinsics=extr, cam_intrinsics=intr, depths_params=None,
        images_folder=os.path.join(dataset_path, "images"), 
        depths_folder=os.path.join(dataset_path, depths) if depths != "" else "", test_cam_names_list=[])
    return sorted(cam_infos_unsorted.copy(), key = lambda x : x.image_name), extr
    
def sample_cam_infos(viewCount, cam_infos, extr):

    randomS = samplers.RandomSampler(viewCount, cam_infos)
    rnd_c_infos = randomS.sample()
    rnd_cs = randomS.get_sparse_cs()
    
    baselineS = samplers.BaselineSampler(viewCount, cam_infos)
    bl_c_infos = baselineS.sample()
    bl_cs = baselineS.get_sparse_cs()
    
    angularS = samplers.AngularSampler(viewCount, cam_infos)
    ang_c_infos = angularS.sample()
    ang_cs = angularS.get_sparse_cs()
    
    visibilityS = samplers.VisibilitySampler(viewCount, cam_infos, extr)
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
    viewCount = VIEWCOUNTS[2]
    sampler = SAMPLERS[2]
    dataset = DATASETS[1]

    match dataset:
        case "db": source_path = os.path.join("data", "db", "playroom")
        case "tandt": source_path = os.path.join("data", "tandt", "train")
        case _ : source_path = os.path.join("data", "dtu_corgs", "scan8")
    
    cam_infos, extr = read_cam_infos(source_path)
    sparse_cam_infos, cs = sample_cam_infos(viewCount, cam_infos, extr)

    sparse_cs = cs[sampler][0]
    highlight_sparse_views(cs["all"], sparse_cs, save_path=f"output/plots/{dataset}-{sampler}-{viewCount}")