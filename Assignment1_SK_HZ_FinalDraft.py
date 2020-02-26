#!/usr/bin/python

#This program was tested with Python 2.7.17
#Assignment 1 for CPSC 323
#Written by Hasib Ziai and Stephanie Kinoshita




#Importing sys library for Terminal/CLI stuff
import sys

# Assigning State Types Here

STATE_OPERATOR = 0  # "OPERATOR"
STATE_SEPARATOR = 1  # "SEPARATOR"
STATE_IDENTIFIER = 2  # "IDENTIFIER"
STATE_KEYWORD = 3  # "KEYWORD"
STATE_INT = 4  # "INT"
STATE_REAL = 5  # "REAL"
STATE_COMMENT = 6  # "!"
STATE_DECIMAL = 7  # "DECIMAL"
STATE_SPACE = 8  # "SPACE"
STATE_ERROR = 9  # "ERROR"



# This array is used to convert the state type to a token

get_token_string = ["OPERATOR", "SEPARATOR", "IDENTIFIER",
                    "KEYWORD", "INT", "REAL", "COMMENT",
                    "DECIMAL", "SPACE", "ERROR"]

# Character Types Definition

CH_ALPHA = 0  # "ALPHA"
CH_SPACE = 1  # "SPACE"
CH_DIGIT = 2  # "DIGIT"
CH_BANG = 3  # "!"
CH_DECIMAL = 4  # "DECIMAL"
CH_DOLLAR = 5  # "$"
CH_OPERATOR = 6  # "OPERATOR"
CH_SEPARATOR = 7  # "SEPARATOR"


#Transition Table Definitions for each State

transition_table = {
    STATE_INT: {
        CH_ALPHA: STATE_ERROR,
        CH_DIGIT: STATE_INT,
        CH_DECIMAL: STATE_DECIMAL,
        CH_DOLLAR: STATE_ERROR,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_OPERATOR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_COMMENT
    },
    STATE_REAL: {
        CH_ALPHA: STATE_ERROR,
        CH_DIGIT: STATE_REAL,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_ERROR,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_OPERATOR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_COMMENT
    },
    STATE_DECIMAL: {
        CH_ALPHA: STATE_ERROR,
        CH_DIGIT: STATE_REAL,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_ERROR,
        CH_SPACE: STATE_ERROR,
        CH_OPERATOR: STATE_ERROR,
        CH_SEPARATOR: STATE_ERROR,
        CH_BANG: STATE_ERROR,
    },
    STATE_SPACE: {
        CH_ALPHA: STATE_KEYWORD,
        CH_DIGIT: STATE_INT,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_ERROR,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_OPERATOR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_COMMENT
    },
    STATE_SEPARATOR: {
        CH_ALPHA: STATE_KEYWORD,
        CH_DIGIT: STATE_INT,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_ERROR,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_OPERATOR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_COMMENT
    },
    STATE_OPERATOR: {
        CH_ALPHA: STATE_KEYWORD,
        CH_DIGIT: STATE_INT,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_ERROR,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_ERROR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_COMMENT
    },
    STATE_KEYWORD: {
        CH_ALPHA: STATE_KEYWORD,
        CH_DIGIT: STATE_IDENTIFIER,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_IDENTIFIER,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_OPERATOR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_COMMENT
    },
    STATE_IDENTIFIER: {
        CH_ALPHA: STATE_IDENTIFIER,
        CH_DIGIT: STATE_IDENTIFIER,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_IDENTIFIER,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_OPERATOR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_COMMENT
    },
    STATE_COMMENT: {
        CH_ALPHA: STATE_COMMENT,
        CH_DIGIT: STATE_COMMENT,
        CH_DECIMAL: STATE_COMMENT,
        CH_DOLLAR: STATE_COMMENT,
        CH_SPACE: STATE_COMMENT,
        CH_OPERATOR: STATE_COMMENT,
        CH_SEPARATOR: STATE_COMMENT,
        CH_BANG: STATE_SPACE
    },
    STATE_ERROR: {
        CH_ALPHA: STATE_ERROR,
        CH_DIGIT: STATE_ERROR,
        CH_DECIMAL: STATE_ERROR,
        CH_DOLLAR: STATE_ERROR,
        CH_SPACE: STATE_SPACE,
        CH_OPERATOR: STATE_OPERATOR,
        CH_SEPARATOR: STATE_SEPARATOR,
        CH_BANG: STATE_ERROR
    }
}

