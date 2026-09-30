# Shared

`jev.py` is a minimal Jev client using only the Python standard library:
- `ask(state, questions)` returns `(payload, seconds)`.
- `MODEL` pins the version the results were measured on.
- `api_key()` reads `TYPESAFE_API_KEY` from the environment and never prints it.
