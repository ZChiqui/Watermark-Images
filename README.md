# Watermarking GUI

Simple Tkinter application to add a watermark logo to images. Select an image, preview it, apply a watermark at the bottom-right corner, and save the result.

## Features

- Upload common image formats: PNG, JPG/JPEG, GIF
- Preview image in-app before and after watermarking
- Transparent watermark support with alpha compositing
- Save the watermarked image as PNG/JPG

## Requirements

- Python 3.8+
- Pillow (PIL fork)
- Tkinter (bundled with most Python installers on Windows/macOS)

Install Pillow:

```bash
pip install pillow
```

## Project Structure

```
.
├─ main.py                     # Tkinter GUI and watermarking logic
└─ images/
   ├─ watermark_transparent.png  # Preferred watermark asset (RGBA)
   └─ watermark.png              # Fallback watermark asset
```

If `images/watermark_transparent.png` is not present, the app falls back to `images/watermark.png`.

## Usage

1. Place your watermark image in `images/` as `watermark_transparent.png` (recommended) or `watermark.png`.
2. Run the app:

```bash
python main.py
```

3. Click "Upload Image" and choose an image file.
4. Click "Add Watermark" to overlay the logo at the bottom-right.
5. Click "Save Image" and choose a destination/filename.

Note: The preview resizes images to 800x600 for display. The saved image reflects the previewed size in the current implementation.

## Notes

- The watermark is composited using its alpha channel for smooth edges.
- You can adjust watermark size and position in `add_watermark()` within `main.py`.

