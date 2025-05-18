from reportlab.lib.pagesizes import portrait, A4
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import re
from glob import glob

# Sort images by extracted time
def extract_time(filename):
    match = re.search(r"npr_(\d\.\d+e[+-]?\d+)\.png", filename)
    return float(match.group(1)) if match else float('inf')

image_files = sorted(glob("npr_*.png"), key=extract_time)

# Create a canvas
output_pdf = "npr_summary_high_quality.pdf"
c = canvas.Canvas(output_pdf, pagesize=portrait(A4))
width, height = portrait(A4)

# Layout settings
margin = 40
usable_height = height - 2 * margin
slot_height = usable_height / 3

for i in range(0, len(image_files), 3):
    for j in range(3):
        if i + j < len(image_files):
            img_path = image_files[i + j]
            img = ImageReader(img_path)
            img_width, img_height = img.getSize()
            aspect = img_height / img_width

            # Target width & height (fit within A4 width)
            target_width = width - 2 * margin
            target_height = target_width * aspect

            # Restrict height to slot if needed
            if target_height > slot_height:
                target_height = slot_height
                target_width = target_height / aspect

            # Compute position
            x = (width - target_width) / 2
            y = height - margin - (j + 1) * slot_height + (slot_height - target_height) / 2

            # Draw image
            c.drawImage(img, x, y, width=target_width, height=target_height, preserveAspectRatio=True)

    c.showPage()

c.save()
print(f"✅ Saved high-quality PDF: {output_pdf}")

