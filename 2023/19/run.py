from dataclasses import dataclass
from functools import cache
import numpy as np
from datetime import datetime
from pathlib import Path
from collections import OrderedDict
import heapq
from collections import deque

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    workflows = []
    for idx, line in enumerate(lines):
        if line == "":
            break
        workflows.append(line)
    
    items = []
    for line in lines[idx+1:]:
        # items
        items.append(line)
    
    return workflows, items

@dataclass
class Item:
    x: int
    m: int
    a: int
    s: int

def do_workflow(workflows, key, item):
    def do_action(action, item):
        if action == "A":
            # accepted
            return item.x + item.m + item.a + item.s
        elif action == "R":
            # rejected
            return 0
        else:
            return do_workflow(workflows, action, item)

    workflow = workflows[key]
    for w in workflow:
        if ":" in w:
            rule, action = w.split(":")
            x = item.x
            m = item.m
            a = item.a
            s = item.s
            if eval(rule):
                return do_action(action, item)
        else:
            # last rule, always performed
            action = w
            return do_action(action, item)
            
        

def star1(filename):
    workflows, items = get_input(filename)
    for i in range(len(items)):
        props = items[i][1:-1].split(",")
        items[i] = Item(*[int(prop.split("=")[1]) for prop in props])
    
    w = {}
    for workflow in workflows:
        key = workflow.split("{")[0]
        rules = workflow.split("{")[1].strip("}").split(",")
        w[key] = rules
        # print(f"{key}: {rules}")
        
    workflows = w
    sum = 0
    for item in items:
        # add up all ratings for all accepted parts
        sum += do_workflow(workflows, "in", item)
        
        
        
    # print(workflows)
    # print(items)
    
    return sum
        

def tests():
    pass

if __name__ == "__main__":
    tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 19114, f"wrong answer: {ans}"
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    # assert ans == 56678
    
    # ans = star2("example.txt")
    # print(f"example star 2: {ans}")
    # assert ans == 952408144115
    
    # ans = star2("input.txt")  
    # print(f"star 2: {ans}")
    # assert ans == 79088855654037
