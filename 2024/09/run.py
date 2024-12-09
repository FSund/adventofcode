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
        
        return RuntimeError("No free block found")

def aoc(filename, star2=False):
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

    n = len(fsobjects)
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


def tests():
    ans = aoc("example.txt")
    print(f"example star 1: {ans}")
    assert ans == 1928, f"wrong answer: {ans}"
    
    # ans = aoc("example.txt", star2=True)
    # print(f"example star 2: {ans}")
    # assert ans == 34, f"wrong answer: {ans}"


if __name__ == "__main__":
    tests()
    
    ans = aoc("input.txt")
    print(f"star 1: {ans}")
    # assert ans == 271
    
    # ans = aoc("input.txt", star2=True)
    # print(f"star 2: {ans}")
    # assert ans == 994
