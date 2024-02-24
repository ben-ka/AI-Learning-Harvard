
class Probability():

    def __init__(self, width, height, mines):
        self.grid = {}
        self.width = width
        self.height = height
        self.mines = mines
        for i in range(height):
            for j in range(width):
                tupleLocation = (i,j)
                self.grid.update({tupleLocation : float(self.mines / (self.width * self.height))})
        
    
    def CellMine(self,location):
        self.grid[location] = 1
    
    def CellSafe(self,location):
        self.grid[location] = 0
    
    
    
    

    def HandleWithSentence(self, sentence, known_safes, known_mines, explored_cells):
        if sentence.count != 0:
            
            changed_probability = []
            for cell in sentence.cells:
                if cell not in known_mines and cell not in known_safes and cell not in explored_cells:
                    
                    changed_probability.append(cell)
                elif cell in known_mines:
                    sentence.count -= 1
            if changed_probability:
                for cells in changed_probability:
                    new_probability = max(float(sentence.count / len(changed_probability)), self.grid[cells])
                    self.grid[cells] = new_probability
                # if self.grid[cells] >
                
            
                


            




