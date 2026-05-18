
import os

from plot import highlight_sparse_views_reduced, plot_dataset_table, plot_delta_table, plot_metrics_table, plot_renders_per_img, plot_renders_per_view, highlight_sparse_views, plot_renders_per_view_even, plot_scene_point_counts, plot_scene_table
from read_output import extract_sparse_cam_sorted, read_sparse_cam_from_json, read_cam_centers_for_scene, fetchPly
import sys

def plot_renders(datasets, scenes, view_counts, test_view_idx):
    for i, sc in enumerate(scenes):
        # for v in view_counts:
        #     if datasets[i] == "tandt":
        #         plot_renders_per_view_even(v, datasets[i], sc, 5, output_path, f"results/per-view-even/{datasets[i]}-{sc}-{v}")
        #     else:
        #         plot_renders_per_view(v, datasets[i], sc, test_view_idx, output_path, f"results/per-view/{datasets[i]}-{sc}-{v}")
        for j in test_view_idx:
            plot_renders_per_img(j, datasets[i], sc, view_counts, output_path, f"results/per-test-img/{datasets[i]}-{sc}-{j}")

def plot_cam_centers(datasets, scenes, view_counts, reducer=None, sparse=False, test=False, save=True):
    for s in samplers:
        for i, sc in enumerate(scenes):
            
            cam_cs = read_cam_centers_for_scene(f"../data/{datasets[i]}/{sc}")
            train_cam_infos, test_cam_infos = extract_sparse_cam_sorted(output_path, datasets[i], sc, s, view_counts)
        
            sparse_cs = [c["position"] for c in train_cam_infos] if sparse else []
            sparse_rs = [c["rotation"] for c in train_cam_infos] if sparse else []
            test_cs = [c["position"] for c in test_cam_infos] if test else []
            print(sparse_rs)
            sys.exit()

            if not reducer == None:
                filename = f"test-{datasets[i]}-{sc}-{reducer}" if test else f"{datasets[i]}-{sc}-{s}-{reducer}"
                save_path_reducer = f"results/cam-centers/{filename}" if save else None
                highlight_sparse_views_reduced(
                    reducer, 
                    cam_cs, 
                    sparse_cs=sparse_cs, 
                    test_cs=test_cs, 
                    title=f"{datasets[i]} {sc} {s}", 
                    save_path=save_path_reducer, 
                    label=True
                )
            else:
                filename = f"test-{datasets[i]}-{sc}" if test else f"{datasets[i]}-{sc}-{s}"
                save_path = f"results/cam-centers/{filename}" if save else None
                highlight_sparse_views(
                    cam_cs, 
                    sparse=sparse_cs,
                    test_cs=test_cs, 
                    title=f"{datasets[i]} {sc} {s}", 
                    save_path=save_path, 
                    label=True
                )
        if test or not sparse: sys.exit()

if __name__ == "__main__":
    output_path = "../output/output-depth"
    output_path_corgs = "../output/output-corgs-r2"

    view_counts = [2,4,6]
    scenes = ["playroom", "drjohnson", "train", "truck", "scan8", "scan40", "scan63"]
    datasets = ["db", "db", "tandt", "tandt", "dtu", "dtu", "dtu"]
    samplers = ["random", "baseline", "angular", "visibility"]
    
## plot test renders
    test_view_idx = [23]
    # plot_renders(["tandt"], ["train"], view_counts, test_view_idx)

## plot cam centers    
    plot_cam_centers(datasets, scenes, view_counts, reducer="pca", sparse=True, test=True) 

## plot metrics
# view_count = view_counts[0]
# sc = "scan63"
# i = 6
# plot_delta_table(["../output/output-depth", "../output/output-corgs-r2"], sc, datasets[i], view_counts, samplers, save_path=f"results/metrics-scene/delta-corgs-drgs-{datasets[i]}-{sc}")

# for i, sc in enumerate(scenes):
#     plot_scene_table(output_path, sc, datasets[i], view_counts, samplers, save_path=f"results/metrics-scene/corgs-{datasets[i]}-{sc}")
    # sys.exit()
    # plot_dataset_table(output_path, scenes, datasets[i], view_counts, samplers, save_path=f"results/metrics-dataset/{datasets[i]}")
## plot point cloud size
# for i, sc in enumerate(scenes): 
#     plot_scene_point_counts(output_path, sc, datasets[i], view_counts, samplers, save_path=f"results/pcd-size-scene/pcd-{datasets[i]}-{sc}")