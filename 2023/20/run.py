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
    LOW_COUNT = 0
    HIGH_COUNT = 0
    def __init__(self):
        self.calls = []
    
    def _call(self, pulse, input):
        print(f"Calling {self.name} with pulse: {pulse}")
        if pulse == HIGH:
            Module.HIGH_COUNT += 1
        else:
            Module.LOW_COUNT += 1
        
        for output in self.outputs:
            output.call(pulse, self)
    
    def add_call(self, pulse, input):
        self.calls.append((pulse, input))
    
    def process_pulses(self):
        for pulse, input in self.calls:
            self._call(pulse, input)
        n_calls = len(self.calls)
        self.calls = []
        return n_calls
    
    def set_outputs(self, outputs):
        self.outputs = outputs

class Broadcaster(Module):
    def __init__(self):
        super().__init__()
        self.name = "broadcaster"

    def call(self, pulse):
        # special case for broadcaster
        if pulse == HIGH:
            Module.HIGH_COUNT += 1
        else:
            Module.LOW_COUNT += 1

        for output in self.outputs:
            output.add_call(pulse, self)

class FlipFlop(Module):
    def __init__(self, name):
        super().__init__()
        self.state = LOW
        self.name = name

    def call(self, pulse, input):
        print(f"Call FlipFlop {self.name} with pulse: {pulse}")
        if pulse == LOW:
            self.state = 1 - self.state
            pulse = self.state
            for output in self.outputs:
                output.add_call(pulse, self)


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

    def call(self, pulse, input):
        print(f"Call Conjunction {self.name} with pulse: {pulse}")
        self.states[input] = pulse
        if all(state == HIGH for state in self.states.values()):
            for output in self.outputs:
                output.add_call(LOW, self)
        else:
            for output in self.outputs:
                output.add_call(HIGH, self)

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
    
    for line in lines:
        module, outputs = line.split(" -> ")
        outputs = outputs.split(", ")
        if module == "broadcaster":
            modules[module].set_outputs([modules[output] for output in outputs])
        else:
            t = module[0]
            name = module[1:]
            modules[name].set_outputs([modules[output] for output in outputs])
            for output in outputs:
                if isinstance(modules[output], Conjunction):
                    modules[output].add_input(modules[name])
    return modules

def star1(filename):
    lines = get_input(filename)
    
    modules = get_modules(lines)

    Module.HIGH_COUNT = 0
    Module.LOW_COUNT = 0
    for i in range(1000):
        modules["broadcaster"].call(LOW)
    
    print(f"High count: {Module.HIGH_COUNT}, low count: {Module.LOW_COUNT}")
    return Module.HIGH_COUNT * Module.LOW_COUNT

def tests():
    lines = get_input("example.txt")
    modules = get_modules(lines)
    
    assert len(modules["broadcaster"].outputs) == 3
    assert len(modules["a"].outputs) == 1
    assert modules["a"].outputs[0] == modules["b"]
    assert len(modules["b"].outputs) == 1
    assert modules["b"].outputs[0] == modules["c"]
    assert len(modules["c"].outputs) == 1
    assert modules["c"].outputs[0] == modules["inv"]
    assert len(modules["inv"].outputs) == 1
    assert modules["inv"].outputs[0] == modules["a"]
    
    Module.HIGH_COUNT = 0
    Module.LOW_COUNT = 0
    modules["broadcaster"].call(LOW)
    n_calls = 1
    while n_calls:
        n_calls = 0
        for module in modules.values():
            print(f"Module {module.name}")
            n_calls += module.process_pulses()
            print()
        print()
    assert Module.HIGH_COUNT == 4
    assert Module.LOW_COUNT == 8


if __name__ == "__main__":
    tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 11687500, f"wrong answer: {ans}"

    # ans = star1("input.txt")
    # print(f"star 1: {ans}")
    # assert ans == 495298

    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 167409079868000

    # ans = star2("input.txt")
    # print(f"star 2: {ans}")
    # assert ans == 132186256794011
