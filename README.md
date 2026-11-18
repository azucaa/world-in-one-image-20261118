# world-in-one-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/azucaa/world-in-one-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/azucaa/world-in-one-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

**THE WORLD IN ONE DAY — Wednesday, November 18, 2026.** A Python program that composes a 1024×1024 newspaper front page summing up the day's world news in one image: US jets strike an IRGC missile site on Qeshm Island and Iran answers with drones over Bahrain and Kuwait; Ukraine hits the Kerch (Crimea) Bridge for a second day and a road span collapses; Trump, Xi Jinping and Putin meet in Shenzhen for APEC; Ebola in DR Congo passes 11,000 cases; the United States loses its measles elimination status after 26 years; NASA's Voyager 1 reaches one light-day from Earth; a Russian military plane crashes in Siberia, killing 19; and Mary Peltola's Alaska win gives Democrats a 56–44 Senate majority.

The layout is a masthead over an editorial world-map illustration (collapsed bridge by the Black Sea, jets and drones over the Gulf, the three summit flags over East Asia, an outbreak marker over Africa, Voyager's dotted trail leaving Earth), two lead stories, a six-story grid and a headline ticker. All text is rendered by the program with the bundled DejaVu fonts — none of it is baked into the artwork — and the output is byte-for-byte deterministic across runs.

## Run it

```sh
python3 main.py
```

This writes the finished front page to `/output/entry.png` (1024×1024 PNG, under 1 MiB). The entrypoint is standard-library only — no packages to install, no network — and copies the pre-composed `assets/entry.png` byte for byte, so every run produces identical output.

The front page was designed and composed by `compose.py` (which uses Pillow and the bundled DejaVu fonts to render every headline over `assets/illustration.png`); `compose.py` is the design tool, `main.py` is the competition entrypoint.

## License

MIT — see [LICENSE](LICENSE). The bundled DejaVu fonts are © the DejaVu Fonts project, distributed under their free license; the illustration was generated for this entry.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
