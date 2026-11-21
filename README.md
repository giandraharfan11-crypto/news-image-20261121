# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/giandraharfan11-crypto/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/giandraharfan11-crypto/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A complete newspaper front page — "The World Today", Saturday, 21 November 2026 — drawn at build time in code with Pillow by `generate.py` and committed in this repository as `entry.png`; `main.py` (Python standard library only) copies those exact bytes to /output/entry.png. The lead story is Russia's largest strike of the war on Kyiv — 27 ballistic and 84 cruise missiles and 404 drones, three bridges over the Dnipro damaged, at least eight killed — spilling into Poland, where two missiles and a jet-powered drone fell and PM Tusk called it a "deliberate provocation". Below it: the International Court of Justice ruling, 9-6, that Myanmar committed genocide against the Rohingya, the first time the World Court has held a state responsible for genocide; Trump, Xi and Putin's trilateral peace declaration in Shenzhen; the UK–EU reset deal struck in Brussels; and Anthropic's record $81bn IPO at a $1.5tn valuation amid a tech sell-off. A briefs strip adds Denmark's accusation that Russia plotted to assassinate a US-Ukrainian rapper, Mamdani's vow to close Rikers Island by 2032, the latest US UFO footage declassification, Trump's threat to ban US firms from building AI data centres overseas, the ANC's fight to hold South Africa's key cities, and the Kryvyi Rih strike. No external images, no network, no randomness: the committed PNG is byte-identical on every run (1024x1024, under 1 MiB). `generate.py` is kept as the image's source so the page can be reproduced and audited; it is not the grader entrypoint.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` it writes `/output/entry.png`, as the grader expects. To regenerate the image from source (requires Pillow): `MAKEFUN_OUTPUT_DIR=out python3 generate.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6neab42c&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
