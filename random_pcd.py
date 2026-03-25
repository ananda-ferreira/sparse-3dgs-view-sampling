# import os
# import numpy as np
# from plyfile import PlyData, PlyElement

# from utils.sh_utils import SH2RGB
# from scene.colmap_loader import read_points3D_text, read_points3D_binary  
# from scene.dataset_readers import storePly

# ## from 3dgs
# # def storePly(path, xyz, rgb):
# #     # Define the dtype for the structured array
# #     dtype = [('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
# #             ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
# #             ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]

# #     normals = np.zeros_like(xyz)

# #     elements = np.empty(xyz.shape[0], dtype=dtype)
# #     attributes = np.concatenate((xyz, normals, rgb), axis=1)
# #     elements[:] = list(map(tuple, attributes))

# #     # Create the PlyData object and write to file
# #     vertex_element = PlyElement.describe(elements, 'vertex')
# #     ply_data = PlyData([vertex_element])
# #     ply_data.write(path)


# ## from corgs

# def topk_(matrix, K, axis=1):
#     if axis == 0:
#         row_index = np.arange(matrix.shape[1 - axis])
#         topk_index = np.argpartition(-matrix, K, axis=axis)[0:K, :]
#         topk_data = matrix[topk_index, row_index]
#         topk_index_sort = np.argsort(-topk_data,axis=axis)
#         topk_data_sort = topk_data[topk_index_sort,row_index]
#         topk_index_sort = topk_index[0:K,:][topk_index_sort,row_index]
#     else:
#         column_index = np.arange(matrix.shape[1 - axis])[:, None]
#         topk_index = np.argpartition(-matrix, K, axis=axis)[:, 0:K]
#         topk_data = matrix[column_index, topk_index]
#         topk_index_sort = np.argsort(-topk_data, axis=axis)
#         topk_data_sort = topk_data[column_index, topk_index_sort]
#         topk_index_sort = topk_index[:,0:K][column_index,topk_index_sort]
#     return topk_data_sort

# def create_rand_ply(source_path, ply_path, num_pts=1000):
#     """ 
#     Generates random pcd, stores it in a ply file.

#     Returns: path of ply file which stores the random point cloud.
#     """
#     print('Init random point cloud.')
    
#     # get xyz to generate rand pcd shape
#     try:
#         bin_path = os.path.join(source_path, "sparse/0/points3D.bin")
#         xyz, rgb, _ = read_points3D_binary(bin_path)
#     except:
#         txt_path = os.path.join(source_path, "sparse/0/points3D.txt")
#         xyz, rgb, _ = read_points3D_text(txt_path)
#     pcd_shape = (topk_(xyz, 100, 0)[-1] + topk_(-xyz, 100, 0)[-1])

#     # generate random points and shs
#     num_pts = 10_00
#     xyz = np.random.random((num_pts, 3)) * pcd_shape * 1.3 - topk_(-xyz, 100, 0)[-1] # - 0.15 * pcd_shape
#     print(f"Generating random point cloud ({num_pts})...")
#     shs = np.random.random((num_pts, 3)) / 255.0
#     storePly(ply_path, xyz, SH2RGB(shs) * 255)
        
# if __name__ == "__main__":
    
#     source_path = "data/"
#     ply_path = os.path.join(source_path, "points3D_random.ply") 
#     ds, scene = "db", "playroom"
#     copy_path = f"{ds}/{scene}/sparse/0/"

#     if not os.path.exists(ply_path):
#         print("Creating random.ply, will happen only the first time you open the scene.")
#         create_rand_ply(source_path, ply_path, num_pts=1000)

    
