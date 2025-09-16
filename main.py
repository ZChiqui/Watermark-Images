"""
Simple GUI app to add a watermark logo to images.

Main flow:
- Upload an image (PNG/JPG/JPEG/GIF) via file dialog.
- Preview is displayed and buttons are enabled.
- Add a watermark (bottom-right corner).
- Save the resulting watermarked image.

Assets:
- Expects a watermark image at `images/watermark_transparent.png`.
- Falls back to `images/watermark.png` if the transparent version is missing.
"""

from tkinter import Tk, Label, filedialog
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os

# Global state for the selected image path and the PIL image instance
path = ""
img = None

# Build the main Tkinter window
window = Tk()
window.title("Water Marking")
window.config(bg="#FFFFFF")

# Title label
my_label = Label(window, text="Welcome to the watermarking program", font=("Arial", 24, "bold"))
my_label.config(bg="#FFFFFF")
my_label.grid(row=0, column=0)

# Label to preview the selected/processed image
image_label = Label(window, bg="#FFFFFF")
image_label.grid(row=1, column=0)

def show_image(image):
    """Render a PIL image into the Tkinter preview label."""
    tk_img = ImageTk.PhotoImage(image)
    image_label.config(image=tk_img)
    image_label.image = tk_img

def save_image():
    """Prompt for a destination and save the current image."""
    global img
    if img:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if filepath:
            img.save(filepath)

def button_clicked():
    """Open a file dialog, load and preview the chosen image."""
    global path, img
    filepath = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")]
    )
    if filepath:
        path = filepath
        try:
            # Load image and normalize to RGBA to support alpha compositing
            img = Image.open(path).convert("RGBA")
            # Resize for a consistent preview size (does not persist original dimensions)
            orig_w, orig_h = img.size
            new_w = int(800 * 0.7)
            new_h = int(orig_h * (new_w / orig_w))
            img = img.resize((new_w, new_h), Image.LANCZOS)
            print(img.size)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image:\n{e}")
            img = None
            return

        show_image(img)
        image_name_label.config(text=f"{os.path.basename(path)}")
        watermark_button.state(['!disabled'])
        save_button.state(['!disabled'])

def add_watermark():
    """Overlay the watermark image on the bottom-right corner of the current image."""
    global img
    if img is None:
        return

    # Prefer a transparent watermark if available
    wm_path = "images/watermark_transparent.png"
    if not os.path.exists(wm_path):
        wm_path = "images/watermark.png"

    # Load and scale watermark logo
    logo = Image.open(wm_path).convert("RGBA")
    logo = logo.resize((100, 100))

    # Bottom-right position with a small margin
    x = img.width - logo.width - 10
    y = img.height - logo.height - 10

    # Composite watermark using its alpha channel as mask
    r, g, b, alpha = logo.split()
    alpha = alpha.point(lambda p: p * 0.3)
    img.paste(logo, (x, y), mask=alpha)

    show_image(img)

# Label to show the currently selected image file name
image_name_label = Label(window, text="No image selected", bg="#FFFFFF")
image_name_label.grid(row=2, column=0)

# ttk styling (best-effort theme selection)
style = ttk.Style()
try:
    style.theme_use('vista')
except Exception:
    pass
style.configure('TButton', padding=(12, 6), font=("Segoe UI", 10))

# Buttons container
buttons_frame = ttk.Frame(window)
buttons_frame.grid(row=3, column=0, pady=16)

upload_button = ttk.Button(buttons_frame, text="Upload Image", command=button_clicked)
upload_button.grid(row=0, column=0, padx=6)

watermark_button = ttk.Button(buttons_frame, text="Add Watermark", command=add_watermark, state='disabled')
watermark_button.grid(row=0, column=1, padx=6)

save_button = ttk.Button(buttons_frame, text="Save Image", command=save_image, state='disabled')
save_button.grid(row=0, column=2, padx=6)

window.mainloop()
