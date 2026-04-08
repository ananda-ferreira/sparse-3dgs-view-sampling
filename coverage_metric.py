# copilot pseudo-code
import numpy as np

def camera_observations(gaussians, cameras):
    obs_counts = np.zeros(len(cameras), dtype=int)

    for g in gaussians:
        for i, cam in enumerate(cameras):
            X_cam = cam.R @ g.position + cam.t
            if X_cam[2] <= 0:
                continue
            uv = project(X_cam, cam.intrinsics)
            if inside_image(uv, cam.image_size):
                obs_counts[i] += 1
    
    return obs_counts