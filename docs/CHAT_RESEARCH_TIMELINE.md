# Chronology of Our Video-Puzzle Investigation (Historical, English)

This is an English reconciliation of the long prior conversation. It is not a claim that all intermediate interpretations were correct. For original numerical results and scripts, consult the bundled `local_sources/` archive; the primary videos remain the source of truth.

## Initial framing and source files

- The user supplied the two original Puzzle 2 parts and later the Puzzle 1 solution/reveal MP4.
- Multiple 720p/60fps frame extraction passes yielded 1,800 frames per Puzzle 2 clip; earlier analyses produced contact sheets, enlarged crops, masks, audio residuals, timing maps and source-comparison videos.
- The Ethereum target `0x1fa8Be9De5bBFE047C72dB8E8E3257128F7661ad` was inferred via same-funder, same-0.05-ETH-pattern research, not presented by the challenge's two statement clips.
- The raw-key 64-digit Ethereum oracle was validated against Puzzle 1 publicly revealed key `4487FC620AD0C4C67E80BE342B2EA1F5A3DC482BE6FB9C2451007322EA8BE35F` (derived address `0xc99A54EEA6036115f913A13D6606e935bcA47a8f`).

## Frame-by-frame Part 1 reconstruction

- Initial glyph reading from lateral edge seams proposed `6A6B0860B4`, with the later left-edge frame about 19/20 positions after its right-edge counterpart. A 10-digit form expanded a 9-moving-digit initial read `6A6B0860B` plus a long-held `4`.
- Reversed footage, frames-per-second conversions, source codec, and font family could affect visual morphology. Original anchors included 1219,1221,1224,1226,1229,1231,1234,1237,1239,1242.
- Top/bottom glyph paths appear ~236 frames after the earlier left/right stream, with the same approximate digits and an offset of 18 frames between upper and lower halves. An initial separate `04` fragment and four independent screen-regions model were **withdrawn**: the top/bottom paths are more likely a cropped, repeated display of the same characters.
- The two B glyphs can resemble D due to clipping 20 pixels from the central notch; both strings `6A6B0860B4` and `6A6D0860D4` were discussed. A local Didot fit favored B over D, but these comparisons used composited rather than fully original glyphs.
- A control focused only on edge-pixel overlap yielded weak significance (p~0.10). A later selected-template pair vs 20,000 permutations gave 84.14% vs 77.42% random-mean and no random score higher, but this conditional test did not eliminate anchor/template-selection bias. Preserve both results.
- A naive font-only blind classifier read `6A6B0860B1` instead of the proposed trailing `4`, illustrating why the last glyph must remain under audit.
- The held `4` produced an unproven “four parts”/delimiter theory. It may simply be the final literal hex character.

## Part 2 mirrored card and last column

- A title card around frame 1260 showed `MIRROR` reversed, a mirrored C and an 8. Horizontal reflection makes the word upright, yielding a likely `C8` pair; 8 is largely symmetric, C is not. Do not automatically apply textual reversal to every subsequent key fragment.
- From approx frames 1550–1618, a narrow vertical column is present; crop `gray[115:605, 620:664]` with the right boundary cut abruptly at x=663.
- Three recurring visual states were distinguished: layer A, layer C and their union B. State sequence durations were reported as `A9-B6-C8-B2-A7-B6-C6-B4-A5-B6-C10` in frame counts. No code was decoded from durations.
- A prior six-glyph model with ~73–75 pixel pitch and ~116–121 pixel height, requiring ~39% vertical overlap, produced `723504`; alternatives for pitch 69–72 yielded other readings (`722269`, `722309`, `722302`, `723A04`).
- GFS Didot Bold model often favored `723504`, whereas Noto Serif Display Medium calibrated on the complete original `C8` sometimes favored `723604` with a negligible score margin. An independent six-band/held-out-position exercise favored `5` over `6` (46 of 50 best selected geometries; broad sweeps correlated), though all rely on six-slot geometry.
- A non-font-based reconstruction used three frames per A layer [1554,1578,1600] and C layer [1568,1590,1611], median (>190), crop y115:605/x620:664, and C-to-left-of-A stitch. The resulting real pixel raster visually read `723504`. Reverse layer ordering and horizontal flips were less legible. Still no proof of substring position in 64-hex private key.
- The three cycles are highly similar (A ~99.9%, C ~99.7%); they are repetitions, not newly discovered messages. Allowing two different text strings improved a fitted model only ~0.271 percentage points versus a single common string.
- Six-symbol model outperformed some four-, five-, seven-, eight-symbol baselines under historical parameters, not across every possible geometry. The six-slot assumption remains a model choice requiring stronger external validation.

