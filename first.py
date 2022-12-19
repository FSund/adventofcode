import cc3d
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def get_input(filename="example.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


def get_max_index(lines):
    max_xyz = [0,0,0]
    for line in lines:
        xyz = eval(line)
        for i in range(3):
            if xyz[i] > max_xyz[i]:
                max_xyz[i] = xyz[i]
    return max(max_xyz)


def get_scan(lines, n):
    scan = np.zeros((n,n,n), dtype=bool)
    for line in lines:
        i, j, k = eval(line)
        scan[i, j, k] = 1
    return scan


def find_area_bfs(voxels, start):
    visited = set() # to keep track of already visited nodes
    bfs_traversal = list()  # the BFS traversal result
    queue = list()  # queue
    parent = {}  # dict
    
    # push the root node to the queue and mark it as visited
    queue.append(start)
    visited.add(start)
    
    adjacent = (
        (0, 0, -1), (0, 0, +1), 
        (0, -1, 0), (0, +1, 0), 
        (-1, 0, 0), (+1, 0, 0),
    )
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to bfs_traversal
        current_pos = queue.pop(0)
        bfs_traversal.append(current_pos)
        
        # check all the neighbour nodes of the current node
        for translation in adjacent:
            pos = (current_pos[0] + translation[0], current_pos[1] + translation[1])
            
            # Make sure within range
            if (pos[0] > (voxels.shape[0] - 1) or pos[0] < 0 
                or pos[1] > (voxels.shape[1] - 1) or pos[1] < 0
                or pos[2] > (voxels.shape[2] - 1) or pos[2] < 0 
            ):
                continue

            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            if pos not in visited:
                visited.add(pos)
                queue.append(pos)
                parent[pos] = current_pos

    return bfs_traversal


def plot_3d(labels):
    # set the colors of each object
    N = np.max(labels)
    norm = mpl.colors.Normalize(vmin=0, vmax=N+1)
    cmap = cm.hot
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    
    colors = np.empty(labels.shape + (4,))
    for label in range(1, N+1):
        colors[labels==label] = m.to_rgba(label)
    
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(labels, facecolors=colors)


if __name__ == "__main__":
    lines = get_input()
    max_xyz = get_max_index(lines)
    scan = get_scan(lines, max_xyz+1)
    
    labels, N = cc3d.connected_components(scan, connectivity=6,return_N=True)
    print(f"{N = }")
    print(np.max(labels))
    
    stats = cc3d.statistics(labels)
    
    plot_3d(labels)
