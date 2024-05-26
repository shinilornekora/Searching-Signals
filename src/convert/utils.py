from pdf2image import convert_from_path
import os
import hashlib

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def generate_unique_name(data):
    hash_obj = hashlib.md5(data.encode())
    return hash_obj.hexdigest()

def convert2Png(pdf_path, output_path):
    images = convert_from_path(pdf_path)

    image_paths = []
    for i, image in enumerate(images):
        output_path = os.path.join(output_path, f"{generate_unique_name(str(i))}.png")
        image.save(output_path, "PNG")
        image_paths.append(output_path)

    return image_paths
