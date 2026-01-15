from challenges.base import BaseChallenge
import random
import string
from pathlib import Path
from state import State
from utils import hash_flag

TOTAL_WORDS = 5000
MIN_WORD_LEN = 3
MAX_WORD_LEN = 12

def random_word() -> str:
    length = random.randint(MIN_WORD_LEN, MAX_WORD_LEN)
    return "".join(random.choices(string.ascii_lowercase, k=length))

class SortFirstWordChallenge(BaseChallenge):
    id = "sort_first_word"
    title = "Find the first word alphabetically"
    requires_flag = True

    description = [
        "A file named 'words.txt' has been created in the workspace.",
        "It contains thousands of randomly generated words, one per line, in random order.",
        "",
        "Among all words, the flag is the first word in alphabetic order."
    ]

    def setup(self, state: State) -> State:
        ws = Path(state.workspace).resolve()
        file_path = ws / "words.txt"

        words = [random_word() for _ in range(TOTAL_WORDS)]
        words.sort()  # sort now to know the correct answer
        last_word = words[0]

        # Write words in random order to the file
        random.shuffle(words)
        file_path.write_text("\n".join(words) + "\n")

        state.flag_hash = hash_flag(last_word)
        state.sort_last_word = last_word  # persist for reference
        return state

    def evaluate(self, state: State, flag: str) -> bool:
        return hash_flag(flag.strip()) == state.flag_hash

