import numpy as np

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

n = len(lines)
n = len(lines[0])
trees = np.empty((n, n),  dtype=int)
for i in range(n):
    for j in range(n):
        trees[i, j] = lines[i][j]
    
visible = np.zeros((n, n),  dtype=bool)
    
# left to right
visible[:, 0] = 1
highest_seen = np.zeros(n, dtype=int)
for j in range(n):
    visible[:, j] += trees[:, j] > highest_seen
    highest_seen = np.maximum(highest_seen, trees[:, j])

# right to left
visible[:, n-1] = 1
highest_seen = np.zeros(n, dtype=int)
for j in range(n)[::-1]:
    visible[:, j] += trees[:, j] > highest_seen
    highest_seen = np.maximum(highest_seen, trees[:, j])

# top to bottom
visible[0, :] = 1
highest_seen = np.zeros(n, dtype=int)
for i in range(n):
    visible[i, :] += trees[i, :] > highest_seen
    highest_seen = np.maximum(highest_seen, trees[i, :])

# bottom to top
visible[n-1, :] = 1
highest_seen = np.zeros(n, dtype=int)
for i in range(n)[::-1]:
    visible[i, :] += trees[i, :] > highest_seen
    highest_seen = np.maximum(highest_seen, trees[i, :])

print(np.sum(np.sum(visible)))

scores = np.zeros((n, n), dtype=int) + 1
for i in range(0,n):
    for j in range(0,n):
        
        row = trees[i,:]
        col = trees[:,j]
        
        h = trees[i,j]
        
        # search left to right
        score = 0
        for jj in range(j+1, n):
            if row[jj] >= h:
                score += 1
                break
            score += 1
        scores[i,j] *= score

        # search right to left
        score = 0
        for jj in range(0, j)[::-1]:
            if row[jj] >= h:
                score += 1
                break
            score += 1
        scores[i,j] *= score

        # search top to bottom
        score = 0
        for ii in range(i+1, n):
            if col[ii] >= h:
                score += 1
                break
            score += 1
        scores[i,j] *= score

        # search bottom to top
        score = 0
        for ii in range(0, i)[::-1]:
            if col[ii] >= h:
                score += 1
                break
            score += 1
        scores[i,j] *= score

print(np.max(np.max(scores)))