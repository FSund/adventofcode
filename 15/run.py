import numpy as np

def find_boundaries(lines):
    x_lim = [1e9, -1e9]
    y_lim = [1e9, -1e9]
    for line in lines:
        l = line.split(": closest beacon is at ")
        sensor = l[0].strip("Sensor at ").split(", ")
        sensor_x = int(sensor[0].split("=")[1])
        sensor_y = int(sensor[1].split("=")[1])
        
        beacon = l[1].split(", ")
        beacon_x = int(beacon[0].split("=")[1])
        beacon_y = int(beacon[1].split("=")[1])
        
        dx = abs(sensor_x - beacon_x)
        dy = abs(sensor_y - beacon_y)
        
        x = [sensor_x + dx, sensor_x - dx, beacon_x + dx, beacon_x - dx]
        x_max = max(x)
        x_min = min(x)
        y = [sensor_y + dy, sensor_y - dy, beacon_y + dy, beacon_y - dy]
        y_max = max(y)
        y_min = min(y)
        
        if x_min < x_lim[0]:
            x_lim[0] = x_min
        if x_max > x_lim[1]:
            x_lim[1] = x_max
        if y_min < y_lim[0]:
            y_lim[0] = y_min
        if y_max > y_lim[1]:
            y_lim[1] = y_max
        
    return x_lim, y_lim


class Sensor:
    def __init__(self, pos, beacon=None):
        self.x = pos[0]
        self.y = pos[1]
        self.beacon = beacon
    
    def __repr__(self):
        return f"Sensor at ({self.x}, {self.y})"


class Beacon:
    def __init__(self, pos, sensor=None):
        self.x = pos[0]
        self.y = pos[1]
        self.sensor = sensor
    
    def __repr__(self):
        return f"Beacon at ({self.x}, {self.y})"


def get_sensors_and_beacons(lines):
    sensors = []
    beacons = []
    for line in lines:
        l = line.split(": closest beacon is at ")
        sensor = l[0].strip("Sensor at ").split(", ")
        sensor_x = int(sensor[0].split("=")[1])
        sensor_y = int(sensor[1].split("=")[1])
        
        beacon = l[1].split(", ")
        beacon_x = int(beacon[0].split("=")[1])
        beacon_y = int(beacon[1].split("=")[1])
        
        sensors.append(Sensor([sensor_x, sensor_y]))
        beacons.append(Beacon([beacon_x, beacon_y]))
        sensors[-1].beacon = beacons[-1]
        beacons[-1].sensor = sensors[-1]
        
    return sensors, beacons


def _get_map_line(sensors, beacons, x_lim, y):
    i = y
    line = f"{i:3d} "
    for j in range(x_lim[0], x_lim[1]):
        add = "."
        for sensor, beacon in zip(sensors, beacons):
            if sensor.y == i and sensor.x == j:
                add = "S"
            elif beacon.y == i and beacon.x == j:
                add = "B"
        line += add

    return line


def print_map(sensors, beacons, x_lim, y_lim, y=None):
    # print same format as website
    if y:
        print(_get_map_line(sensors, beacons, x_lim, y))
    else:
        for y in range(y_lim[0], y_lim[1]):
            print(_get_map_line(sensors, beacons, x_lim, y))


def get_col(x_lim, y_lim, sensors, beacons, y):
    m = x_lim[1] - x_lim[0]
    # n = y_lim[1] - y_lim[0]

    col = np.zeros(m, dtype=int)
    for sensor, beacon in zip(sensors, beacons):
        # size of diamond at sensor position
        # calculated using l1 distance (manhattan distance)
        max_radius = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

        # calculate width of "diamond" that overlaps with y=<wanted line>
        distance_to_line = abs(sensor.y - y)
        if distance_to_line > max_radius:
            continue

        radius = max_radius - distance_to_line
        # print(radius)
        if radius == 0:
            # check if I'm stupid
            assert(distance_to_line == max_radius)
            # assert(beacon.y == y or sensor.y == y)
        
        # index shifted by x_min
        i = sensor.x + abs(x_lim[0])
        i0 = i - radius
        if i0 < 0:
            raise RuntimeError(f"{i0 =}")
            i0 = 0
        i1 = i + radius
        if i1 >= col.shape[0]:
            raise RuntimeError(f"{i1 =}")
            i1 = col.shape[0] - 1
        
        col[i0:i1+1][col[i0:i1+1] == 0] = 1
        
        if beacon.y == y:
            col[beacon.x + abs(x_lim[0])] = 2
        if sensor.y == y:
            col[sensor.x + abs(x_lim[0])] = 3

    return col


