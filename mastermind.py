from __future__ import division

"""
The game has 4 slots each of which can have 1 of 6 colors, so there are 6^4 = 1,296 combinations
Scores also have 4 positions, black for correct color in correct place, white for correct color in the wrong place and blank for incorrect color.
These are always ordered black, white blank. This leads to 14 different scores.
None of these are big numbers, so we're going to start with an interactive greedy solver.
The idea is at each stage make the guess that is gaurenteed to cut the most remaining options.
So for each possible guess we score all the remaining options and group them by score.
The best guess is the one whose largest group is smallest. As that will minimise the number of remaining options after making that guess.
I wonder is it ever useful to guess something we know to be impossible? for now we will just in case.
After we have the interactive version going we can run it automatically for every possible game and see how it does in aggregate.
This will let us answer the question above. It will also let us inspect the worst cases and perhaps generalize what it does in human terms.

Let's start with a super simple data model
Colors we'll represent as integers 0-5
Options / guesses we'll represent as lists of 4 colors, converting to tuples if we need to key off them anywhere
Scores we'll represent as a two tuple of the black count and white count
"""

from collections import Counter, defaultdict
import itertools
import string

COLORS = 6
PLACES = 4


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, func):
       self.func = func
       self.cache = {}
    def __call__(self, *args):
       if args in self.cache:
          return self.cache[args]
       else:
          value = self.func(*args)
          self.cache[args] = value
          return value
    def __repr__(self):
       '''Return the function's docstring.'''
       return self.func.__doc__
    def __get__(self, obj, objtype):
       '''Support instance methods.'''
       return functools.partial(self.__call__, obj)


@memoized
def count_matching_colors(a, b):
    count = 0
    ai = iter(sorted(a))
    bi = iter(sorted(b))
    av = next(ai)
    bv = next(bi)
    try:
        while True:
            if av == bv:
                count += 1
                av = next(ai)
                bv = next(bi)
            elif av < bv:
                av = next(ai)
            else:
                bv = next(bi)
    except StopIteration:
        return count


@memoized
def calc_score(guess, answer):
    blacks = sum(1 for a, b in zip(guess, answer) if a == b)
    color_matches = count_matching_colors(guess, answer)
    whites = color_matches - blacks
    return blacks, whites


def evaluate_guess(guess, remaining_options):
    by_score = defaultdict(list)
    for option in remaining_options:
        score = calc_score(guess, option)
        by_score[score].append(option)
    quality = max(len(options) for options in by_score.values())
    return quality, by_score


def get_starting_options(start=0, count=PLACES):
    for i in range(start, COLORS):
        if count > 1:
            for v in get_starting_options(i, count-1):
                yield (i,) + v
        else:
            yield (i,)


def get_best_guess(all_options, remaining_options):
    best_quality = float("inf")
    best_by_score = None
    best_guess = None
    for guess in all_options:
        quality, by_score = evaluate_guess(guess, remaining_options)
        if quality < best_quality:
            best_quality = quality
            best_by_score = by_score
            best_guess = guess
    return best_guess, best_quality, best_by_score


def format_guess(guess):
    return ", ".join(string.ascii_letters[g] for g in guess)


def human_input(guess):
    print format_guess(guess)
    return input("score: ")


class ComputerInput(object):
    def __init__(self, answer):
        self.answer = answer
        self.guesses = 0
    def __call__(self, guess):
        self.guesses += 1
        return calc_score(guess, self.answer)


def get_all_options():
    return list(itertools.product(range(COLORS), repeat=PLACES))


@memoized
def get_first_guess():
    return get_best_guess(get_starting_options(), get_all_options())


def play(get_input):
    all_options = get_all_options()
    guess, quality, by_score = get_first_guess()
    while True:
        score = get_input(guess)
        remaining_options = by_score[score]
        if len(remaining_options) == 1:
            return remaining_options[0]
        guess, quality, by_score = get_best_guess(all_options, remaining_options)


def check_all():
    worst_guesses = 0
    worst_option = None
    total_guesses = 0
    count = 0

    for option in get_all_options():
        ci = ComputerInput(option)
        assert play(ci) == option
        count += 1
        total_guesses += ci.guesses
        print option, ci.guesses, total_guesses / count
        if ci.guesses > worst_guesses:
            worst_guesses = ci.guesses
            worst_option = option
    print
    print worst_option, worst_guesses
    print total_guesses / len(get_all_options())


def main():
    print format_guess(play(human_input))
    #check_all()


if __name__ == "__main__":
    main()
