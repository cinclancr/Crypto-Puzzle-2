# Machine-Readable Evidence (2026-11-23 audit session)

All files were produced by the scripts in `scripts/` against the user-supplied
720p60 MP4s (SHA-256 pinned in `data/source_manifest.json`). JSON reports
embed **ASCII renderings of the derived pixel masks** so every glyph claim is
checkable without redistributing video-derived imagery; regenerate the PNG
renders locally with the same scripts if you have lawful access to the
videos.

| File | Produced by | Content |
| --- | --- | --- |
| `flash_audit_report.json` | `scripts/audit_puzzle1_flash.py` | Puzzle 1 flash mask bands, per-glyph same-font classification (top-3 IoU per cell), data-driven single-pass string; the adjudicated reading is in `docs/EVIDENCE_DOSSIER.md` A2 |
| `flash_glyph_classification_multifont.json` | multi-font synthetic template pass | per-cell IoU across 7 font families for the 43 flash cells |
| `flash_samefont_disputes.json` | same-font dispute resolution | the six disputed flash glyphs with anchor comparisons (3 vs 8, 5 vs 6, D vs 0, ...) |
| `part1_edge_report.json` | `scripts/decode_part1_edges.py` | the ten edge-fragment composites: pair frames, geometry, per-cell status and ASCII renderings; reading `6A6B0860B4` with documented per-cell confidence |
| `part2_column_report.json` | `scripts/decode_part2_column.py` | state-machine statistics (B = A∪C at 99.8%), A/B/C pixel counts, raster ASCII renderings and the six-window ASCII renderings; reading `723504` (model-dependent) |

Each JSON is self-contained (parameters, frame indexes, thresholds) so a
reviewer can rerun the script on their own copy of the video and diff the
outputs. The ASCII renderings use 3-6 px per character; they are lower
fidelity than the PNG renders but sufficient to verify every disputed glyph
claim recorded in the documentation.
