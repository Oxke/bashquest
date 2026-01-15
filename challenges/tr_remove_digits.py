from challenges.base import BaseChallenge
from pathlib import Path
from state import State
from utils import hash_flag
import random
import string

TOTAL_LINES = 1000           # total number of lines in the file
MIN_LINE_LEN = 20
MAX_LINE_LEN = 60
MIN_DIGITS = 5
MAX_DIGITS = 15

# List of 50 uppercase words (pure letters) for the flag
FLAG_WORDS = [
"APPLE", "BANANA", "CHERRY", "DATE", "ELDERBERRY", "FIG", "GRAPE", "HONEYDEW", "KIWI", "LEMON",
"LIME", "MANGO", "NECTARINE", "ORANGE", "PAPAYA", "PEACH", "PEAR", "PLUM", "POMEGRANATE", "QUINCE",
"RASPBERRY", "STRAWBERRY", "TANGERINE", "UGLI", "WATERMELON", "BLUEBERRY", "BLACKBERRY", "CRANBERRY", "DRAGONFRUIT", "JACKFRUIT",
"LYCHEE", "MULBERRY", "OLIVE", "PASSIONFRUIT", "PERSIMMON", "PINEAPPLE", "COCONUT", "APRICOT", "CLEMENTINE", "FIGS",
"GRAPEFRUIT", "GUAVA", "MANDARIN", "MELON", "RAISIN", "STARFRUIT", "YUZU",
]

def random_line_with_FLAG_letters(min_len=20, max_len=60) -> str:
    """Generate a random sequence of uppercase letters, including many F/L/A/G."""
    length = random.randint(min_len, max_len)
    letters = string.ascii_uppercase
    # Add extra F, L, A, G letters to make manual search harder
    extra_flags = random.choices('FLAG', k=random.randint(0, 10))
    chars = [random.choice(letters) for _ in range(length)] + extra_flags
    random.shuffle(chars)
    return "".join(chars)


def disperse_digits(line: str) -> str:
    """Insert a random number of digits at random positions in the line."""
    num_digits = random.randint(MIN_DIGITS, MAX_DIGITS)
    digits = random.choices(string.digits, k=num_digits)
    line_chars = list(line)
    for d in digits:
        pos = random.randint(0, len(line_chars))
        line_chars.insert(pos, d)
    return "".join(line_chars)


class TrRemoveDigitsFlagWordChallenge(BaseChallenge):
    id = "tr_remove_digits_flagword"
    title = "Remove digits to find the FLAG word"
    suggestion = "tr -d '0-9' < mess.txt | grep FLAG:"
    requires_flag = True

    description = [
        "A file named 'mess.txt' has been created in the workspace.",
        "It contains {total_lines} lines of random uppercase letters.",
        "Every line also contains random digits dispersed throughout.",
        "",
        "One line contains the flag in the form: 'FLAG:flag_word', where 'flag_word' is the flag.",
        "Remove all digits, and locate the line starting with 'FLAG:',",
        "The flag word contains only letters; digits appear only in the noise lines.",
    ]

    def setup(self, state: State) -> State:
        ws = Path(state.workspace).resolve()
        file_path = ws / "mess.txt"

        lines = []
        flag_inserted = False

        # Pick the flag word from the list (only letters)
        flag_word = random.choice(FLAG_WORDS)
        full_flag_line = f"FLAG:{flag_word}"

        for _ in range(TOTAL_LINES):
            if not flag_inserted and random.random() < 0.01:
                # insert the flag line randomly
                line = full_flag_line
                flag_inserted = True
            else:
                line = random_line_with_FLAG_letters()

            line = disperse_digits(line)
            lines.append(line)

        # Ensure flag is in the file if not already
        if not flag_inserted:
            lines.append(disperse_digits(full_flag_line))

        file_path.write_text("\n".join(lines) + "\n")

        state.total_lines = len(lines)
        state.flag_word = flag_word  # store only the word, not "FLAG:"
        state.flag_hash = hash_flag(flag_word)

        return state

    def evaluate(self, state: State, flag: str) -> bool:
        return hash_flag(flag.strip()) == state.flag_hash
