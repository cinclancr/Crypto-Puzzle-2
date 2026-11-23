# Figures

This directory intentionally ships **no video-derived imagery** by default:
frame crops, composites, layer masks and window montages are derivatives of
copyrighted YouTube footage, and redistribution rights for derived imagery
have not been confirmed (see `docs/PUBLISHING_AND_RIGHTS.md`).

The published, copyright-safe evidence is the ASCII rendering embedded in
the JSON reports under `data/evidence/`. To regenerate the full-resolution
PNG renders locally (with lawful access to the videos):

```bash
python scripts/decode_part1_edges.py --video 'local_sources/videos/Solve The 2nd Crypto Puzzle  - Win 0.05 Ethereum - Part 1.mp4' --output results/edges
python scripts/decode_part2_column.py --video 'local_sources/videos/Solve The 2nd Crypto Puzzle - Win 0.05 Ethereum - Part 2.mp4' --output results/column
python scripts/audit_puzzle1_flash.py --video 'local_sources/videos/Crypto Puzzle 1 Solved!.mp4' --output results/flash_audit
```

Original scientific diagrams (e.g., redrawn architecture or timeline charts
that do not contain video pixels) may be added here under an open license.
