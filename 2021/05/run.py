from dataclasses import dataclass
import numpy as np

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines



@dataclass
class Segment:
    x1: int
    y1: int
    x2: int
    y2: int


def star1(filename, star2=False):
    lines = get_input(filename)
    segments = []
    maxpos = [0,0]
    for line in lines:
        segment = [[int(s) for s in pair.split(",")] for pair in line.split(" -> ")]
        segment = Segment(
            segment[0][0],
            segment[0][1],
            segment[1][0],
            segment[1][1],
        )
        segments.append(segment)
        maxpos[0] = max(maxpos[0], segment.x1)
        maxpos[0] = max(maxpos[0], segment.x2)
        maxpos[1] = max(maxpos[1], segment.y1)
        maxpos[1] = max(maxpos[1], segment.y2)

    maxpos[0] += 1
    maxpos[1] += 1
    grid = np.zeros(maxpos, dtype=int)
    for segment in segments:
        if segment.x1 == segment.x2:
            x = segment.x1
            start = min(segment.y1, segment.y2)
            stop = max(segment.y1, segment.y2)
            for y in range(start, stop+1):
                grid[y, x] += 1
        elif segment.y1 == segment.y2:
            y = segment.y1
            start = min(segment.x1, segment.x2)
            stop = max(segment.x1, segment.x2)
            for x in range(start, stop+1):
                grid[y, x] += 1
        else:
            if not star2:
                continue

            if segment.x2 > segment.x1:
                xx = list(range(segment.x1, segment.x2+1))
            else:
                xx = list(range(segment.x1, segment.x2-1, -1))
            
            if segment.y2 > segment.y1:
                yy = list(range(segment.y1, segment.y2+1))
            else:
                yy = list(range(segment.y1, segment.y2-1, -1))
                
            assert len(xx) == len(yy)
            for x, y in zip(xx, yy):
                grid[y, x] += 1
    
    # print(grid)
    return np.sum(grid >= 2)


def tests():
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 5, f"wrong answer: {ans}"
    
    ans = star1("example.txt", star2=True)
    print(f"example star 2: {ans}")
    assert ans == 12, f"wrong answer: {ans}"

if __name__ == "__main__":
    tests()
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 6005

    ans = star1("input.txt", star2=True)
    print(f"star 2: {ans}")
    assert ans == 23864
