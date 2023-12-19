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

def count_accepted(workflows, key, ranges):
    workflow = workflows[key]
    
    def do_action(action, ranges):
        if action == "A":
            # accepted
            accepted_count = 1
            for r in ranges:
                accepted_count *= len(r)
            return accepted_count
        elif action == "R":
            # rejected
            return 0
        else:
            key = action
            return count_accepted(workflows, key, ranges)
    
    n_accepted = 0
    for w in workflow:
        if ":" in w:
            rule, action = w.split(":")
            rule_int = int(rule[2:])
            operator = rule[1]
            idx = {"x": 0, "m": 1, "a": 2, "s": 3}[rule[0]]
            r = ranges[idx]
            
            if operator == ">":
                if r.start > rule_int and r.stop > rule_int:
                    # whole range passes check
                    pass
                elif r.start < rule_int and r.stop < rule_int:
                    # no part of range passes check
                    continue
                else:
                    # this range passes check
                    # should perform action
                    ranges2 = ranges.copy()
                    ranges2[idx] = range(rule_int+1, r.stop)
                    n_accepted += do_action(action, ranges2)

                    # this range does not pass check
                    # this range should go to the next rule
                    ranges[idx] = range(r.start, rule_int+1)
            else:  # operator == "<"
                if r.start < rule_int and r.stop < rule_int:
                    # whole range passes check
                    n_accepted += do_action(action, ranges)
                elif r.start > rule_int and r.stop > rule_int:
                    # no part of range passes check
                    continue
                else:
                    # this range passes check
                    # should perform action
                    ranges2 = ranges.copy()
                    ranges2[idx] = range(r.start, rule_int)
                    n_accepted += do_action(action, ranges2)

                    # this range does not pass check
                    # this range should go to the next rule
                    ranges[idx] = range(rule_int, r.stop)
        
        else:
            # last rule, always performed
            n_accepted += do_action(w, ranges)
            
    return n_accepted

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
        
    return sum

def parse_workflows(w):
    workflows = {}
    for workflow in w:
        key = workflow.split("{")[0]
        rules = workflow.split("{")[1].strip("}").split(",")
        workflows[key] = rules
        
    return workflows

def star2(filename):
    # How many distinct combinations of ratings will be accepted by the Elves' workflows?
    
    workflows, _ = get_input(filename)
    
    w = {}
    for workflow in workflows:
        key = workflow.split("{")[0]
        rules = workflow.split("{")[1].strip("}").split(",")
        w[key] = rules
        
    workflows = w
    n_accepted = count_accepted(workflows, "in", [range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)])
    return n_accepted

def tests():
    workflows = parse_workflows(["in{x>3999:R,A}"])
    n = count_accepted(workflows, "in", [range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)])
    assert n == 3999*(4000**3), f"wrong answer: {n} != {3999*(4000**3)}"

    
    workflows = parse_workflows(["in{x>3999:A,R}"])
    n = count_accepted(workflows, "in", [range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)])
    assert n == 4000**3, f"wrong answer: {n} != {4000**3}"
    
    workflows = parse_workflows(["in{m>3999:A,R}"])
    n = count_accepted(workflows, "in", [range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)])
    assert n == 4000**3
    
    workflows = parse_workflows(["in{a>3999:A,R}"])
    n = count_accepted(workflows, "in", [range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)])
    assert n == 4000**3
    
    workflows = parse_workflows(["in{s>3999:A,R}"])
    n = count_accepted(workflows, "in", [range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)])
    assert n == 4000**3
    
    workflows = parse_workflows(["in{x>3998:A,R}"])
    n = count_accepted(workflows, "in", [range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)])
    assert n == 2*4000**3
    
    

if __name__ == "__main__":
    tests()

    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 19114, f"wrong answer: {ans}"
    
    ans = star1("input.txt")
    print(f"star 1: {ans}")
    assert ans == 495298
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 167409079868000
    
    ans = star2("input.txt")  
    print(f"star 2: {ans}")
    assert ans == 132186256794011
