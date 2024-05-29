import argparse
import dataloader.horto3dlm.dataset as dataset
import dataloader.laserscan as laserscan
import os
import numpy as np
import open3d as o3d
import tqdm
import time
import matplotlib.pyplot as plt

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
    
    positions = tfs[:,0:3,3]
        
    # plot the path 2D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    arraw = np.eye(4)
    nframes = len(tfs)
    
    indices = np.arange(0,1500,5)
    for i in indices:
        tf = tfs[i]
        
        parrow = tf*arraw
        #ax.text(position[i,0],position[i,1],position[i,2],str(i))
        position =tf[0:3,3]
        
        # plot reference frame
        ax.quiver(position[0],position[1],position[2],parrow[0,0],parrow[0,1],parrow[0,2],color='r') # Args: x,y,z,u,v,w
        ax.quiver(position[0],position[1],position[2],parrow[1,0],parrow[1,1],parrow[1,2],color='g')
        ax.quiver(position[0],position[1],position[2],parrow[2,0],parrow[2,1],parrow[2,2],color='b')
    
    
    #ax.plot(position[:,0],position[:,1],position[:,2])
    # define min max for the plot
    xmni = np.min(positions[:,0])
    xmx = np.max(positions[:,0])
    ymni = np.min(positions[:,1])
    ymx = np.max(positions[:,1])
    zmni = np.min(positions[:,2])
    zmx = np.max(positions[:,2])
    
    print(xmni,xmx,ymni,ymx,zmni,zmx)
    ax.set_xlim3d(xmni, xmx)
    ax.set_ylim3d(ymni, ymx)
    ax.set_zlim3d(zmni, zmx)
    
    # set the aspect ratio of the 3D pot
    #ax.set_aspect('equal')
    #ax.axis('equal')
    plt.show()
    
    # Your code goes here


if __name__ == "__main__":
    # create input arguments
    parser = argparse.ArgumentParser("./build_maps")
    parser.add_argument("--root", default='/home/tiago/workspace/DATASET', help="Input file")
    parser.add_argument("--sequence", default='GWJ23', help="Input file")
    # Add your argument definitions here
    args, unparsed = parser.parse_known_args()
    
    main(args)