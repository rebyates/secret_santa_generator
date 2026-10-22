# secret_santa_generator
A quick streamlit app for randomly allocating names in a group for Secret Santa.

## How it works

1. Put everyone's names in `names.txt`, one per line.
2. Set a secret `draw_seed` (any text you like, e.g. `"santa-2026-xyz"`).
   The seed fixes the draw, so everyone sees the same allocation every time
   they open the app. Changing the seed re-draws everyone.
3. Each person opens the app, types their name and taps **Reveal** to see
   only who they're buying for.

Nobody gets themselves, and every name is allocated exactly once.

## Running locally

Create `.streamlit/secrets.toml` (it's git-ignored, so the seed stays private):

```toml
draw_seed = "change-me-to-something-secret"
```

Then:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying on Streamlit Community Cloud

Deploy `app.py` from this repo, then in the app's **Settings → Secrets** add:

```toml
draw_seed = "change-me-to-something-secret"
```
