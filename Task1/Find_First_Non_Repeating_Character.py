"""A command line script to find the first non repeating character of the input string.

  Typical usage example:
      find_First_Non_Repeating_Character("EntwicklerHeld")
  
  Script usage example:
      python3 Find_First_Non_Repeating_Character.py "EntwicklerHeld"
      
"""

import sys


def find_First_Non_Repeating_Character(s_String):
    """
    This function runs the algorithm to find the first non repeating character of a string that is passed as input. 
    Also, the case of the characters doesn't matter
    1) As a example, given a the sequence ‘EntwicklerHeld’, the function will return ‘n’.
    2) For a sequence ‘abcabc’ – the function will return ‘None’
    3) For a character "", passed as input, the function returns ‘None’

    Args:
        s_String (string): The input string to be processed

    Returns:
        A string
    """

    s_String = s_String.lower()
    d_Char_Count = {}
    l_Chars = []
    

    for c_Literal in s_String:

        if c_Literal in d_Char_Count:
            d_Char_Count[c_Literal] += 1
        else:
            l_Chars.append(c_Literal)
            d_Char_Count[c_Literal] = 1

    for c_Literal in l_Chars:
        if d_Char_Count[c_Literal] == 1:
            return c_Literal

    return None


def main():
    """
    The main function of the script which dictates the program execution
    
    """

    try:
        s_Input_String = sys.argv[1]
    except:
        print("Invalid Input, please give a string as argument")
        sys.exit(1)

    c_First_Non_Repeating_Char = find_First_Non_Repeating_Character(s_Input_String)
    print("The first non repeating character of the string %s is -- %s " % (s_Input_String, c_First_Non_Repeating_Char))
   

if __name__ == "__main__":
    main()


