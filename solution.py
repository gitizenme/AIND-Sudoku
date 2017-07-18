import itertools

assignments = []



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

# BEFORE
#
#   1   237   4  | 2357  9   257 |  27   6    8
#   9    5    6  |  27   1    8  |  27   3    4
#   23  237   8  |  4    37   6  |  9    5    1
# ---------------+---------------+---------------
#   5    1   2379| 237  347  279 |  34   8    6
#   8    37  379 |  6   347  579 | 345   1    2
#   6    4    23 | 1235  8   125 |  35   9    7
# ---------------+---------------+---------------
#   7    8    1  |  9    2    3  |  6    4    5
#   4    9    5  |  17   6    17 |  8    2    3
#   23   6    23 |  8    5    4  |  1    7    9
#
# AFTER
#
#   1   237   4  | 2357  9   257 |  27   6    8
#   9    5    6  |  27   1    8  |  27   3    4
#   23  237   8  |  4    37   6  |  9    5    1
# ---------------+---------------+---------------
#   5    1   2379| 237  347  279 |  34   8    6
#   8    37  379 |  6   347  579 | 345   1    2
#   6    4    23 | 1235  8   125 |  35   9    7
# ---------------+---------------+---------------
#   7    8    1  |  9    2    3  |  6    4    5
#   4    9    5  |  17   6    17 |  8    2    3
#   23   6    23 |  8    5    4  |  1    7    9
#
# POSSIBLE SOLUTION
#
#   1   237   4  | 2357  9   257 |  27   6    8
#   9    5    6  |  27   1    8  |  27   3    4
#   23  237   8  |  4    37   6  |  9    5    1
# ---------------+---------------+---------------
#   5    1    79 | 237  347  279 |  34   8    6
#   8    37   79 |  6   347  579 | 345   1    2
#   6    4    23 | 1235  8   125 |  35   9    7
# ---------------+---------------+---------------
#   7    8    1  |  9    2    3  |  6    4    5
#   4    9    5  |  17   6    17 |  8    2    3
#   23   6    23 |  8    5    4  |  1    7    9


def naked_twins(values):
    """
    Remove values from same unit when two boxes are found to be one of two values.
    :param values: A sudoku in dictionary form.
    :return: The resulting sudoku in dictionary form.
    """

    for unit in unitlist:  # for each unit (row/column/square/diagonal)
        unit_list = [values[element] for element in unit]
        twins = dict(zip(unit, unit_list))
        inverse_twins = {}
        for key, value in twins.items():
            inverse_twins.setdefault(value, []).append(key)
        inverse_map = {key: value for key, value in inverse_twins.items() if len(value) == 2 and len(key) == 2}

        candidate_boxes = [key for key in twins.keys() if len(twins[key]) > 1]

        for twin_value, twin_box in inverse_map.items():
            for unsolved_box in candidate_boxes:
                if unsolved_box not in twin_box:
                    for digit in twin_value:
                        new_value = values[unsolved_box].replace(digit, '')
                        assign_value(values, unsolved_box, new_value)
    return values


def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            new_value = values[peer].replace(digit, '')
            assign_value(values, peer, new_value)
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                new_value = digit
                box = dplaces[0]
                assign_value(values, box, new_value)
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, try all possible values."""
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudoku, and
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag_units = [[y+x for y,x in zip(rows, cols)], [y+x for y,x in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
