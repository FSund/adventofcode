def get_input(filename="input.txt"):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


MAX_LENGTH = 10

# node with pointer to next and prev for the new list
class Node:
    def __init__(self, data, prev=None):
        self.data = data
        self.next = None
        self.prev = prev


def print_list_n(node, n):
    for i in range(n):
        print(node.data)
        node = node.next


def get_node_zero(node):
    it = 0
    while node.data != 0:
        # print(f"{node.data = }")
        node = node.next
        it += 1
        if it > MAX_LENGTH:
            raise RuntimeError("unable to locate node.data == 0")
    return node


def get_elements(node):
    elements = []
    node = get_node_zero(node)
    it = 0
    while node.next.data != 0:
        elements.append(node.data)
        node = node.next
        it += 1
        if it > MAX_LENGTH:
            raise RuntimeError("unable to locate node.data == 0")
    
    # add final element
    elements.append(node.data)
    
    return elements


def get_elements_reverse(node):
    elements = []
    node = get_node_zero(node)
    it = 0
    while node.prev.data != 0:
        elements.append(node.data)
        node = node.prev
        it += 1
        if it > MAX_LENGTH:
            raise RuntimeError("unable to locate node.data == 0")
    
    # add final element
    elements.append(node.data)
    
    return elements


def print_list(node):
    e = get_elements(node)
    print(e)


def print_list_reverse(node):
    e = get_elements_reverse(node)
    print(e)


def check_list(node, n, nodes):
    seen_nodes = []
    for i in range(n):
        if node not in nodes:
            raise RuntimeWarning("node not in list of original nodes")
        if node in seen_nodes:
            raise RuntimeWarning(f"duplicate nodes (value: {node.data})")
        seen_nodes.append(node)
        node = node.next

    e1 = get_elements(node)
    e2 = get_elements_reverse(node)
    e1.sort()
    e2.sort()
    # assert(e1 == e2)
    if len(e1) > len(e2):
        raise RuntimeError("Element missing from reverse list")
    elif len(e2) > len(e1):
        raise RuntimeError("Element missing from forward list")


def increment(node, n, mod):
    # increment list by node.data
    n = n % mod
    # print(n)
    for i in range(n):
        node = node.next

    return node


def decrement(node, n, mod):
    # decrement list by node.data
    n = abs(n)
    n = n % mod
    for i in range(n):
        node = node.prev

    return node


def star1(filename):
    lines = get_input(filename)
    numbers = []
    for line in lines:
        numbers.append(int(line))

    global MAX_LENGTH
    MAX_LENGTH = len(lines)
    
    # create doubly linked list
    nodes = [Node(numbers[0])]  # the original list
    for i in range(1, len(numbers)):
        nodes.append(Node(data=numbers[i], prev=nodes[i-1]))
        nodes[i-1].next = nodes[i]

    # close loop
    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]
    
    # print_list(nodes[0])
    
    # loop through nodes(?)
    # point previous node to next node ("pop" current)
    # point next node.prev to previous
    # find position of node in new list
    # point next2 of previous and next node to current node
    for node in nodes:
         # skip moves that do nothing
        if node.data == 0:
            continue

        # remove current node from linked list
        new_next = node.next
        new_prev = node.prev
        node.prev.next = new_next
        node.next.prev = new_prev
        
        if node.data > 0:
            # increment list by node.data
            prev = increment(node.prev, node.data, MAX_LENGTH-1)
        elif node.data < 0:
            # decrement list by node.data
            prev = decrement(node.prev, node.data, MAX_LENGTH-1)
      
        # insert current node in linked list
        node_next = prev.next
        node_prev = prev
        prev_next = node
        prev_prev = prev.prev
        next_prev = node
        node.next = node_next
        node.prev = node_prev
        prev.next.prev = node
        prev.next = prev_next
        prev.prev = prev_prev

    # find coordinates
    head = get_node_zero(node)
    for i in range(1000):
        head = head.next
    x = head.data
    for i in range(1000):
        head = head.next
    y = head.data
    for i in range(1000):
        head = head.next
    z = head.data
    
    print([x,y,z])
    print(sum([x,y,z]))
    
    return sum([x,y,z])


def star2_example(filename):
    decryption_key = 811589153
    # decryption_key = 81158915
    # decryption_key = 2
    
    lines = get_input(filename)
    numbers = []
    for line in lines:
        numbers.append(int(line) * decryption_key)
        
    global MAX_LENGTH
    MAX_LENGTH = len(lines)
    
    # create doubly linked list
    nodes = [Node(numbers[0])]  # the original list
    for i in range(1, len(numbers)):
        nodes.append(Node(data=numbers[i], prev=nodes[i-1]))
        nodes[i-1].next = nodes[i]

    # close loop
    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]
    
    def mix(nodes):
        # loop through nodes(?)
        # point previous node to next node ("pop" current)
        # point next node.prev to previous
        # find position of node in new list
        # point next2 of previous and next node to current node
        for node in nodes:
            # skip moves that do nothing
            if node.data == 0:
                # print("data == 0, skipping")
                continue
            
            # remove current node from linked list
            new_next = node.next
            new_prev = node.prev
            node.prev.next = new_next
            node.next.prev = new_prev
            
            if node.data > 0:
                # increment list by node.data
                prev = increment(node.prev, node.data, MAX_LENGTH-1)
            elif node.data < 0:
                # decrement list by node.data
                prev = decrement(node.prev, node.data, MAX_LENGTH-1)
            
            # insert current node in linked list
            node_next = prev.next
            node_prev = prev
            prev_next = node
            prev_prev = prev.prev
            next_prev = node
            node.next = node_next
            node.prev = node_prev
            prev.next.prev = node
            prev.next = prev_next
            prev.prev = prev_prev
            
        
        return node
    
    for i in range(10):
        print(f"{i = }")
        node = mix(nodes)

    # find coordinates
    head = get_node_zero(node)
    for i in range(1000):
        head = head.next
    x = head.data
    for i in range(1000):
        head = head.next
    y = head.data
    for i in range(1000):
        head = head.next
    z = head.data
    
    print([x,y,z])
    print(sum([x,y,z]))
    
    return sum([x,y,z])


if __name__ == "__main__":
    s1 = star1("20/example.txt")
    assert(s1 == 3)
    
    s1 = star1("20/input2.txt")  # [2893, 3940, -446]
    assert(s1 == 6387)
    
    s1 = star1("20/input.txt")  # [-160, 9392, -930]
    assert(s1 == 8302)
    
    assert(star2_example("20/input.txt") == 656575624777)
    assert(star2_example("20/input2.txt") == 2455057187825)
