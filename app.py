import random

import streamlit as st


def parse_names(text):
    """Split input into a list of names, one per line or comma-separated."""
    raw = text.replace(",", "\n").splitlines()
    return [name.strip() for name in raw if name.strip()]


def allocate(names):
    """Randomly pair each name with another name.

    Shuffles the names and gives each person the next person in the
    shuffled order (the last wraps round to the first). This guarantees
    nobody gets themselves and every name is given out exactly once.
    """
    shuffled = names[:]
    random.shuffle(shuffled)
    return {
        giver: shuffled[(i + 1) % len(shuffled)]
        for i, giver in enumerate(shuffled)
    }


st.set_page_config(page_title="Secret Santa Generator", page_icon="🎅")
st.title("🎅 Secret Santa Generator")
st.write("Enter the names below, one per line (or separated by commas).")

names_text = st.text_area("Names", height=200, placeholder="Alice\nBob\nCharlie")

if st.button("Generate"):
    names = parse_names(names_text)
    duplicates = sorted({n for n in names if names.count(n) > 1})

    if len(names) < 2:
        st.error("Please enter at least two names.")
    elif duplicates:
        st.error(f"Each name must be unique. Duplicates: {', '.join(duplicates)}")
    else:
        pairs = allocate(names)
        st.success("Names allocated!")
        st.table(
            [{"Person": giver, "Buys a gift for": pairs[giver]} for giver in names]
        )
