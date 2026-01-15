from challenges.base import BaseChallenge
from pathlib import Path
from state import State
from utils import hash_flag
import random
import string

MIN_WORDS = 100
MAX_WORDS = 500
MIN_WORD_LEN = 3
MAX_WORD_LEN = 10

def random_word() -> str:
    length = random.randint(MIN_WORD_LEN, MAX_WORD_LEN)
    return "".join(random.choices(string.ascii_lowercase, k=length))

def random_line(n_words: int) -> str:
    return " ".join(random_word() for _ in range(n_words))


class CutNthWordChallenge(BaseChallenge):
    id = "cut_nth_word"
    title = "Extract the n-th word from a line"
    requires_flag = True

    description = [
        "A file named 'line.txt' has been created in the workspace.",
        "It contains a single line with {num_words} random words separated by spaces.",
        "",
        "The flag is the {nth_word}-th word in the line (1-based indexing).",
        "You must use the `cut` command to extract the word.",
    ]

    def setup(self, state: State) -> State:
        ws = Path(state.workspace).resolve()
        file_path = ws / "line.txt"

        n_words = random.randint(MIN_WORDS, MAX_WORDS)
        line = random_line(n_words)

        # Pick n-th word for the flag
        nth_word = random.randint(1, n_words)
        flag_word = line.split()[nth_word - 1]

        # Write the line to file
        file_path.write_text(line + "\n")

        # Store in state
        state.num_words = n_words
        state.nth_word = nth_word
        state.flag_hash = hash_flag(flag_word)

        return state

    def evaluate(self, state: State, flag: str) -> bool:
        return hash_flag(flag.strip()) == state.flag_hash

