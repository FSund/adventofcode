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


def go_deeper(valves, node_name, minutes_left, path):
    global max_pressures
    # print(f"{node_name}, {minutes_left}")

    # max pressure from children of this node
    max_pressure = 0
    
    for open_valve in [False, True]:
        pressure_from_this_node = 0
        if open_valve:
            minutes_left -= 1  # subtract time to open valve
            pressure_from_this_node = valves[node_name]["flow"] * minutes_left

        if minutes_left <= 0:
            break
        
        # go through connecting nodes
        for name in valves[node_name]["connections"]:
            if max_pressures[name][minutes_left - 1] != -1:
                pressure_released = max_pressures[name][minutes_left - 1]
            else:
                pressure_released, path = go_deeper(valves, name, minutes_left - 1, path)
                # if pressure_released > max_pressures[name][minutes_left - 1]:
                #     max_pressures[name][minutes_left - 1] = pressure_released
                
            if pressure_released > max_pressure:
                max_pressure = pressure_released
        
    if minutes_left == 18:
        print(f"{node_name}, {minutes_left}, {max_pressure + pressure_from_this_node}")
    
    if max_pressure + pressure_from_this_node > 1651:
        raise RuntimeError("Found too high pressure")

    # max pressure from this node and connections
    result = max_pressure + pressure_from_this_node
    
    # update dict
    # if max_pressures[name][minutes_left] != -1:
    #     raise RuntimeError(f"{name} {minutes_left} -> {max_pressures[name][minutes_left]}")
    max_pressures[node_name][minutes_left] = result

    return result, path


def brute_force(valves, start):
    queue = [].append(start)
    max_flow = 0
    path = []
    # while queue:
    #     name = queue.pop()
    #     for name in valves[name]["connections"]:
    #         queue.append(name)
    go_deeper(valves, start, 30, path=[start])


def star1_example():
    lines = []
    with open("example.txt") as file:
        for line in file:
            lines.append(line.strip("\n"))

    valves = get_valves(lines)
    n = 30
    
    global max_pressures
    for name in valves.keys():
        max_pressures[name] = np.empty(n, dtype=int)
        max_pressures[name].fill(-1)
    
    print(valves)
    start = "AA"
    brute_force(valves, start)    


if __name__ == "__main__":
    star1_example()
    # star1()
    # star2()
    # star2_example()