def get_col_fast(x_lim, y_lim, sensors, beacons, y):
    m = x_lim[1] - x_lim[0]
    # n = y_lim[1] - y_lim[0]

    col = np.zeros(m, dtype=int)
    for sensor, beacon in zip(sensors, beacons):
        # size of diamond at sensor position
        # calculated using l1 distance (manhattan distance)
        max_radius = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

        # calculate width of "diamond" that overlaps with y=<wanted line>
        distance_to_line = abs(sensor.y - y)
        if distance_to_line > max_radius:
            continue

        radius = max_radius - distance_to_line
        
        # index shifted by x_min
        i = sensor.x + abs(x_lim[0])
        i0 = i - radius
        i1 = i + radius
        
        col[i0:i1+1] = 1
        
        if beacon.y == y:
            col[beacon.x + abs(x_lim[0])] = 2
        if sensor.y == y:
            col[sensor.x + abs(x_lim[0])] = 3

    return col


def check_col(sensors, beacons, y, x_max=4_000_000):
    # the distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.
    min_coord = 0
    max_coord = x_max

    if y < min_coord or y > max_coord:
        return False

    col = np.zeros(max_coord+1, dtype=bool)
    for sensor, beacon in zip(sensors, beacons):
        # size of diamond at sensor position
        # calculated using l1 distance (manhattan distance)
        max_radius = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

        # calculate width of "diamond" that overlaps with y=<wanted line>
        distance_to_line = abs(sensor.y - y)
        if distance_to_line > max_radius:
            continue

        radius = max_radius - distance_to_line
        x0 = sensor.x - radius
        x1 = sensor.x + radius

        # if all relevant coords are covered by this (sensor, beacon)-combo
        if x0 < min_coord and x1 > max_coord:
            return False
        
        i0 = x0  # col starts at x = 0 now
        i1 = x1
        
        # if all coords outside relevant range, skip this (sensor, beacon)-combo
        if (i0 < min_coord and i1 < min_coord) or (i0 > max_coord and i1 > max_coord):
            continue
            
        if i0 < min_coord:
            i0 = min_coord
        if i1 > max_coord:
            i1 = max_coord
        
        col[i0:i1+1] = True

    min_idx = np.argmin(col)
    if col[min_idx] == 0:
        return min_idx

    return False


def example():
    lines = []
    with open("example.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))


    x_lim, y_lim = find_boundaries(lines)
    # x_lim[0] -= 100
    # x_lim[1] += 100
    # print(x_lim, y_lim)

    m = x_lim[1] - x_lim[0]
    n = y_lim[1] - y_lim[0]
    # print(f"gbytes = {m*n/8/1024/1024/1024}")

    # Consult the report from the sensors you just deployed. 
    # In the row where y=2000000, how many positions cannot contain a beacon?

    sensors, beacons = get_sensors_and_beacons(lines)

    # print_map(sensors, beacons, x_lim, y_lim, y=10)
    
    sensors = [sensors[6]]
    beacons = [beacons[6]]
    
    # sensors = [sensors[6]]
    # beacons = [Beacon([20, 7])]
    
    # check line by line
    for y in range(y_lim[0], y_lim[1]):
        col = get_col(x_lim, y_lim, sensors, beacons, y)

        val2char = {0: ".", 1: "#", 2: "B", 3: "S"}
        line = f"{y:3d} "
        for val in col:
            line += val2char[val]
    
    # use matrix
    grid = np.zeros((m, n), dtype=int)
    for y in range(y_lim[0], y_lim[1]):
        col = get_col(x_lim, y_lim, sensors, beacons, y)
        j = y + abs(y_lim[0])
        grid[:,j] = col
    
    grid = np.transpose(grid)
    for i in range(grid.shape[0]):
        val2char = {0: ".", 1: "#", 2: "B", 3: "S"}
        
        y = i - abs(y_lim[0])
        line = f"{y:3d} "
        for j in range(grid.shape[1]):
            line += val2char[grid[i,j]]
        print(line)

    col = get_col(x_lim, y_lim, sensors, beacons, y=10)
    print(col)
    # print(row)
    # print(row[-4+abs(x_lim[0]):27+abs(x_lim[0])])

    # print(np.sum(row==1))
    # print(np.sum(row==1)/float(row.shape[0]))
    print(f"star 1: {np.sum(col==1)}")


def star1():
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))


    x_lim, y_lim = find_boundaries(lines)
    x_lim = [x_lim[0], 5870939]
    # x_lim[0] -= 200
    # x_lim[1] += 200
    # print(x_lim, y_lim)

    # m = x_lim[1] - x_lim[0]
    # n = y_lim[1] - y_lim[0]
    # print(f"gbytes = {m*n/8/1024/1024/1024}")

    # Consult the report from the sensors you just deployed. 
    # In the row where y=2000000, how many positions cannot contain a beacon?

    sensors, beacons = get_sensors_and_beacons(lines)

    # print_map(sensors, beacons, x_lim, y_lim)

    # sensors.sort(key=lambda a: a.x)
    assert(sorted(sensors, key=lambda a: a.x)[0].x == 24076)

    # beacons.sort(key=lambda a: a.x)
    assert(sorted(beacons, key=lambda a: a.x)[0].x == -615866)

    col = get_col(x_lim, y_lim, sensors, beacons, y=2000000)
    # col = get_col_fast(x_lim, y_lim, sensors, beacons, y=2000000)

    # print(np.sum(row==1))
    # print(np.sum(row==1)/float(row.shape[0]))
    result = np.sum(col==1)
    assert(result == 4827924)
    print(f"star 1: {result}")

    # 992979 is too low
    # 4879436 is too high
    # 4879435 is too high
    # 2540142 is wrong
    # 4721467 is not right
    # 4721467 ........
    # 4721467
    # 4721567
    # 4827924 IS CORRECT


