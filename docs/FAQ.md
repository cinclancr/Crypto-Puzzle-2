# Research FAQ / Status Snapshot

**As of:** 2026-11-23 · **Puzzle status:** OPEN / UNSOLVED (no 64-hex private
key verified against the escrow address).

## The ten questions newcomers ask first

**1. What exactly is being solved?**
A public Ethereum prize puzzle published in 2018 by the YouTube channel
"Crypto Puzzles" (two ~30 s videos). The intended answer is believed to be a
raw 32-byte secp256k1 private key written as exactly 64 hexadecimal digits
(the same format the author used for the solved Puzzle 1), not a BIP39 phrase
or a BIP44-derived wallet. Only a candidate whose derived public key hashes
(Ethereum Keccak-256 of the 64-byte uncompressed public key, last 20 bytes)
to the escrow address counts as solved.

**2. What is the prize address, and how confident are we?**
`0x1fa8Be9De5bBFE047C72dB8E8E3257128F7661ad`. Confidence: high but inferred —
it received exactly one incoming 0.05 ETH transaction on 2018-08-01 from the
same funder wallet that funded the solved Puzzle 1 escrow, and it has never
spent (verified via etherscan, 2026-11-23). Additionally the Puzzle 1
solution video flashed this exact address for two frames (independently
re-read character-by-character this session; see
`docs/PUZZLE1_CONTROL.md`), which upgrades it from "inferred" to
"author-disclosed, independently verified".

**3. Is the puzzle solved by this repository?**
No. No complete 64-hex candidate has been verified. All glyph strings below
are candidate *fragments* at best.

**4. What fragments have been reproduced?**
- Part 1 edge glyphs: `6A6B0860B4` (mechanic now code-verified; cells 4/9
  carry a documented B/8/D residual ambiguity; alternatives `6A6D0860D4`,
  `6A68086084`).
- Part 2 vertical column: `723504` (model-dependent; `723604` alternative;
  six-slot geometry is itself hypothesis-conditioned).
- Part 2 mirrored card: `C8` (could be data or instruction).
- Plus the historical Puzzle 1 key as the cryptographic control vector.

**5. Why can't we just brute-force the missing digits?**
If only ~18 hex digits are known (10 + 6 + 2), the remaining 46 digits span
16^46 ≈ 2^184 possibilities — cryptographically infeasible. The information
must come from the puzzle itself, not from search.

**6. What is the four-part hypothesis and why is it unproved?**
The idea that the 64-hex key consists of four 16-hex blocks, with
`6A6B0860B4`+`723504` (10+6=16) being one block. It is numerically neat but
no evidence establishes contiguity, block count, ordering, or membership.
The 2-4-1-3 ordering is verified ONLY for the Puzzle 1 four-line public
address flash — not for private-key fragments.

**7. Did the videos hide anything in audio or metadata?**
The only audio anomaly (16 differing AAC packets, ~20.53–20.94 s, Part 1 vs
Part 2) reproduces as an ~800 Hz transient consistent with an encoder
artifact; PCM correlation 0.999998 overall. No message structure established.
No hidden end-of-video key flash exists in either Puzzle 2 video (scanned
frame-by-frame; the only 1–2-frame brightening flash in the whole corpus is
the Puzzle 1 address flash).

**8. Why do community frame numbers differ from yours?**
Community analyses used the 360p/30fps rendition YouTube currently serves;
our sources are 720p/60fps local files. Their frame n ≈ our frame 2n.

**9. What would a verified solution require?**
A complete 64-hex candidate string C such that `verify_ethereum.py
--candidate C` derives an address equal (case-insensitively) to the escrow.
If you find it: do NOT publish the key; contact the repository owner and the
video author first (see `SECURITY.md`).

**10. What are the highest-information-gain next steps?**
1. Capture the two Puzzle 1 statement videos (`3l1jFa3Mw0s`,
   `hX-pOBj8VsI`; android player client reportedly works) and run the flash
   detector with a known ground truth as positive control.
2. Same-font template pass on the Part 2 column using a font library that
   actually matches the column's face (the Puzzle 1 solution-screen font
   demonstrably does NOT match — IoU ≤ 0.27).
3. Rendition/archival hunt for unclipped pixels (the column is hard-cut at
   x=663; the edge glyphs are cut at the frame boundary; only a different
   crop or higher-resolution source can add real pixels).

See `docs/RESEARCH_PLAN.md` for the full ranked experiment list and
`docs/EXPERIMENT_LEDGER.md` for what already failed.
