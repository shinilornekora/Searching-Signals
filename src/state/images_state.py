images = []

def add_images(images_paths):
    for path in images_paths:
        images.append(path)

def clear_images():
    images.clear()


def get_images():
    return images.copy()