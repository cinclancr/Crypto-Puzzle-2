# Research Plan: Highest-Information-Gain Experiments

| Rank | Question | Experimental design | Stop/go criterion |
| --- | --- | --- | --- |
| 1 | Is the two-frame Puzzle 1 reveal flash really the Puzzle 2 public address? | Extract frames 726–729 from source; subtract neighboring frames; randomize line order/omit target; blind transcribe every character, compare afterward to independently verified funding address | Pass only if all 40 chars read unambiguously without target guidance; otherwise preserve alternatives |
| 2 | Does Part 1 edge lag represent true object continuity? | Compare x-t motion paths across 1200–1500, wrap-around geometry, random permutation controls, train/test anchor split, B/D and direction alternatives | Robust movement/evidence under multiple thresholds/encodes; no artificially merged glyphs |
| 3 | Can the Part 2 column be read without geometry seeded by `723504`? | Fit six-slot pitch/height/overlap on held-out regions, compare model complexity across 4–8 symbols, use C8 as independent font control, compare all glyph hypotheses | Stable per-character interpretations across font/codec/threshold and spatial holdouts |
| 4 | Are C/A genuinely complementary halves or repeated information? | Pixel set and mask comparisons, multiple cycles, alternate C+A/A+C/flip order, synthesis vs raw, register edges with nonempty strokes | Distinctive objective seam criterion with uncertainty; never rely on zero mismatch between empty columns |
| 5 | Are there other source assets/hints? | Search official video IDs, early archive snapshots, channel comments, title descriptions, higher bitrate encodes, editing templates, public GitHub discussions and historical comments | New attributable primary pixels or creator guidance; else log absence accurately |
| 6 | Does the 4-block model predict a complete key? | Define explicit 16-hex grouping, ordered pieces and ordering cue independently from known key/address | Validate 64-hex candidate against oracle; otherwise reject or mark unresolved |
| 7 | Is the 20.5s audio residual intentional? | Compare AAC packets and decoded PCM, sound editor / compression controls, synchronized visuals, spectral residual, positive and negative controls | Demonstrable non-encoder payload/message; else record as unexplained audio difference |

Do not run huge key-space searches on unconstrained unknown digits. Review previously negative families before spending compute. Use hypothesis/version identifiers and persist test results deterministically.
