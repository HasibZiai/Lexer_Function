#!/usr/bin/python

#Assignment 1 for CPSC 323
#Written by Hasib Ziai and Stephanie Kinoshita

#importing system for terminal/CLI stuff
import sys

#Different State Type Assignments
STATE_OPERATOR = 0
STATE_SEPARATOR = 1
STATE_IDENTIFIER = 2
STATE_KEYWORD = 3
STATE_INT = 4
STATE_REAL = 5
STATE_COMMENT = 6
STATE_DECIMAL = 7
STATE_SPACE = 8
STATE_ERROR = 9

#Array to store string names for each State
get_token_string = ["OPERATOR", "SEPARATOR", "IDENTIFIER",
                    "KEYWORD", "INT", "REAL", "COMMENT",
                    "DECIMAL", "SPACE", "ERROR"]

# Character Types
CH_ALPHA = 0  # "ALPHA"
CH_SPACE = 1  # "SPACE"
CH_DIGIT = 2  # "DIGIT"
CH_BANG = 3  # "!"
CH_DECIMAL = 4  # "DECIMAL"
CH_DOLLAR = 5  # "$"
CH_OPERATOR = 6  # "OPERATOR"
CH_SEPARATOR = 7  # "SEPARATOR"

transition_table={
	STATE_KEYWORD: {
	CH_ALPHA: STATE_KEYWORD,
	CH_DIGIT: STATE_IDENTIFIER,
	CH_DECIMAL: STATE_ERROR,
	CH_DOLLAR: STATE_IDENTIFIER,
	CH_SPACE: STATE_SPACE,
	CH_OPERATOR: STATE_OPERATOR,
	CH_SEPARATOR: STATE_SEPARATOR,
	CH_BANG: STATE_COMMENT
	}
}

# Group Character Type definitions
# I couldn't find examples of keywords we would be using on the Assignment1 pdf??
# So I looked up some example keywords and used their version for reference
# Let me know if you need the referenced pages!

SEPARATORS = "'()}{[],.:;"
OPERATORS = "*+-=/><%"
KEYWORDS = ["int", "float", "bool", "if", "else", "then",
	"endif", "while", "whileend",
	"do", "doend", "for", "forend", "input",
	"output", "and", "or", "function"]



#Lexer Class Definition

class Lexer:
	def __init__(self, path):
		self._file = open(path)
		self.line_number = 1
		self.token = ""
		self.current_state = STATE_SPACE

	def get_char_type(self, char):
		char_type = None

		if(char.isspace() or char == ''):
			char_type = CH_SPACE
		elif (char.isdigit()):
			char_type = CH_DIGIT
		elif ('!' == char):
			char_type = CH_EXCLAMATION
		elif('.' == char):
			char_type = CH_DECIMAL
		elif ('$' == char):
			char_type = CH_DOLLAR
		elif (char in OPERATORS):
			char_type = CH_OPERATOR
		elif (char in SEPARATORS):
			char_type = CH_SEPARATOR
		elif (char.isalpha()):
			char_type = CH_ALPHA

		return char_type

	#The get_token function will open a file
	#then start going through the FSM
	#WARNING: Currently it's not fully implemented
	#And we'll need to figure out how to add the rest.
	#This may cause some errors so bear with me here.
	#Mainly trying to just get Keywords first
	
	def get_token(self):
        	print("We are now in the get token function")


#The following section is for command line interfaces and Usage
#Don't forget to change modification permissions!
#Example: chmod a+x Assignment1_SK_HZ.py

#Driver
if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print("Usage: ./Assignment1_SK_HZ.py [path_of_textfile]")
		print("Don't forget to change file permissions! chmod a+x Assignment1_HasibZiai.py")
		sys.exit(1)

    
	path = sys.argv[1]
	lexer = Lexer(path)


	print("Tokens\t\t\tLexemes")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	#while True:
	#token = lexer.get_token()
	#if(token is None):
	#break
		#print("{0:<10}\t\t{1}".format(token[0], token[1]))return char_type
