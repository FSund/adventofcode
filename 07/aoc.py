class FileSystem:
    def __init__(self):
        self.dirs = Dir("/")

    def mkdir_p(self, path):
        if len(path) > 1:
            self.dirs.mkdir_p(path[1:])

    def get_subdir(self, path):
        if len(path) == 1:
            return self.dirs
        else:
            return self.dirs.get_subdir(path[1:])

    def add_files(self, path, size):
        if len(path) == 1:
            self.dirs.size_of_files += size
        else:
            self.dirs.get_subdir(path[1:]).size_of_files += size
    
    def get_total_size(self):
        return self.dirs.get_total_size()

class Dir:
    totals = []

    def __init__(self, name):
        self.size_of_files = 0
        self.total_size = None
        self.name = name
        self.dirs = {}
    
    def get_subdir(self, path):
        if len(path) > 1: # nested
            # recursive
            return self.dirs[path[0]].get_subdir(path[1:])
        else:
            return self.dirs[path[0]]

    def add_subdir(self, name):
        if name not in self.dirs:
            self.dirs[name] = Dir(name)

    def mkdir_p(self, path):
        self.add_subdir(path[0])
        if len(path) > 1:
            self.dirs[path[0]].mkdir_p(path[1:])

    def get_total_size(self):
        if not self.total_size:
            self.total_size = self.size_of_files + sum([dir.get_total_size() for key, dir in self.dirs.items()])
            Dir.totals.append(self.total_size)
            # print(f"{self.name}: total size: {self.total_size}")
        
        return self.total_size

    def __str__(self):
        return f"Dir({self.name})"

    def __repr__(self):
        return self.__str__()
