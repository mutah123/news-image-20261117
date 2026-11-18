# The World in One Day

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/mutah123/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/mutah123/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

A one-page newspaper front page that sums up **Tuesday 17 November 2026** in a
single image: 24 real stories from six continents.

Website: https://make.fun/bounty/news-image-20261117

## What is on the page

- **Masthead** — "THE WORLD IN ONE DAY", dated Tuesday 17 November 2026.
- **Stats strip** — six numbers from the day: 11,000+ Ebola cases in DR Congo,
  $115.8bn Nvidia market value, Dow -849, 1.4M people in acute hunger in Gaza,
  19 dead in the Siberian An-12 crash, Voyager 1 one light-day from Earth.
- **Three illustrated lead stories** — the Kerch Bridge span crashing into the
  sea, a tanker burning in the Strait of Hormuz, and the Quad leaders meeting
  in Manila.
- **Four secondary stories** — Nvidia's chief quits in a spy scandal, allies
  press Israel to open Gaza aid crossings, Japan scrambles jets, Houthis
  advance in Yemen.
- **IN BRIEF** — 17 more stories, numbered 8–24.
- **Dot-matrix world map** — land drawn as dots, with numbered pins at the
  real places of the day's stories and a full 1–24 index.
- **MARKETS strip** and a **DATE CHECK** footer: every story was verified as
  17 November 2026 news.

## How it is built

`draw.py` draws the whole front page with Pillow (PIL) — no network, no
randomness, no timestamps, so the output is byte-for-byte deterministic.
`main.py` (standard library only) copies the rendered `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (default `/output`).

```bash
python3 draw.py        # renders entry.png (1024x1024)
python3 main.py        # copies entry.png to the output directory
```

## License

MIT — see `LICENSE`.
