from challenges.base import BaseChallenge
import random
import string
from pathlib import Path
from state import State
from utils import hash_flag

TOTAL_WORDS = 5000
MIN_WORD_LEN = 3
MAX_WORD_LEN = 12
DELTA = 1000  # range around middle line to select flag

def random_word() -> str:
    length = random.randint(MIN_WORD_LEN, MAX_WORD_LEN)
    return "".join(random.choices(string.ascii_lowercase, k=length))

class NthWordChallenge(BaseChallenge):
    id = "nth_word"
    title = "Find the n-th word"
    requires_flag = True

    description = [
        "A file named 'words.txt' has been created in the workspace.",
        "It contains thousands of randomly generated words, one per line.",
        "",
        "The flag is to the word that appears at line number {nth_word_line} in the original file.",
        "Note: Line numbering starts from 1.",
    ]

    def setup(self, state: State) -> State:
        ws = Path(state.workspace).resolve()
        file_path = ws / "words.txt"

        # Generate words
        words = [random_word() for _ in range(TOTAL_WORDS)]

        # Determine n-th line for the flag
        mid = TOTAL_WORDS // 2
        n = random.randint(mid - DELTA, mid + DELTA)
        flag_word = words[n]

        # Write words to file in original order
        file_path.write_text("\n".join(words) + "\n")

        # Persist flag
        state.flag_hash = hash_flag(flag_word)
        state.nth_word_flag = flag_word
        state.nth_word_line = n + 1  # optional, 1-based line for reference

        return state

    def evaluate(self, state: State, flag: str) -> bool:
        return hash_flag(flag.strip()) == state.flag_hash

