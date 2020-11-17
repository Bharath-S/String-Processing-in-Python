"""A command line script to find the words in a matrix.

  An algorithm to find the hidden word in a n*n matrix which is connected through a path.
  
  There are 2 navigation variants, which cane be switched using a method in the class: 
  1. Horizontal and Vertical directions
  2. Horizontal, Vertical and Diagonal directions
  
  The  word should contain all the letters in the matrix

  Example:
  1. Given is the following n*n numpy array: ([A, M], [G, E]), the algorithm finds ‘GAME’.
  2. In navigation variatant that included diagonal strides, for a n*n numpy array: ([H, R], [Z, E]), the algorithm finds ‘HERZ’
  
  Class Usage Example:
  
  1. For navigation variant 1:
  
    oWordPuzzle = Find_words_in_grid("WordPuzzle.txt","./words.txt" ) 
    oWordPuzzle.find()
  
  2. For navigation variant 2:
  
    oWordPuzzle = Find_words_in_grid("WordPuzzle.txt","./words.txt" ) 
    oWordPuzzle.enable_Diagonal_Search(True)
    oWordPuzzle.find()
    
  Prerequisites:
  
  1. A text file named "words.txt" containing the english words to be placed in the current directory
  2. A text file named "WordPuzzle.txt" containing the character matrix to be placed in the current directory

"""

import numpy as np
    

class Find_words_in_grid:
    """
    This class maintains all the functionalities required to process the input file, find and display the words in the matrix
    
    """

    def __init__(self, gridFile, dictionaryFile):
        """
        Constructor of the class, initializes all the class variables, reads the words from the dictionary file, parses the 
        matrix file to a numpy array and inturn a suitable grid structure and computes all neigbors to all positions of the grid
        
        Args:
            gridFile - An input txt file containing the user defined matrix structure
            dictionaryFile - An input txt file containing the required words to be used as a lexical dictionary
        
        """
    
        self.bEnable_diagonal_search = False
        self.lexicon_words, self.lexicon_stems = self.get_dictionary(dictionaryFile)
        self.InputArray = np.loadtxt(gridFile, dtype='str', delimiter=',')
        self.Grid = self.make_grid(self.InputArray)
        self.all_valid_neighbors = self.valid_grid_neighbors()
        self.valid_paths = []

    def make_grid(self, input_array):
        """
        A method that creates a suitable grid structure based on the input NumPy array
        
        Args:
            input_array - An input NumPy array that contains the user defined matrix values
        
        Return:
            A dictionary where the key is a tuple containing the coordinates and the value is the character
        
        """
        
        return {(row, col): input_array[row,col].upper()
            for row in range(input_array.shape[0])
            for col in range(input_array.shape[1])
        }

    def get_dictionary(self,dictionary_file):
        """
        A method that processes the input dictionary file and parses it to internal structures
        
        Args:
            dictionary_file - An input txt file containing the list of required words
        
        Return:
            A tuple that contains the words and the corresponding stem words
        
        """

        all_words, all_stems = set(), set()

        with open(dictionary_file) as f:
            for word in f:
                word = word.strip().upper()
                all_words.add(word)

                for i in range(1, len(word)):
                    all_stems.add(word[:i])
                    
        return all_words, all_stems
    
    def find_Neighbors(self,position):   
        """
        A method that generates all possible neighboring coordinates for a given coordinate.
        
        There are 2 variants of navigation:
        1. Horizontal and Vertical directions
        2. Horizontal, Vertical and Diagonal directions
        
        These can be enabled or disabled using a method - enable_Diagonal_Search
        
        See:
            enable_Diagonal_Search(boolean)
         
        Args:
            position - A given coordinate of the grid
        
        Return:
            A list of all posible coordinates for the given coordinate
        
        """

        row = position[0]
        col = position[1]
    
        top_left = (row - 1, col - 1)
        top_center = (row - 1, col)
        top_right = (row - 1, col + 1)

        left = (row, col - 1)
        right = (row, col + 1)

        bottom_left = (row + 1, col - 1)
        bottom_center = (row + 1, col)
        bottom_right = (row + 1, col + 1)
        
        with_Diagonal_Stride = [top_left, top_center, top_right,
                    left, right,
                    bottom_left, bottom_center, bottom_right]
                    
        without_Diagonal_Stride = [top_center,
                    left, right, bottom_center]
                    
        if self.bEnable_diagonal_search == True:
            return with_Diagonal_Stride
        
        return without_Diagonal_Stride


    def valid_grid_neighbors(self):
        """
        A method that validates the generated neighboring coordinates for a given coordinate
        
        See:
            find_Neighbors(tuple)
        
        Return:
            A list of all valid coordinates in the grid
        
        """

        valid_neighbors = {}
        
        for position in self.Grid:
            position_neighbors = self.find_Neighbors(position)
            valid_neighbors[position] = [p for p in position_neighbors if p in self.Grid]
            
        return valid_neighbors

    def path_to_word(self,path):
        """
        A method that joins the characters in the path to form a word.
         
        Args:
            path - A list of coordinates
        
        Return:
            character joined to form words
        
        """
    
        return ''.join([self.Grid[p] for p in path])
             
        
    def enable_Diagonal_Search(self, bVal):
        """
        A method to enable or disable diagonal neighbours search
         
        Args:
            bVal - predicate to enable or disable the diagonal search
        
        """
        self.bEnable_diagonal_search = bVal
        self.all_valid_neighbors = self.valid_grid_neighbors()    
        
    def do_search(self, path):
        """
        A recursive method implementing the core logic of the words search in the path.
        
        The words found are appended to a list of valid words.
        Recursion end point is when the word being formed doesn't exist in the stem of the dictionary.
         
        Args:
            path - A list of coordinates
        
        """
    
        word = self.path_to_word(path)
        
        if word in self.lexicon_words:
            self.valid_paths.append(path)
            
        if word not in self.lexicon_stems:
            return 
            
        for next_pos in self.all_valid_neighbors[path[-1]]:
            if next_pos not in path:
                self.do_search(path + [next_pos])

    def find(self):
        """
        A method for the word search algorithm implemented for all the paths in the grid
        
        The core word search algorithm is run for all the positions of the grid.
        Only the words that contain all the letters in the matrix are considered and displayed at the end
        
        See:
            do_search(tuple)
        
        """

        for position in self.Grid:
            self.do_search([position])
    
        words = []
        for path in self.valid_paths:
            if len(self.path_to_word(path)) == self.InputArray.shape[0] * self.InputArray.shape[1]:
                words.append(self.path_to_word(path))
        
        self.display_words(set(words))


    def display_words(self, words):
        """
        A method that displays user friendly logs on the console, that contains all the words found by the search
        
        Args:
            words: A list of words found by the search algorithm
        
        """
        
        print("***************************************\n")
        print(" The Input Grid")
        print(self.InputArray)
        print("\n")
    
        if self.bEnable_diagonal_search:
            print("---- Diagonal search is ON --------\n")
        else:
            print("---- Diagonal search is OFF -------\n")
    
        print("Found %s words\n" % len(words))
        print("\n".join(sorted(words)))
        print("\n***************************************\n")
        

def main():

    oWordPuzzle = Find_words_in_grid("WordPuzzle.txt","./words.txt" ) 
    oWordPuzzle.enable_Diagonal_Search(True)
    oWordPuzzle.find()
   

if __name__ == "__main__":
    main()
