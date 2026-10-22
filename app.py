import random
from pathlib import Path

import streamlit as st

NAMES_FILE = Path(__file__).parent / "names.txt"


def parse_names(text):
    """Split input into a list of names, one per line or comma-separated."""
    raw = text.replace(",", "\n").splitlines()
    return [name.strip() for name in raw if name.strip()]


def allocate(names, seed):
    """Pair each name with another name, the same way every time for a seed.

    Shuffles the names and gives each person the next person in the
    shuffled order (the last wraps round to the first). This guarantees
    nobody gets themselves and every name is given out exactly once.
    Using a fixed seed means everyone who opens the app sees the same draw.
    """
    shuffled = sorted(names)
    random.Random(seed).shuffle(shuffled)
    return {
        giver: shuffled[(i + 1) % len(shuffled)]
        for i, giver in enumerate(shuffled)
    }


def get_seed():
    """Read the secret draw seed from Streamlit secrets, or None if not set."""
    try:
        return st.secrets.get("draw_seed")
    except FileNotFoundError:
        return None


st.set_page_config(page_title="Secret Santa", page_icon="🎅")
st.title("🎅 Secret Santa")

if not NAMES_FILE.exists():
    st.error("No names.txt file found. Add one with a name on each line.")
    st.stop()

names = parse_names(NAMES_FILE.read_text())
duplicates = sorted({n for n in names if names.count(n) > 1})
seed = get_seed()

if len(names) < 2:
    st.error("names.txt needs at least two names.")
    st.stop()
if duplicates:
    st.error(f"Each name in names.txt must be unique. Duplicates: {', '.join(duplicates)}")
    st.stop()
if seed is None:
    st.error("No draw seed set. Add `draw_seed` to the app's secrets.")
    st.stop()

pairs = allocate(names, str(seed))
names_by_key = {name.casefold(): name for name in names}

entered = st.text_input("Enter your name to see who you're buying for")

if st.button("Reveal") and entered.strip():
    name = names_by_key.get(entered.strip().casefold())
    if name is None:
        st.error("That name isn't on the list. Check the spelling and try again.")
    else:
        st.success(f"Hi {name}! You're buying a gift for **{pairs[name]}** 🎁")
        st.caption("Keep it secret!")
