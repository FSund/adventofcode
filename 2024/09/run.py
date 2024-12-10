def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines

# Each file on disk also has an ID number based on the order of the files as 
# they appear before they are rearranged, starting with ID 0.
class FSObject:
    def __init__(self, size, id=None):
        self.blocks = [id] * size
        self.size = size
    
    def is_empty(self):
        return self.blocks.count(None) == len(self.blocks)

    def is_full(self):
        return self.blocks.count(None) == 0

    def get_last_file_block(self):
        assert not self.is_empty(), "Tried to get file block from empty object"
        for i in range(self.size)[::-1]:  # reverse loop
            if self.blocks[i] is not None:
                out = self.blocks[i]
                self.blocks[i] = None
                return out
        
        raise RuntimeError("No file block found")

    def insert_file_block(self, id):
        assert not self.is_full(), "Tried to insert block in full object"
        for i in range(self.size):
            if self.blocks[i] is None:
                self.blocks[i] = id
                return True
        
        raise RuntimeError("No free block found")

def star1(filename):
    lines = get_input(filename)
    line = lines[0]
    
    fsobjects = []
    id = 0
    for idx, size in enumerate(line):
        size = int(size)
        if idx % 2 == 0:
            # file
            fsobjects.append(FSObject(size, id))
            id += 1
        else:
            # free space
            fsobjects.append(FSObject(size, None))

    assert fsobjects[1].blocks.count(None)
    assert fsobjects[-1].blocks.count(None) < len(fsobjects[-1].blocks)
    contigous = False
    while not contigous:
        # find first with free space
        for idx, obj in enumerate(fsobjects):
            if obj.blocks.count(None):
                break
        
        free_space_obj = obj
        # print(f"Free space in {idx} ({obj.blocks})")
        
        # get last with something in it
        for idx, obj in enumerate(fsobjects[::-1]):
            if not obj.is_empty():
                break
        
        file_obj = obj
        # print(f"File in {idx} ({obj.blocks})")
        
        free_space_obj.insert_file_block(file_obj.get_last_file_block())
            
        # check if contigous
        # find last full
        for idx, obj in enumerate(fsobjects):
            if not obj.is_full():
                break
        
        # idx can be partially filled or empty, that doesn't matter
        
        # check that all after are empty
        contigous = True
        for obj in fsobjects[idx+1:]:
            if not obj.is_empty():
                contigous = False
                break

    pos = 0
    checksum = 0
    for obj in fsobjects:
        for block in obj.blocks:
            if block is None:
                break
            checksum += pos * block
            pos += 1

    return checksum


def get_string_repr(fsobjects):
    s = ""
    for obj in fsobjects:
        b = [str(b) for b in obj.blocks]
        s += "".join(b)
    s = s.replace("None", ".")
    return s


def star2(filename):
    lines = get_input(filename)
    line = lines[0]
    
    fsobjects = []
    id = 0
    for idx, size in enumerate(line):
        size = int(size)
        if idx % 2 == 0:
            # file
            fsobjects.append(FSObject(size, id))
            id += 1
        else:
            # free space
            fsobjects.append(FSObject(size, None))

    assert fsobjects[1].blocks.count(None)
    assert fsobjects[-1].blocks.count(None) < len(fsobjects[-1].blocks)
    
    # attempt to move each file once
    for idx in reversed(range(0, len(fsobjects), 2)):
        file_obj = fsobjects[idx]
        
        assert file_obj.is_full()
        if file_obj.size == 0:
            continue

        # find first with enough free space
        free_space_obj = None
        for _, obj in enumerate(fsobjects[0:idx]):
            if obj.blocks.count(None) >= len(file_obj.blocks):
                free_space_obj = obj
                break
        
        # if no free space found, skip moving this file
        if not free_space_obj:
            continue
        
        # move the whole file
        for block_idx, block in enumerate(file_obj.blocks):
            free_space_obj.insert_file_block(block)
            file_obj.blocks[block_idx] = None

    if len(fsobjects) < 20:
        s = get_string_repr(fsobjects)
        print(s)
        assert s == "00992111777.44.333....5555.6666.....8888.."
        

    pos = 0
    checksum = 0
    for obj in fsobjects:
        for block in obj.blocks:
            if block is None:
                block = 0
            checksum += pos * block
            pos += 1

    return checksum


def tests():
    ans = star1("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 1928, f"wrong answer: {ans}"
    
    ans = star2("example.txt")
    print(f"example star 2: {ans}")
    assert ans == 2858, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    # ans = star1("input.txt")
    # print(f"star 1: {ans}")
    # assert ans == 6353658451014
    
    ans = star2("input.txt")
    print(f"star 2: {ans}")
    # assert ans == 994
