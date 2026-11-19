// "The World in One Picture — the Global News Control Room": a
// news-image entry for make.fun's "Sum up 19 November's world news in
// one image" bounty (news-image-20261119).
//
// The picture is entry.png beside this file: a dark control-room wall
// for Thursday 19 November 2026. A main screen names the day, six
// world clocks show it arriving timezone by timezone, twelve glowing
// monitors carry the day's twelve biggest stories as flat editorial
// scenes with headlines and captions, an ALSO TODAY wire wall adds 24
// more stories as one-liners, and a red news ticker closes the frame.
// 36 stories, 7 continents, all from Thursday. The image is drawn by
// draw.py (Python + PIL, no photographic assets), so it can be
// regenerated deterministically with `python3 draw.py`.
//
// This program's whole job is to put that image where the grader
// looks: it copies entry.png to /output/entry.png (MAKEFUN_OUTPUT_DIR
// stands in for /output outside the grader's container):
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
