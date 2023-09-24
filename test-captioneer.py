#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, IptcImagePlugin, ExifTags
from datetime import datetime
from pathlib import Path
import imghdr
import time

# We can user getter function to get values from specific IIM codes
# https://iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
def get_caption(image):
    iptc = IptcImagePlugin.getiptcinfo(image)
    return iptc.get((2, 5)).decode()


def get_date(image):
    iptc = IptcImagePlugin.getiptcinfo(image)
    print(iptc)
    date = iptc.get((2, 55)).decode()
    # date = iptc.get((2, 55), None)
    print(date)
    my_date = datetime.strptime(date, "%Y-%m-%d")
    # Return date to be printed
    return f'{str(my_date.strftime("%B"))} {str(my_date.year)}'


def test_captioneer():
    # Configure variables
    image_files = []
    sub_dirs = []
    process_iteration_counter = 1

    for sub_dir in Path.cwd().iterdir():
        if sub_dir.is_dir():
            # print(sub_dir)
            sub_dirs.append(sub_dir)
            for filename in Path(sub_dir).iterdir():
                if filename.is_dir():
                    # print(filename)
                    continue
                image_type = imghdr.what(filename)
                if image_type == 'jpeg' or image_type == 'tiff':
                    print(filename)
                    image_files.append(filename)

                    img = Image.open(filename)

                    caption = get_caption(img)
                    print(f'Caption: {caption}')

                    date = get_date(img)
                    print(f'Date: {date}')

if __name__ == '__main__':
    test_captioneer()
