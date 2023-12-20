from dataclasses import dataclass
from functools import cache
import numpy as np
from datetime import datetime
from pathlib import Path
from collections import OrderedDict
import heapq
from collections import deque

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
    
    def call(self, pulse, source) -> tuple[bool, Module, str]:
        # print(f"Call Output {self.name} with pulse: {pulse}")
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
    received from each of their connected input modules; they initially default 
    to remembering a low pulse for each input. When a pulse is received, the 
    conjunction module first updates its memory for that input. Then, if it 
    remembers high pulses for all inputs, it sends a low pulse; otherwise, it 
    sends a high pulse.
    """

    def __init__(self, name):
        super().__init__()
        self.states = {}
        self.name = name
    
    def add_input(self, input):
        self.states[input] = LOW

    def call(self, pulse, source) -> tuple[bool, Module, str]:
        # print(f"Call Conjunction {self.name} with pulse: {pulse}")
        self.states[source] = pulse
        calls = []
        if all(state == HIGH for state in self.states.values()):
            for output in self.outputs:
                calls.append((LOW, self.name, output))
        else:
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

def star1(filename):
    lines = get_input(filename)
    
    modules = get_modules(lines)
    # modules["output"] = 
    
    broadcaster_outputs = []
    for line in lines:
        if line.startswith("broadcaster"):
            broadcaster_outputs = line.split(" -> ")[1].split(", ")
    
    low_count = 0
    high_count = 0
    
    for i in range(1000):
        calls = deque()
        # button -> broadcaster
        low_count += 1
        for output in broadcaster_outputs:
            calls.append((LOW, "broadcaster", output))
        
        while calls:
            pulse, source, destination = calls.popleft()
            if pulse == LOW:
                low_count += 1
            else:
                high_count += 1
            # print(f"{source} {pulse} -> {destination}")
            calls.extend(modules[destination].call(pulse, source))
        
    print(f"{high_count = }, {low_count = }")
    
    return high_count * low_count

def tests():
    pass


if __name__ == "__main__":
    tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 32000000, f"wrong answer: {ans}"
    
    # ans = star1("example2.txt")
    # print(f"example star 1: {ans}")
    # assert ans == 11687500, f"wrong answer: {ans}"

    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 666795063

    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 167409079868000

    # ans = star2("input.txt")
    # print(f"star 2: {ans}")
    # assert ans == 132186256794011
