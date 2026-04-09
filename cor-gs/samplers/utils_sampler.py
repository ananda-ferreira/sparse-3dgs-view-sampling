import numpy as np

# following github: lecture excercise (instead of scipy's cdist)
def calc_pairwise_distances(points: list):
    pts = np.array(points)
    # broadcasting: None inserts a new axis, to get a N,N,3 matrix (for pts.shape = N,3)
    diff = pts[:, None, :] - pts[None, :, :]
    # L2 norm for euclidean distance, axis -1 for last axis => xyz vectors
    out = np.linalg.norm(diff, axis=-1) # before it was 1, which is wrong
    return out

def euclidean_dist(c, sparse_cs):
    # sqrt computation unnecessary 
    return np.sum((c - sparse_cs) ** 2, axis=1)

# following medium post;
def farthest_point_sampling(viewCount, points, sparse_points):
    """
    Sample n points from input cam center or view direction points using Farthest Point Sampling. n = viewCount

    Parameters:
    points: numpy.ndarray
        Cam centers or view direction, a numpy array of shape (N, D) where N is the
        number of points and D is the dimensionality of each point.
    viewCount: int
        The number of points to sample.

    Returns:
    sparse_points: numpy.ndarray
        The sampled pointcloud data, a numpy array of shape (viewCount, D).
    """
    sparse = sparse_points.copy()
    sparse_idxs = []
    initalSparseCount = 2 # len(sparse_points)

    for _ in range(initalSparseCount, viewCount):
        # for each point 1. track how close this point is to the current sparse points. 2. only save the distance to the closest point.
        min_dists = []
        for c in points: 
            dists = euclidean_dist(c, sparse) # distances from each points to the already selected sparse views!
            min_dists.append(np.min(dists))

        # get the point that is furtherst (has the max min-distance) to the current sparse points
        max_idx = np.argmax(min_dists)

        sparse.append(points[max_idx])
        sparse_idxs.append(max_idx)
    return sparse_idxs

def maximize_point_cloud_visibility(viewCount, unique_pts, best_view_idx):
    """
    Maximize coverage by finding the views that together cover most scene points. 

    Parameters:
    viewCount: int
        The number of views to sample.
    unique_pts: list of numpy.ndarray
        For each camera in the scene, a numpy array of unique 3d point ids that it covers.
    best_view_idx: int
        Index of first view with highest coverage of points. 

    Returns:
    views: list[int]
        The sampled view indices, a list of ints.
    """
    if viewCount <= 0: 
        return []
    
    view_ixds = [best_view_idx]
    views_pts = unique_pts[best_view_idx]

    for _ in range(1, viewCount):
        new_idx = -1
        new_pts = np.array([])
        for i in range(0, len(unique_pts)):
            if i in view_ixds: continue
            current_pts = np.union1d(views_pts, unique_pts[i])
            if current_pts.shape > new_pts.shape:
                new_idx = i
                new_pts = current_pts
        view_ixds.append(np.int64(new_idx))
        views_pts = new_pts
    return view_ixds
