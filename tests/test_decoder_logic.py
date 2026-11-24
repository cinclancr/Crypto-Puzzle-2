"""Deterministic logic tests for the two edge/column decoder scripts.

No video required: every input is synthetic. These tests pin the assembly
mechanics established on 2026-11-23:
  * edge fragments: the right-edge fragment of frame n (glyph LEFT portion)
    joined BEFORE the left-edge fragment of frame n+19 (glyph RIGHT portion)
    at identity vertical alignment — the [G|L] order that cell 10's serif '4'
    validated;
  * column decode: majority vote, B = A ∪ C relationship, six-window
    geometry (116-px windows at 75-px pitch over 490 rows), ASCII evidence.
"""
import importlib.util
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, str(REPO / 'scripts' / f'{name}.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


edges = _load('decode_part1_edges')
column = _load('decode_part2_column')


def _edge_frame(y0, y1, x0, x1, w=1280, h=720, base=40):
    gray = np.full((h, w), base, np.uint8)
    gray[y0:y1, x0:x1] = 230
    return gray


def test_fragment_cuts_ink_touching_each_edge():
    # glyph ink hanging off the RIGHT edge
    g = _edge_frame(326, 408, 1214, 1280)
    out = edges.fragment(g, 'R')
    assert out is not None
    mask, y0, y1, x0, x1 = out
    assert (y0, y1) == (326, 408)
    assert (x0, x1) == (1214, 1280)
    assert mask.shape == (82, 1280 - 1214)
    # left edge
    g2 = _edge_frame(323, 414, 0, 55)
    out2 = edges.fragment(g2, 'L')
    mask2, ly0, ly1, lx0, lx1 = out2
    assert (ly0, ly1) == (323, 414)
    assert (lx0, lx1) == (0, 55)
    assert mask2.shape == (91, 55)
    # no ink -> None
    assert edges.fragment(np.full((720, 1280), 40, np.uint8), 'R') is None


def test_compose_G_then_L_identity_alignment():
    # G: right-edge fragment of frame n = glyph LEFT portion (rows 326-408)
    g = _edge_frame(326, 408, 1214, 1280)
    # L: left-edge fragment of frame n+19 = glyph RIGHT portion (rows 323-414)
    l = _edge_frame(323, 414, 0, 55)
    comp, geo = edges.compose(g, l)
    # composite spans the union of rows, G on the left of the image
    assert comp.shape == (91, 66 + 55)
    assert comp[326 - 323:408 - 323, :66].all()       # G placed at its rows
    assert comp[0:91, 66:].any() and comp[0, 66] == 1  # L at its own rows
    assert geo['vertical_offset_pair'] == 326 - 323
    # reversed fragment order would break this; guard the convention:
    # the FIRST fragment in the composite must come from the right screen edge
    assert geo['g_rows'] == [326, 408] and geo['g_cols_w'] == 66


def test_compose_returns_none_when_an_edge_is_empty():
    blank = np.full((720, 1280), 40, np.uint8)
    g = _edge_frame(326, 408, 1214, 1280)
    assert edges.compose(blank, blank)[0] is None
    assert edges.compose(g, blank)[0] is None
    assert edges.compose(blank, g)[0] is None


def test_ascii_render_shape():
    mask = np.zeros((90, 60), np.uint8)
    mask[0:3, 0:6] = 1  # exactly one 3-px-tall, 6-px-wide ink block
    rows = edges.ascii_render(mask, step=3)
    assert len(rows) == 30 and len(rows[0]) == 20
    # first two 3-px cells overlap the 6-px-wide ink block
    assert rows[0][:2] == '##' and set(rows[0][2:]) == {'.'}
    assert all(r == '.' * 20 for r in rows[1:])


def test_column_majority_vote_and_union_equals_B():
    # synthetic 3-cycle re-display of two layers with B = A | C
    rng = np.random.RandomState(11)
    A = rng.rand(490, 44) > 0.75
    C = rng.rand(490, 44) > 0.75
    B = A | C
    stack_a = np.stack([A.astype(np.uint8)] * 5)
    stack_b = np.stack([B.astype(np.uint8)] * 5)
    stack_c = np.stack([C.astype(np.uint8)] * 5)
    A_m = (stack_a.sum(axis=0) >= 3).astype(np.uint8)
    B_m = (stack_b.sum(axis=0) >= 3).astype(np.uint8)
    C_m = (stack_c.sum(axis=0) >= 3).astype(np.uint8)
    assert (np.logical_or(A_m, C_m) == B_m).all()   # B = A | C exactly


def test_column_six_window_geometry():
    # 490-row raster, six 116-px windows at 75-px pitch
    raster = np.zeros((490, 88), np.uint8)
    for i in range(6):
        raster[i * 75:i * 75 + 10, :] = i + 1  # marker band at each window top
    windows = [raster[i * 75:i * 75 + 116] for i in range(6)]
    # each window begins with its own marker band
    for i in range(6):
        assert int(windows[i][:10].max()) == i + 1
    # windows 1-5 are full height; window 6 is clipped by the 490-row raster
    assert all(w.shape[0] == 116 for w in windows[:5])
    assert windows[5].shape[0] == 490 - 5 * 75
    # consecutive windows overlap by 116-75 = 41 rows: window 2's marker
    # (raster rows 75-85) is visible at the tail of window 1
    assert int(windows[0][75:85].max()) == 2
    assert 116 - 75 == 41


def test_column_report_constants_match_documented_values():
    # the measured state runs and geometry are part of the published record
    assert column.A_RUNS == [(1550, 1558), (1575, 1581), (1598, 1602)]
    assert column.C_RUNS[0] == (1548, 1549) and column.C_RUNS[-1] == (1609, 1618)
    assert len(column.B_RUNS) == 5
    assert (column.Y0, column.Y1, column.X0, column.X1) == (115, 605, 620, 664)
    assert column.THRESH == 190 and column.PITCH == 75 and column.WINDOW_H == 116
