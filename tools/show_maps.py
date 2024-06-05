import argparse
import os
import open3d as o3d
import numpy as np
from scipy.spatial.transform import Rotation as R

PARAM = {
    'FR_ORCHARD_01_NOV23': {
        'min_bounds': [-200, -200, -2],
        'max_bounds': [200, 200, 5],
        'angles': [0, 1.1, 0]
    },
    'PT_GH_E3_JUN23':{
        'min_bounds': [-200, -200, -2],
        'max_bounds': [200, 200, 5],
        'angles': [0, 1.1, 0]
    }
}


def extract_roi_from_pcd(pcd,min_bound,max_bound):

    pcd_np = extract_roi(pcd,min_bound,max_bound)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pcd_np)
    return pcd

def extract_roi(point_cloud, min_bound, max_bound):
    """
    Extracts a region of interest (ROI) from a point cloud.

    Args:
        point_cloud (np.array): Nx3 array of points.
        min_bound (np.array): 1x3 array of minimum x, y, z coordinates of the ROI.
        max_bound (np.array): 1x3 array of maximum x, y, z coordinates of the ROI.

    Returns:
        np.array: Nx3 array of points within the ROI.
    """
    # Use logical indexing to find points within the bounds
    if not isinstance(point_cloud,np.ndarray):
        point_cloud = np.asarray(point_cloud.points)

    within_bounds = np.all((point_cloud >= min_bound) & (point_cloud <= max_bound), axis=1)
    # Extract the points within the bounds
    roi_points = point_cloud[within_bounds]
    return roi_points

def custom_draw_geometry(pcd, path, point_size=2.0):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    
    vis.add_geometry(path)
    render_option = vis.get_render_option()
    render_option.point_size = point_size  # Set the point size
    vis.run()
    vis.destroy_window()
    
    
def main(parser,**kwargs):
    
    map_file = os.path.join(parser.root,"HORTO-SLAM",parser.sequence,'GT','cloudGlobal.pcd')
    assert os.path.isfile(map_file),"Map file does not exist: " + map_file
    map = o3d.io.read_point_cloud(map_file)
    
    
    
    points_map = np.array(map.points).reshape(-1,3)
    cm_map = np.array(map.points).reshape(-1,3).mean(axis=0)
    points_map = points_map - cm_map.reshape(1,3)
    
    # rotate using the rotation matrix euler angles
    rotation = R.from_euler('xyz', [-0, 7, 0],degrees=True).as_matrix()
    
    points_map = np.dot(rotation,points_map.T).T
    map = o3d.geometry.PointCloud()
    map.points = o3d.utility.Vector3dVector(points_map)
    
    map = extract_roi_from_pcd(map, kwargs['min_bounds'],  kwargs['max_bounds'])
    
    trajectory_file = os.path.join(parser.root,"HORTO-SLAM",parser.sequence,'GT','trajectory.pcd')
    assert os.path.isfile(map_file),"Trajectory file does not exist: " + trajectory_file
    # Load the map
    trajectory = o3d.io.read_point_cloud(trajectory_file)
    
    trajectory_points = np.array(trajectory.points).reshape(-1,3)
    trajectory_points = trajectory_points - cm_map.reshape(1,3)
    print(trajectory_points.shape)
    
    trajectory_points = np.dot(rotation,trajectory_points.T).T
    
    trajectory_points[:,2] = trajectory_points[:,2] + 4.0
    
    trajectory = o3d.geometry.PointCloud()
    trajectory.points = o3d.utility.Vector3dVector(trajectory_points)
    trajectory.paint_uniform_color([1,0,0])
    
    # custom_draw_geometry(map, trajectory, point_size=2.0)
    # Visualize the map
    o3d.visualization.draw_geometries([map])
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser("./build_maps")
    parser.add_argument("--root", default='/home/tiago/workspace/Dropbox/SHARE/DATASET', help="Input file")
    parser.add_argument("--sequence", default='PT_GH_E3_JUN23', help="Input file")
    
    args = parser.parse_args()
    main(args,min_bounds=[-200,-200,-5],max_bounds=[200,200,5])