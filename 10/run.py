import numpy as np
import matplotlib.pyplot as plt

# Find the signal strength during the 
# 20th, 60th, 100th, 140th, 180th, and 220th cycles. 
# What is the sum of these six signal strengths?

# signal strength: the cycle number multiplied by the value of the X register)

lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip("\n"))

register = 1
cycle = 0
# sum_of_signal_strengths = 0
# targets = [20, 60, 100, 140, 180, 220]
m = 6
n = 40
screen = np.zeros((m, n), dtype=int)

def draw(cycle, screen, register):
    idx = cycle % (m*n)
    j = idx % n
    i = idx // 40
    
    if register - 1 <= j <= register + 1:
        screen[i, j] = 1

# def check_cycle(cycle):
#     global sum_of_signal_strengths
#     global register
#     if cycle in targets:
#         signal_strength = cycle*register
#         sum_of_signal_strengths += signal_strength


for line in lines:
    if "noop" in line:
        draw(cycle, screen, register)
        cycle += 1
        continue
    elif "addx" in line:
        draw(cycle, screen, register) # during first cycle of addx
        cycle += 1
        draw(cycle, screen, register) # during second cycle of addx
        cycle += 1
        register += int(line.split(" ")[-1])

# print(sum_of_signal_strengths)


fig, ax = plt.subplots()
# im = ax.imshow(tail_grid)
im = ax.imshow(screen)
# ax.grid()
plt.show()
