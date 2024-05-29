import argparse
import dataloader.horto3dlm.dataset as dataset
import dataloader.laserscan as laserscan
import os
import numpy as np
import open3d as o3d
import tqdm
import time

def load_pose(file:str)->np.ndarray: 
    """ Loading the poses file to RAM. 
    The pose file as the default structure of KITTI poses.txt file:
    In each line, there are 16 values, which are the elements of a 4x4 Transformation matrix
    
    The elements are separated by spaces, and the values are in row-major order.

   [nframe,R11,R12,R13,tx,R21,R22,R23,ty,R31,R32,R33,tz,0,0,0,1]
    
    Args:
        file (str): default poses.txt file

    Returns:
        positions (np.array): array of positions (x,y,z) of the path (N,3)
        Note: N is the number of data points, No orientation is provided
    """
    assert os.path.isfile(file),"pose file does not exist: " + file
    pose_array = []
    frame_ids = []
    for line in open(file):
        values_str = line.strip().split(' ')
        frame_ids.append(int(values_str[0]))
        values = np.array([float(v) for v in values_str[1:]])
        coordinates = np.array(values).reshape(4,4)
        pose_array.append(coordinates)
 
    return(np.array(pose_array),np.array(frame_ids))

def main(args):
    
    sequence_path = os.path.join(args.root,"HORTO-3DLM",args.sequence,'slam','LIO_SAM_poses.txt')
    # load poses from txt
    tfs,frame_ids = load_pose(sequence_path)
    
    loader = dataset.file_structure(args.root,"HORTO-3DLM",args.sequence,position_file=None,verbose=True)
    scan   = laserscan.LaserScan(clean_zeros=True)
    maps = o3d.geometry.PointCloud()
    
    #vis = o3d.visualization.Visualizer()
    #vis.create_window()
    
    n_frames = len(loader)
    n_frames = 1000
    
    #calib_tf = 
   
    for i in tqdm.tqdm(range(n_frames),desc='Building maps'):
        pcd_file,name = loader._get_point_cloud_file_(i)
        scan.open_scan(pcd_file)
        points,remission = scan.get_points()
        tf = tfs[i]
        #gtf = np.dot(tf,gtf)
        source = o3d.geometry.PointCloud()
        source.points = o3d.utility.Vector3dVector(points)
        source_down = source.voxel_down_sample(voxel_size=0.1)
    
        source_global = source_down.transform(tf)
        maps += source_global

        #vis.update_geometry(maps)
            #self.vis.get_render_option().point_size = 1
        #vis.poll_events()
        #vis.update_renderer()
    # plot maps
    o3d.visualization.draw_geometries([maps])
        
   
        
    # Your code goes here


if __name__ == "__main__":
    # create input arguments
    parser = argparse.ArgumentParser("./build_maps")
    parser.add_argument("--root", default='/home/tiago/workspace/DATASET', help="Input file")
    parser.add_argument("--sequence", default='GWJ23', help="Input file")
    # Add your argument definitions here
    args, unparsed = parser.parse_known_args()
    
    main(args)