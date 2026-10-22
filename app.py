import random
from pathlib import Path

import streamlit as st

NAMES_FILE = Path(__file__).parent / "names.txt"
PARTNERS_FILE = Path(__file__).parent / "partners.txt"


def parse_names(text):
    """Split input into a list of names, one per line or comma-separated."""
    raw = text.replace(",", "\n").splitlines()
    return [name.strip() for name in raw if name.strip()]


def parse_partners(text):
    """Read partner groups, one group per line with names separated by commas."""
    groups = []
    for line in text.splitlines():
        group = [name.strip() for name in line.split(",") if name.strip()]
        if len(group) > 1:
            groups.append(group)
    return groups


def build_exclusions(names, partner_groups):
    """Map each name to the set of people they can't buy for.

    Returns the exclusions and a list of any partner names not in the names list.
    """
    names_by_key = {name.casefold(): name for name in names}
    excluded = {name: {name} for name in names}
    unknown = []
    for group in partner_groups:
        members = []
        for partner in group:
            name = names_by_key.get(partner.casefold())
            if name is None:
                unknown.append(partner)
            else:
                members.append(name)
        for name in members:
            excluded[name].update(members)
    return excluded, unknown


def allocate(names, excluded, seed):
    """Pair each name with another name, the same way every time for a seed.

    Tries people's options in a random order and backtracks when someone is
    left with nobody they're allowed to buy for. Nobody gets themselves or a
    partner, and every name is given out exactly once. Using a fixed seed
    means everyone who opens the app sees the same draw.
    Returns None if no valid draw exists.
    """
    rng = random.Random(seed)
    givers = sorted(names)
    pairs = {}
    taken = set()

    def assign(i):
        if i == len(givers):
            return True
        giver = givers[i]
        options = [n for n in givers if n not in taken and n not in excluded[giver]]
        rng.shuffle(options)
        for receiver in options:
            pairs[giver] = receiver
            taken.add(receiver)
            if assign(i + 1):
                return True
            taken.remove(receiver)
        return False

    return pairs if assign(0) else None


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
partner_groups = parse_partners(PARTNERS_FILE.read_text()) if PARTNERS_FILE.exists() else []
excluded, unknown_partners = build_exclusions(names, partner_groups)
seed = get_seed()

if len(names) < 2:
    st.error("names.txt needs at least two names.")
    st.stop()
if duplicates:
    st.error(f"Each name in names.txt must be unique. Duplicates: {', '.join(duplicates)}")
    st.stop()
if unknown_partners:
    st.error(f"These names in partners.txt aren't in names.txt: {', '.join(unknown_partners)}")
    st.stop()
if seed is None:
    st.error("No draw seed set. Add `draw_seed` to the app's secrets.")
    st.stop()

pairs = allocate(names, excluded, str(seed))
if pairs is None:
    st.error("There's no way to do the draw without someone buying for their partner.")
    st.stop()

names_by_key = {name.casefold(): name for name in names}

entered = st.text_input("Enter your name to see who you're buying for")

if st.button("Reveal") and entered.strip():
    name = names_by_key.get(entered.strip().casefold())
    if name is None:
        st.error("That name isn't on the list. Check the spelling and try again.")
    else:
        st.success(f"Hi {name}! You're buying a gift for **{pairs[name]}** 🎁")
        st.caption("Keep it secret!")
