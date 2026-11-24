# Previous Experiments and Negative Results (not necessarily deduplicated)

The following numbers were reported during earlier chat investigations; unless accompanied by a fresh, verified event ledger, regard them as **historical, not additive**.

## Verified session experiments (2026-11-23, this audit)

| # | Experiment | Method (reproducible command) | Result | Status |
| --- | --- | --- | --- | --- |
| S1 | Input integrity + codec audit | `sha256sum -c SHA256SUMS.txt`; ffprobe `-count_frames` | 75/75 files match manifest; 3×1800 frames at 1280×720/60fps | VERIFIED |
| S2 | Oracle certification | `python scripts/verify_ethereum.py --selftest`; eth_keys cross-check | Puzzle 1 key → `0xc99A...47a8f`; Keccak vectors pass; independent-library match | VERIFIED |
| S3 | On-chain escrow audit | etherscan retrieval 2026-11-23 | Puzzle 2 escrow: 1 in-tx, 0 out-tx, 0.05 ETH held; Puzzle 1 escrow emptied 2018-07-26 | VERIFIED (explorer-sourced) |
| S4 | Puzzle 1 flash existence + line count | signed diff mask (`scripts/analyze_flash.py` + signed arithmetic) | exactly 4 text lines at y≈226/306/389/469, flash frames 727–728 only, brightening-only; "fifth line" was a uint8 wrap-around artifact | VERIFIED |
| S5 | Flash character-by-character read | 3-way adjudication incl. same-font matching vs solution screen | `0x1FA8BE9DE5BBFE047C72DB8E8E3257128F7661AD` = on-chain escrow address; disputes resolved with quantified IoU (3:0.747 vs 8:0.544; 5:0.678 vs 6:0.469; D:0.535 vs 0:0.307) | VERIFIED (address disclosure; not a key fragment) |
| S6 | Part 1 seam read | composite right(n)+left(n+19), rot90CW; VLM per-glyph | `6A6B0860B4` reproduced; B/D unresolved (synthetic D 0.50–0.51 vs B 0.476–0.482) | REPLICATED (parameter-dependent) |
| S7 | Part 2 state machine | majority-vote masks over 45 state frames | A9-B6-C8-B2-A7-B6-C6-B4-A5-B6-C10(+C 1548-49); B=A∪C at 99.8% | VERIFIED |
| S8 | Part 2 column read | same-font/structure adjudication of six windows | `723504` supported; pos4 5-vs-6 persists (flat top bar → 5); `723604` recorded | REPLICATED (model-dependent) |
| S9 | Hidden-flash scan, both Puzzle 2 videos | isolated-spike detector over all 3600 frames | no 1–2-frame brightening overlay anywhere (only the Puzzle 1 control flash at 727/728); f1718 event is a persistent scene re-grade | NEGATIVE (threshold-dependent) |
| S10 | AAC packet + PCM audit | ADTS re-split; decoded PCM correlation/band energy | 16/1295 packets differ at 20.526–20.944 s; residual = ~800 Hz transient, correlation 0.999998 overall; consistent with encoder artifact, no message | NEGATIVE for intentional signal (unexplained residue preserved) |
| S11 | Edge-fragment mechanic deep audit | `python scripts/decode_part1_edges.py ... --check-redisplay` | Static cut fragments confirmed (no interior ink); 10/10 pairs at +19; [right(f_n) | left(f_n+19)] identity join correct; cell 10 '4' structurally confirmed; cells 4/9 = B by left-stem pixel profile | VERIFIED (mechanic + 8/10 cells) |
| S12 | Same-font adjudication of edge glyphs vs Puzzle 1 solution screen | height-normalized IoU template match | max IoU 0.18–0.27 across all cells — solution-screen font does NOT match the edge glyph face | NEGATIVE (fonts differ) |
| S13 | Archived-composite reverse engineering | concat/overlay/grayscale-merge alignment search over all (n, n+19) fragment pairs | best correlation ~0.38 vs archived PNG — earlier session composites not byte-reproducible; retained as historical evidence only | NEGATIVE (construction unknown) |
| S14 | Bottom-edge +236 re-display check | template correlation, tight bbox | f1230→f1466 bottom edge: 0.527 at x=103, y=621 | OBSERVED (weak-moderate, supporting) |

## Historical chat-reported families (NOT deduplicated; do not sum)

| Family | Reported experiment | Outcome | Limitation |
| --- | --- | --- | --- |
| One-piece hashes/padding | ~3,528 candidates from `6A6B0860B4`, `723504`, `C8` combinations, SHA-256/Keccak/SHA3/double SHA, padding, repetition | No target match | Inputs are partial and may not be a derivation seed |
| Four-block ordering | ~3,456 candidates with `04` as separate group, 24 orders, reversals and hash methods | No match | `04` separate-group assumption later withdrawn |
| Additional ordering/hash tests | ~6,731 keys exploring `2-4-1-3`, fragment orders, transformations, relation to historic Puzzle 1 key | No match | Candidate overlap with earlier batches unknown |
| Revised two-model permutations | ~1,288 tests of literal `4` vs marker `4` | No match | Does not establish whether `4` is instruction |
| Community broad work | ~8.9 million candidate derivations reported in floflo777 issue #5 | No reported match | External claim; audit methods/ledger before inheriting counts |
| Part 1 typography | GFS Didot B vs D comparison ~70.7% vs ~65.2% | Favored B | Geometry and composites can be biased |
| Part 1 seam | ~19/20 frame lag and random-control tests | Supports continuity conditionally | One simple pixel control p~0.10; later template permutation p<0.00005 conditional on selected anchors |
| Part 2 font-dependent decoding | Pitch 69..74; Noto vs Didot comparisons | `723504` strongest at 73–75, `723604` sometimes | Calibration initially influenced by proposed sequence |
| Part 2 held-out fourth glyph | 46/50 best geometries favored `5` | Supports `723504` | Correlated geometries, six-slot assumption and fixed other chars |
| Part 2 layer comparison | C+A raw reconstruction; A+C and mirroring controls | C+A visually more legible | Seam score of empty boundaries is uninformative |
| Video flash detection | 3600 Puzzle 2 frames plus solved Puzzle 1 control | No additional conclusive full-key end flashes | Depends on detector thresholds and source encodes |
| Audio residual | 16 of 1295 AAC packets differed near 20.5–21s | Unexplained localized difference | Not yet decoded or proved intentional |

**Rule:** Every new attempt must log canonical input, transformation, dedup hash, expected test, actual output (without exposing undisclosed secrets) and tested version. A failure of an arbitrary derivation transform says nothing about untested transforms or whether the clips contain sufficient entropy.
