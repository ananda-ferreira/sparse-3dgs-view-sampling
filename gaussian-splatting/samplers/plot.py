import matplotlib.pyplot as plt
import numpy as np


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

def plot_view_directions(view_dirs):
    view_dirs = np.array(view_dirs)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # origin for all vectors
    origin = np.zeros((view_dirs.shape[0], 3))

    ax.quiver(
        origin[:,0], origin[:,1], origin[:,2],
        view_dirs[:,0], view_dirs[:,1], view_dirs[:,2],
        length=1.0, normalize=True
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_box_aspect([1,1,1])
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])

    plt.show()
