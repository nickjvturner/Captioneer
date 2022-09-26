#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, IptcImagePlugin, ExifTags
from datetime import datetime
from pathlib import Path
import imghdr
import time

# Check if 'desired' directory exists, if not, create it!


def dir_check_make(dir_path, dir_name):
    if not Path(dir_path).is_dir():
        dir_path.mkdir()
        print(f'Directory {dir_name} Created\n')
    else:
        print(f'Directory {dir_name} already exists\n')


def get_image_dimensions(pil_img):
    width, height = pil_img.size

    desired_margin = int((height / 10) + 10)
    desired_caption_font_size = int(desired_margin / 2)
    desired_date_font_size = int(desired_margin / 4)
    desired_date_y_value = int(desired_margin / 2.5)

    return desired_margin, desired_caption_font_size, desired_date_font_size, desired_date_y_value


# We can user getter function to get values from specific IIM codes
# https://iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
def get_caption(image):
    iptc = IptcImagePlugin.getiptcinfo(image)
    return iptc.get((2, 5)).decode()


def get_date(image):
    for DateTimeOriginal in ExifTags.TAGS.keys():
        if ExifTags.TAGS[DateTimeOriginal] == 'DateTimeOriginal':
            break

    exif = dict(image._getexif().items())
    date = str(exif[DateTimeOriginal])
    my_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    # Return date to be printed
    return f'{str(my_date.strftime("%B"))} {str(my_date.year)}'


def add_margin(image, top, right, bottom, left, color):
    width, height = image.size
    new_width = width + right + left
    new_height = height + top + bottom
    image_with_margin = Image.new(image.mode, (new_width, new_height), color)
    image_with_margin.paste(image, (left, top))
    return image_with_margin


def add_caption(image, caption, desired_caption_font_size, desired_margin):
    width, height = image.size
    font = ImageFont.truetype("Avenir.ttc", desired_caption_font_size)
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(caption, font=font)
    text_slim_count = 0
    if text_width > width:
        while text_width > (width - 300):
            text_slim_count += 1
            print('Text width too great for image, slimming', desired_caption_font_size)
            desired_caption_font_size -= 2
            font = ImageFont.truetype("Avenir.ttc", desired_caption_font_size)
            text_width, text_height = draw.textsize(caption, font=font)

        image_with_caption = draw.text(((width - text_width) / 2, height - (desired_margin - text_slim_count)), caption, (0, 0, 0), font=font)
    else:
        image_with_caption = draw.text(((width - text_width) / 2, height - desired_margin), caption, (0, 0, 0), font=font)
    return image_with_caption


def add_date(image, date, desired_date_y_value, desired_date_font_size):
    date = str(date)
    width, height = image.size
    font = ImageFont.truetype("Avenir.ttc", desired_date_font_size)
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(date, font=font)
    image_with_date = draw.text(((width - text_width) / 2, height - desired_date_y_value), date, (0, 0, 0), font=font)
    return image_with_date


def captioneer():
    # Configure variables
    output_dir_name = 'newly_stamped_images'
    output_dir = Path.cwd() / output_dir_name
    image_files = []
    sub_dirs = []
    process_iteration_counter = 1

    for sub_dir in Path.cwd().iterdir():
        if sub_dir.is_dir():
            # Skip over pre-existing newly_stamped_images folder
            if sub_dir.name == output_dir_name:
                pass
            else:
                sub_dirs.append(sub_dir)
                for filename in Path(sub_dir).iterdir():
                    if filename.is_dir():
                        continue
                    image_type = imghdr.what(filename)
                    if image_type == 'jpeg':
                        image_files.append(filename)

    total_images = len(image_files)
    print(f'''
    Subdirectories: {len(sub_dirs)}
       Image files: {total_images}
    ''')

    proceed_question = input(
        'Do you wish to stamp these images with Captions and dates? [Y]es/No ')

    # Moment to breath before execution, review the total number of files and directories
    if proceed_question.casefold() == 'no' or proceed_question.casefold() == 'n':
        exit()

    # Capture process start time
    process_start_time = time.time()

    # Create an output directory for the 'newly stamped images'
    dir_check_make(output_dir, output_dir_name)

    for sub_dir in sorted(sub_dirs):
        print(
            f'{"#" * ((len(str(sub_dir.name)))+38)}\n'
            f'Processing images from subdirectory "{sub_dir.name}"\n'
            f'{"#" * ((len(str(sub_dir.name)))+38)}\n')
        output_sub_dir = output_dir / sub_dir.name
        # print(outputSubDir)

        try:
            dir_check_make(output_sub_dir, sub_dir.name)
            sub_dir_image_files = []
        except Exception:
            print(f'subdirectory creation failed')

        try:
            for filename in Path(sub_dir).iterdir():
                image_type = imghdr.what(filename)
                # Optionally print identified file type for all files within subDir
                # print(imageType)
                if image_type == 'jpeg':
                    sub_dir_image_files.append(filename)

            for filename in sorted(sub_dir_image_files):
                try:
                    img = Image.open(filename)
                    print(f'{filename.name}\n{"-" * len(filename.name)}\n'
                          f'{process_iteration_counter} of {total_images}')
                    process_iteration_counter += 1
                except Exception as e:
                    print(e)
                    print(f'Open image {filename} failed')

                try:
                    caption = get_caption(img)
                    print(f'Caption: {caption}')
                except Exception:
                    caption = sub_dir.name
                    print(
                        f'{"+" * (int((len(str(caption)))/2)-2)} NO IPTC DATA {"+" * (int((len(str(caption)))/2)-2)}\n'
                        f'Using subdirectory name instead\n'
                        f'Caption: {sub_dir.name}\n'
                        f'{"+" * ((len(str(caption)))+10)}\n')

                try:
                    date = get_date(img)
                    print(f'Date: {date}')
                except Exception:
                    print(
                        f'------------------------------------------------------------\n'
                        f'-------------------- NO DATE AVAILABLE ---------------------\n'
                        f'------------------------------------------------------------\n')
                    manual_date = input(
                        f'Manual date entry required!\n'
                        f'Enter date as you wish text to appear on stamped photo\n'
                        f'"Month Year", "January 2021" or "November 1980" (for example)\n'
                        f'Please enter date: ')
                    date = str(manual_date)

                desired_margin, desired_caption_font_size, desired_date_font_size, desired_date_y_value = get_image_dimensions(img)

                try:
                    image_output = add_margin(img, 0, 0, desired_margin, 0, (255, 255, 255))
                    add_caption(image_output, caption, desired_caption_font_size, desired_margin)
                    add_date(image_output, date, desired_date_y_value, desired_date_font_size)
                except Exception as e:
                    print(
                        f'margin/caption/date failure\n'
                        f'{e}')

                try:
                    output_filename = f'{filename.stem}-stamped.jpg'
                    image_output.save(output_sub_dir / output_filename, quality=95)
                    print('\n')
                except Exception as e:
                    print(
                        f'Adding border and filename to image {filename} failed\n'
                        f'{e}')
        except Exception as e:
            print(e)
            pass

    process_complete_time = time.time()
    process_duration = process_complete_time - process_start_time

    print(f'''
    #############################
          PROCESS COMPLETE
    #############################

    +=+=+=+=+ Summary +=+=+=+=+
      Sub-directories: {len(sub_dirs)}
      Files processed: {total_images}
     Process duration: {int(process_duration)} seconds
    for an Average of: {round(process_duration / total_images, 2)} seconds per image
    ''')


if __name__ == '__main__':
    captioneer()
