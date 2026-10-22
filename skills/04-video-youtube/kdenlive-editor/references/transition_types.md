# Kdenlive Transition Reference Catalog

This reference details the transition classes and composition behaviors available in Kdenlive / MLT.

---

## 1. Primary Inline Transitions (Same Track)

### Cross-Dissolve (Mix)
* **Description:** Standard linear or smooth opacity blend between two overlapping clips on the same track.
* **Recommended Durations:**
  * Quick Cut / Pacing: 6–10 frames (~0.25s – 0.4s @ 25fps)
  * Standard Transition: 12–15 frames (~0.5s @ 25fps)
  * Narrative / Slow Fade: 25–50 frames (1.0s – 2.0s @ 25fps)
* **MCP Method:** `add_transitions_batch(track_index=0, duration=13)` or `add_transition`.

---

## 2. Luma Wipe Transitions (Multi-Track Composition)

Wipe transitions use a grayscale gradient map (Luma Matte) to reveal the lower or upper clip along defined geometric paths.

| Pattern Name | Description | Best Used For |
|--------------|-------------|---------------|
| `horizontal_wipe` | Sweeps left-to-right or right-to-left | Scene changes, location shifts |
| `vertical_wipe` | Sweeps top-to-bottom or bottom-to-top | Content reveals, infographic transitions |
| `radial_clock` | Sweeps in a 360-degree clock sweep | Time-lapse shifts, elapsed time narrative |
| `circle_iris` | Iris circle expanding or contracting | Focal point reveals, retro/vlog styling |
| `blinds` | Multiple horizontal or vertical slats opening | Modern editorial transition |
| `soft_blur_dissolve` | Defocused dissolve with high feathering | Dream sequences, retrospectives |

---

## 3. Audio Cross-Fades
* **Standard Audio Dissolve:** 8–15 frames.
* **Room Tone / Ambience Blend:** 25–40 frames to avoid sudden silence dips.
* **J-Cut / L-Cut:** Keep audio overlapping by 12–25 frames ahead of or following the video cut.
