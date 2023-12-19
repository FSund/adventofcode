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

def count_accepted(workflows, key, x_range, m_range, a_range, s_range):
    workflow = workflows[key]
    
    def do_action(action, x_range, m_range, a_range, s_range):
        if action == "A":
            # accepted
            return len(x_range) * len(m_range) * len(a_range) * len(s_range)
        elif action == "R":
            # rejected
            return 0
        else:
            key = action
            return count_accepted(workflows, key, x_range, m_range, a_range, s_range)
    
    n_accepted = 0
    for w in workflow:
        if ":" in w:
            rule, action = w.split(":")
            rule_int = int(rule[2:])
            operator = rule[1]
            if rule[0] == "x":
                if operator == ">":
                    if x_range.start > rule_int and x_range.stop > rule_int:
                        # whole range passes check
                        pass
                    elif x_range.start < rule_int and x_range.stop < rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(rule_int+1, x_range.stop)
                        n_accepted += do_action(action, accepted_range, m_range, a_range, s_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        x_range = range(x_range.start, rule_int+1)
                else: # operator == "<"
                    if x_range.start < rule_int and x_range.stop < rule_int:
                        # whole range passes check
                        n_accepted += do_action(action, x_range, m_range, a_range, s_range)
                    elif x_range.start > rule_int and x_range.stop > rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(x_range.start, rule_int)
                        n_accepted += do_action(action, accepted_range, m_range, a_range, s_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        x_range = range(rule_int, x_range.stop)
            elif rule[0] == "m":
                if operator == ">":
                    if m_range.start > rule_int and m_range.stop > rule_int:
                        # whole range passes check
                        pass
                    elif m_range.start < rule_int and m_range.stop < rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(rule_int+1, m_range.stop)
                        n_accepted += do_action(action, x_range, accepted_range, a_range, s_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        m_range = range(m_range.start, rule_int+1)
                else:
                    if m_range.start < rule_int and m_range.stop < rule_int:
                        # whole range passes check
                        n_accepted += do_action(action, x_range, m_range, a_range, s_range)
                    elif m_range.start > rule_int and m_range.stop > rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(m_range.start, rule_int)
                        n_accepted += do_action(action, x_range, accepted_range, a_range, s_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        m_range = range(rule_int, m_range.stop)
            elif rule[0] == "a":
                if operator == ">":
                    if a_range.start > rule_int and a_range.stop > rule_int:
                        # whole range passes check
                        pass
                    elif a_range.start < rule_int and a_range.stop < rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(rule_int+1, a_range.stop)
                        n_accepted += do_action(action, x_range, m_range, accepted_range, s_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        a_range = range(a_range.start, rule_int+1)
                else:
                    if a_range.start < rule_int and a_range.stop < rule_int:
                        # whole range passes check
                        n_accepted += do_action(action, x_range, m_range, a_range, s_range)
                    elif a_range.start > rule_int and a_range.stop > rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(a_range.start, rule_int)
                        n_accepted += do_action(action, x_range, m_range, accepted_range, s_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        a_range = range(rule_int, a_range.stop)
            elif rule[0] == "s":
                if operator == ">":
                    if s_range.start > rule_int and s_range.stop > rule_int:
                        # whole range passes check
                        pass
                    elif s_range.start < rule_int and s_range.stop < rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(rule_int+1, s_range.stop)
                        n_accepted += do_action(action, x_range, m_range, a_range, accepted_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        s_range = range(s_range.start, rule_int+1)
                else:
                    if s_range.start < rule_int and s_range.stop < rule_int:
                        # whole range passes check
                        n_accepted += do_action(action, x_range, m_range, a_range, s_range)
                    elif s_range.start > rule_int and s_range.stop > rule_int:
                        # no part of range passes check
                        continue
                    else:
                        # this range passes check
                        # should perform action
                        accepted_range = range(s_range.start, rule_int)
                        n_accepted += do_action(action, x_range, m_range, a_range, accepted_range)

                        # this range does not pass check
                        # this range should go to the next rule
                        s_range = range(rule_int, s_range.stop)

        
            # finished checking this rule
            # n_accepted += do_action(action, x_range, m_range, a_range, s_range)  # don't do this here
        else:
            # last rule, always performed
            n_accepted += do_action(w, x_range, m_range, a_range, s_range)
            
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
        
        
        
    # print(workflows)
    # print(items)
    
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
    n_accepted = count_accepted(workflows, "in", range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
    return n_accepted

def tests():
    workflows = parse_workflows(["in{x>3999:R,A}"])
    n = count_accepted(workflows, "in", range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
    assert n == 3999*(4000**3), f"wrong answer: {n} != {3999*(4000**3)}"

    
    workflows = parse_workflows(["in{x>3999:A,R}"])
    n = count_accepted(workflows, "in", range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
    assert n == 4000**3, f"wrong answer: {n} != {4000**3}"
    
    workflows = parse_workflows(["in{m>3999:A,R}"])
    n = count_accepted(workflows, "in", range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
    assert n == 4000**3
    
    workflows = parse_workflows(["in{a>3999:A,R}"])
    n = count_accepted(workflows, "in", range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
    assert n == 4000**3
    
    workflows = parse_workflows(["in{s>3999:A,R}"])
    n = count_accepted(workflows, "in", range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
    assert n == 4000**3
    
    workflows = parse_workflows(["in{x>3998:A,R}"])
    n = count_accepted(workflows, "in", range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
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
