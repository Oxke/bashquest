from challenges.base import BaseChallenge
from pathlib import Path
from state import State
from utils import hash_flag
import random
import string


TOTAL_LINES = 2000


def random_word(min_len=3, max_len=10) -> str:
    length = random.randint(min_len, max_len)
    return "".join(random.choices(string.ascii_lowercase, k=length))


class TailKthLineChallenge(BaseChallenge):
    id = "tail_kth_line"
    title = "Find the k-th line from the end"
    requires_flag = True

    description = [
        "A file named 'log.txt' has been created in the workspace.",
        "It contains many lines of random text.",
        "",
        "The flag is the {k}-th line from the end of the file.",
        "Line numbering starts from 1.",
    ]

    def setup(self, state: State) -> State:
        ws = Path(state.workspace).resolve()
        file_path = ws / "log.txt"

        # Generate random lines
        lines = [random_word() for _ in range(TOTAL_LINES)]

        # Choose k (distance from end)
        k = random.randint(100, 1000)
        flag_line = lines[-k]

        # Write file
        file_path.write_text("\n".join(lines) + "\n")

        # Persist state
        state.k = k
        state.flag_hash = hash_flag(flag_line)

        return state

    def evaluate(self, state: State, flag: str) -> bool:
        return hash_flag(flag.strip()) == state.flag_hash
