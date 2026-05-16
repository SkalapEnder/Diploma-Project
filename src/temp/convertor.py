from PIL import Image
import os

# ----------------------------
# SETTINGS
# ----------------------------
input_folder = "input_images"
output_folder = "output_images"
output_format = "bmp"   # change to: "tiff", "bmp", "jpg", etc.

# create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# supported input formats
valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp")

# ----------------------------
# CONVERSION LOOP
# ----------------------------
for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_extensions):
        input_path = os.path.join(input_folder, filename)

        # open image
        img = Image.open(input_path)

        # remove extension from name
        name_without_ext = os.path.splitext(filename)[0]

        output_path = os.path.join(
            output_folder,
            f"{name_without_ext}.{output_format}"
        )

        # convert and save
        img.save(output_path)

        print(f"Converted: {filename} → {output_path}")

print("Done!")