# Assignment Tokens and Lexemes List
SEPARATORS = "'(){}[],.:;"
OPERATORS = "*+-=/><%"
KEYWORDS = ["int", "float", "bool", "true", "false", "if", "else", "then",
            "endif", "while", "whileend",
            "do", "doend", "for", "forend", "input",
            "output", "and", "or", "not"]


#This function checks each character

def get_char_type(char):
    char_type = None

    if(char.isspace() or char == ''):
        char_type = CH_SPACE
    elif (char.isdigit()):
        char_type = CH_DIGIT
    elif ('!' == char):
        char_type = CH_BANG
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


#This is the beginning of Lexer function

def lexer(path):
    token = ""
    tokens = []
    illegal_tokens = []
    current_state = STATE_SPACE
    line_number = 1

    with open(path) as f:
        while True:
            char = f.read(1)
            if(char == '\n'):
                line_number = line_number + 1

            char_type = get_char_type(char)

            new_state = transition_table[current_state][char_type]

            # If the state has changed....
            if(current_state != new_state):
                # If the current state was just a space or a comment we do not want to append them to the token.
                # Instead we start a fresh token using the new char
                if(current_state == STATE_SPACE or current_state == STATE_COMMENT):
                    token = char

                # If there is a state change and we are changing into a decimal point or out of a decimal point
                # we want to concat that to the current token
                elif(current_state == STATE_DECIMAL or new_state == STATE_DECIMAL):
                    token = token + char

                # If there is a state change and the new state is an identifier, then we are transitioning
                # from a keyword to an identifier, so just concat the char to the token.
                elif(new_state == STATE_IDENTIFIER):
                    token = token + char

                # If there is a state change and we have entered an error state
                # the previous token is part of that error.  Append the new char
                # and continue building the illegal token
                elif(new_state == STATE_ERROR):
                    token = token + char

                # If any other state change occurs...
                else:
                    # If we're currently in the keyword state, make sure it is in the keyword list,
                    # Otherwise, it's an identifier.
                    if(current_state == STATE_KEYWORD and token not in KEYWORDS):
                        tokens.append((get_token_string[STATE_IDENTIFIER], token))

                    # If we are exiting an error state, append the illegal token to our
                    # illegal token dictionary with the line number where it occurred
                    elif(current_state == STATE_ERROR):
                        illegal_tokens.append((line_number, token))

                    # All other cases append the token that we've built.
                    else:
                        tokens.append((get_token_string[current_state], token))

                    # start a new token with the new char
                    token = char

            # If it's not a state change, append the char to the token and continue.
            else:
                token = token + char

            current_state = new_state

            # If done reading the file...
            if not char:
                # print("End of file")
                break
    return tokens, illegal_tokens


#Driver and CLI stuff
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: ./Assignment1_SK_HZ.py [path_of_textfile]")
        sys.exit(1)


    path = sys.argv[1]

    tokens, illegal_tokens = lexer(path)

    orig_stdout = sys.stdout
    g = open('output.txt', 'w')
    sys.stdout = g
    print("TOKENS\t\t\tLEXEMES")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for token in tokens:
        print("{0:10}\t\t{1}".format(token[0], token[1]))
    if(len(illegal_tokens) > 0):
        print("\nILLEGAL TOKENS")
        print("Line\t\t\tIllegal Token")
        for token in illegal_tokens:
            print("{0}\t\t\t{1}".format(token[0], token[1]))
    sys.stdout = orig_stdout
    g.close()
