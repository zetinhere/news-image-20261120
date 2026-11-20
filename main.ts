// A working news-image-daily entry (Node 22, standard library only): its image is the entry.png beside this file, and
// the program copies it to /output/entry.png. The image was drawn from scratch with Python/PIL (see draw.py)
// from the real news of Friday 20 November 2026: the Senate war-powers vote and the Hormuz tanker mine,
// Anthropic closing +17% on its record debut as markets slid, Europe ready for Russia talks, the COP31
// draft dropping fossil fuels, Storm Dana's evacuation in India, and the ICJ genocide ruling.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
