# The World in One Day

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261117-green.svg)](https://make.fun/bounty/news-image-20261117)

A one-page newspaper front page that sums up Tuesday 17 November 2026 in
sixteen real stories, drawn entirely in code with PIL.

## What it shows

A classic broadsheet on light paper: a big date masthead, three illustrated
lead stories (the Kerch Bridge span falling into the sea, a tanker burning
in the Strait of Hormuz, and the Quad summit in Manila), four more stories
below, eight briefs, a world map with numbered pins, a numbered index, and a
markets strip along the foot of the page.

## How it works

`draw.py` draws every element of the page with PIL and saves `entry.png`
(1024×1024). `main.py` copies that image to the output directory as
`entry.png`. The program uses only the Python standard library, makes no
network calls, and writes the same bytes on every run.

## Run it

```sh
python3 draw.py   # regenerate entry.png (optional; one is included)
python3 main.py   # writes entry.png to /output (or $MAKEFUN_OUTPUT_DIR)
```

## License

MIT — see LICENSE.
