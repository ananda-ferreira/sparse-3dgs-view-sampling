import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

## plot camera info
def highlight_sparse_views(cs, sparse_cs = [], center = None, label=False, save_path=None):

    sparse = []
    others = []

    sparse_cs_set = {tuple(x) for x in sparse_cs}
    sparse = [(i+1, c) for i, c in enumerate(cs) if tuple(c) in sparse_cs_set]
    others = [(i+1, c) for i, c in enumerate(cs) if tuple(c) not in sparse_cs_set]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plot all other cameras
    for i, c in others:
        ax.scatter(c[0], c[1], c[2], color='blue')
        if label: ax.text(c[0], c[1], c[2], str(i), color='blue', fontsize=8)

    # Plot highlighted subset
    for i, c in sparse:
        ax.scatter(c[0], c[1], c[2], color='red')
        if label: ax.text(c[0], c[1], c[2], str(i), color='red', fontsize=8)
    
    # add world center
    ax.scatter(0,0,0, color='green')
    if label: ax.text(0,0,0, "world", color='green', fontsize=8)
    
    # add scene center
    if center:
        ax.scatter(center[0], center[1], center[3], color='green')
        if label: ax.text(0,0,0, "scene", color='green', fontsize=8)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Set axis limits from -6 to 6
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-6, 6)

    ax.set_box_aspect([1,1,1])  # equal axis scaling
    ax.view_init(elev=20, azim=-60)
                 
    # ✅ Save or show
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_view_direction_points(view_dirs):
    view_dirs = np.array(view_dirs)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(
        view_dirs[:,0],
        view_dirs[:,1],
        view_dirs[:,2],
        s=20
    )

    ax.set_box_aspect([1,1,1])
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])

    plt.show()

## plot renders
def plot_renders_per_view(viewCount, dataset, scene, indices, output_path, save_path):
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

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(4*num_cols, 3.5*num_rows))

    # Handle edge case when only 1 row
    if num_rows == 1:
        axes = [axes]

    for row_idx, img_idx in enumerate(indices):
        axes[row_idx][0].set_ylabel(img_idx, fontsize=20, rotation=0, labelpad=32, va='center')
        
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
                ax.set_title(sampler, fontsize=20, pad=24)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.02, wspace=0.02)
    plt.savefig(save_path)
    plt.close()

def plot_renders_per_img(index, dataset, scene, view_counts, output_path, save_path):
    renders_path = "test/ours_30000/renders"
    gt_path = "test/ours_30000/gt"

    samplers = ["gt", "random", "baseline", "angular", "visibility"]
    num_cols = len(samplers)
    num_rows = len(view_counts)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(4*num_cols, 3.5*num_rows))

    # Handle edge case when only 1 row
    if num_rows == 1:
        axes = [axes]

    for row_idx, vc in enumerate(view_counts):
        axes[row_idx][0].set_ylabel(f"{vc}v", fontsize=20, rotation=0, labelpad=32, va='center')
        
        for col_idx, sampler in enumerate(samplers):
            ax = axes[row_idx][col_idx]

            if sampler == "gt": 
                path = gt_path
                smpl = "random"
            else: 
                path = renders_path
                smpl = sampler
            img_path = os.path.join(output_path, f"{dataset}-{scene}-{smpl}-{vc}", path, f"{index:05d}.png")
            
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
                ax.set_title(sampler, fontsize=20, pad=24)

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

## plot quantitative results

def plot():
    pass