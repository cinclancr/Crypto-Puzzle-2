# Evidence Dossier — Puzzle 2 Observations with Exact Uncertainty

**Updated:** 2026-11-23 (independent audit session)
**Status classes used throughout:** VERIFIED OBSERVATION / REPLICATED (parameter-dependent) / HYPOTHESIS / NEGATIVE TEST / EXTERNAL CLAIM / UNRESOLVED.

All frame numbers are 0-based against the user-supplied 1280×720 / 60 fps MP4
files (SHA-256 pinned in `data/source_manifest.json`). Community analyses
performed on the currently served 360p/30fps rendition use frame numbers
that are approximately half of ours (their frame n ≈ our frame 2n); we note
rendition mapping wherever it matters.

---

## A. Puzzle 1 control (video `Crypto Puzzle 1 Solved!.mp4`)

### A1. Solution screen and key — VERIFIED OBSERVATION
- Stable "THE SOLUTION" screen at approximately frames 1035–1700 with the
  64-hex key in three lines (23 + 23 + 18 chars) at y≈307, 387, 467.
- VLM transcription of the three lines reads
  `4487FC620AD0C4C67E80BE3` / `42B2EA1F5A3DC482BE6FB9C` / `2451007322EA8BE35F`
  (the second line also renders with segment ambiguity near the `1` glyph).
- The assembled key matches the publicly disclosed Puzzle 1 key and derives
  (via our offline oracle) to `0xc99A54EEA6036115f913A13D6606e935bcA47a8f`.
- On-chain check (etherscan, retrieved 2026-11-23): funded 0.05 ETH on
  2018-07-19 (tx `0xa8de9727...`) from `0x0A937eC94ABC55d92f5740a988a122eBdCAb2e15`,
  spent 2018-07-26 in two outgoing txs, balance 0.

### A2. The 1–2-frame mirrored flash — NOW VERIFIED OBSERVATION (upgraded 2026-11-23)

**Existence (quantitative):**
- Frames 726→727 and 728→729 each change ~4,900 px in bbox x[236,1044] y[227,493];
  frames 727 vs 728 differ by ≤1 px above 25 → the overlay is present exactly
  in frames 727–728 and static between them.
- Signed-intensity analysis: the flash only BRIGHTENS pixels (7,017 px by >12;
  only 4 px darken). Four text rows at y ≈ 226–250, 306–330, 389–413, 469–493
  (25 px tall each). An apparent "fifth line" below row 4 was a uint8
  wrap-around artifact of unsigned differencing; with signed arithmetic there
  are exactly FOUR lines.
- Glyph grid: ~45 px horizontal pitch; 13 + 14 + 7 + 9 = 43 cells
  (40 hex digits + a `0x` prefix + one 3-px-wide narrow mark at line-1 x≈393).

**Orientation:** The overlay is rotated 180° (not merely mirrored). Reading
each line in the rot180 view with glyphs in reverse x order, the four visual
lines read in order **2 → 4 → 1 → 3**.

**Independent character-by-character read (2026-11-23):**
Per-glyph classification used three mutually reinforcing methods, none of
which pre-loads the target string:
1. Multi-font synthetic template matching (7 font families, IoU).
2. Focused vision-model reads of isolated, background-suppressed glyph
   renders at 6–10× zoom, including explicit "give alternatives" prompts.
3. **Same-font intra-video clustering**: the flash glyphs were matched
   against glyph bitmaps extracted from the *same video's* stable
   "THE SOLUTION" screen (same font family and size class), and disputed
   glyphs were compared pixel-by-pixel against confirmed anchors.

Disputed glyphs resolved by same-font comparison (IoU, disputed vs anchor):
- Position (line 1, x691) — claimed `3`: `3` 0.747 vs `8` 0.544 → **3**
- Position (line 1, x602) — claimed `5`: `5` 0.678 vs `6` 0.469 → **5**
- Position (line 3, x341) — claimed `D`: `D` 0.535 vs `0` 0.307 → **D**
- Position (line 2, x704) — claimed `E`: pixel-level ASCII comparison shows
  left stem + three arms (top/middle/bottom) = **E** (F and B lack the third arm)
- Controls: x473 `2` 0.72 vs `8` 0.386; x516 `5` 0.637 vs `3` 0.421;
  x482 `6` 0.659 vs `0` 0.642.

Assembled flash text (read order 2-4-1-3):

```
0X1FA8BE9DE5BB FE047C72D B8E8E3257128[•] F7661AD
```

