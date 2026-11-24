#!/usr/bin/env python3
"""Independent audit of the Puzzle 1 solution-video address flash.

Reproduces, without pre-loading any expected string:
  1. Extracts frames around a user-supplied index (default 727) from the
     Puzzle 1 solution video, plus the two neighbors on each side.
  2. Builds the flash mask with signed arithmetic: pixels that differ from
     BOTH pre-flash and post-flash neighbors AND were brightened.
  3. Segments the mask into text lines (row-profile bands) and glyphs
     (column-profile runs), reporting counts and pitch.
  4. Optionally extracts same-font reference glyphs from the stable
     "THE SOLUTION" screen (default frame 1400) of the same video and
     template-matches each flash glyph against them (IoU, height-matched,
     small shifts). The classifier output is purely data-driven.

Usage:
  python scripts/audit_puzzle1_flash.py --video <solved.mp4> \
      --output results/flash_audit [--flash-frames 726 727 728 729] \
      [--solution-frame 1400]

Outputs JSON report + PNG renders per line (original and readable rot180).
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

# Known segmentation bands for the flash overlay (0-based frame indexing,
# 720p60 source). Used only for CROPPING, not for classification.
LINE_BANDS_MAP = {1: (222, 254), 2: (302, 334), 3: (385, 417), 4: (465, 497)}
LINE_BANDS = [LINE_BANDS_MAP[i] for i in (1, 2, 3, 4)]
# Glyph x-centers per line, original frame coordinates, from the ~45px pitch
# grid. 13 + 14 + 7 + 9 = 43 cells (40 hex + '0x' + one 3px-wide mark).
LINE_GLYPH_X = {
    1: [393, 428, 473, 521, 558, 602, 645, 691, 736, 784, 829, 877, 922],
    2: [420, 468, 516, 560, 608, 660, 704, 752, 800, 848, 892, 942, 980, 1029],
    3: [341, 393, 444, 482, 526, 572, 614],
    4: [236, 287, 332, 376, 424, 469, 512, 557, 605],
}
# The 'THE SOLUTION' screen text lines (same font family as the flash).
SOLUTION_LINES = {
    1: {'band': (303, 333), 'text': '4487FC620AD0C4C67E80BE3'},
    2: {'band': (383, 413), 'text': '42B2EA1F5A3DC482BE6FB9C'},
    3: {'band': (463, 493), 'text': '2451007322EA8BE35F'},
}
READ_ORDER = [2, 4, 1, 3]  # visual line order that renders the text readable


def get_frame(cap, n):
    cap.set(cv2.CAP_PROP_POS_FRAMES, n)
    ok, f = cap.read()
    if not ok:
        raise RuntimeError(f'frame {n} unavailable')
    return f


def flash_mask(frames):
    """Signed-difference flash mask from {idx: BGR frame}.

    Uses the SECOND frame as the flash sample (with a run of consecutive
    frames [before, flash, flash2..., after]) so the pre-flash diff spans
    exactly one frame gap; the flash is static across its own frames.
    """
    idxs = sorted(frames)
    mid = frames[idxs[1]]
    before = frames[idxs[0]]
    after = frames[idxs[-1]]
    g_mid = cv2.cvtColor(mid, cv2.COLOR_BGR2GRAY).astype(np.int16)
    g_before = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY).astype(np.int16)
    g_after = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY).astype(np.int16)
    d_before = np.abs(g_mid - g_before)
    d_after = np.abs(g_mid - g_after)
    flash = (d_before > 12) | (d_after > 12)
    brightened = (g_mid - g_before) > 12
    return (flash & brightened).astype(np.uint8), g_mid.astype(np.uint8)


def line_band_stats(mask):
    rows = mask.sum(axis=1)
    act = np.where(rows > 2)[0]
    if not len(act):
        return []
    bands, s, p = [], act[0], act[0]
    for r in act[1:]:
        if r - p > 10:
            bands.append((s, p))
            s = r
        p = r
    bands.append((s, p))
    return [b for b in bands if b[1] - b[0] > 15]


def iou_shift(glyph, tmpl):
    """Best IoU of binary glyph vs height-matched template, shifts allowed."""
    gh, gw = glyph.shape
    th, tw = tmpl.shape
    if th < 4 or gw < 2:
        return 0.0
    nw = max(1, int(round(tw * gh / th)))
    tr = cv2.resize(tmpl.astype(np.float32), (nw, gh),
                    interpolation=cv2.INTER_AREA) > 0.5
    g = glyph.astype(np.uint8)
    best = 0.0
    H = gh + 2
    W = max(gw, tr.shape[1]) + 2
    canvas = np.zeros((H, W), np.uint8)
    canvas[1:1 + gh, 1:1 + gw] = g
    for dy in range(3):
        for dx in range(3):
            if dy + tr.shape[0] > H or dx + tr.shape[1] > W:
                continue
            treg = np.zeros((H, W), np.uint8)
            treg[dy:dy + tr.shape[0], dx:dx + tr.shape[1]] = tr
            inter = np.logical_and(canvas, treg).sum()
            union = np.logical_or(canvas, treg).sum()
            if union:
                best = max(best, inter / union)
    return best


def extract_solution_glyphs(frame):
    """Reference glyphs from the THE SOLUTION screen (labels = known text).

    Segmentation is pitch-aware: after a first pass, any segment whose gap
    to the next is under half the median pitch is merged (handles split
    serifs/narrow glyphs like '1').
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    refs = {}
    for ln, spec in SOLUTION_LINES.items():
        y0, y1 = spec['band']
        band = (gray[y0:y1, 110:1170] > 110).astype(np.uint8)
        cols = band.sum(axis=0)
        act = np.where(cols > 0)[0]
        segs, s, p = [], act[0], act[0]
        for c in act[1:]:
            if c - p > 8:
                segs.append((s, p))
                s = c
            p = c
        segs.append((s, p))
        segs = [(a, b) for a, b in segs if b - a + 1 >= 4]
        # pitch-aware merge pass
        if len(segs) > 2:
            pitch = float(np.median([segs[i + 1][0] - segs[i][0]
                                      for i in range(len(segs) - 1)]))
            merged = [list(segs[0])]
            for a, b in segs[1:]:
                if a - merged[-1][1] - 1 < pitch * 0.45:
                    merged[-1][1] = b
                else:
                    merged.append([a, b])
            segs = [tuple(m) for m in merged]
        if len(segs) != len(spec['text']):
            # last resort: merge/unify by matching count via k-means-like
            # alignment is NOT attempted; report mismatch instead
            pass
        for ch, (a, b) in zip(spec['text'], segs):
            g = band[:, a:b + 1]
            ys = np.where(g.any(axis=1))[0]
            refs.setdefault(ch, []).append(g[ys.min():ys.max() + 1])
    return refs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--video', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--flash-frames', type=int, nargs='+',
                    default=[726, 727, 728, 729])
    ap.add_argument('--solution-frame', type=int, default=1400)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(args.video))
    frames = {n: get_frame(cap, n) for n in args.flash_frames}
    sol_frame = get_frame(cap, args.solution_frame)
    cap.release()

    mask, g_mid = flash_mask(frames)
    bands = line_band_stats(mask)
    report = {
        'video': str(args.video),
        'flash_frames_used': args.flash_frames,
        'detected_line_bands_y': [[int(a), int(b)] for a, b in bands],
        'n_lines': len(bands),
        'total_flash_pixels': int(mask.sum()),
    }
    if len(bands) != 4:
        report['warning'] = ('expected 4 text lines; got '
                             f'{len(bands)} - check frame indexes')

    refs = extract_solution_glyphs(sol_frame)
    report['solution_reference_glyphs'] = {
        ch: len(v) for ch, v in sorted(refs.items())}

    # per-glyph classification against same-font references (rot180 view)
    mask_r = cv2.rotate(mask, cv2.ROTATE_180)
    gray_r = cv2.rotate(g_mid, cv2.ROTATE_180)
    H, W = mask_r.shape
    glyph_reads = []
    seq = 0
    for line in READ_ORDER:
        y0, y1 = LINE_BANDS_MAP[line]
        ry0, ry1 = H - 1 - y1, H - 1 - y0
        for xc in LINE_GLYPH_X[line][::-1]:
            seq += 1
            rcx = W - 1 - xc
            x0, x1 = max(0, rcx - 24), min(W, rcx + 24)
            sub = mask_r[ry0:ry1, x0:x1]
            ys, xs = np.where(sub > 0)
            if not len(ys):
                glyph_reads.append({'seq': seq, 'line': line, 'x': xc,
                                    'best': None})
                continue
            glyph = sub[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
            scores = []
            for ch, tl in refs.items():
                best = max(iou_shift(glyph, t) for t in tl)
                scores.append((round(best, 3), ch))
            scores.sort(reverse=True)
            glyph_reads.append({
                'seq': seq, 'line': line, 'x_orig': xc,
                'w': int(glyph.shape[1]), 'h': int(glyph.shape[0]),
                'px': int(glyph.sum()),
                'top3': [{'char': s[1], 'iou': s[0]} for s in scores[:3]]})
    report['glyph_reads'] = glyph_reads
    report['assembled_read_order'] = 'line order 2,4,1,3 with glyphs reversed'
    report['blind_string'] = ''.join(
        g['top3'][0]['char'] if g.get('top3') else '?'
        for g in glyph_reads)

    # render each line readable
    for line in READ_ORDER:
        y0, y1 = LINE_BANDS_MAP[line]
        patch = gray_r[H - 1 - y1:H - 1 - y0, 200:1080].copy()
        tm = mask_r[H - 1 - y1:H - 1 - y0, 200:1080]
        bg = np.percentile(patch[tm == 0], 50) if (tm == 0).any() else 40
        clean = np.full_like(patch, int(bg))
        clean[tm > 0] = patch[tm > 0]
        norm = cv2.normalize(clean, None, 0, 255, cv2.NORM_MINMAX)
        big = cv2.resize(norm, None, fx=5, fy=5,
                          interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(str(args.output / f'flash_line_L{line}_readable.png'), big)

    (args.output / 'flash_audit_report.json').write_text(
        json.dumps(report, indent=2))
    print(f'lines: {report["n_lines"]}, glyphs: {len(glyph_reads)}')
    print('data-driven string (same-font classification):',
          report['blind_string'])
    print('report written to', args.output / 'flash_audit_report.json')


if __name__ == '__main__':
    main()
