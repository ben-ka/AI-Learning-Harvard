from crossword import Crossword, Variable


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        
    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variables,words in self.domains.items():
            copySet = words.copy()
            for word in copySet:
                if len(word) != variables.length:
                    words.remove(word)



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[(x, y)] == None:
            return False
        else:
            index1 = self.crossword.overlaps[(x, y)][0]
            index2 = self.crossword.overlaps[(x, y)][1]
            
        
        
        isChange = False
        isOk = False
        copySet = self.domains[x].copy()
        for word in copySet:
            letter = word[index1]
            
            for otherWords in self.domains[y]:
                if otherWords[index2] == letter:
                    
                    isOk = True
                
            if isOk == False:
                isChange = True
                self.domains[x].remove(word)
            isOk = False
          
        return isChange



def main():
    crossword1 = Crossword("crossword/data/structure0.txt","crossword/data/words0.txt" )
    creator = CrosswordCreator(crossword1)
    x = Variable(4, 1, 'across', 4)
    y = Variable(0, 1, 'down', 5)
    creator.enforce_node_consistency()
    print(creator.revise(x,y))
    
    

main()
    
