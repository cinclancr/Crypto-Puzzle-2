# Solved Puzzle 1 — Positive Cryptographic Control

The challenge series' earlier puzzle was solved publicly in 2018. Its reveal
("THE SOLUTION" screen, held ~6 s) displayed the raw 32-byte private key:

```
4487FC620AD0C4C67E80BE342B2EA1F5A3DC482BE6FB9C2451007322EA8BE35F
```

The corresponding Ethereum address is:

```
0xc99A54EEA6036115f913A13D6606e935bcA47a8f
```

This is **historic, disclosed** key material for a solved puzzle, never a
candidate for Puzzle 2. It validates the exact Ethereum Keccak/secp256k1
transformation (last 20 bytes of Keccak-256 of the uncompressed public key
without the 0x04 prefix; SHA3-256 is NOT equivalent):

```
python scripts/verify_ethereum.py --selftest
```

The self-test additionally cross-checks the pure-Python implementation
against an independent library (`eth_keys`) during development; CI runs the
zero-dependency version. On-chain: the address was funded 0.05 ETH on
2018-07-19 by `0x0a937eC94...2e15` and emptied on 2018-07-26 (verified on
etherscan 2026-11-23 — see `docs/SOURCES.md`).

## The frames 727–728 address flash — independently verified 2026-11-23

A 1–2-frame, 180°-rotated overlay appears in this video at zero-based frames
727–728 (~12.12 s). It contains four lines of ~25-px text. Read in visual
line order 2 → 4 → 1 → 3 (each line's glyphs reversed), the overlay spells:

```
0x1FA8BE9DE5BBFE047C72DB8E8E3257128F7661AD
```

This equals the Puzzle 2 escrow address inferred from the funding pattern
and verified on-chain — so the author disclosed the Puzzle 2 **public
address** here. The read was reproduced without target injection via
(a) signed-difference masking (exactly four text lines; brightening-only),
(b) three-way glyph adjudication (multi-font templates, focused vision
reads, same-font matching against the solution screen's own glyphs), and
(c) quantified tie-breaks on the historically disputed cells (3/8, 5/6,
D/0, E/F/B). Run the reproduction:

```
python scripts/audit_puzzle1_flash.py --video local_sources/videos/"Crypto Puzzle 1 Solved!.mp4" --output results/flash_audit
```

Scope limits (unchanged): this is a disclosure of the *address*. It does
NOT reveal any private-key fragment and does NOT prove that Puzzle 2's key
pieces use the 2-4-1-3 order or a four-block structure.

## Statement-video flashes — external claim, not verified here

Community reports single-frame flashes in Puzzle 1's *statement* videos
(360p/30fps indexes: part 1 frame 1180; part 2 frames 1024, 1039, 1053,
1180) reading `482BE6FB9C` and (with their own correction) `1007322EA`.
Those videos are not part of the local package; obtain them (channel IDs in
`docs/SOURCES.md`) and run the flash detector as a positive control before
relying on any negative "no flash" result for Puzzle 2.
