class Bfs():
    def setup(self, start ,end, sw):
        self.queue = [start]
        self.explored = [start]
        self.parent = {}
        self.sw = sw
        self.start = start
        self.end = end
        self.result = False
    def solve(self):
        while self.queue != []:
            self.result = self.step()
            if self.result == True:
                return True
        return False
    def step(self):
        self.v = self.queue.pop(0)
        if self.v == self.end:
            return True
        if self.sw == 0:
            for n in self.v.get_neighbors():
                if n not in self.explored:
                    self.parent[n] = self.v
                    self.queue.append(n)
                    self.explored.append(n)
        else:
            for n in self.v.get_neighbors():
                if n not in self.explored:
                    self.parent[n] = self.v
                    self.queue.insert(0, n)
                    self.explored.append(n)
        return False
        print(self.v)
        print(' ~ '.join([str(i) for i in self.queue]))
    def path(self):
        self.v = self.end
        path = [self.v]
        while self.v!=self.start:
            self.v = self.parent[self.v]
            path.insert(0,self.v)
        print(' - '.join([str(i) for i in path]))
        return path