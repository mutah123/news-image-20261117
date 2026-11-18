# The World in One Day — v3

A front-page image summing up the world's news of **Tuesday 17 November 2026** — 43 real stories from six continents, drawn as a newspaper front page: a giant one-line date, a six-number stats strip, three illustrated lead stories (the Kerch Bridge span collapse, the Gulf drone war, the Quad summit in Manila), ten illustrated secondary stories, a solid-continent world map with numbered pins, and one "Also on Tuesday 17 November" list. Every story on the page happened or was first reported on that day; disputed claims are marked as claims.

![make.fun](https://make.fun/badge/news-image-20261117.svg)
![rank](https://make.fun/badge/news-image-20261117/mutah123/news-image-20261117/rank.svg)
![reward](https://make.fun/badge/news-image-20261117/mutah123/news-image-20261117/reward.svg)

## How it is built

`draw.py` draws the whole 1024×1024 front page with Pillow (no network, no randomness, no timestamps — the same input always produces the same bytes). `main.py` (stdlib only) runs it and writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).

## Stories

43 in total: 3 leads + 10 secondaries + 30 in the "Also" list. All real Tuesday 17 November 2026 news — the Kerch Bridge, the Gulf, the Quad summit, Ebola in DR Congo, the measles-free status loss, Nvidia's $115.8bn quarter, COP31 in Antalya, Mongolia's president resigning, the Serbia student MP, Bangladesh garment workers, the An-12 crash, Gaza crossings, Japan scrambling jets, and 30 more, each tagged by region and field.

## License

MIT. See LICENSE.
