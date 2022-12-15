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

    print_map(sensors, beacons, x_lim, y_lim, y=10)
    
    y = 10
    row = np.zeros(m, dtype=int)
    for sensor, beacon in zip(sensors, beacons):
        # x = sensor.x
        
        # if sensor.y <= y and beacon.y >= y:
        #     # sensor below line and beacon above
        #     pass
        # elif sensor.y >= y and beacon.y <= y:
        #     # sensor above line and beacon below
        #     pass
        
        
        # dy = abs(beacon.y - sensor.y) - abs(sensor.y - y)
        # print(dy)
        
        
        
        # size of diamond at sensor position
        # calculated using l1 distance (manhattan distance)
        # max_width = abs(beacon.x - sensor.x)
        max_radius = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
        # max_width = 2*max_distance

        # calculate width of "diamond" that overlaps with y=<wanted line>
        distance_to_line = abs(sensor.y - y)
        if distance_to_line > max_radius:
            continue

        radius = max_radius - distance_to_line
        if radius == 0:
            # check if I'm stupid
            assert(distance_to_line == max_radius)

        print(f"{radius = }")
        
        # max_length = dx
        # length = dx - 
        
        # index shifted by x_min
        i = sensor.x + abs(x_lim[0])
        i0 = i - int(radius)
        i1 = i + int(radius)
        row[i0:i1+1] = 1
        
        if beacon.y == y:
            row[beacon.x + abs(x_lim[0])] = 2
        if sensor.y == y:
            row[sensor.x + abs(x_lim[0])] = 3

    print(row[-4+abs(x_lim[0]):27+abs(x_lim[0])])

    # print(np.sum(row==1))
    # print(np.sum(row==1)/float(row.shape[0]))
    print(f"star 1: {np.sum(row==1)}")


def star1():
    lines = []
    with open("input.txt") as file:
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

    # print_map(sensors, beacons, x_lim, y_lim)

    # sensors.sort(key=lambda a: a.x)
    assert(sorted(sensors, key=lambda a: a.x)[0].x == 24076)

    # beacons.sort(key=lambda a: a.x)
    assert(sorted(beacons, key=lambda a: a.x)[0].x == -615866)


    # y = 2000000
    # sensor_idx = 0
    # beacon_idx = 0
    # for x in range(x_lim[0], x_lim[1]):
    #     # find nearest sensor and beacon
    #     for sensor, beacon in zip(sensors, beacons):
    #         if sensor[0] == x:
    #             print(sensor)
    #         if beacon[0] == x:
    #             print(beacon)

    y = 2000000
    row = np.zeros(m, dtype=int)
    for sensor, beacon in zip(sensors, beacons):
        # size of diamond at sensor position
        # calculated using l1 distance (manhattan distance)
        max_radius = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

        # calculate width of "diamond" that overlaps with y=<wanted line>
        distance_to_line = abs(sensor.y - y)
        if distance_to_line > max_radius:
            continue

        radius = max_radius - distance_to_line
        if radius == 0:
            # check if I'm stupid
            assert(distance_to_line == max_radius)

        print(f"{radius = }")
        
        # index shifted by x_min
        i = sensor.x + abs(x_lim[0])
        i0 = i - int(radius)
        i1 = i + int(radius)
        row[i0:i1+1] = 1
        
        if beacon.y == y:
            row[beacon.x + abs(x_lim[0])] = 2
        # if sensor.y == y:
        #     row[sensor.x + abs(x_lim[0])] = 3


    # print(np.sum(row==1))
    # print(np.sum(row==1)/float(row.shape[0]))
    print(f"star 1: {np.sum(row==1)}")

    # 992979 is too low
    # 4879436 is too high
    # 4879435 is too high
    # 2540142 is wrong
    # 4721467 is not right


if __name__ == "__main__":
    example()
    # star1()