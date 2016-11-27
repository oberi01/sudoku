# Sudoku puzzle solver using constraint package. Based heavily on Peter Norvig's approach
# This file is intentionally close to Peter's source, so a diff shows the changed parts easily.
from constraint import *

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

_digits  = range(1, 10) # constraint solver uses int variables
digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print 'All tests pass.'

################ Parse a Grid ################

#def parse_grid(grid):
    #"""Convert grid to a dict of possible values, {square: digits}, or
    #return False if a contradiction is detected."""
    ### To start, every square can be any digit; then assign values from the grid.
    #values = dict((s, digits) for s in squares)
    #for s,d in grid_values(grid).items():
        #if d in digits and not assign(values, s, d):
            #return False ## (Fail if we can't assign d to square s.)
    #return values

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [str(c) for c in grid if c in digits or c in '0.']   # convert constraint solver result to str
    assert len(chars) == 81
    return dict(zip(squares, chars))

################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print

################ Search ################

def solve(grid): return search(grid_values(grid))

def d_to_string(f):
    "Decorator to adapt int to string values in the result dic."
    def decorator(dic):
        res = f(dic)
        for k,v in res.iteritems():
            res[k]=str(v)
        return res
    return decorator

@d_to_string
def search(values):
    "Search solution using constraint package."
    problem = Problem()

    # Define the square variables with their domain values
    for s in squares:
        problem.addVariable(s,_digits)

    # Each unit (row, column, 3x3block) has different values
    for u in unitlist:
        problem.addConstraint(AllDifferentConstraint(),u)

    # Add Constraints for all non-empty squares
    for s,v in values.iteritems():
        if not v in '0.':
            problem.addConstraint(lambda var, val=int(v): var==val, (s,))

    return problem.getSolution()

################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return file(filename).read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ System test ################

import time, random

def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print '(%.2f seconds)\n' % t
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 0:
        print "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

# def random_puzzle(N=17):
#     """Make a random puzzle with N or more assignments. Restart on contradictions.
#     Note the resulting puzzle is not guaranteed to be solvable, but empirically
#     about 99.8% of them are solvable. Some have multiple solutions."""
#     values = dict((s, digits) for s in squares)
#     for s in shuffled(squares):
#         if not assign(values, s, random.choice(values[s])):
#             break
#         ds = [values[s] for s in squares if len(values[s]) == 1]
#         if len(ds) >= N and len(set(ds)) >= 8:
#             return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
#     return random_puzzle(N) ## Give up and make a new puzzle

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
if __name__ == '__main__':
    test()
    # some inline sudokus to solve
    gridL = ['4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......',
             '52...6.........7.13...........4..8..6......5...........418.........3..2...87.....',
             '6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....',
             '.....6....59.....82....8....45........3........6..3.54...325..6..................',]
    solve_all( gridL, "Random demo", 0.0)


## References used:
## http://norvig.com/sudoku.html
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/