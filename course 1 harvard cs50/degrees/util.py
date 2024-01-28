class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        if state in self.frontier:
            
            return True
        else:
            return False

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = Node(self.frontier[0].state, self.frontier[0].parent, self.frontier[0].action)
            if len(self.frontier) > 1:
                self.frontier = self.frontier[1:]
            else:
                self.frontier = []
            return node
        
        


