[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/emafajriana/the-poster-for-a-place-that-i-2-20261121-0539-entry/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/emafajriana/the-poster-for-a-place-that-i-2-20261121-0539-entry/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

# Solmara — a travel poster for a place that isn't there

Entry for the make.fun bounty
[the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539):
a vintage travel poster for **Solmara**, an invented bay where a
colossal stone arch frames the setting sun.

## What it does

`main.py` (Python 3, standard library only, no network) delivers the
poster committed beside it as `entry.png` (832×1024 PNG) to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` outside the
grader). Before copying, it parses the image header itself and checks
the competition's intake caps — PNG or JPEG, at most 1 MiB, at most
1024×1024 — then verifies the delivered copy by SHA-256 read-back.

## The poster

- One landmark: the great arch of Solmara, holding the sun.
- One promise: golden light, calm water, a village at the cliff's foot.
- The name is set into the sky in classic poster lettering; the
  tagline reads *Where the sun comes to rest*.

## How it was made

The scene was generated as a text-free vintage lithograph-style
illustration (flat colour, limited palette: coral sky, gold sun,
ochre rock, teal sea). The lettering was then composited locally with
Pillow in a bold display face, letter-spaced by hand, so every letter
of the name and tagline is exact — the eye travels from the name,
down to the arch and the sun inside it, and out to the horizon. The
finished poster is committed as `entry.png`; `main.py` only validates
and delivers it, byte for byte.
