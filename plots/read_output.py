import json
import os
from typing import NamedTuple
import numpy as np
from plyfile import PlyData

def read_cam_centers_for_scene(source_path):
    with open(os.path.join(source_path, "cam_centers.txt"), "r") as cf:
        line = cf.readline()
        line = line.replace("[", "").replace("]", "")
        points_split = line.split()
        points_split = [float(f) for f in points_split]
        cs = np.array(points_split).reshape(-1, 3)
    return cs

def extract_sparse_cam_sorted(output_path, dataset, scene, sampler, views=[2,4,6]):
    train_cam_infos = []
    test_cam_infos = []
    for v in views:
        output_dir = f"{dataset}-{scene}-{sampler}-{v}"
        test_cams, train_cam_infos_v = read_sparse_cam_from_json(os.path.join(output_path, output_dir), v)
        existing = {v["img_name"] for v in train_cam_infos}
        new = [v for v in train_cam_infos_v if v["img_name"] not in existing]
        train_cam_infos.extend(new)
        test_cam_infos = test_cams
    return train_cam_infos, test_cam_infos

def read_sparse_cam_from_json(model_path, viewCount):
    with open(os.path.join(model_path, "cameras.json"), "r") as json_f:
        d = json.load(json_f)
    return d[:-viewCount], d[-viewCount:]

def read_metrics_from_json(model_path):
    with open(os.path.join(model_path, "results.json"), "r") as json_f:
        d = json.load(json_f)
    return d

## taken from 3dgs
class BasicPointCloud(NamedTuple):
    points : np.array
    count : int
    # colors : np.array
    # normals : np.array
    
def fetchPly(path):
    plydata = PlyData.read(path)
    vertices = plydata['vertex']
    positions = np.vstack([vertices['x'], vertices['y'], vertices['z']]).T
    count = vertices.count
    # colors = np.vstack([vertices['red'], vertices['green'], vertices['blue']]).T / 255.0
    # normals = np.vstack([vertices['nx'], vertices['ny'], vertices['nz']]).T
    return BasicPointCloud(points=positions, count=count)