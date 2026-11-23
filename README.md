# Crypto Puzzle 2 — Evidence-Driven Ethereum Video Puzzle Research

**Status: OPEN / UNSOLVED.** No full private key has been cryptographically verified.

This repository documents and provides reproducible tooling for a public Ethereum video puzzle published in 2018 by the YouTube channel **Crypto Puzzles**. The challenge consists of two short, 60 fps video clips and offers a historically funded 0.05 ETH prize. Our working target is the 20-byte Ethereum address:

`0x1fa8Be9De5bBFE047C72dB8E8E3257128F7661ad`

This is an **inferred** target based on public funding history (same funder wallet, amount and timing as the solved Puzzle 1 escrow — verified on-chain 2026-11-23; the address holds 0.05 ETH with zero outgoing transactions). The two challenge videos never state the address, but the author DID flash it for two frames in the Puzzle 1 solution video (independently verified here; see `docs/PUZZLE1_CONTROL.md`). Check current balance with a trusted Ethereum node before making any claim.

**Primary assets:** [Puzzle 2 Part 1](https://www.youtube.com/watch?v=TRUUTryah70), [Puzzle 2 Part 2](https://www.youtube.com/watch?v=U_0DtYHDPy0), and the [Puzzle 1 solution/reveal](https://www.youtube.com/watch?v=0jJ6XadOAWk). Full videos are **not tracked** here. Researchers may use their own lawfully acquired copies under `local_sources/videos/`.

## Verified baseline vs. candidate extractions

| Item | Current interpretation | Confidence / limitation |
| --- | --- | --- |
| Expected answer | Raw 32-byte secp256k1 private key represented by 64 hex digits | Strong, corroborated by solved Puzzle 1; no BIP39 path |
| Historical Puzzle 1 key | `4487FC620AD0C4C67E80BE342B2EA1F5A3DC482BE6FB9C2451007322EA8BE35F` | Public known-good oracle vector; **not Puzzle 2** |
| Puzzle 1 derived address | `0xc99A54EEA6036115f913A13D6606e935bcA47a8f` | Independently verifiable from public key vector |
| Puzzle 2 Part 1 edge glyphs | `6A6B0860B4` | Reproducible candidate; 19–20 frame pairing, clipping, B/D and ordering uncertainties |
| Puzzle 2 Part 2 mirrored card | `MIRROR` plus likely `C8` | Strong visual instruction; whether characters are key data is unknown |
| Puzzle 2 Part 2 last column | `723504` | Improved raw C+A layer reconstruction; six-glyph/75-px geometry assumed; `723604` remains model-dependent alternative |
| Four 16-hex blocks | First candidate `6A6B0860B4723504` | Numerical coincidence; positions, concatenation and existence of 4 blocks unproved |
| Address flash in Puzzle 1 reveal | Frames 727–728 (720p60), four 180°-rotated lines read in visual order 2→4→1→3 | **Independently verified 2026-11-23** to spell `0x1FA8BE9DE5BBFE047C72DB8E8E3257128F7661AD`, equal to the on-chain escrow; address disclosure only — proves nothing about key-fragment ordering |
| Full Puzzle 2 private key | **Unknown** | No verified 64-hex candidate or Ethereum address match |

**Do not confuse a visually plausible glyph string with a verified secret-key substring.** Do not represent failed hypothesis families as a general proof of impossibility.

## Quick start

```
python -m pip install -r requirements.txt
python scripts/verify_ethereum.py --selftest
python scripts/inspect_media.py --input-dir local_sources/videos --output results/inspection
python scripts/extract_reconstructions.py --part2 'local_sources/videos/Solve The 2nd Crypto Puzzle - Win 0.05 Ethereum - Part 2.mp4' --output results/reconstructed
python scripts/audit_puzzle1_flash.py --video 'local_sources/videos/Crypto Puzzle 1 Solved!.mp4' --output results/flash_audit
python scripts/decode_part1_edges.py --video 'local_sources/videos/Solve The 2nd Crypto Puzzle  - Win 0.05 Ethereum - Part 1.mp4' --output results/edges --check-redisplay
python scripts/decode_part2_column.py --video 'local_sources/videos/Solve The 2nd Crypto Puzzle - Win 0.05 Ethereum - Part 2.mp4' --output results/column
python -m pytest -q
```

Reference outputs of the JSON evidence reports (with ASCII renderings) are
committed under `data/evidence/` so reviewers can diff their regenerated
reports without access to the videos.

`ffmpeg` and `ffprobe` should be installed for media inspection. The Ethereum self-test itself uses a zero-external-dependency Python implementation of secp256k1 and original Keccak-256 and is deliberately slow but auditable. Cross-check independently with an external implementation such as `eth_keys` before using candidate results.

## Research documentation

- [Evidence dossier](docs/EVIDENCE_DOSSIER.md) — observations, source timestamps, uncertainty and historical corrections
- [Source registry](docs/SOURCES.md) — original YouTube, Ethereum explorer, open research, user evidence and rights notes
- [Research plan](docs/RESEARCH_PLAN.md) — ranked falsifiable experiments, not open-ended brute forcing
- [Prior negative tests](docs/EXPERIMENT_LEDGER.md) — avoid repeating expensive dead ends
- [Puzzle 1 control](docs/PUZZLE1_CONTROL.md) — validate Ethereum cryptography and video-forensic methods
- [FAQ / status snapshot](docs/FAQ.md) — the ten questions newcomers ask first
- [Architecture](docs/ARCHITECTURE.md) — pipeline diagram and evidence-class separation
- [Publishing and rights](docs/PUBLISHING_AND_RIGHTS.md) — copyright, secrets, input handling
- [Findings](docs/FINDINGS.md) — latest verified status; add new experiments here with witnesses
- [Research timeline](docs/CHAT_RESEARCH_TIMELINE.md) — chronological history of the investigation

## Research discipline

1. Analyze original sources frame-for-frame, pin SHA-256, record frame numbers (0-based), threshold values and exact code version.
2. Separate source observations, derived reconstructions, author claims, community claims, and speculative interpretations.
3. Confirm clip identity and timestamps; do not rely on text recovered from another puzzle or different YouTube channel.
4. Verify any complete 64-hex candidate against the target using **Ethereum Keccak-256**, not SHA3-256.
5. Keep experiments, candidate deduplication, provenance and exceptions machine-readable; seek positive controls and out-of-sample measurements.
6. Treat unresolved missing key entropy as an information problem, not a brute-force parameter.

## Repository status and attribution

This project is being assembled from previously performed analyses and user-supplied video sources as of November 23, 2026. Reported prior test counts are not necessarily deduplicated. The repository's existing MIT `LICENSE` is intentionally left untouched; attribution concerns must be resolved by the owner rather than silently rewritten. Public video content is linked, not redistributed by default.
