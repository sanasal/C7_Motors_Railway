from PIL import Image
import os

input_folder = "media"
output_folder = "media_resized"
os.makedirs(output_folder, exist_ok=True)

normal_width = 340
retina_width = normal_width * 2

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Retina size
        w_percent_2x = retina_width / float(img.width)
        h_size_2x = int(img.height * w_percent_2x)
        img_retina = img.resize((retina_width, h_size_2x), Image.LANCZOS)
        output_retina = os.path.join(output_folder, os.path.splitext(filename)[0] + "-680.webp")
        img_retina.save(output_retina, "WEBP", quality=100, method=6 , lossless=True)

print("All images resized and converted to high-quality WebP!")
