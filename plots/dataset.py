import os

from plot import highlight_sparse_views
from scene.dataset_readers_ext import read_extr_and_intr, readColmapCameras
import samplers

VIEWCOUNTS = [3,6,9]
SAMPLERS = ["random", "baseline", "angular", "visibility"]
DATASETS = ["db", "dtu", "tandt"]
SCENES = ["playroom", "scna8", "train"]

def read_scene_cam_centers(source_path):
    cs = []
    with open(os.path.join(source_path, "cam_centers.txt"), "r") as cf:
        elems = cf.split()
    return cs

def sample_cam_cs_per_scene(source_path, model_path):    
    # 1. for scene read cs from cam_centers.txt in source_path
    cs = read_scene_cam_centers(source_path)
    
    # 2. for each config in

    # cs = {
    #     "all": randomS.get_cs(),
    #     "random": rnd_cs,
    #     "baseline": bl_cs,
    #     "angular": ang_cs,
    #     "visibility": vis_cs
    # }

    # cam_infos = {
    #     "random": rnd_c_infos,
    #     "baseline": bl_c_infos,
    #     "angular": ang_c_infos,
    #     "visibility": vis_c_infos
    # }
    
    return (cam_infos, cs)

def read_sparse_cs(model_path):
    with open(os.path.join(model_path, "sparse_views.txt"), "r") as cf:
        while True:
            line = cf.readline()
            if not line:
                break
            line = line.strip()
            viewCount = line.split()[0]
            view_names = cf.readline().split()
            line = cf.readline().strip()
            line = line.replace("[", "").replace("]", "")
            elems = line.split()
            cam_centers = [list(map(float, elems[i:i+3]) for i in range(0, len(elems), 3))] # cgpt
            return cam_centers

if __name__ == "__main__":
    viewCount = VIEWCOUNTS[2]
    sampler = SAMPLERS[2]
    dataset_id = 1
    dataset = DATASETS[dataset_id]
    scene = SCENES[dataset_id]

    match dataset:
        case "db": source_path = os.path.join("data", "db", "playroom")
        case "tandt": source_path = os.path.join("data", "tandt", "train")
        case _ : source_path = os.path.join("data", "dtu_corgs", "scan8")
    
    model_path = os.path.join("./output", f"{dataset}-{scene}-{sampler}-{viewCount}")
    sparse_cs = read_sparse_cs(model_path)

    highlight_sparse_views(cs["all"], sparse_cs, save_path=f"./output/{dataset}-{sampler}-{viewCount}")