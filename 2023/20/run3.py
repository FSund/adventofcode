from dataclasses import dataclass
from functools import cache
import numpy as np
from datetime import datetime
from pathlib import Path
from collections import OrderedDict
import heapq
from collections import deque
from math import lcm

HIGH = 1
LOW = 0

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines

class Module:
    # LOW_COUNT = 0
    # HIGH_COUNT = 0
    def __init__(self):
        pass
    
    def set_outputs(self, outputs):
        self.outputs = outputs

class Output(Module):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.called = False
    
    def call(self, pulse, source) -> tuple[bool, Module, str]:
        # print(f"Call Output {self.name} with pulse: {pulse}")
        if pulse == LOW:
            self.called = True
        return []

class Broadcaster(Module):
    def __init__(self):
        super().__init__()
        self.name = "broadcaster"

    def call(self, pulse, _source) -> tuple[bool, Module, str]:
        # print(f"Call Broadcaster with pulse: {pulse}")
        calls = []
        for output in self.outputs:
            calls.append((pulse, self.name, output))
            
        return calls

class FlipFlop(Module):
    def __init__(self, name):
        super().__init__()
        self.state = LOW
        self.name = name

    def call(self, pulse, _source) -> tuple[bool, Module, str]:
        # print(f"Call FlipFlop {self.name} with pulse: {pulse}")
        calls = []
        if pulse == LOW:
            self.state = 1 - self.state
            pulse = self.state
            for output in self.outputs:
                calls.append((pulse, self.name, output))
        return calls


class Conjunction(Module):
    """
    Conjunction modules (prefix &) remember the type of the most recent pulse 
    received from each of their connected input modules; 
    - they initially default to remembering a low pulse for each input. 
    - When a pulse is received, the conjunction module first updates its memory for that input. 
    - Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it 
    sends a high pulse.
    """

    def __init__(self, name):
        super().__init__()
        self.states = {}
        self.name = name
        self.all_high = False
    
    def add_input(self, input):
        self.states[input] = LOW

    def call(self, pulse, source) -> tuple[bool, Module, str]:
        # print(f"Call Conjunction {self.name} with pulse: {pulse}")
        self.states[source] = pulse
        calls = []
        if all(state == HIGH for state in self.states.values()):
            self.all_high = True
            for output in self.outputs:
                calls.append((LOW, self.name, output))
        else:
            self.all_high = False
            for output in self.outputs:
                calls.append((HIGH, self.name, output))
                
        return calls

def get_modules(lines):
    modules = {}
    for line in lines:
        module, outputs = line.split(" -> ")
        outputs = outputs.split(", ")
        if module == "broadcaster":
            modules[module] = Broadcaster()
        else:
            t = module[0]
            name = module[1:]
            if t == "%":
                modules[name] = FlipFlop(name)
            elif t == "&":
                modules[name] = Conjunction(name)
    
    modules["rx"] = Output("rx")
    modules["output"] = Output("output")
    
    # set up outputs
    for line in lines:
        module, outputs = line.split(" -> ")
        outputs = outputs.split(", ")
        if module == "broadcaster":
            modules[module].set_outputs([modules[output].name for output in outputs])
        else:
            t = module[0]
            name = module[1:]
            modules[name].set_outputs([modules[output].name for output in outputs])
            for output in outputs:
                if isinstance(modules[output], Conjunction):
                    modules[output].add_input(modules[name].name)
    return modules

def star2(filename):
    lines = get_input(filename)
    
    modules = get_modules(lines)
    # modules["output"] = 
    
    modules = get_modules(lines)
    # modules["output"] = 
    
    broadcaster_outputs = []
    for line in lines:
        if line.startswith("broadcaster"):
            broadcaster_outputs = line.split(" -> ")[1].split(", ")
    
    loops = {
        # "xp": 0,
        # "xl": 0,
        # "gp": 0,
        # "ln": 0,
        "zp": 0,
        "rg": 0,
        "sj": 0,
        "pp": 0,
    }
    for i in range(1000000000):  # button presses
        if i % 10000 == 0:
            print(f"{i = }")
        calls = deque()
        for output in broadcaster_outputs:
            calls.append((LOW, "broadcaster", output))
        
        while calls:
            pulse, source, destination = calls.popleft()
            calls.extend(modules[destination].call(pulse, source))
            if modules["zp"].all_high and loops["zp"] == 0:
                print(f"zp all_high at {i = }")
                loops["zp"] = i
            if modules["rg"].all_high and loops["rg"] == 0: 
                print(f"rg all_high at {i = }")
                loops["rg"] = i
            if modules["sj"].all_high and loops["sj"] == 0:
                print(f"sj all_high at {i = }")
                loops["sj"] = i
            if modules["pp"].all_high and loops["pp"] == 0:
                print(f"pp all_high at {i = }")
                loops["pp"] = i

            # if modules["xp"].all_high and loops["xp"] < 2:
            #     print(f"xp all_high at {i = }")
            #     loops["xp"] = i
            # if modules["xl"].all_high and loops["xl"] < 2:
            #     print(f"xl all_high at {i = }")
            #     loops["xl"] = i
            # if modules["gp"].all_high and loops["gp"] < 2:
            #     print(f"gp all_high at {i = }")
            #     loops["gp"] = i
            # if modules["ln"].all_high and loops["ln"] < 2:
            #     print(f"ln all_high at {i = }")
            #     loops["ln"] = i
            
            if all(val > 1 for val in loops.values()):
                # return loops["xp"] * loops["xl"] * loops["gp"] * loops["ln"]
                return (loops["zp"], loops["rg"], loops["sj"], loops["pp"])
    

def tests():
    pass


if __name__ == "__main__":
    tests()

    # ans = star1("example.txt")
    # print(f"example star 1: {ans}")
    # assert ans == 32000000, f"wrong answer: {ans}"
    
    # ans = star1("example2.txt")
    # print(f"example star 1: {ans}")
    # assert ans == 11687500, f"wrong answer: {ans}"

    # ans = star1("input.txt")
    # print(f"star 1: {ans}")
    # assert ans == 666795063

    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 167409079868000

    factors = star2("input.txt")
    common = lcm(*factors)
    print(f"{common = }")
    
    print([common/factor for factor in factors])
    
    ans = lcm(*[factor + 1 for factor in factors])
    
    
    print(f"star 2: {ans}")
    assert ans == 253302889093151
    
    # 253048940352000 too low
    # 253048940352000 too low
    # 253302889093151


# rg all_high at i = 3832
# pp all_high at i = 4020
# zp all_high at i = 4050
# sj all_high at i = 4056
    
# rg all_high at i = 7665
# pp all_high at i = 8041
# zp all_high at i = 8101
# sj all_high at i = 8113


# rg all_high at i = 11498
# pp all_high at i = 12062
# zp all_high at i = 12152
# sj all_high at i = 12170