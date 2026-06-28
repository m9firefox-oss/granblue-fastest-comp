from PIL import Image
import glob, os

for file in glob.glob("*.webp"):
    img = Image.open(file).convert("RGB")
    png_file = file.replace(".webp", ".png")
    img.save(png_file, "PNG")
    print(f"Converted: {file} -> {png_file}")
