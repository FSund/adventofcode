class Dir:
    def __init__(self, name):
        self.size_of_files = 0
        self.total_size = None
        self.name = name
        self.dirs = {}
    
    def get_dir(self, path):
        if len(path) > 1:
            return self.dirs[path[1]].get_dir(path[1:])
        else:
            return self

    def add_subdir(self, name):
        if name not in d:
            self.dirs[name] = Dir(name)
        
    def mkdir_p(self, path):
        if path[0] in d:
            self.dirs[path[0]].mkdir_p(path[1:])

    def get_total_size(self):
        if not self.total_size:
            self.total_size = self.size_of_files + sum([dir.get_total_size() for dir in self.dirs])
        
        return self.total_size

    def __str__(self):
        return f"Dir({self.name})"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    d = Dir("foo")
    d.add_subdir("bar")
    d.add_subdir("test")
    print(d)
    print(d.get_dir(["foo"]))
    print(d.get_dir(["foo", "bar"]))
