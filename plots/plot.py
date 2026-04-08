import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from read_output import read_metrics_from_json

## plot camera info
def highlight_sparse_views(cs, sparse_cs = [], title = "", center = None, label=False, save_path=None):

    sparse, others = [], []

    def is_in_sparse(c, sparse_cs, tol=1e-6):
        return any(np.allclose(c, s, atol=tol) for s in sparse_cs)
    
    for i, c in enumerate(cs):
        if is_in_sparse(c, sparse_cs):
            sparse.append((i+1, c))
        else:
            others.append((i+1, c))

    # sparse = [(i+1, c) for i, c in enumerate(cs) if is_in_sparse(c, sparse_cs)]
    # others = [(i+1, c) for i, c in enumerate(cs) if not is_in_sparse(c, sparse_cs)]

    fig = plt.figure()
    fig.suptitle(title, fontsize=8)
    ax = fig.add_subplot(111, projection='3d')

    # plot all other cameras
    for i, c in others:
        ax.scatter(c[0], c[1], c[2], color='blue', alpha=0.1)
        if label: ax.text(c[0], c[1], c[2], str(i), color='blue', alpha=0.2, fontsize=8)

    # Plot highlighted subset
    for j, (i, c) in enumerate(sparse):
        print(c)
        if j < 2:
            color = (1, 0.8, 0, 1)
        elif j < 4:
            color = (1, 0.6, 0, 1)
        else:
            color = (1, 0.2, 0, 1)
        ax.scatter(c[0], c[1], c[2], color=color)
        if label: ax.text(c[0], c[1], c[2], str(i), color='red', fontsize=8)
    
    # add world center
    ax.scatter(0,0,0, color='grey')
    if label: ax.text(0,0,0, "world", color='grey', fontsize=8)
    # ax.quiver(0, 0, 0, 0, 0, 1, length=2) 
    
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
    ax.view_init(-75, -90) # elev: rotation from side to top/bottom view; azim: rotation only around z axis
                 
    # Save or show
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

import os
import matplotlib.pyplot as plt

def plot_metrics_table(output_path, scenes, datasets, sparse_view_counts, samplers):
    rows = []
    table_data = []

    for view_count in sparse_view_counts:
        for i, sc in enumerate(scenes):
            row_name = f"{datasets[i]} {sc} {view_count}"
            row_values = []

            for metric in ["PSNR", "LPIPS", "SSIM"]:
                for s in samplers:
                    output_dir = f"{datasets[i]}-{sc}-{s}-{view_count}"
                    path = os.path.join(output_path, output_dir)

                    try:
                        results = read_metrics_from_json(path)["ours_30000"]
                        value = results[metric]
                    except Exception:
                        value = None

                    # Format nicely (or leave blank)
                    row_values.append(f"{value:.3f}" if value is not None else "")

            rows.append(row_name)
            table_data.append(row_values)

    # Column labels
    col_labels = []
    for metric in ["PSNR", "LPIPS", "SSIM"]:
        for s in samplers:
            col_labels.append(f"{metric}\n{s}")

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.axis('off')

    table = ax.table(
        cellText=table_data,
        rowLabels=rows,
        colLabels=col_labels,
        loc='center',
        cellLoc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    plt.tight_layout()
    plt.show()

def plot_scene_table(output_path, scene, dataset, sparse_view_counts, samplers, save_path):
    table_data = []
    row_labels = []

    for view_count in sparse_view_counts:
        row_labels.append(f"{view_count} views")
        row = []

        # Order: PSNR → SSIM → LPIPS
        for metric in ["PSNR", "SSIM", "LPIPS"]:
            for s in samplers:
                output_dir = f"{dataset}-{scene}-{s}-{view_count}"
                path = os.path.join(output_path, output_dir)

                try:
                    results = read_metrics_from_json(path)["ours_30000"]
                    value = results[metric]
                except Exception:
                    value = None

                row.append(f"{value:.3f}" if value is not None else "")

        table_data.append(row)

    # Column labels
    col_labels = (
        [f"PSNR\n{s}" for s in samplers] +
        [f"SSIM\n{s}" for s in samplers] +
        [f"LPIPS\n{s}" for s in samplers]
    )

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.axis('off')

    table = ax.table(
        cellText=table_data,
        rowLabels=row_labels,
        colLabels=col_labels,
        loc='center',
        cellLoc='center'
    )

    color_metric_headers(table, samplers)
    # add_group_separators(ax, table, samplers)
    highlight_best_per_row(table, table_data, samplers)

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)

    ax.set_title(f"{dataset} – {scene}", fontsize=12, pad=8)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

