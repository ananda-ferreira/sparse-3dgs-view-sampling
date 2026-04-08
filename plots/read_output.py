import json
import os

import numpy as np

def read_cam_centers_per_scene(source_path):
    with open(os.path.join(source_path, "cam_centers.txt"), "r") as cf:
        line = cf.readline()
        line = line.replace("[", "").replace("]", "")
        points_split = line.split()
        points_split = [float(f) for f in points_split]
        cs = np.array(points_split).reshape(-1, 3)
    return cs

def read_sparse_cam_from_json(model_path, viewCount):
    with open(os.path.join(model_path, "cameras.json"), "r") as json_f:
        d = json.load(json_f)
    return d[-viewCount:]

def read_metrics_from_json(model_path):
    with open(os.path.join(model_path, "results.json"), "r") as json_f:
        d = json.load(json_f)
    return d

# def read_sparse_cs(model_path):
#     with open(os.path.join(model_path, "sparse_views.txt"), "r") as cf:
#         while True:
#             line = cf.readline()
#             if not line:
#                 break
#             line = line.strip()
#             viewCount = line.split()[0]
#             view_names = cf.readline().split()
#             line = cf.readline().strip()
#             line = line.replace("[", "").replace("]", "")
#             elems = line.split()
#             cam_centers = [list(map(float, elems[i:i+3]) for i in range(0, len(elems), 3))] # cgpt
#             return cam_centers
   
