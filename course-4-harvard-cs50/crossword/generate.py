import sys

from crossword import Crossword, Variable

STRUCTURE_PATH = "C:/Users/Administrator/OneDrive/Documents/Python-Projects/ai-learning/course-4-harvard-cs50/crossword/data/structure"

WORDS_PATH = "C:/Users/Administrator/OneDrive/Documents/Python-Projects/ai-learning/course-4-harvard-cs50/crossword/data/words"

class Queue():

    def __init__(self, initial = None):
        if initial is not None:
            self.queue = list(initial)
        else:
            self.queue = []
    
    def insert(self, value):
        self.queue.append(value)
    
    def remove(self):
        returned = self.queue.pop(0)
        return returned
    
    def length(self):
        return len(self.queue)
    
    def isEmpty(self):
        return self.length() == 0
    
    def __str__(self):
        return f"{self.queue}"

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
        self.relationship = dict()
        self.createRelDict()

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == variable.DOWN else 0)
                j = variable.j + (k if direction == variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

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

    def createRelDict(self):
        for key in self.crossword.overlaps:
            connectionSet = set()
            myVar = key[0]
            for otherKey in self.crossword.overlaps:
                if otherKey[0] == myVar:
                    connectionSet.add(otherKey[1])
            self.relationship[myVar] = connectionSet
        
    def domainsEmpty(self):

        for key, value in self.domains.items():
            if len(value) == 0:
                return True
        
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        if arcs is None:
            arcs = set()
            for variables, indexes in self.crossword.overlaps.items():
                if indexes is not None:
                    arcs.add(variables)
            
        
        queue = Queue(arcs)
        
        while queue.isEmpty() == False:
            if self.domainsEmpty():
                return False
            variables = queue.remove()
            varX = variables[0]
            varY = variables[1]
            isChange = self.revise(varX, varY)
            if isChange:
                for otherVar in self.relationship[varX]:
                    queue.insert((otherVar, varX))

        return True  
                
            






    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for key,value in self.domains.items():
            if key not in assignment.keys():
                return False
        
        for value in assignment.values():
            if value is None:
                return False
        
        return True
            


    def isConnOk(self, wordX, wordY, Indexes):
        if wordX[Indexes[0]] != wordY[Indexes[1]]:
            return False
         
        return True
    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for key,value in self.domains.items():
            if key not in assignment.keys():
                return False
        
        for value in assignment.values():
            if value is None:
                return False
        
        return True
            


    def isConnOk(self, wordX, wordY, Indexes):

        if Indexes is None:
            return True

        if wordX[Indexes[0]] != wordY[Indexes[1]]:
            return False
         
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for key,  value in assignment.items():
            for otherKey, otherValue in assignment.items():
                if key == otherKey:
                    continue

                if value == otherValue and key != otherKey:
                    return False
                
                if key != otherKey and self.crossword.overlaps[(key, otherKey)] != None:
                    if self.isConnOk(value, otherValue, self.crossword.overlaps[(key, otherKey)]) == False:
                        return False
        
        return True
        
            
            

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        old_list = list(self.domains[var])
        constraintCount = {}
        for word in old_list:
            count = 0  
            for otherVar in self.relationship[var]:
                if otherVar not in assignment:
                    for newWord in self.domains[otherVar]:
                        if self.isConnOk(word, newWord, self.crossword.overlaps[(var, otherVar)]) == False:
                            count += 1
            constraintCount[word] = count
        newList = []
        while len(constraintCount.values()) != 0:
            minCount = 10e10
            for key, value in constraintCount.items():
                if value < minCount:
                    minCount = value
                    minKey = key

            newList.append(minKey)
            constraintCount.pop(minKey)
        
        return newList




        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        minDomains = int(10e6)
        posVariables = []
        for var, possibleVal in self.domains.items():
            if var not in assignment:
                if minDomains >= len(possibleVal):

                    if minDomains == len(possibleVal):
                        posVariables.append(var)
                    else:
                        posVariables.clear()
                        posVariables.append(var)

                    minDomains = len(possibleVal)
        
        minDegree = 10e10
        for var in posVariables:
            if len(self.relationship[var]) < minDegree:
                minDegree = len(self.relationship[var])
                minVar = var
                
        return minVar



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        isOk = False
        if self.assignment_complete(assignment): 
            return assignment
        
        variable = self.select_unassigned_variable(assignment=assignment)
        domains = self.order_domain_values(variable, assignment)
        domains_before = {}
        for d in domains:
            assignment[variable] = d
            print(assignment)
            print()
            if self.consistent(assignment):
                isOk = True
                arcs = set()
                for relVar in self.relationship[variable]:
                    if relVar not in assignment:
                        arcs.add((relVar,variable))

                domains_before = self.domains
                
                if not(self.ac3(arcs = arcs)):
                    assignment.pop(variable)
                    self.domains = domains_before

                result = self.backtrack(assignment)
                if result != None:
                    return result
            
            assignment.pop(variable)
            

        
        return None

                



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)




if __name__ == "__main__":
    main()
