Audience
========
Anyone who is interested in Python and wants to explore new techniques.
In this particular case using the constraint library, which uses a declarative approach:
The problem is specified in a formalized way and no algorithmic code for Search and
Constraint Propagation has to be written as it is contained in the CSP-solver.

What is this code good for?
===========================
Primarily it demonstrates how the Python constraint library can be used in an practical example
such as solving a Sudoku puzzle.
As there is already a lot of code for solving Sudoku puzzles, I based this example quite
heavily on the great work of Peter Norvik and plugged-in the library parts at the appropriate places.
The code is intentionally left close to Peter's source, so a diff shows the changed parts easily.

What is it not?
===============
It is not optimized, so you will find that Peter's code is (sometimes quite a bit) faster, as obviously
it has a Constraint Propagation optimized for Sudoku.

Further Reading
===============
- http://norvig.com/sudoku.html
- http://stackoverflow.com/questions/321535/getting-started-with-constraint-programming
