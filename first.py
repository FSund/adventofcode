import numpy as np


class Valve:
    def __init__(self, flow, connections=[]):
        self.flow = flow
        self.connections = connections


def get_valves(lines):
    valves = {}
    for line in lines:
        name = line.lstrip("Valve ")[:2]
        flow = int(line.split("rate=")[-1].split(";")[0])
        connections = [c.strip() for c in line.split("to valve")[-1].strip("s").strip().split(", ")]
        valves[name] = {}
        valves[name]["flow"] = flow
        valves[name]["connections"] = connections
        
        for c in connections:
            if len(c) > 2:
                raise RuntimeError
    
    return valves


# max pressure from node XX with N remaining minutes
max_pressures = {}


def get_max_pressure(valves, node_name, minutes_left, path):
    global max_pressures

    # if max_pressures[node_name][minutes_left] != -1:
    #     raise RuntimeError

    max_pressure = 0  # max pressure from children of this node
    pressure_from_this_node = 0
    shortcut = False
    for open_valve in [False, True]:
        # TODO: Handle already opened valve!!!
        if open_valve:
            minutes_left -= 1  # subtract time to open valve
            pressure_from_this_node = valves[node_name]["flow"] * minutes_left
            
            # check new "minutes left"
            if max_pressures[node_name][minutes_left] != -1:
                shortcut = True
                max_pressure = max_pressures[name][minutes_left - 1]
                break

        if minutes_left <= 0:
            break
        
        # go through connecting nodes
        for name in valves[node_name]["connections"]:
            if max_pressures[name][minutes_left - 1] != -1:
                pressure_released = max_pressures[name][minutes_left - 1]
            else:
                pressure_released, path = get_max_pressure(valves, name, minutes_left - 1, path)
                max_pressures[node_name][minutes_left - 1] = pressure_released

            if max_pressure < pressure_released:
                max_pressure = pressure_released

    # max pressure from this node and connections
    result = max_pressure + pressure_from_this_node

    # if result > 1651:
    #     raise RuntimeError(f"Found too high pressure ({node_name}, ")

    # update dict
    # if max_pressures[node_name][minutes_left] != -1:
    #     if result != max_pressures[node_name][minutes_left]:
    #         raise RuntimeError(f"max_pressure[{node_name}][{minutes_left}] = {max_pressures[node_name][minutes_left]} != {result}")
    #     max_pressures[node_name][minutes_left] = result
    
    max_pressures[node_name][minutes_left] = result
    
    if minutes_left == 2:
        if not shortcut:
            print(f"{node_name}, {minutes_left}, {result}")

    return result, path


def brute_force(valves, start, minutes):
    queue = [].append(start)
    max_flow = 0
    path = []
    # while queue:
    #     name = queue.pop()
    #     for name in valves[name]["connections"]:
    #         queue.append(name)
    return get_max_pressure(valves, start, minutes, path=[start])


def star1_example():
    lines = []
    with open("example.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))

    valves = get_valves(lines)
    n = 3
    
    global max_pressures
    for name in valves.keys():
        max_pressures[name] = np.empty(n+1, dtype=int)
        max_pressures[name].fill(-1)
    
    print(valves)
    start = "AA"
    max_pressure, path = brute_force(valves, start, minutes=n)
    print(f"{max_pressure = }")
    print(f"{path = }")


if __name__ == "__main__":
    star1_example()
    # star1()
    # star2()
    # star2_example()

