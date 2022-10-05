# (Py)thon Interpreted (Prog)ramming Language

## How to Compile and Run
Enter the following command in your terminal
```
python parser.py
```
parser.py will read immediately read input where you can paste in or write up a test program.
The parser will read through your program and tell you if the program is grammatically correct, alerting you of any syntax errors.

### Requirements:
Python 3.10+

## The Language
All details for the language are contained within:
- attributed_grammar.pdf - defines the base grammer (pre-changes)
- denotational_semantics.pdf - defines the base denotational semantics for the language (pre-changes)
- State Transition Diagram.png - state transition diagram for part 1
- part1_writeup.pdf
- part2_writeup.pdf

test.prog is a test program in the pyprog language. 

## Project Purpose
The purpose of this project was to develop a deeper understanding of how a programming language is designed and built, and to learn about all the different parts of a compiler. The class didn't get far enough to finish the actual compiler for the language, but we finished the lexer and the parser. The lexer verifies that every token and keyword in the program is a valid token or keyword. The parser uses the lexer to make sure that the program you've written is syntactically correct and will alert you of any syntax errors. 

## Implementation
I chose to use python (hence the name) to build my language. 
The parser contains the driver program and reads in the test program. 
The parser ues
