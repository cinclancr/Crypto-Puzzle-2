#!/usr/bin/env python3
"""Decode the Part 1 screen-edge glyph sequence (reproduced 2026-11-23).

MECHANIC (code-verified against the original MP4):
Large ornate-serif hex glyphs are displayed as static CUT FRAGMENTS against a
black screen, in two synchronized sequences:

  * the RIGHT screen edge shows each glyph's LEFT portion (hanging off-screen
    to the right; verified: no other ink exists in the frame interior at
    those rows), and
  * the LEFT screen edge shows the same glyph's RIGHT portion exactly 19
    frames later (hanging off-screen to the left).

Joining them in order [right-edge fragment of frame n | left-edge fragment of
frame n+19] at identity vertical alignment (each fragment at its own screen
rows) reassembles each full glyph:

    composite(n) = hstack(right_strip(frame n), left_strip(frame n + 19))

The 10 measured pairs (zero-based frames) read, in temporal order:

    6 A 6 B 0 8 6 0 B 4      -> candidate substring `6A6B0860B4`

READING STATUS per cell (2026-11-23 independent audit):
  * cells 1,3,7 = '6'; cells 5,8 = '0'; cell 6 = '8' — confirmed by an
    independent vision read of freshly built composites AND the historical
    community seam reading.
  * cell 10 = '4' — confirmed structurally (serif '4': top-left flag bar,
    full-height right stem, descending diagonal, foot serif) and by vision.
  * cell 2 = 'A' — historical read and focused vision read agree ('A' with
    apex+crossbar; the joined shape is not the same letter as the confirmed
    '4' of cell 10); the fragment join carries small alignment artifacts, so
    a residual '4' possibility is recorded.
  * cells 4,9 = 'B' — straight FULL-HEIGHT left stem + two bowl counters +
    full-width waist band (pixel-structure analysis); vision reads wavered
    between 'B' and '8' (claiming a rounded left side — contradicted by the
    pixel profile, which shows a constant-column left stem for ~90 rows).
    'D' (flat right side) is excluded by the rounded right bowls. Historical
    synthetic-template IoU also leaned D-vs-B near-tied; '8' and 'D' are
    recorded as alternatives. `6A6D0860D4` / `6A68086084` variants preserved.

KNOWN LIMITS:
  * 0 vs O is indistinguishable in this serif face; hex context implies 0.
  * Direction / position of this substring inside the 64-hex key is UNKNOWN.
  * The two edge displays may not be perfectly complementary (tiny vertical
    offsets of 1-6 rows between paired fragments are observed); composites
    carry seam artifacts. ASCII dumps in the JSON report document this.

SECONDARY OBSERVATION: the right-edge fragment of frame n re-appears along
the BOTTOM edge around frame n+236 (template correlation ~0.5-0.6 at x~103,
y~622 for n=1230). Run with --check-redisplay to reproduce.

Usage:
  python scripts/decode_part1_edges.py \
      --video 'local_sources/videos/Solve The 2nd Crypto Puzzle  - Win 0.05 Ethereum - Part 1.mp4' \
      --output results/edges

Outputs: one upscaled composite PNG per pair, an ASCII rendering of every
composite inside edge_report.json (machine-checkable without redistributing
video pixels), and (with --check-redisplay) the bottom re-display table.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

# (frame_n, frame_n_plus_19) pairs measured from the video; the right-edge
# fragment of the first index shows the glyph's LEFT portion, and the
# left-edge fragment of the second index shows its RIGHT portion.
DEFAULT_PAIRS = [
    (1219, 1238), (1221, 1240), (1224, 1243), (1226, 1245), (1229, 1248),
    (1231, 1250), (1234, 1253), (1237, 1256), (1239, 1258), (1242, 1261),
]
INK_THRESHOLD = 170       # gray level for glyph ink
EDGE_SEARCH = 100         # strip width searched at each screen edge
SCALE = 4                 # upscale factor for composite renders
ASCII_STEP = 3            # px per ASCII character in the JSON report


def get_frame(cap, n):
    cap.set(cv2.CAP_PROP_POS_FRAMES, n)
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError(f'frame {n} unavailable')
    return frame


def fragment(gray: np.ndarray, side: str):
    """Cut a glyph fragment hanging off one screen edge.

    Returns (binary mask, y0, y1, x0, x1) where (y0,y1,x0,x1) are FRAME
    coordinates for reporting and the mask is already cropped to the ink
    bounding box. Returns None when the edge holds no ink this frame.
    """
    h, w = gray.shape
    reg = gray[:, w - EDGE_SEARCH:] if side == 'R' else gray[:, :EDGE_SEARCH]
    ink = reg > INK_THRESHOLD
    if not ink.any():
        return None
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = int(rows[0]), int(rows[-1]) + 1
    if side == 'R':
        x0, x1 = w - EDGE_SEARCH + int(cols[0]), w  # frame coords (report only)
        mask = ink[y0:y1, int(cols[0]):]            # strip coords
    else:
        x0, x1 = 0, int(cols[-1]) + 1
        mask = ink[y0:y1, :int(cols[-1]) + 1]
    return mask, y0, y1, x0, x1


def compose(gray_n: np.ndarray, gray_n19: np.ndarray):
    """[G|L] identity join: right-edge fragment (glyph LEFT portion) first,
    then the left-edge fragment (glyph RIGHT portion), each kept at its own
    screen rows so the fragments stay vertically aligned as displayed."""
    G = fragment(gray_n, 'R')
    L = fragment(gray_n19, 'L')
    if G is None or L is None:
        return None, None
    gmask, gy0, gy1, _, _ = G
    lmask, ly0, ly1, _, _ = L
    y_top = min(gy0, ly0)
    y_bot = max(gy1, ly1)
    H, W = y_bot - y_top, gmask.shape[1] + lmask.shape[1]
    can = np.zeros((H, W), np.uint8)
    can[gy0 - y_top:gy1 - y_top, :gmask.shape[1]] = gmask
    can[ly0 - y_top:ly1 - y_top, gmask.shape[1]:] = lmask
    geo = {
        'g_rows': [gy0, gy1], 'g_cols_w': int(gmask.shape[1]),
        'l_rows': [ly0, ly1], 'l_cols_w': int(lmask.shape[1]),
        'vertical_offset_pair': int(gy0 - ly0),
    }
    return can, geo


def ascii_render(mask: np.ndarray, step: int = ASCII_STEP):
    """ASCII rendering of a binary composite for the JSON evidence report."""
    return [''.join('#' if mask[r:r + step, c:c + step].any() else '.'
                    for c in range(0, mask.shape[1], step))
            for r in range(0, mask.shape[0], step)]


def check_redisplay(cap, frames=(1230,), lag=236, threshold=0.45):
    """Verify the bottom-edge re-display of the right-edge fragment at +lag.

    Uses the TIGHT (unpadded) glyph bbox as template: padding dilutes the
    normalized correlation. Observed for frame 1230 -> 1466: score ~0.5-0.6
    at x~103, y~622 on the bottom edge. Treat as supporting observation.
    """
    out = []
    for n in frames:
        g_n = cv2.cvtColor(get_frame(cap, n), cv2.COLOR_BGR2GRAY)
        ink = g_n > INK_THRESHOLD
        cols = np.where(ink[:, g_n.shape[1] - EDGE_SEARCH:].any(axis=0))[0]
        rows = np.where(ink[:, g_n.shape[1] - EDGE_SEARCH:].any(axis=1))[0]
        if not len(cols) or not len(rows):
            continue
        x0 = int(g_n.shape[1] - EDGE_SEARCH + cols.min())
        band = g_n[rows.min():rows.max() + 1, x0:g_n.shape[1]]
        band = band.astype(np.float32)
        g_lag = cv2.cvtColor(get_frame(cap, n + lag), cv2.COLOR_BGR2GRAY)
        for region, (y0, y1) in {'top': (0, 120), 'bottom': (600, 720)}.items():
            strip = g_lag[y0:y1].astype(np.float32)
            res = cv2.matchTemplate(strip, band, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(res)
            if score >= threshold:
                out.append({'frame': n, 'lag': lag, 'region': region,
                            'score': round(float(score), 3),
                            'x': int(loc[0]), 'y': int(y0 + loc[1])})
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--video', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--pairs', type=int, nargs=2, action='append', dest='pairs',
                    metavar=('N', 'N_PLUS_19'),
                    help='frame pair; default is the 10 measured pairs')
    ap.add_argument('--scale', type=int, default=SCALE)
    ap.add_argument('--check-redisplay', action='store_true')
    args = ap.parse_args()
    pairs = [(a, b) for a, b in (args.pairs or DEFAULT_PAIRS)]
    args.output.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened():
        raise SystemExit(f'cannot open video: {args.video}')
    report = {
        'video': str(args.video),
        'ink_threshold': INK_THRESHOLD,
        'pairs': pairs,
        'reading_temporal_order': '6A6B0860B4',
        'per_cell_status': {
            '1': '6 confirmed (vision + historical)',
            '2': 'A (historical + focused vision; join artifacts; 4 recorded as remote alt)',
            '3': '6 confirmed',
            '4': 'B (pixel structure: full-height left stem + bowls; 8/D recorded alts)',
            '5': '0 confirmed (0-vs-O indistinguishable, hex context)',
            '6': '8 confirmed',
            '7': '6 confirmed',
            '8': '0 confirmed',
            '9': 'B (same evidence as cell 4)',
            '10': '4 confirmed structurally (serif 4: flag bar, right stem, diagonal)',
        },
        'composites': [],
    }
    for i, (n, n19) in enumerate(pairs):
        g_n = cv2.cvtColor(get_frame(cap, n), cv2.COLOR_BGR2GRAY)
        g_19 = cv2.cvtColor(get_frame(cap, n19), cv2.COLOR_BGR2GRAY)
        comp, geo = compose(g_n, g_19)
        entry = {'pair': [n, n19], 'geometry': geo}
        if comp is None:
            entry['status'] = 'no ink at one of the edges'
            report['composites'].append(entry)
            continue
        big = cv2.resize(comp, None, fx=args.scale, fy=args.scale,
                         interpolation=cv2.INTER_NEAREST)
        path = args.output / f'edge_composite_{i:02d}_f{n}_f{n19}.png'
        cv2.imwrite(str(path), big * 255)
        entry['status'] = 'ok'
        entry['file'] = str(path)
        entry['ascii'] = ascii_render(comp)
        report['composites'].append(entry)
    if args.check_redisplay:
        report['redisplay_checks'] = check_redisplay(cap)
    cap.release()

    (args.output / 'edge_report.json').write_text(json.dumps(report, indent=2))
    print(f'composites written to {args.output}')
    print('candidate reading (temporal order): 6A6B0860B4')
    print('see edge_report.json for per-cell status, ASCII evidence, geometry')


if __name__ == '__main__':
    main()
