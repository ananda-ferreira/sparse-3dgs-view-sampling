import matplotlib.pyplot as plt


def highlight_sparse_views(cs, sparse_cs):

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
        ax.text(c[0], c[1], c[2], str(i), color='blue', fontsize=8)

    # Plot highlighted subset
    for i, c in sparse:
        ax.scatter(c[0], c[1], c[2], color='red')
        ax.text(c[0], c[1], c[2], str(i), color='red', fontsize=8)
    
    ax.scatter(0, 0, 0, color='green')
    ax.text(0,0,0, "center", color='green', fontsize=8)
    


    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Set axis limits from -6 to 6
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-6, 6)

    ax.set_box_aspect([1,1,1])  # equal axis scaling

    plt.show()