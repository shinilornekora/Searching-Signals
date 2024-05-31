from pdf2image import convert_from_path
import os
import hashlib
import asyncio

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def generate_unique_name(data):
    hash_obj = hashlib.md5(data.encode())
    return hash_obj.hexdigest()




def convert2Png(pdf_path, output_path, slice_width=1200, slice_height=600):
    images = convert_from_path(pdf_path, dpi=300, strict=True, thread_count=3)
    for image in images:
        image.save("original.png")
    
    image_paths = []
    for i, image in enumerate(images):
        num_slices_horizontal = image.width // slice_width
        num_slices_vertical = image.height // slice_height

        # Slice the image
        for y in range(num_slices_vertical):
            for x in range(num_slices_horizontal):
                left = x * slice_width
                upper = y * slice_height
                right = left + slice_width
                lower = upper + slice_height
                slice_img = image.crop((left, upper, right, lower))

                out = os.path.join(output_path, f"{generate_unique_name(str(i))}_{y}-{x}.png")
                slice_img.save(out)
                image_paths.append(out)
    
    return image_paths, num_slices_horizontal, num_slices_vertical