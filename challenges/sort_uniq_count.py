from challenges.base import BaseChallenge
import random
from pathlib import Path
from state import State
from utils import hash_flag

TOTAL_LINES = 10000
HIGH_FREQ_REPEAT = 100
LOW_FREQ_REPEAT = 2

HIGH_FREQ_WORDS = [
    "apple", "banana", "orange", "grape", "lemon",
    "peach", "melon", "kiwi", "mango", "plum",
    "apricot", "fig", "papaya", "cherry", "coconut",
    "avocado", "pomegranate", "lime", "tangerine", "nectarine",
    "pear", "persimmon", "quince", "cranberry", "date",
    "elderberry", "guava", "lychee", "passionfruit", "blueberry",
    "raspberry", "strawberry", "blackberry", "mulberry", "boysenberry",
    "cantaloupe", "honeydew", "jackfruit", "kiwano", "kumquat",
    "longan", "loquat", "mandarin", "marionberry", "miraclefruit",
    "plantain", "pricklypear", "rambutan", "soursop", "ugli"
]

LOW_FREQ_WORDS = [
    "carrot", "broccoli", "cauliflower", "spinach", "lettuce",
    "cabbage", "kale", "arugula", "radish", "beet",
    "turnip", "parsnip", "celery", "fennel", "okra",
    "zucchini", "squash", "pumpkin", "eggplant", "tomato",
    "pepper", "chili", "jalapeno", "habanero", "cucumber",
    "onion", "garlic", "shallot", "leek", "scallion",
    "basil", "parsley", "cilantro", "dill", "sage",
    "thyme", "rosemary", "oregano", "marjoram", "tarragon",
    "mint", "chive", "lavender", "bayleaf", "lemongrass",
    "nasturtium", "watercress", "sorrel", "endive", "rhubarb"
]

class SortUniqChallenge(BaseChallenge):
    id = "sort_uniq_count"
    title = "Count unique words"
    requires_flag = True

    description = [
        "A file named 'words.txt' has been created in the workspace.",
        "It contains thousands of words, one per line.",
        "",
        "Some words appear very often, others appear just a few times.",
        "",
        "Your task is to count how many **different words** are present in the file.",
        "The flag is the total number of unique words."
    ]

    def setup(self, state: State) -> State:
        ws = Path(state.workspace).resolve()
        file_path = ws / "words.txt"

        # Randomly select number of words from each group
        x = random.randint(5, len(HIGH_FREQ_WORDS))
        y = random.randint(5, len(LOW_FREQ_WORDS))

        high_selected = random.sample(HIGH_FREQ_WORDS, x)
        low_selected = random.sample(LOW_FREQ_WORDS, y)

        words_pool = []

        # Generate lines for high-frequency words
        for w in high_selected:
            words_pool.extend([w] * HIGH_FREQ_REPEAT)

        # Generate lines for low-frequency words
        for w in low_selected:
            words_pool.extend([w] * LOW_FREQ_REPEAT)

        # Shuffle all words
        random.shuffle(words_pool)

        # Write to file
        file_path.write_text("\n".join(words_pool) + "\n")

        # Persist the flag: number of unique words
        unique_count = len(high_selected) + len(low_selected)
        state.flag_hash = hash_flag(str(unique_count))
        state.unique_word_count = unique_count

        return state

    def evaluate(self, state: State, flag: str) -> bool:
        return hash_flag(flag.strip()) == state.flag_hash
