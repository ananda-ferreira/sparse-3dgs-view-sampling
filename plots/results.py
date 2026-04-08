
import os

from plot import plot_metrics_table, plot_renders_per_img, plot_renders_per_view, highlight_sparse_views, plot_scene_table
from read_output import read_metrics_from_json, read_sparse_cam_from_json, read_cam_centers_per_scene

if __name__ == "__main__":
    output_path = "../output/output-depth"

    test_view_idx = [0,1,2,3,4]
    sparse_view_counts = [2,4,6]
    scenes = ["playroom", "drjohnson", "train", "truck", "scan8", "scan40", "scan63"]
    datasets = ["db", "db", "tandt", "tandt", "dtu", "dtu", "dtu"]
    samplers = ["random", "baseline", "angular", "visibility"]
    
## plot test renders
    # for i, sc in enumerate(scenes):
    #     for v in sparse_view_counts:
    #         plot_renders_per_view(v, datasets[i], sc, [0,1,2,3,4], output_path, f"results/per-view/{datasets[i]}-{sc}-{v}")
    #     for j in test_view_idx:
    #         plot_renders_per_img(j, datasets[i], sc, [2,4,6], output_path, f"results/per-test-img/{datasets[i]}-{sc}-{j}")
        
## plot cam centers    
    # # scene = scenes[4]
    # # dataset = datasets[4]
    # # sampler = samplers[1]
    # max_view_count = sparse_view_counts[-1:]

    # for i, sc in enumerate(scenes):
    #     for s in samplers:
    #         output_dir = f"{datasets[i]}-{sc}-{s}-{max_view_count}"

    #         train_cam_infos = read_sparse_cam_from_json(os.path.join(output_path, output_dir), max_view_count)
    #         sparse_cs = [c["position"] for c in train_cam_infos]
    #         cam_cs = read_cam_centers_per_scene(f"../data/{datasets[i]}/{sc}")

    #         highlight_sparse_views(cam_cs, sparse_cs, title=f"{datasets[i]} {sc} {s}", save_path=f"results/cam-centers/{output_dir}")

## plot metrics
view_count = sparse_view_counts[0]
sc = "playroom"
i = 0
s = "random" 

for i, sc in enumerate(scenes):
    plot_scene_table(output_path, sc, datasets[i], sparse_view_counts, samplers, save_path=f"results/metrics/{datasets[i]}-{sc}")