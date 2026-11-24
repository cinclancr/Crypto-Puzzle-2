#!/usr/bin/env python3
"""Decode the Part 2 final vertical column (reproduced 2026-11-23).

MECHANIC (code-verified against the original MP4):
Part 2 ends with a thin vertical column of glyph strokes at the right side of
the screen — region gray[115:605, 620:664] (490x44), hard-cut at x=663 (ink
present at x=663, zero at x=664; the missing right portions of the glyphs are
NEVER shown in any frame and are unrecoverable without model assumptions).

The column cycles through three temporal states (zero-based 720p60 frames):

    C 1548-1549, A 1550-1558, B 1559-1564, C 1565-1572, B 1573-1574,
    A 1575-1581, B 1582-1587, C 1588-1593, B 1594-1597, A 1598-1602,
    B 1603-1608, C 1609-1618, empty from 1619.

Layer B is the pixel-level UNION of layers A and C (99.8% agreement measured;
A-intersects-C = 3,614 px), and the three cycles of A (resp. C) agree with
each other at >= 99.7%: the cycles are RE-DISPLAYS of the same two layers,
not independent messages.

READING (model-dependent): stitching C then A side-by-side and slicing six
116-px-tall windows at 75-px pitch yields a raster supporting `723504`
(position 4 '5' vs '6' is the persistent ambiguity: the glyph shows a flat
TOP BAR, which favors 5; `723604` is recorded as the font-dependent
alternative). The six-slot geometry itself is hypothesis-conditioned (pitch
from autocorrelation peaks 72/75 px; overlapping glyphs; right portions
clipped at x=663). This is a CANDIDATE, not a verified key substring.

Usage:
  python scripts/decode_part2_column.py \
      --video 'local_sources/videos/Solve The 2nd Crypto Puzzle - Win 0.05 Ethereum - Part 2.mp4' \
      --output results/column

Outputs: layer PNGs, C+A / A+C rasters (+ mirrored controls), the six-window
montage, and column_report.json with per-cycle pixel agreement statistics and
ASCII renderings (copyright-safe machine-checkable evidence).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

# Zero-based state runs measured independently (720p60 source).
A_RUNS = [(1550, 1558), (1575, 1581), (1598, 1602)]
C_RUNS = [(1548, 1549), (1565, 1572), (1588, 1593), (1609, 1618)]
B_RUNS = [(1559, 1564), (1573, 1574), (1582, 1587), (1594, 1597),
          (1603, 1608)]
Y0, Y1, X0, X1 = 115, 605, 620, 664
THRESH = 190
WINDOW_H = 116          # window height (hypothesis-conditioned)
PITCH = 75              # window pitch (hypothesis-conditioned)
ASCII_STEP = 6          # px per ASCII character in the JSON report


def get_frame(cap, n):
    cap.set(cv2.CAP_PROP_POS_FRAMES, n)
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError(f'frame {n} unavailable')
    return frame


def state_masks(cap):
    """Majority-vote binary mask per state over ALL frames of each run."""
    stacks = {'A': [], 'B': [], 'C': []}
    runs = {'A': A_RUNS, 'B': B_RUNS, 'C': C_RUNS}
    for state, rlist in runs.items():
        for a, b in rlist:
            for n in range(a, b + 1):
                gray = cv2.cvtColor(get_frame(cap, n), cv2.COLOR_BGR2GRAY)
                stacks[state].append(gray[Y0:Y1, X0:X1] > THRESH)
    masks = {}
    stats = {}
    for state, arr in stacks.items():
        stack = np.stack(arr)
        mask = (stack.sum(axis=0) >= len(arr) // 2 + 1)
        masks[state] = mask.astype(np.uint8)
        agree = [float((f == mask).mean()) for f in arr]
        stats[state] = {
            'frames': len(arr),
            'per_frame_vs_mask_min': round(min(agree), 4),
            'per_frame_vs_mask_mean': round(float(np.mean(agree)), 4),
        }
    return masks, stats


def ascii_render(mask: np.ndarray, step: int = ASCII_STEP):
    return [''.join('#' if mask[r:r + step, c:c + step].any() else '.'
                    for c in range(0, mask.shape[1], step))
            for r in range(0, mask.shape[0], step)]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--video', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--window-h', type=int, default=WINDOW_H)
    ap.add_argument('--pitch', type=int, default=PITCH)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened():
        raise SystemExit(f'cannot open video: {args.video}')
    masks, stats = state_masks(cap)
    cap.release()
    A, B, C = masks['A'], masks['B'], masks['C']
    union = np.logical_or(A, C)
    report = {
        'video': str(args.video),
        'crop': f'gray[{Y0}:{Y1},{X0}:{X1}]',
        'threshold': THRESH,
        'state_runs': {'A': A_RUNS, 'B': B_RUNS, 'C': C_RUNS},
        'state_stats': stats,
        'pixels': {
            'A': int(A.sum()), 'C': int(C.sum()), 'B': int(B.sum()),
            'A_and_C': int(np.logical_and(A, C).sum()),
            'A_or_C': int(union.sum()),
        },
        'union_vs_B_agreement': round(float((union == B).mean()), 4),
        'reading': '723504 (model-dependent; pos4 5-vs-6; alt 723604)',
        'geometry_caveat': ('six-slot geometry hypothesis-conditioned; '
                           'pitch from autocorrelation peaks; glyphs clipped '
                           'at x=663 in every frame'),
    }

    for name, M in masks.items():
        cv2.imwrite(str(args.output / f'layer_{name}.png'), M * 255)

    rasters = {
        'C_plus_A': np.concatenate([C, A], axis=1),
        'A_plus_C': np.concatenate([A, C], axis=1),
        'mirrorC_plus_A': np.concatenate([np.fliplr(C), A], axis=1),
        'C_plus_mirrorA': np.concatenate([C, np.fliplr(A)], axis=1),
    }
    for name, R in rasters.items():
        cv2.imwrite(str(args.output / f'{name}.png'), R * 255)
    report['raster_ascii'] = {k: ascii_render(v, 3) for k, v in rasters.items()}

    # six windows from C+A (control raster A+C as well)
    for raster_name in ('C_plus_A', 'A_plus_C'):
        R = rasters[raster_name]
        cells = []
        for i in range(6):
            y0 = i * args.pitch
            y1 = min(R.shape[0], y0 + args.window_h)
            cells.append(R[y0:y1])
        board = np.zeros((6 * (args.window_h + 6), R.shape[1]), np.uint8)
        for i, win in enumerate(cells):
            board[i * (args.window_h + 6):
                  i * (args.window_h + 6) + win.shape[0], :win.shape[1]] = win * 255
        big = cv2.resize(board, None, fx=4, fy=4,
                         interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(str(args.output / f'six_windows_{raster_name}.png'), big)
        report[f'six_windows_ascii_{raster_name}'] = ascii_render(board, 6)

    (args.output / 'column_report.json').write_text(json.dumps(report, indent=2))
    print('layers/rasters/windows written to', args.output)
    print('state stats:', json.dumps(stats))
    print('union(A,C) vs B agreement:', report['union_vs_B_agreement'])
    print('candidate reading: 723504 (model-dependent; see column_report.json)')


if __name__ == '__main__':
    main()
