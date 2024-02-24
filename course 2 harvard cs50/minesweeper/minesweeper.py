import itertools
import random
import probability


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"


    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        known_mines_set = set()

        if self.count == 0:
            return known_mines_set

        if self.cells is not None: 
            if self.count == len(self.cells) and  len(self.cells) != 0 :
                for cell in self.cells:
                    known_mines_set.add(cell)
                return known_mines_set
        return known_mines_set
            


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        known_safes_set = set()
        if self.cells is not None:
            if self.count == 0 and len(self.cells) != 0:
                for cell in self.cells:
                    known_safes_set.add(cell)
                return known_safes_set

            if self.count == len(self.cells):
                return known_safes_set

        return known_safes_set

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)  # Fix: Use remove without assigning to self.cells
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if self.cells is not None:
            if cell in self.cells:
                self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8, CountMines = 8):

        # Set initial height and width
        self.height = height
        self.width = width
        self.prob = probability(width, height, CountMines)
        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        self.prob.CellMine()
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        self.prob.CellSafe()
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        self.moves_made.add(cell)

        self.mark_safe(cell)

        new_sentence_set = set()
        cell_height = int(cell[0])
        cell_width = int(cell[1])

        neighboors_possible = [(0,1),(1,1),(1,0),(1,-1),(-1,1),(-1,0),(-1,-1),(0,-1)]
        # looping for every single possible neighbor
        for neighboor in neighboors_possible:

            new_cell_height = int(int(neighboor[0]) + cell_height)
            new_cell_width = int(int(neighboor[1]) + cell_width)

            # checking if the cell is in the boundaries of the minesweeper game
            if new_cell_height >= 0 and new_cell_height < self.height and new_cell_width >= 0 and new_cell_width < self.width:
                new_cell = (new_cell_height, new_cell_width)
                if new_cell not in self.moves_made:
                # checking if the cell is not in the already found mines
                    if new_cell not in self.mines:
                        new_sentence_set.add(new_cell)
                    else:
                        count -= 1

        new_sentence = Sentence(new_sentence_set, count)
        

        newMines = new_sentence.known_mines()

        


        newSafes = new_sentence.known_safes()

        self.mines = self.mines.union(newMines)
        self.safes = self.safes.union(newSafes)
        self.knowledge.append(new_sentence)
        
        new_combined_sentences = []

        for sentence in self.knowledge[:len(self.knowledge) - 1]:
            try:
                difference_int = abs(len(sentence.cells.difference(new_sentence.cells)))
                if difference_int == abs(len(new_sentence.cells) - len(sentence.cells)) and difference_int != 0 and difference_int != None:
                    combined_sentence = sentence(sentence.cells.difference(new_sentence.cells), abs(sentence.count - new_sentence.count))
                    new_combined_sentences.append(combined_sentence)
            except:
                pass    

        ## fix for tommorow - the difference returns none change it
        
        self.knowledge += new_combined_sentences
        
        for kb in self.knowledge:
            self.mines = self.mines.union(kb.known_mines())
            self.safes = self.safes.union(kb.known_safes())

        for mine in self.mines:
            self.prob.CellMine()
        for safe in self.safes:
            self.prob.CellSafe()    

        print(self.mines)
        print(self.moves_made)
            


                





    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
       
        for safe_move in self.safes:
            if safe_move not in self.moves_made:
                return safe_move
            
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        i = 0
        while i < self.height:
            j = 0  # Reset j to 0 for each iteration of the outer loop
            while j < self.width:
                possible_cell = (i, j)
                if possible_cell not in self.moves_made and possible_cell not in self.mines:
                    return possible_cell
                j += 1
            i += 1
        return None

        
