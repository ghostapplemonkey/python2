class Bfs():
    def solve(self, start ,end):
        self.queue = [start]
        self.explored = [start]
        self.parent = {}
        while self.queue != []:
            v = self.queue.pop(0)
            if v == end:
                return True
            for n in v.get_neighbors():
                if n not in self.explored:
                    self.parent[n] = v
                    self.queue.append(n)
                    self.explored.append(n)
            print(v)
            print(' ~ '.join([str(i) for i in self.queue]))
    def path(self, start ,end):
        v = end
        path = [v]
        while v!=start:
            v = self.parent[v]
            path.append(v)
        print(' - '.join([str(i) for i in path]))
        return path
            


 
        return False