Python interpreted programming language created for CS 4337
Ethan Fischer ejf180001

lexer.py - lexical analyzer for the language
parser.py - parser for the language, includes the driver program to run the parser and evaluates the program,
ensuring it is grammatically correct

test.prog - test program in the pyprog language for the lexer.py driver program

attributed_grammar.pdf - defines the base grammar for the language (pre changes)

denotational_semantics.pdf - defines the base denotational semantics of the language (pre changes)

State Transition Diagram.png - state transition diagram for part 1 (also in writeup)

part1_writeup.pdf - writeup for part 1 of the project
part2_writeup.pdf - writeup for part 2 of the project

HOW TO RUN AND COMPILE:
The parser.py file includes the driver program, so you just need to run lexer.py
Can be run in terminal using 'python parser.py' or any code editor that supports python code compilation
Python version: 3.10+
The only technical requirement is python 3.10 or greater, because I used match/case statements to avoid a 
long chain of if/else statements which are only supported in python 3.10

NOTES:
When you run parser.py, it immediately reads input for the program, where you can paste or 
write up a test program. When you finish, you can press Ctrl + D to signify end of file.
The parser will run through the program and ensure it is grammatically correct, alerting
you of any syntax errors.