## The user-discovered mirrored flash in the Puzzle 1 solution video

- The user supplied a screenshot of the `TIME TAKEN / 2HRS & 56MINS` title with faint mirrored hexadecimal rows, originally thought absent from the clip. Later frame-by-frame analysis found matching overlays on frames 727 and 728 of the 60-fps original, absent from 726 and 729.
- The overlay was interpreted as the public Puzzle 2 Ethereum target, split into four visually positioned rows to be read 2→4→1→3. Earlier numerical validation aligned screenshot/background at ~frame725. Subsequent exact frame search found 727–728.
- This does **not** provide the private key, and an exact blind transcription still has to be reported. Do not confuse a public address with a secret key or import the 2-4-1-3 read order into private-key assembly without independent evidence. Public research which calls the target a funding-based inference may predate the hidden flash analysis.

## User's four-part hypothesis and tested compositions

- The user suspected the answer might be extracted as four parts and then reordered. A tempting arithmetic coincidence is 10 digits from Part 1 plus six from Part 2 `=16`, i.e. one quarter of a 64-digit key. This candidate fragment was displayed as `6A6B0860B4723504`, but never matched a complete verified Ethereum key.
- Another speculative model removed terminal `4`s as markers: 9+5+2=16 from `6A6B0860B`, `72350`, `C8`. Later data did not support special duration of the last `4` in the Part 2 column. Keep the literal-data model as default but do not close alternatives.
- The line-order cue `2-4-1-3` in the purported public-address flash was tested as a private-key block order using small transformations and produced zero matches; testing arbitrary hashing on incomplete data cannot establish it false or true.
- A separate `04` region model initially yielded `047235046A6B0860B4C8` with 20 digits, but was retracted because the 04 digits were duplicated and temporal stitching was not independent.

## Audio, hidden frames, and cross-video subtraction

- A differential AAC scan reported 1,279/1,295 packets bitwise identical and 16 mismatched packets near 20.526–20.991 seconds. PCM comparisons found small residual components at ~20.568/.648/.693/.942s, possibly aligned with edge glyph movement. No reproducible Morse, text, number or steganographic message was recovered.
- All 3,600 Puzzle 2 frames were decoded. A single-frame flash detector found no full-key flash analogous to the target-like Puzzle 1 solution/reveal flash at the end of either statement video. This is detector and source-encode dependent; do not claim a mathematical absence.
- Backgrounds between Part 1/2 were aligned to isolate glyph differences through frame subtraction; periods of interest include center 12.17–26.97s, right 20.32–22.13s, left 20.63–22.53s, top 24.23–26.25s, bottom 24.55–26.53s, vertical 25.83–26.97s.

## Already attempted candidate derivations and known blockers

- Hashes SHA-256, Ethereum Keccak, SHA3-256, double-SHA; simple padding/repetition; string permutations; four-side transpositions; reversals; frame-time and ordering heuristics; relation to Puzzle 1 public key; hundreds/thousands of candidate encodings. Individual batches have counts like 3,528, 3,456, 6,731, 1,288, plus external millions. None matched the target; dedup/cumulative count not certified.
- At least 46 hexadecimal digits are missing if the 18 recovered candidates are all genuinely independent literal key digits. No feasible brute-force approach fills 2^184 of unknown space without additional information.
- The necessary advance is a new source, independent geometric/readout proof, or an explicit derivation rule from the creator's multimedia encoding. If such evidence is absent, the puzzle remains unsolved. Do not claim it can be solved from present material with certainty.

## Current recommended priority order

1. Blind transcribe and verify the 727–728 Puzzle 1 overlay, comparing source variants, without knowing the target string.
2. Solve the Part 1 seam continuity and B/D problem with objective motion tracking and independent controls.
3. Reconstruct Part 2 C/A with out-of-sample geometry/model selection, eliminate 5-vs-6 ambiguity without answer tuning.
4. Search historical primary material for missing data and creator instructions before attempting private key assembly.
5. Maintain source hashes, candidate experiment ledger, and only claim success after full 64-digit key address verification.
