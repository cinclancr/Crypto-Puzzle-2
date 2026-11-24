# Research Findings and Status

**Session date:** 2026-11-23 (independent audit of all supplied sources)
**Status:** **OPEN / UNRESOLVED.** No 64-hex private key for the inferred
escrow has been cryptographically verified. No candidate below is a
confirmed key substring.

## What this session verified end-to-end

1. **Input integrity** — all 75 archive files match the SHA-256 manifest
   (`SHA256SUMS.txt`); the three MP4s are H.264 1280×720@60fps with exactly
   1800 decoded frames each (ffprobe `-count_frames`).
2. **Ethereum oracle** — pure-Python Keccak-256 (legacy Ethereum domain
   suffix 0x01) + secp256k1 scalar multiply reproduces Puzzle 1's public key
   → `0xc99A54EEA6036115f913A13D6606e935bcA47a8f`, and matches an
   independent `eth_keys` implementation on the same vector and Keccak test
   vectors. `pytest -q`: 6/6 passed.
3. **On-chain escrow verification (etherscan, retrieved 2026-11-23)**
   - Puzzle 1 escrow `0xc99A...47a8f`: 0.05 ETH in on 2018-07-19
     (tx `0xa8de9727...`) from `0x0A937eC94...2e15`; two outgoing txs on
     2018-07-26; balance 0 — consistent with "solved and claimed".
   - Puzzle 2 escrow `0x1fa8...61ad`: exactly one incoming tx
     (`0x8eb982eb...`, 0.05 ETH, 2018-08-01, block 6,067,019) from the same
     funder; **no outgoing transactions; balance 0.05 ETH to this day.**
   - The inferred target rests on the shared funder + amount + timing
     pattern, which we confirmed directly.

## Upgraded: the Puzzle 1 address flash is now a VERIFIED OBSERVATION

The 2-frame mirrored overlay (frames 727–728, ~12.12 s) was re-analyzed with
signed-difference masking (fixes a uint8 wrap-around that faked a "fifth
line") and read character-by-character with three independent methods
(multi-font template matching; focused vision reads; same-font matching
against glyphs extracted from the same video's THE SOLUTION screen). The
assembled four-line text, read in visual order 2-4-1-3, is

```
0x1FA8BE9DE5BBFE047C72DB8E8E3257128F7661AD
```

which equals the escrow address verified on-chain above — i.e. the author DID
disclose the Puzzle 2 address in the Puzzle 1 solution video, contradicting
the earlier dossier statement that the address was never published.
Disputed glyphs were settled with quantified same-font evidence
(`3` 0.747 vs `8` 0.544; `5` 0.678 vs `6` 0.469; `D` 0.535 vs `0` 0.307;
`E` resolved by pixel-level three-arm structure). Reproduce with
`scripts/audit_puzzle1_flash.py`; its unattended single pass resolves ~35/43
cells and the balance with the documented adjudication. The flash remains a
PUBLIC ADDRESS disclosure only; it does not verify any ordering rule for
private-key fragments.

## Replicated (parameter-dependent) extractions

- **Part 1 seam read `6A6B0860B4`** — reproduced TWICE independently and now
  structurally grounded (see `docs/EVIDENCE_DOSSIER.md` B2/B2b): the edge
  events are static CUT FRAGMENTS (no interior ink) — the right-edge
  fragment of frame n is the glyph's LEFT portion and the left-edge fragment
  of frame n+19 is the SAME glyph's RIGHT portion (10/10 pairs at exactly
  +19); joining `[right(f_n) | left(f_n+19)]` at identity alignment
  reassembles each glyph. Cell 10 is a structurally confirmed serif `4`
  (which also proves the join order); cells 1/3/7=`6`, 5/8=`0`, 6=`8`,
  2=`A` (historical + focused vision) are multi-source; cells 4/9=`B` carry
  a documented residual B/8/D ambiguity (pixel profile shows a straight
  full-height left stem → B; vision wavered B/8; historical synthetic IoU
  D-vs-B near-tied; `6A6D0860D4` and `6A68086084` variants preserved).
  Reading direction and position in the key remain unknown. Reproduce with
  `scripts/decode_part1_edges.py` (embeds ASCII evidence in the JSON report;
  also reproduces the bottom-edge +236 re-display at 0.527 correlation).
- **Part 2 column read `723504`** — state machine (A9/B6/C8/B2/A7/B6/C6/B4/
  A5/B6/C+) and B = A∪C (99.8%) reproduced; majority-vote reconstruction
  from 45 state frames reproduces the raster supporting `723504`; position 4
  `5` vs `6` is the persistent ambiguity (flat top bar favors `5`, matching
  the 46/50 held-out historical result); `723604` stays recorded. Six-slot
  geometry itself is hypothesis-conditioned; pixel content is hard-cut at
  x=663 and absent pixels are unrecoverable without model assumptions.
- **Part 2 MIRROR card** — mirrored `C`+`8` (reads `C8` after horizontal flip)
  and reversed `MIRROR` confirmed at ≈frame 1260.

## Negative tests reproduced this session

- **No hidden end-of-video key flash in either Puzzle 2 video** —
  isolated-spike scan over all 3600 frames: the only Puzzle-1-style 1–2-frame
  brightening overlay is the 727/728 address flash itself. Part 1's big
  change at frame 1718 is a persistent scene re-grade, not an overlay.
- **Audio differences are localized and consistent with encoder artifacts**
  — 16/1295 differing AAC packets at 20.526–20.944 s reproduced; PCM
  correlation 0.999961 locally / 0.999998 globally / 1.000000 in controls;
  the residual is a ~800 Hz transient band, 12× band-energy of control
  windows, but no message structure was found and none is claimed.
- **Part 2 supplies no complementary edge halves** (no edge-touching content
  in any of its frames).

## Not established

- Any verified Puzzle 2 private-key substring, block structure (the
  "four 16-hex blocks" idea), concatenation rule, or ordering rule for key
  fragments. The 2-4-1-3 order is verified only for the address flash.
- Whether `C8` is key data or an instruction; whether the static trailing
  `4` in Part 1 is data, decoy, or instruction.
- Whether additional primary sources exist (statement-video flashes are an
  unverified external claim; archived channel pages list exactly 5 videos).
- Description byte-for-byte capture (typos `intellience`/`decidely` and the
  index-73 coincidence are external claims pending our own snapshot capture).

## Highest-information-gain next experiments

1. **Capture the two Puzzle 1 statement videos** (IDs `3l1jFa3Mw0s`,
   `hX-pOBj8VsI`, android player client per community note) at the best
   available rendition and run the flash detector as a positive control with
   a known ground truth (the `482BE6FB9C` / `1007322EA` claims).
2. **Same-font template pass on Part 2's column at higher fidelity** —
   build the reference library from the Puzzle 1 solution screen (as
   `scripts/audit_puzzle1_flash.py` already does), then classify the column's
   six windows with per-glyph uncertainty; resolve the `5`/`6` slot with
   the flat-top-bar criterion and the others' alternatives explicitly.
3. **Rendition hunt for unclipped glyphs** — the right-edge glyphs are cut
   by the frame boundary and the column is cut at x=663; only a different
   crop or a higher-resolution source can add real pixels. Check archive.org
   snapshot captures of the watch pages and any 2018-era re-uploads before
   spending more effort on in-frame reconstruction.

## Standing rule

No glyph reading is a key substring until a complete 64-hex candidate
derives to the target address. The puzzle remains OPEN.