def star2():
    lines = []
    with open("input.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))


    x_lim, y_lim = find_boundaries(lines)
    x_lim = [x_lim[0], 5_870_939]

    # Your handheld device indicates that the distress signal is coming from a 
    # beacon nearby. The distress beacon is not detected by any sensor, but the 
    # distress beacon must have x and y coordinates each no lower than 0 and no 
    # larger than 4 000 000.

    # To isolate the distress beacon's signal, you need to determine its tuning 
    # frequency, which can be found by multiplying its x coordinate by 4000000 
    # and then adding its y coordinate.

    # In the example above, the search space is smaller: instead, the x and y 
    # coordinates can each be at most 20. With this reduced search area, there 
    # is only a single position that could have a beacon: x=14, y=11. The 
    # tuning frequency for this distress beacon is 56000011.

    # Find the only possible position for the distress beacon. What is its 
    # tuning frequency?

    sensors, beacons = get_sensors_and_beacons(lines)

    for y in range(4_000_000):
        # col = get_col_fast(x_lim, y_lim, sensors, beacons, y)
        min_idx = check_col(sensors, beacons, y)
        if y % 1000 == 0:
            print(y)
        if min_idx:
            print(f"{min_idx = } {y = }")
            print(f"star 2: {min_idx*4_000_000 + y}")
            break

    # perhaps
    #     2973000
    #     min_idx = 3244277 y = 2973564
    #     star 2: 12977110973564


def star2_example():
    lines = []
    with open("example.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))

    # Your handheld device indicates that the distress signal is coming from a 
    # beacon nearby. The distress beacon is not detected by any sensor, but the 
    # distress beacon must have x and y coordinates each no lower than 0 and no 
    # larger than 4 000 000.

    # To isolate the distress beacon's signal, you need to determine its tuning 
    # frequency, which can be found by multiplying its x coordinate by 4000000 
    # and then adding its y coordinate.

    # In the example above, the search space is smaller: instead, the x and y 
    # coordinates can each be at most 20. With this reduced search area, there 
    # is only a single position that could have a beacon: x=14, y=11. The 
    # tuning frequency for this distress beacon is 56000011.

    # Find the only possible position for the distress beacon. What is its 
    # tuning frequency?

    sensors, beacons = get_sensors_and_beacons(lines)
    max_coordinate = 20

    for y in range(max_coordinate):
        min_idx = check_col(sensors, beacons, y, x_max=max_coordinate)
        if y % 1000 == 0:
            print(y)
        if min_idx:
            print(f"{min_idx = } {y = }")
            print(f"star 2: {min_idx*4_000_000 + y}")
            break



if __name__ == "__main__":
    # example()
    # star1()
    star2()
    # star2_example()
