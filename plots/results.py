
import os

from plot import plot_renders_per_img, plot_renders_per_view, highlight_sparse_views
from read_output import read_sparse_cam_from_json

if __name__ == "__main__":
    output_path = "../output/output-depth"

    sparse_view_counts = [2,4,6]
    test_view_idx = [0,1,2,3,4]
    scenes = ["playroom", "drjohnson", "train", "truck", "scan8", "scan40", "scan63"]
    datasets = ["db", "db", "tandt", "tandt", "dtu", "dtu", "dtu"]
    
## plot test renders
    # for i, sc in enumerate(scenes):
    #     for v in sparse_view_counts:
    #         plot_renders_per_view(v, datasets[i], sc, [0,1,2,3,4], output_path, f"results/per-view/{datasets[i]}-{sc}-{v}")
    #     for j in test_view_idx:
    #         plot_renders_per_img(j, datasets[i], sc, [2,4,6], output_path, f"results/per-test-img/{datasets[i]}-{sc}-{j}")
        
## plot cam centers    
    samplers=["random", "baseline", "angular", "visibility"]
    output_dir = f"{datasets[0]}-{scenes[0]}-{samplers[1]}-{sparse_view_counts[0]}"

    train_cam_infos = read_sparse_cam_from_json(os.path.join(output_path, output_dir), sparse_view_counts[0])
    sparse_cs = [c["position"] for c in train_cam_infos]
    sparse_names = [c["img_name"] for c in train_cam_infos]

    # highlight_sparse_views(cs, sparse_cs, save_path=f"results/cam_centers/{output_dir}")