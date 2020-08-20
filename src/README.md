## Heuristic Solver
Heuristics means that a series of logical deductions are used to figure out which value
goes into each cell. No guess work is done here, and all of the techniques used are 
established techniques used to solve sudoku puzzles. In essence, these techniques serve
to find groups of cells that can only contain a certain subset of values, which in turn
restricts those values from appearing in other cells that are related.

For the heuristic solver, because we want to be able to find groups of cells that contain
similar candidates, we opt for a binary representation approach. That is, each value in
the candidate list corresponds to the possible candidates/values that the cell can take.
They are represented in the form 0bxxxxxxxxx, where x is 1 if that value is a candidate 
for this cell, and 0 if that value cannot be a candidate, from 1 to 9 in MSB order.

In other words, say for example cell (1, 3) has candidates 1, 3, 4, 7, 8. Then, in cell
(1, 3) (which is index (0, 2)) in candidate list is 0b101100110. We see the first, third,
fourth, seventh, and eighth bits counting from the most significant bit are set to 1.

### Naked Singles
This is the most basic part of the heuristic sudoku solver, and it's the only part where the
actual board is updated. All other methods are simply used to limit the number of candidates.

Naked singles are simply cells where there is only one possible candidate value. If there is
only one possible valid candidate in the cell, then obviously that cell must take that value.
This does this, and updates the cell in the board and the cell's candidate list as well.

When this candidate is placed into a certain cell, this means that all cells in the same row,
column, or block as this cell can no longer contain that same candidate value. Hence we also
want to remove from those cells this candidate from their respective candidate lists when we
insert this value into that cell.


### Hidden Sets
This is one of the basic strategies in sudoku solving. Hidden sets simply involves finding
a group of cells in the same unit that can only contain a subset of candidates. To understand
this better, we have to understand the concept of naked and hidden sets.

Because of sudoku constraints, we know that the numbers from 1 to 9 can only appear once in
each row, column, and block. Hence we can take each row, or each column, or each block, and
look at its candidates. For example, let's look at row 1, and say the candidates are:
```
[168, 0, 345, 35, 368, 0, 138, 45, 0]
```
Note that 0 means that the cell already has a value and hence has no candidates left. We see
that none of the cells have a naked single, as all cells have multiple candidates. But when
we look closely, we see that in cells 3, 4, and 8 (one-indexed), we see that there are only
three possible candidates for all these cells (3, 4, and 5). Since we know that there are 
only three candidates for these three cells, it must be that these candidates can only appear
in these three cells. If for example the candidate 5 appears in another cell, then we'd have
three empty cells but only two possible candidates left, as we cannot repeat a 5 in the same
row. Hence it must be that these candidates go into these cells, and we can then remove these
candidates from other cells. This is the concept of naked sets, as only these n candidates
can appear in these n cells, so all other cells cannot contain these n candidates.

Let's look at the same row with the same candidates again:
```
[168, 0, 345, 35, 368, 0, 138, 45, 0]
```
We saw what we could deduce from the values 3, 4, and 5. How about the other values? Where
can the other candidates go? We see that in cells 1, 5, and 7 (one-indexed), that they 
contain candidates 1, 3, 6, and 8. We notice that there are three cells but four candidates,
so this is not a naked set. However, consider the candidates 1, 6, and 8. Where can they go?
We see that from the candidate list for this row, these candidates can only appear in cells
1, 5, and 7 (one-indexed). These three candidates can only appear in three cells, and hence
these cells cannot contain other candidates. Therefore, we then know that cells 1, 5, and 7
(one-indexed) can only contain the candidates 1, 6, and 8. This is a hidden set. Even though
there are other candidates in those cells, these n candidates can only appear in these n cells,
and so these n cells can only contain these n candidates. This is the concept of hidden sets.

So what's the difference? In essence, naked sets and hidden sets asks almost the same question
but in different ways. Naked sets asks the questions - in these cells, what are the candidates?
Hidden sets asks the questions - for these candidates, which cells can they appear in? In
naked sets, we identified cells 3, 4, and 8 (one-indexed) and asked the saw that only three 
candidates could go into those cells. In hidden sets, we identified candidates 1, 6, and 8 and
saw that they could only go into three cells. Hence we see that they approach the same problem 
of finding sets of cells and candidates, but by asking slightly different questions.

So what's the relationship between these? We notice that the hidden set and the naked set found
in the example above are complimentary in both cell and candidates. That is, we see that the
possible candidates are 1, 3, 4, 5, 6, 8. In naked sets, we identified candidates 3, 4, and 5, 
and in hidden sets, we identified candidates 1, 6, and 8. For the cells, we saw that cells
1, 3, 4, 5, 7, 8 (one-indexed) had candidates, and in naked sets, we identified cells 3, 4, and
8, while in hidden sets, we identified cells 1, 5, and 7. Hence we see that if a row has
N unfilled cells (which trivially means that there are N possible candidates in total), then if
there is a naked set of size n, then there is a hidden set of size N - n. 

Why is this so? We can think about this in two ways. 