"""Deterministic logic tests for scripts/audit_puzzle1_flash.py.

No video required: every input is synthetic. These tests pin the exact
behaviors that the 2026-11-23 flash audit depended on:
  * the flash mask is BRIGHTENING-ONLY (signed arithmetic; a darkening
    region must NOT appear — regression for the uint8 wrap-around that
    faked a "fifth line" in unsigned differencing);
  * line segmentation finds exactly the four text bands;
  * height-normalized IoU with shifts ranks identical glyphs above
different ones.
"""
import importlib.util
from pathlib import Path

import numpy as np

SCRIPT = (Path(__file__).resolve().parents[1] / 'scripts'
          / 'audit_puzzle1_flash.py')
spec = importlib.util.spec_from_file_location('flash_audit', str(SCRIPT))
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


def _frames(flash_pixels):
    """Synthetic [before, flash, flash2, after] BGR frames, 720x1280."""
    rng = np.random.RandomState(7)
    before = rng.randint(30, 60, (720, 1280)).astype(np.uint8)
    before = np.repeat(before[:, :, None], 3, axis=2)
    flash = before.copy()
    for y0, y1, x0, x1 in flash_pixels:
        flash[y0:y1, x0:x1] = 235
    dark = before.copy()
    dark[600:640, 300:340] = 20  # a DARKENING region (wrap-around trap)
    after = dark.copy()
    return {0: before, 1: flash, 2: flash.copy(), 3: after}


def test_flash_mask_is_brightening_only_and_signed():
    regions = [(100, 130, 200, 400), (300, 330, 200, 900),
               (500, 530, 200, 700), (640, 670, 300, 900)]
    frames = _frames(regions)
    mask, _ = fa.flash_mask(frames)
    assert mask.shape == (720, 1280)
    for y0, y1, x0, x1 in regions:
        assert mask[y0:y1, x0:x1].all()
    # the darkening region must NOT be in the mask (uint8 wrap regression)
    assert mask[600:640, 300:340].sum() == 0
    # everything else must be empty
    assert int(mask.sum()) == sum((y1 - y0) * (x1 - x0) for y0, y1, x0, x1 in regions)


def test_line_band_stats_finds_exactly_four_bands():
    mask = np.zeros((720, 1280), np.uint8)
    bands = [(226, 250), (306, 330), (389, 413), (469, 493)]
    for y0, y1 in bands:
        mask[y0:y1, 100:1100] = 1
    mask[540, 100:1100] = 1  # 1-row noise band -> ignored (too short)
    found = fa.line_band_stats(mask)
    assert len(found) == 4
    for (y0, y1), (f0, f1) in zip(bands, found):
        assert abs(f0 - y0) <= 1 and abs(f1 - (y1 - 1)) <= 1


def test_iou_shift_identity_and_discrimination():
    rng = np.random.RandomState(3)
    glyph = (rng.rand(40, 20) > 0.5).astype(np.uint8)
    assert round(fa.iou_shift(glyph, glyph), 3) >= 0.99
    # a SOLID glyph shifted by 2 px still matches well (sub-pixel jitter)
    solid = np.zeros((40, 20), np.uint8)
    solid[4:36, 3:17] = 1
    solid_shift = np.zeros((40, 20), np.uint8)
    solid_shift[4:36, 5:19] = 1
    assert fa.iou_shift(solid, solid_shift) > 0.5
    # an L-shaped glyph vs an I-bar must score lower than identity
    other = np.zeros((40, 20), np.uint8)
    other[:, 8:12] = 1
    other[0:6, 8:20] = 1
    assert fa.iou_shift(glyph, other) < fa.iou_shift(glyph, glyph)
    # tiny inputs are rejected gracefully
    assert fa.iou_shift(np.ones((3, 1)), np.ones((5, 5))) == 0.0
