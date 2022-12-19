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


def get_scan_with_buffer(lines, n):
    scan = np.zeros((n+2,n+2,n+2), dtype=bool)
    for line in lines:
        i, j, k = eval(line)
        scan[i+1, j+1, k+1] = 1
    return scan


def find_area_bfs(labels, start):
    visited = set() # to keep track of already visited nodes
    bfs_traversal = list()  # the BFS traversal result
    queue = list()  # queue
    parent = {}  # dict
    
    total_area = 0
    
    # push the root node to the queue and mark it as visited
    queue.append(start)
    visited.add(start)
    
    label = labels[start[0], start[1], start[2]]
    
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
        
        # start at max, subtract 1 for each neighbor with matching label
        current_area = 6
        
        # check all the neighbour nodes of the current node
        for translation in adjacent:
            pos = (
                current_pos[0] + translation[0],
                current_pos[1] + translation[1],
                current_pos[2] + translation[2],
            )
            
            # Make sure within range
            if (pos[0] > (labels.shape[0] - 1) or pos[0] < 0 
                or pos[1] > (labels.shape[1] - 1) or pos[1] < 0
                or pos[2] > (labels.shape[2] - 1) or pos[2] < 0 
            ):
                continue
        
            # only check matching labels
            if labels[pos[0],pos[1],pos[2]] != label:
                continue

            # update area
            current_area -= 1

            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            if pos not in visited:
                visited.add(pos)
                queue.append(pos)
                parent[pos] = current_pos

        total_area += current_area

    # print(f"{total_area = }")

    return bfs_traversal, total_area


def fill_water_bfs(labels, start, water_label=99):
    visited = set() # to keep track of already visited nodes
    bfs_traversal = list()  # the BFS traversal result
    queue = list()  # queue
    parent = {}  # dict
    
    labels_copy = np.copy(labels)
    
    # push the root node to the queue and mark it as visited
    queue.append(start)
    visited.add(start)
    
    label = labels[start[0], start[1], start[2]]
    
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
        
        labels_copy[current_pos[0],current_pos[1],current_pos[2]] = water_label
        
        # check all the neighbour nodes of the current node
        for translation in adjacent:
            pos = (
                current_pos[0] + translation[0],
                current_pos[1] + translation[1],
                current_pos[2] + translation[2],
            )
            
            # Make sure within range
            if (pos[0] > (labels.shape[0] - 1) or pos[0] < 0 
                or pos[1] > (labels.shape[1] - 1) or pos[1] < 0
                or pos[2] > (labels.shape[2] - 1) or pos[2] < 0 
            ):
                continue
            
            # only check matching labels
            if labels[pos[0],pos[1],pos[2]] != label:
                continue

            # if the neighbour nodes are not already visited, 
            # push them to the queue and mark them as visited
            if pos not in visited:
                labels_copy[pos[0],pos[1],pos[2]] = water_label

                visited.add(pos)
                queue.append(pos)
                parent[pos] = current_pos

    return labels_copy


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


def star1(filename):
    lines = get_input(filename)
    max_xyz = get_max_index(lines)
    scan = get_scan(lines, max_xyz+2)
    
    labels, N = cc3d.connected_components(scan, connectivity=6,return_N=True)
    # print(f"{N = }")
    # print(np.max(labels))
    
    stats = cc3d.statistics(labels)
    
    if False:
        plot_3d(labels)
    
    # max_label = max(stats["voxel_counts"][1:])
    voxel_counts = stats["voxel_counts"][1:]
    # print(f"{voxel_counts = }")
    max_label = 1 + max(range(len(voxel_counts)), key=voxel_counts.__getitem__)
    # print(f"{max_label = }")

    total_area = 0
    for label in range(1, N+1):
        # find starting point
        start = np.argmax([labels==label])
        start = np.unravel_index(start, labels.shape)
        # print(labels[start])
        # print(f"{start = }")
        
        _, area = find_area_bfs(labels, start)
        total_area += area
    
    # print(f"{total_area = }")
    
    return total_area


def star2(filename):
    lines = get_input(filename)
    max_xyz = get_max_index(lines)
    scan = get_scan_with_buffer(lines, max_xyz+1)
    
    labels, N = cc3d.connected_components(scan, connectivity=6,return_N=True)
    stats = cc3d.statistics(labels)
    voxel_counts = stats["voxel_counts"][1:]
    max_label = 1 + max(range(len(voxel_counts)), key=voxel_counts.__getitem__)
    
    # print(f"n labels: {N}")
    # print(f"{voxel_counts}")
    
    start = (1,1,1)
    
    water_label = 99
    new_labels = fill_water_bfs(labels, start, water_label)
    assert(water_label != max_label)
    
    # print(f"n old labels==0: {np.sum(labels==0)}")
    # print(f"n water: {np.sum(new_labels==water_label)}")

    # calculate area of "water" voxels
    
    # print(f"label: {new_labels[start[0], start[1], start[2]]}")
    assert(new_labels[start[0],start[1],start[2]] == water_label)
    _, area = find_area_bfs(new_labels, start)
    # print(area)
    
    # subtract boundaries
    area -= 2*(labels.shape[0]**2 + labels.shape[1]**2 + labels.shape[2]**2)
    print(f"star 2? {area}")
    
    # fill center with something instead
    
    # plot_3d(new_labels)
    # plt.show()
    

    return area


if __name__ == "__main__":
    assert(star1("example.txt") == 64)
    # print(f'star 1: {star1("input.txt")}')
    assert(star1("input.txt") == 3586)
    
    # print(f'star 2 example: {star2("example.txt")}')  # correct
    assert(star2("example.txt") == 58)
    
    star2("input.txt")
    
    # 2066 is too low
    # 2330 too high
    