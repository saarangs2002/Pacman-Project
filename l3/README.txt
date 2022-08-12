The kakuro.py is in folder simple

COMMAND FORMAT 1:kakuro.py

NOTE: input should be location of input file 
NOTE: the output file generated will have the name "output.txt"


->another command type with arguments is shown below

COMMAND FORMAT 2: kakuro.py <inputFileLocation> <outputFileLocation> <whatToPerform>

NOTE: in this format no input need to be given, input file location is passed as parameter
NOTE: outputFileLocation has default value "output.txt"
NOTE: No of backtrackings will be output in the terminal


valid values of <whatToPerform>
AC3 - for outputing the reduced variable domain
BACK - for outputing the solution but BACKTRACKING search will take AC3 reduced domain
MAC - for outputing the solution but MAC search will take AC3 reduced domain
BACKnoAC3 - for outputing the solution but BACKTRACKING search will not take AC3 reduced domain
MACnoAC3 - for outputing the solution but MAC search will not take AC3 reduced domain
