# Source Registry and Provenance

**Updated:** 2026-11-23. All external claims below were retrieved/verified this
date unless noted. Cite as `docs/SOURCES.md` of the repository.

## Primary publisher / original public material

| Source | URL | Role / notes |
| --- | --- | --- |
| Puzzle 2, Part 1 | https://www.youtube.com/watch?v=TRUUTryah70 | Primary clip; wrap-around edge glyphs (posted 2018-08-06 per dossier; Part 2 upload date differs between dossiers — see note) |
| Puzzle 2, Part 2 | https://www.youtube.com/watch?v=U_0DtYHDPy0 | Primary clip; MIRROR card + vertical column |
| Puzzle 1 solution reveal | https://www.youtube.com/watch?v=0jJ6XadOAWk | Public key oracle vector; 2-frame address flash at frames 727–728 (720p60 indexing) |
| Puzzle 1 statement part 1 | https://www.youtube.com/watch?v=3l1jFa3Mw0s | NOT SUPPLIED locally; flash claims are external |
| Puzzle 1 statement part 2 | https://www.youtube.com/watch?v=hX-pOBj8VsI | NOT SUPPLIED locally; flash claims are external |
| Channel "Crypto Puzzles" | https://www.youtube.com/channel/UCR8-P07nNhxyEr6fwJXvjQQ | Exactly 5 videos per archived channel pages (2020-10-20, 2025-08-23; external claim) |

Rendition status (community note, 2026-08): only itag 18 (640×360, 30 fps) is
served for all five videos; YouTube returns HTTP 403 to the default client
(android player client reportedly works). The user-supplied 1280×720/60 fps
MP4s are therefore a superior, locally held source; their SHA-256 values are
pinned in `data/source_manifest.json`. Do not commit them (see
`docs/PUBLISHING_AND_RIGHTS.md`).

Upload-date discrepancy (external claims, unresolved): the floflo777 dossier
dates both Puzzle 2 parts to 2018-08-06; the agntn.dev collection states
Part 1 2018-08-06 and Part 2 2018-08-27, and lists Puzzle 1 statement videos
as 2018-07-25/26 while floflo777 dates them 2018-07-19. Verify from the
watch pages / archive snapshots before citing either.

## Ethereum chain (verified via etherscan on 2026-11-23)

- Puzzle 2 target (inferred escrow): https://etherscan.io/address/0x1fa8Be9De5bBFE047C72dB8E8E3257128F7661ad —
  one incoming tx `0x8eb982ebfb492eb535724c1f9a68253bef31598712315b5ff3a11b5efa71bbdf`
  (0.05 ETH, 2018-08-01, block 6067019) from the funder; **no outgoing
  transactions; balance 0.05 ETH** at retrieval time.
- Puzzle 1 historical escrow: https://etherscan.io/address/0xc99A54EEA6036115f913A13D6606e935bcA47a8f —
  incoming `0xa8de9727e5166795b2a2e8d7b61762418dfaf3841dd9055769996bcaff74da46`
  (0.05 ETH, 2018-07-19, block 5990424); two outgoing on 2018-07-26
  (`0xab150c5d...` 0.049682 ETH, `0xaf47c9c3...` 0.000171 ETH); balance 0.
- Funder wallet (both escrows): `0x0a937ec94abc55d92f5740a988a122ebdcab2e15`.
  The Puzzle 2 destination is an inference from this shared funding pattern
  plus the amount/timing, not an address stated in the videos — although the
  727–728 flash in the Puzzle 1 solution video independently displays it
  (see `docs/EVIDENCE_DOSSIER.md` §A2).
- Algorithm: secp256k1 scalar multiply → 64-byte x‖y public key → legacy
  Keccak-256 → last 20 bytes. Puzzle 1's disclosed key is the control vector
  (`docs/PUZZLE1_CONTROL.md`).

## Community / independent research (claims audited, not inherited as fact)

- floflo777 dossier: https://github.com/floflo777/open-crypto-puzzles/blob/main/3-small-prizes/crypto-puzzles-2018-puzzle-2-0-05eth/README.md
  — formal dossier, same funder/target inference, "part 1 reads 10 hex
  characters `6A6B0860B4`" (matches our independent read), open status,
  last on-chain check 2026-08-16.
- Tested ledger: https://github.com/floflo777/open-crypto-puzzles/blob/main/3-small-prizes/crypto-puzzles-2018-puzzle-2-0-05eth/analysis/tested.md
  — 12-row negative/structural ledger on the 360p rendition: payload
  glyphs are cut by the frame boundary; part 2 supplies no complementary
  halves; C (0.771) and 8 (0.849) after flip; alternating-column components
  are truncated; "external-info" reclassification (360p ceiling).
- Issue #5 discussion: https://github.com/floflo777/open-crypto-puzzles/issues/5
  — diploux reads `6A6B0860B` (Didot) and `723504` (6 chars, "99% certain",
  vertical overlap described); timothy-barus: 19-frame lag via change
  schedule, 10th char `4`, seam-B 20-px truncation explains `6A6D0860D4`,
  Puzzle-1 statement-video flash claims (frame 1180 etc., with their own
  `2007322EA` misread correction to `1007322EA`), @fuyr 2018 comment
  "I have 16 hex", description typo transcriptions and the index-73
  coincidence, ~8.9M candidate derivations (methods unaudited — do not
  inherit the count).
- agntn.dev collection: https://puzzles.agntn.dev/collections/crypto-puzzles
  — independent series record; corroborates Puzzle 1 key/address and the
  unclaimed Puzzle 2 balance (checked 2026-10-18); different upload dates
  for the Puzzle 2 parts (see discrepancy note above).
- Secondary snapshot: https://github.com/itsnex1s/crypto-puzzle-list/blob/main/unsolved/crypto-puzzles-2018-puzzle-2-0-05eth.md
  (metadata echo; verify before quoting).

## User-provided local assets (not committed)

- Three original 1280×720/60fps H.264/AAC MP4s under `local_sources/videos/`
  (hashes in `data/source_manifest.json`); `image(4).png` user screenshot;
  Spanish-language historical reports/scripts/CSVs under
  `local_sources/previous_reports`, `previous_scripts`, `measurements`,
  `figures` — historical evidence, superseded by the English documentation
  where they disagree; the crucial technical content is summarized in
  `docs/EVIDENCE_DOSSIER.md` and `docs/CHAT_RESEARCH_TIMELINE.md`.

## External research TODO (capture-before-test)

- Original description bytes for both Puzzle 2 videos (typos `intellience` /
  `decidely` + double space; verify the index-73 `g`/double-space claim).
- Wayback snapshots of the two watch pages and the channel page over time
  (the 2020-10-20 / 2025-08-23 archived pages reportedly list exactly 5
  videos — verify that no third Puzzle 2 part ever existed).
- The two Puzzle 1 statement videos (positive control for flash detection).
- 2018-era comment threads (the @fuyr claim) and any author statements.
