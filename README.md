# Mastermind
A solver for the game mastermind.

The game has a hidden combination with 4 slots each of which can have 1 of 6 colors, for a total off 6^4 = 1,296 combinations.

On each turn the player makes a guess which is scored on accuracy. Scores also have 4 slots a black is given for a correct color in the correct place, white for correct color in the wrong place and blank for incorrect color. The score slots do not correspond to the combination slots. Instead scores are always ordered black, white, blank. This leads to 14 different scores.

None of these are big numbers, so we're going to start with an interactive greedy solver.

The idea is at each stage we make the guess that is gaurenteed to cut the most remaining options.
After each guess is scored we can eliminate any options that couldn't have recieved that score for that guess.
To pick our next guess we go through all the possible guesses and for each we'll score all the remaining (not yet eliminated) options and group them by score.
The best guess is the one whose largest score group is smallest as that will minimise the number of remaining options after making that guess.

# Further thoughts...
I wonder is it ever useful to guess something we know to be impossible? for now we will allow it just in case.
After we have the interactive version going we can run it automatically for every possible game and see how it does in aggregate.
This will let us answer that question. It will also let us inspect the worst cases and perhaps generalize what it does in human terms.

# Implementation details
Let's start with a super simple data model
Colors we'll represent as integers 0-5
Options / guesses we'll represent as lists of 4 colors, converting to tuples if we need to key off them anywhere
Scores we'll represent as a two tuple of the black count and white count
