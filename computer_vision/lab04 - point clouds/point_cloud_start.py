import copy
import numpy as np
import open3d as o3d

def rknn_test(pcd):
	r"""
	Method which tests the functionality of the Hybrid KDTree build for finding nearest neighbours 
	with open3d. The Hybrid KNN combines the the KNN search with the RNN search returning at most k 
	nearest neighbors that have distances to the anchor point less than a given radius.

	:param pcd: input point cloud
	"""
	print("Paint the point cloud gray.")
	pcd.paint_uniform_color([0.5, 0.5, 0.5])
	pcd_tree = o3d.geometry.KDTreeFlann(pcd)

	print("Paint the 1st point red.")
	pcd.colors[1] = [1, 0, 0]

	print("Find its 2000 nearest neighbors and paint them blue.")
	[k, idx, _] = pcd_tree.search_knn_vector_3d(pcd.points[1500], 2000)
	np.asarray(pcd.colors)[idx[1:], :] = [0, 0, 1]

	print("Find its neighbors with distance less than 0.02 and paint them green.")
	[k, idx, _] = pcd_tree.search_radius_vector_3d(pcd.points[1500], 0.02)
	np.asarray(pcd.colors)[idx[1:], :] = [0, 1, 0]

	print("Visualize the point cloud.")
	o3d.visualization.draw_geometries([pcd])


def display_outlier(cloud, ind):
	r"""
	Helper which graphically visualise inlier and outliers.

	:param cloud: input point cloud 
	:param ind: inlier indices
	"""

	inlier = cloud.select_by_index(ind)
	outlier = cloud.select_by_index(ind, invert=True)

	print("Showing outliers (red) and inliers (gray): ")
	outlier.paint_uniform_color([1, 0, 0])
	inlier.paint_uniform_color([0.8, 0.8, 0.8])
	o3d.visualization.draw_geometries([inlier, outlier])


if __name__ == "__main__":
	# Creates the reference frame with the axis
	# ref_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.025, origin=[0,0,0])
	
	'''
	Translation, rotation, scaling and affine transformation
	'''

	# Read point cloud
	pcd = o3d.io.read_point_cloud('material/bunny/bunny.ply')
	
	# Translate each point by a certain vector
	translated_pcd = copy.deepcopy(pcd).translate([0.3, 0, 0])

	# Rotate each point around a pivot
	R = pcd.get_rotation_matrix_from_xyz([np.pi/2, 0, np.pi]) # Translate the radian angles to a rotation matrix
	rotated_pcd = copy.deepcopy(pcd).rotate(R, [0, 0, 0])
	
	# Apply scaling to all the points
	scaled_pcd = copy.deepcopy(pcd).scale(3.0, pcd.get_center())

	# All of the previous transformation can be summarized by a single matrix: affine transformaton
	T = np.eye(4) # Create square 4x4 diagonal matrix
	T[:3, :3] = R # Add rotation
	T[:3, 3] = [0.2, 0, 0.1] # Add translation
	T[3, 3] = 1/5 # Add scaling
	transformed_pcd = copy.deepcopy(pcd).transform(T)

	# Display point clouds
	# o3d.visualization.draw_geometries([pcd, translated_pcd, rotated_pcd, scaled_pcd, transformed_pcd])

	'''
	Downsampling, normal estimation and cropping
	'''
	
	# Downsampling points
	downpcd = copy.deepcopy(pcd).voxel_down_sample(0.005) # Voxel window size for downsampling. Larger window = less sampled points

	# Normals estimation: estimate the normal vectors of the surfaces of the object.
	# Tow main problems to solve in normals estimation:
	# 1) Sign of the normal: find the right orientation of the surface
	# 2) Scale factor: choose the right number of k nearest points to determine the surface

	# Visualize k-nearest-neighbors of a point
	# rknn_test(pcd) 

	# Estimate normals
	#pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=10, max_nn=30))
	#pcd.normalize_normals()
	#pcd.orient_normals_consistent_tangent_plane(30)

	# Interactive cropping
	# o3d.visualization.draw_geometries_with_editing([pcd])

	# Remove ears from point cloud
	ears = o3d.io.read_point_cloud('material/bunny/cropped_ears.ply')
	dists = np.asarray(pcd.compute_point_cloud_distance(ears))

	ind = np.where(dists > 0.0001)[0] # Keep pints that does not have a small distance w.r.t to the ears' points
	bunny_no_ears = pcd.select_by_index(ind)

	# Outliers detection
	#cl, ind = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=1.0)
	cl, ind = pcd.remove_radius_outlier(nb_points=50, radius=0.005)
	#display_outlier(pcd, ind)

	# Surface reconstruction
	radii = [0.005]
	mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(radii))
	mesh.compute_vertex_normal()
	o3d.visualization.draw_geometries([mesh])


	# Display point clouds
	o3d.visualization.draw_geometries([bunny_no_ears])