def color_metric_headers(table, samplers):
    n = len(samplers)

    # Colors for each metric group
    colors = {
        "PSNR": (0.6, 0, 0, 0.15),   
        "SSIM": (0, 0.6, 0, 0.15),   
        "LPIPS": (0, 0, 0.6, 0.15)  
    }

    # Header row is row=0 in matplotlib tables
    for col in range(3 * n):
        if col < n:
            color = colors["PSNR"]
        elif col < 2 * n:
            color = colors["SSIM"]
        else:
            color = colors["LPIPS"]

        table[(0, col)].set_facecolor(color)

def highlight_best_per_row(table, table_data, samplers):
    n = len(samplers)

    for row_idx, row in enumerate(table_data):
        # Convert row to floats (ignore empty)
        values = []
        for v in row:
            try:
                values.append(float(v))
            except:
                values.append(None)

        # Split into metric groups
        psnr_vals = values[0:n]
        ssim_vals = values[n:2*n]
        lpips_vals = values[2*n:3*n]

        # Find best indices
        def best_idx(vals, mode="max"):
            valid = [(i, v) for i, v in enumerate(vals) if v is not None]
            if not valid:
                return None
            if mode == "max":
                return max(valid, key=lambda x: x[1])[0]
            else:
                return min(valid, key=lambda x: x[1])[0]

        best_psnr = best_idx(psnr_vals, "max")
        best_ssim = best_idx(ssim_vals, "max")
        best_lpips = best_idx(lpips_vals, "min")

        # Apply highlight (row+1 because header is row 0)
        if best_psnr is not None:
            # table[(row_idx+1, best_psnr)].set_facecolor((0.8, 0.8, 0, 0.15))  # green
            cell = table[(row_idx+1, best_psnr)]
            cell.set_text_props(weight='bold')

        if best_ssim is not None:
            # table[(row_idx+1, n + best_ssim)].set_facecolor((0.8, 0.8, 0, 0.15))
            cell = table[(row_idx+1, n + best_ssim)]
            cell.set_text_props(weight='bold')

        if best_lpips is not None:
            # table[(row_idx+1, 2*n + best_lpips)].set_facecolor((0.8, 0.8, 0, 0.15))
            cell = table[(row_idx+1, 2*n + best_lpips)]
            cell.set_text_props(weight='bold')

def add_group_separators(ax, table, samplers):
    n = len(samplers)

    # Total number of columns
    total_cols = 3 * n

    # Get table bounding box in axes coords
    cells = table.get_celld()

    # We use header row (0) to determine column positions
    def get_x(col):
        cell = cells[(0, col)]
        return cell.get_x()

    def get_right_x(col):
        cell = cells[(0, col)]
        return cell.get_x() + cell.get_width()

    # Vertical span of the table
    y_bottom = min(cell.get_y() for cell in cells.values())
    y_top = max(cell.get_y() + cell.get_height() for cell in cells.values())

    # Draw separators after PSNR and SSIM groups
    separators = [n-1, 2*n-1]

    for col in separators:
        x = get_right_x(col)

        ax.plot(
            [x, x],
            [y_bottom, y_top],
            color='black',
            linewidth=2,
            transform=ax.transAxes,
            clip_on=False
        )