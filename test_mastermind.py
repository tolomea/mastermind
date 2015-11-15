from mastermind import calc_score, play


def test_calc_score():
    assert calc_score((0,0,0,0), (0,0,0,0)) == (4,0)
    assert calc_score((1,2,3,4), (1,2,3,4)) == (4,0)
    assert calc_score((4,3,2,1), (1,2,3,4)) == (0,4)
    assert calc_score((1,1,0,0), (1,2,1,2)) == (1,1)


class TestInput(object):
    def __init__(self, guesses, answer):
        self.guesses = guesses
        self.answer = answer
    def __call__(self, guess):
        expected = self.guesses.pop(0)
        assert guess == expected
        return calc_score(guess, self.answer)


def test_play():
    guesses = [
        (0, 0, 1, 1),
        (2, 2, 3, 4),
        (2, 5, 2, 5),
        (0, 0, 3, 3),
    ]
    answer = (4, 5, 3, 4)
    assert answer == play(TestInput(guesses, answer))
