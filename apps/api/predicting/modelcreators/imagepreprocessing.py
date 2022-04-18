import os
from PIL import Image

path = 'C:/Users/Dominik/Desktop/niepsy'


def process():
    to_remove = []

    for subdir, dirs, files in os.walk(path):
        for file in files:
            base, extension = os.path.splitext(file)

            if str(extension) in ['.jpeg', '.JPEG']:
                continue

            file_path = os.path.join(subdir, file)

            if str(extension) in ['.webp', '.WEBP']:
                to_remove.append(file_path)
                continue

            try:
                image = Image.open(file_path)
                rgb_image = image.convert('RGB')
                rgb_image.save(os.path.join(subdir, base + ".jpeg"))
            except:
                to_remove.append(file_path)
                continue

            to_remove.append(file_path)

    for file in to_remove:
        os.remove(file)

    print('Removed ' + str(len(to_remove)) + ' files')

#process()