where `[•]` is the 3-px narrow mark (visually a thin vertical stroke,
consistent with a faint `1` or a fragment; it sits immediately after the
40th hex digit and does not extend the address).

**Result: the flash spells `0x1FA8BE9DE5BBFE047C72DB8E8E3257128F7661AD`,
byte-for-byte the inferred Puzzle 2 escrow address verified on-chain.**

Automation note: `scripts/audit_puzzle1_flash.py` reproduces the mask, the
four-line segmentation and a fully data-driven per-glyph classification
(uncertainty retained as top-3 IoU). Its unattended single-pass read resolves
~35/43 cells correctly; the remaining confusables (X, E/F/B, 5/6, 3/8, D/0
and faint line-3 glyphs) were settled by the focused adjudication above.
The flash does NOT prove anything about private-key fragment ordering; it is
a public-address disclosure only.

### A3. Puzzle 1 statement videos — EXTERNAL CLAIM (not supplied, NOT VERIFIED)
Community (issue #5, timothy-barus): single-frame flashes at 98% through the
statement videos (part 1 frame 1180; part 2 frames 1024/1039/1053/1180 in
the 360p/30fps rendition) reading `482BE6FB9C` and `2007322EA` — note their
own correction: the published key contains `1007322EA` at that position, so
their flash transcription itself contained a misread. These videos are not in
our local set; treat as unverified external claims.

---

## B. Puzzle 2 Part 1 (video `Solve The 2nd Crypto Puzzle - Win 0.05 Ethereum - Part 1.mp4`)

### B1. Edge glyph events — VERIFIED OBSERVATION (720p60 timeline)
- Right-edge bright content (>150 gray, x≥1210): frames 1219–1310.
- Left-edge content (x<70): frames 1238–1334.
- Top-edge content: frames 1454–1554; bottom-edge: 1474–1572 — the top/bottom
  run begins ≈236 frames (~3.93 s) after the right/left run, consistent with
  the community's rendition-scaled observation.
- Structure: a two-phase sequence (title letters ≈ f48–300; giant "2" ≈ f304+).

### B2. Wrap-around reading `6A6B0860B4` — REPLICATED (parameter-dependent)
- Composite construction: right-edge strip of frame n + left-edge strip of
  frame n+19, rotated 90° clockwise, matches the community method.
- Independent vision-model read of the 10 composites
  (anchors 1219, 1221, 1224, 1226, 1229, 1231, 1234, 1237, 1239, 1242)
  reproduces **`6A6B0860B4`** exactly, with the 0-vs-O caveat irrelevant in hex.
- Lag sweep (17–22): lags 19/20/21 produce identical glyph extents; the
  top match flips between B and D across fonts at ~0.47–0.51 IoU.
- **B-vs-D ambiguity remains unresolved at the pixel level** in the composite:
  synthetic matching gives `D` 0.501–0.512 vs `B` 0.476–0.482 (FreeSerif /
  DejaVu); the historical Didot comparison favored B. The community explains
  the top/bottom (seam B) rendering loses exactly the 20-px band carrying the
  B/D notch, producing `6A6D0860D4` there. Keep both `6A6B0860B4` and
  `6A6D0860D4` as alternatives; both position and reading direction within the
  key are unknown (reversed candidate `4B0680B6A6` equally consistent).
- The trailing `4` (right-edge content continues f1241–1310 as a long-held
  static glyph on the right while the left edge receives the next glyph)
  is the longest-held glyph; function unknown (data, decoy, or "four parts"
  instruction) — HYPOTHESIS only.

### B2b. Edge-fragment mechanic and per-cell audit (2026-11-23, deep re-analysis)
A second independent pass rebuilt the composites from scratch and
established the underlying display mechanic exactly:

- **Fragment structure (VERIFIED OBSERVATION):** at the right edge the ink
  occupies e.g. frame-1219 x[1214,1280], rows [326,407], and the ENTIRE frame
  interior at those rows contains no other ink (checked x[900,1214],
  rows[280,460]: 0 px). The edge events are therefore static CUT FRAGMENTS of
  glyphs hanging off-screen — not scrolling text, and not glyphs with bodies
  in the frame interior.
- **Pairing (VERIFIED):** the right-edge fragment of frame n shows the glyph's
  LEFT portion; the left-edge fragment of frame n+19 shows the SAME glyph's
  RIGHT portion (10/10 pairs at exactly +19; fragment bands within 1–6 rows
  of each other). Correct assembly is
  `hstack(right_strip(f_n), left_strip(f_n+19))` with each fragment kept at
  its own screen rows ("identity alignment"). A reversed order corrupts the
  glyphs (a mis-ordered join read as `6N68086084`-class noise).
- **Per-cell status after the rebuild:**
  - cell 10 = **4** — structurally confirmed (serif 4: top-left flag bar,
    full-height right stem, descending diagonal, foot serif) and vision-read
    as 4; this asymmetric glyph also validates the join ORDER.
  - cells 1/3/7 = 6, cells 5/8 = 0, cell 6 = 8 — fresh vision read of the
    rebuilt composites agrees with the historical seam reading.
  - cell 2 = **A** — historical read and a focused high-zoom vision read
    (apex + crossbar, no flat-topped bar) both give A; the rebuilt shape is
    demonstrably NOT the same letter as the confirmed 4 of cell 10. Residual
    join artifacts keep a remote 4 alternative recorded.
  - cells 4/9 = **B** — pixel-structure analysis: a straight full-height LEFT
    stem (constant left-edge column across ~90 rows) plus two bowl counters
    and a full-width waist band. The straight left stem excludes 8 (bowl left
    side); the rounded right bowls exclude D. Fresh vision reads wavered
    B/8 (claiming a rounded left side — contradicted by the pixel profile),
    so `8` is recorded as a vision-level alternative and the earlier
    synthetic D-vs-B near-tie remains: B preferred, 8/D recorded.
- **Negative tests from this pass:** (a) the Puzzle 1 solution-screen font
  library does NOT match the edge glyph face (max height-normalized IoU
  0.18–0.27 across all cells) — different cuts/weights, so same-font
  adjudication from the solution screen is inapplicable here; (b) an earlier
  session's archived composite files could not be reproduced byte-for-byte
  from the (n, n+19) fragments by concat, overlay, or grayscale merge (best
  correlation ~0.38) — their exact construction is uncertain and they are
  retained as historical evidence only; the fresh composites and the code in
  `scripts/decode_part1_edges.py` are the reproducible record.
- Reproduce everything with
  `python scripts/decode_part1_edges.py --video <part1.mp4> --output results/edges --check-redisplay`
  (the JSON report embeds an ASCII rendering of every composite as
  copyright-safe machine-checkable evidence, plus the bottom-edge +236
  re-display check: correlation 0.527 at x=103, y=621 for f1230→f1466).

### B3. Frame 1718 scene change — VERIFIED OBSERVATION (not a hidden flash)
A large one-time change (56,687 px) at frame 1718 persists to video end —
it is a global re-grade/color transition of the closing scene, not a text
flash. No brightening-overlay signature like the Puzzle 1 flash.

### B4. Negative: end-of-video key flash — NEGATIVE TEST
Isolated-spike scan over all 1800 Part 1 frames and all 1800 Part 2 frames
(thresholded mean-abs-diff with local-context suppression): the only
Puzzle-1-like single-frame overlay flash is at 727/728 of the SOLUTION video;
neither Puzzle 2 video contains a comparable 1–2-frame brightening flash.
Absence is detector/threshold-dependent (community scanned 360p at thresholds
140/170/200 with the same negative result).

---

## C. Puzzle 2 Part 2 (video `Solve The 2nd Crypto Puzzle - Win 0.05 Ethereum - Part 2.mp4`)

### C1. MIRROR card — VERIFIED OBSERVATION
At ≈frame 1260 the frame contains a large mirrored `C` and `8` plus the
reversed word `MIRROR`. After horizontal flip the word reads `MIRROR` and the
pair reads **C8** (C left, 8 right). Whether `C8` is key data or an
instruction is UNRESOLVED.

### C2. Final vertical column state machine — VERIFIED OBSERVATION
- Column region gray[115:605, 620:664] (490×44), abruptly cut at x=663.
- Zero-based state runs measured from majority-voting pixel masks
  (threshold >190): C 1548–1549 (2), A 1550–1558 (9), B 1559–1564 (6),
  C 1565–1572 (8), B 1573–1574 (2), A 1575–1581 (7), B 1582–1587 (6),
  C 1588–1593 (6), B 1594–1597 (4), A 1598–1602 (5), B 1603–1608 (6),
  C 1609–1618 (10), empty from 1619.
- B = A ∪ C verified at 99.8% pixel agreement (12,462 vs 12,454 px;
  A∩C = 3,614 px). The three cycles of A agree with each other at
  ≥99.9% pixel and C cycles at ≥99.7%: **the cycles are re-displays, not
  independent messages.**

### C3. Column reading `723504` — REPLICATED (model-dependent)
- Independent reconstruction (21 A-frames, 24 C-frames, majority vote) with
  C-then-A stitching and six 116-px windows at 75-px pitch reproduces a
  raster on which the reading **`723504`** is supported:
  - Position 1 `7`: full-width top bar + long diagonal (pixel-level ASCII).
  - Position 4 `5` vs `6`: the glyph has a flat TOP BAR (`###...` rows 0–5)
    and left-side entry stroke; a `6` has a closed left stem from the top,
    a `5` has the flat top bar → **5** (matches template top-scores 0.543
    and the held-out historical result 46/50).
  - Position 6 `4`: vertical stem + diagonal + crossbar, unambiguous.
- Automation caveat: unattended template matching over all 8 orientation
  variants ranks C_then_A/rot180-highest and yields `224504`-class strings;
  vision reads of isolated windows give 7 / 2 / 3 / (5 or 3) / 0 / 4 with
  positions 2–4 the least certain. The `723604` font-dependent alternative
  remains recorded.
- **The six-slot geometry itself is hypothesis-conditioned** (75-px pitch from
  autocorrelation peaks 72/75 px; window height 116 px; overlapping glyphs).
- Real pixel content ends at x=663 (ink 125 px at x=663, zero at x=664):
  each glyph's right portion is clipped by the internal window; pixels absent
  in every frame cannot be recovered without model assumptions.

### C4. Negative: complementary halves — NEGATIVE TEST (community + ours)
Part 2 has no edge-touching bright content at any frame; it does not supply
the halves clipped off Part 1's right-edge glyphs (floflo777 row 10), and
Part 1's left-edge run is its own sequence. The two videos are not
complementary halves of one glyph stream.

---

## D. Audio

### D1. AAC packet comparison — VERIFIED OBSERVATION
- Both Part 1 and Part 2 audio: 1295 AAC frames each.
- 1279/1295 frames byte-identical; **16 differing frames at t≈20.526–20.944 s**
  (reproduced independently by ADTS re-split).
- Decoded PCM: correlation 0.999961 in the 20.4–21.2 s window, 0.999998 over
  the full track, and 1.000000 in control windows (10–11 s).
- The difference signal is a transient ~750–850 Hz-band component localized
  to 20.54–20.77 s and 20.94–20.98 s, ~53 units std, max ±424 (on a signal
  whose RMS is ~5,970). Band energy in the differing window is 12× the
  control window's. **Consistent with an encoder/segment-boundary artifact,
  not a designed message. No Morse/voice/encoded content established.**

---

## E. User's four-part hypothesis — HYPOTHESIS (unproven)

- `6A6B0860B4` (10) + `723504` (6) = 16 hex digits is a numerical
  coincidence; contiguity, ordering, and even membership of either block in
  the key are unverified.
- The 2-4-1-3 ordering is now VERIFIED for the Puzzle 1 address flash, but
  that establishes only that the author used non-linear line ordering for a
  four-line disclosure; it does NOT prove Puzzle 2 uses four blocks or that
  ordering for key fragments.
- If only 18 reliable digits are known (10 + 6 + C8) then 46 literal hex
  digits are unknown: 16^46 ≈ 2^184 candidates. A single known 16-digit block
  still leaves 2^192. No derivation from the public address is possible.

## F. Descriptions — EXTERNAL CLAIM (exact bytes not yet captured by us)

Community transcription (issue #5, diploux):
- Part 1: "Do you have the intellience to solve the Crypto Puzzle? 0.05ETH is
  waiting for the best puzzler solver. Is it you?" — missing `g` in
  "intellience"; `g` occurs exactly once in the description, at index 73
  (0-based).
- Part 2: "The first puzzle was solved in hours, so our second is decidely
  trickier. Are you smart enough?" — missing `d` in "decidely"; double space
  after "trickier" also at index 73.
- The index-73 coincidence is unexplained; index hypotheses remain
  UNVERIFIED until we capture the original description bytes and archived
  snapshots ourselves.

---

## Rendition note (important for reproduction)

The user-supplied MP4s are 1280×720 / 60 fps / H.264 with 1800 decoded video
frames each (verified with ffprobe `-count_frames`). Community analyses were
performed on the only rendition YouTube currently serves (itag 18,
640×360 / 30 fps); their frame indexes are approximately half of ours, and
their "360p recovery ceiling" does not apply to these 720p60 files. YouTube
returns HTTP 403 to the default client for this channel's video IDs
(android player client reportedly works), so treat the 720p60 local files as
the superior source and record any re-acquisition attempt in
`docs/SOURCES.md`.
