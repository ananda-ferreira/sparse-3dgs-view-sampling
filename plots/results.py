import os
import matplotlib.pyplot as plt
from PIL import Image

def plot_test_renders(output_path, dataset, scene, viewCount, indices, save_path):
    renders_path = "test/ours_30000/renders"
    paths = {
        "gt": os.path.join(output_path, f"{dataset}-{scene}-random-{viewCount}", "test/ours_30000/gt"),
        "random": os.path.join(output_path, f"{dataset}-{scene}-random-{viewCount}", renders_path),
        "baseline": os.path.join(output_path, f"{dataset}-{scene}-baseline-{viewCount}", renders_path),
        "angular": os.path.join(output_path, f"{dataset}-{scene}-angular-{viewCount}", renders_path),
        "visibility": os.path.join(output_path, f"{dataset}-{scene}-visibility-{viewCount}", renders_path),
    }

    samplers = list(paths.keys())
    num_rows = len(indices)
    num_cols = len(samplers)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(4*num_cols, 4*num_rows))

    # Handle edge case when only 1 row
    if num_rows == 1:
        axes = [axes]

    for row_idx, img_idx in enumerate(indices):
        axes[row_idx][0].set_ylabel(img_idx, fontsize=20, rotation=0, labelpad=20, va='center')
        
        for col_idx, sampler in enumerate(samplers):
            ax = axes[row_idx][col_idx]

            img_path = os.path.join(paths[sampler], f"{img_idx:05d}.png")
            
            if os.path.exists(img_path):
                img = Image.open(img_path)
                ax.imshow(img)
            else:
                ax.text(0.5, 0.5, "Missing", ha='center', va='center')
            
            # ax.axis("off")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Column titles
            if row_idx == 0:
                ax.set_title(sampler, fontsize=20, pad=16)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.02, wspace=0.02)
    plt.savefig(save_path)
    plt.close()

def plot_test_renders_even(output_path, dataset, scene, viewCount, count, save_path):
    renders_path = "test/ours_30000/renders"
    paths = {
        "gt": os.path.join(output_path, f"{dataset}-{scene}-random-{viewCount}", "test/ours_30000/gt"),
        "random": os.path.join(output_path, f"{dataset}-{scene}-random-{viewCount}", renders_path),
        "baseline": os.path.join(output_path, f"{dataset}-{scene}-baseline-{viewCount}", renders_path),
        "angular": os.path.join(output_path, f"{dataset}-{scene}-angular-{viewCount}", renders_path),
        "visibility": os.path.join(output_path, f"{dataset}-{scene}-visibility-{viewCount}", renders_path),
    }

    samplers = list(paths.keys())

        # --- Get all filenames from one sampler (assume all match) ---
    all_files = [
        f for f in os.listdir(paths["random"]) if f.endswith(".png")
    ]

    total = len(all_files)

    # --- Pick evenly spaced indices ---
    selected_positions = np.linspace(0, total - 1, count, dtype=int)
    selected_files = [all_files[i] for i in selected_positions]

    num_rows = len(selected_files)
    num_cols = len(samplers)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(4*num_cols, 4*num_rows))

    # Handle edge case when only 1 row
    if num_rows == 1:
        axes = [axes]

    for row_idx, filename in enumerate(selected_files):
        for col_idx, sampler in enumerate(samplers):
            ax = axes[row_idx][col_idx]

            img_path = os.path.join(paths[sampler], filename)
            
            if os.path.exists(img_path):
                img = Image.open(img_path)
                ax.imshow(img)
            else:
                ax.text(0.5, 0.5, "Missing", ha='center', va='center')
            
            ax.axis("off")

            # Column titles
            if row_idx == 0:
                ax.set_title(sampler)

            # Row labels (image index)
            if col_idx == 0:
                ax.set_ylabel(f"idx {filename}")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

if __name__ == "__main__":
        view_counts = [6]
        datasets = ["db"]
        scenes = ["drjohnson"]
        # scenes = ["playroom", "drjohnson", "train", "truck", "scan8", "scan40", "scan63"]
        # datasets = ["db", "db", "tandt", "tandt", "dtu", "dtu", "dtu"]
        
        for i, s in enumerate(scenes):
            for v in view_counts:
                plot_test_renders("../output/output-depth", datasets[i], s, v, [0,1,2,3,4], f"results/{datasets[i]}-{s}-{v}")