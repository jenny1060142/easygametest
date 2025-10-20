import builtins
import minesweeper

# prepare a sequence of inputs to test mark parsing
# using a small board so indices are in range
inputs = iter([
    'm12',    # compact
    'm1,2',   # comma
    'm 1 2',  # spaced
    'm:1,2',  # with colon
    'q'       # quit
])

orig_input = builtins.input

def fake_input(prompt=''):
    try:
        val = next(inputs)
        print(prompt + val)
        return val
    except StopIteration:
        return 'q'

builtins.input = fake_input
try:
    # run play on small board; use 3x3 with 1 bomb to keep it quick
    minesweeper.play(3, 1, auto=False)
finally:
    builtins.input = orig_input
