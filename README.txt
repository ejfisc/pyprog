#pyprog
Python interpreted programming language created for CS 4337

lexer.py - lexical analyzer for the language, includes the driver program to run the lexer
and prints all tokens to the screen

test.prog - test program in the pyprog language for the lexer.py driver program

writeup

HOW TO RUN AND COMPILE:
The lexer.py file includes the driver program, so you just need to run lexer.py
Can be run in terminal using 'python lexer.py' or any code editor that supports python code compilation
Python version: 3.10+
The only technical requirement is python 3.10 or greater, because I used match/case statements to avoid a 
long chain of if/else statements which are only supported in python 3.10

NOTES:
When you run lexer.py, it immediately prompts for the program, where you can paste or 
write up a test program. When you finish, you can press Ctrl + D to signify end of file.
The lexer will read through the program and print out each token to the terminal.