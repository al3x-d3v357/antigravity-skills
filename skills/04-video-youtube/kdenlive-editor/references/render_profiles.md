# Kdenlive Render & Export Profiles

Target specifications, recommended bitrates, and encoder configurations for video rendering.

---

## 1. Web & Social Media Targets

### YouTube / Standard Web (1080p 60fps)
* **Resolution:** 1920 × 1080
* **Aspect Ratio:** 16:9
* **Frame Rate:** 60.0 fps (or 30.0 fps)
* **Video Codec:** H.264 (`libx264`) or H.265 / HEVC (`libx265`)
* **Bitrate:** 12,000–16,000 kbps (VBR 2-pass or CRF 18–20)
* **Audio Codec:** AAC-LC @ 320 kbps, 48 kHz stereo

### YouTube Shorts / TikTok / Reels (Vertical 9:16)
* **Resolution:** 1080 × 1920
* **Aspect Ratio:** 9:16
* **Frame Rate:** 60.0 fps
* **Video Codec:** H.264
* **Bitrate:** 14,000–18,000 kbps (CRF 19)
* **Audio Codec:** AAC @ 320 kbps, 48 kHz

### Ultra HD / 4K Master
* **Resolution:** 3840 × 2160
* **Aspect Ratio:** 16:9
* **Frame Rate:** 60.0 fps
* **Video Codec:** H.265 / HEVC or Apple ProRes 422 HQ
* **Bitrate:** 45,000–60,000 kbps

---

## 2. Hardware Encoders for Windows (Ryzen / Radeon Vega)

* **AMD AMF (Advanced Media Framework):**
  * Profile: `h264_amf` / `hevc_amf`
  * Hardware accelerated on Ryzen 2400G Vega 11.
  * Extremely fast export speeds with low CPU overhead.
* **Software Fallback:**
  * `libx264` preset `medium` or `fast`, `crf=19`.
