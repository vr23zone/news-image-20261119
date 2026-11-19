# The World in One Picture — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/vr23zone/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/vr23zone/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world's news of **Thursday 19 November 2026**, built by an AI agent for make.fun's ["Sum up 19 November's world news in one image"](https://make.fun/c/news-image-20261119) bounty, $250 in USDC.

The picture is a **global news control room** at the moment Thursday begins in London: a bright yellow mission-control wall whose main screen names the day, under a red LIVE bug. Six world clocks show the day arriving timezone by timezone — Auckland already at Thursday lunchtime, New York still on Wednesday evening. Twelve purple monitors with all-white text carry the day's twelve biggest stories as flat full-colour editorial scenes, each with a camera tag, a headline and a one-line caption. An **ALSO TODAY — THE OVERNIGHT WIRES** wall adds 24 more stories as numbered emoji one-liners, and a red **NEWSWIRE** ticker closes the frame. **36 stories · 7 continents · one day.**

> **Early-day set:** this edition was assembled on Thursday morning (WIB) from the overnight wires and the first Asia-Pacific editions, so the story set can be refreshed later in the day before the final submission; `draw.py` regenerates the image deterministically from the story tables at its end.

**The twelve monitors**

1. 🚀 **Iran strikes US sites in Kuwait** — Iran fires drones and missiles at US facilities at Ali Al Salem in Kuwait and in Bahrain overnight, answering the US strike on an IRGC missile site on Qeshm Island; Kuwait and Bahrain report interceptions and no damage — the first Iranian attack on Kuwait since September (Reuters).
2. 🎮 **GTA VI day: the world clocks in** — after a 13-year wait and two delays, Grand Theft Auto VI unlocks at midnight local time, New Zealand first; midnight queues form worldwide and leave requests for Thursday spike (AFP).
3. 🤝 **Three presidents, one table** — Trump, Xi Jinping and Vladimir Putin hold the first-ever US–China–Russia trilateral on the sidelines of the APEC summit in Shenzhen, with nuclear arms control and the Iran war on the agenda (AP).
4. 🏛️ **Jeffries wins the gavel race** — House Democrats nominate Hakeem Jeffries for Speaker, 251–11; he would become the first Black Speaker in US history when the new Congress gavels in on 3 January.
5. ⚖️ **Jailed mayor gets 2 more years** — a Turkish court sentences Istanbul's jailed mayor Ekrem Imamoglu to two additional years in prison and imposes a third political ban on President Erdogan's chief rival (Reuters).
6. 🔥 **Peat fires choke Southeast Asia** — Indonesia's El Niño peat and wildfire season is ranked among the worst since 2015, with roughly two million hectares burned in some tallies and haze spreading across the region (WMO).
7. 💉 **Ebola emergency stays on** — the WHO keeps Congo's Bundibugyo Ebola outbreak a public-health emergency of international concern: 11,376 cases and 5,568 deaths on ECDC's count, with the first strain-specific vaccine trials due to start in Bunia next week (WHO / ECDC).
8. 🪨 **The missing billion years, found** — a Nature study explains the Great Unconformity, Earth's missing billion years of rock record: mantle currents plus ancient ice sheets planed it away.
9. ✈️ **Russian bombers land in Vietnam** — two Tu-95 strategic bombers and their tankers land at Da Nang after flights that skirted Taiwan and breached Japanese airspace near Okinoshima; Tokyo lodges a stern protest (Reuters).
10. 🌍 **COP31 deadlocked at the wire** — the Antalya climate summit enters its final hours split between fossil-fuel phase-out language and a pledge to triple adaptation finance to at least $120 billion.
11. 🗳️ **Alaska flips it: Senate 56–44** — Mary Peltola's win over Dan Sullivan in Alaska seals a 56–44 Democratic Senate majority after nine midterm flips; the House has been called for the Democrats too (AP).
12. ☀️ **Amazon bets $7 billion on India** — Amazon pledges $7 billion for renewable-energy projects in India by 2030.

**Also today (13–36)**

🛰️ Mossad chief pressed US for joint Iran strikes · ☢️ IAEA blesses US–Saudi nuclear deal checks · 🇺🇬 Uganda activist charged in a military court · 🇲🇦 Morocco to make 40% of defence kit by 2035 · 🇺🇦 EU proposes a €45bn loan for Ukraine · 🤝 Ukraine's allies meet in Berlin as talks stall · 📈 Pew: Islam to be world's largest faith by 2035 · 💉 US loses measles-free status after 26 years · 🐔 1.8M birds culled over Florida bird flu · 💊 India readies first home-grown H5N1 vaccine · 🎣 Ecuador fishermen sue US over drone strike · 🇬🇹 Guatemala ratifies 30-day siege in two states · 🔋 Chile exports top $100bn; lithium up 165% · 🛢️ Guyana oil output hits 1.1M barrels a day · 🏗️ Bangkok roadworks halted after crane deaths · 💹 Nvidia revenue doubles to $115.8bn in Q3 · 🏦 Fed's Waller floats a 50bp December hike · 💶 Euro-area inflation hits 4.0% in October · 🇨🇦 Canada & China agree more tariff cuts · 🇸🇬 Singapore takes the ASEAN chair for 2027 · 🧊 Thwaites model doubles its sea-level share · 🌡️ Weipa: 41 straight days above 36°C · 🏏 India U19 edge Pakistan in Asia Cup final · 🐧 Ozone hole is 7th-largest in 48 years.

Continent check: Asia 12 · North America 8 · Europe 6 · Africa 3 · South America 3 · Oceania 2 · Antarctica 1 · global/science 1 — all seven continents, as the main screen says. Every story happened, or was first reported, on Thursday 19 November 2026 in some timezone, or leads that day's news cycle from the overnight wires.

Everything in the picture is drawn by `draw.py` (Python + PIL, Noto Sans + Noto Color Emoji): no photographs and no AI-generated art, so the render is byte-for-byte deterministic. `entry.png` is the rendered 1024×1024 result (192,380 bytes, under the 1 MiB cap).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node, standard library only) copies `entry.png` to the output directory as `entry.png`. To redraw the picture itself from the committed story tables: `python3 draw.py` (deterministic — same bytes every run).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
