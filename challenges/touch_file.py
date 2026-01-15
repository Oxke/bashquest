from challenges.base import BaseChallenge
from pathlib import Path
from state import State
import random


ADJECTIVES = [
    "admiring", "brave", "calm", "clever", "cool",
    "determined", "eager", "focused", "friendly", "happy",
    "hopeful", "inspiring", "keen", "lucid", "mystifying",
    "nervous", "practical", "quirky", "relaxed", "stoic",
]

NAMES = [
    "albattani", "archimedes", "bohr", "curie", "darwin",
    "einstein", "fermi", "galilei", "hypatia", "lovelace",
    "newton", "noether", "pasteur", "tesla", "turing",
    "wright", "hawking", "kepler", "maxwell", "heisenberg",
]


class TouchFileChallenge(BaseChallenge):
    id = "touch_file"
    title = "Create an empty file"
    requires_flag = False

    description = [
        "In the workspace, create an empty file named '{target_filename}'.",
        "The file must be located directly in the workspace directory.",
        "The flag is the file itself with proper name."
    ]

    def setup(self, state: State) -> State:
        ws = Path(state.workspace).resolve()

        adjective = random.choice(ADJECTIVES)
        name = random.choice(NAMES)
        filename = f"{adjective}_{name}.txt"

        # Store value for description rendering and evaluation
        state.target_filename = filename

        return state

    def evaluate(self, state: State, flag: str | None) -> bool:
        ws = Path(state.workspace).resolve()
        target = ws / state.target_filename

        return target.exists() and target.is_file()

