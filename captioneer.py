#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, IptcImagePlugin, ExifTags
from datetime import datetime
from pathlib import Path
import imghdr


# Check if 'desired' directory exists, if not, create it!
def dir_check_make(dir_path, dir_name):
	if not Path(dir_path).is_dir():
		dir_path.mkdir()
		print(f'Directory {dir_name} Created\n')
	else:
		print(f'Directory {dir_name} already exists\n')
	

# Create an output directory for the 'newly stamped images'
output_dir_name = 'newly_stamped_images'
output_dir = Path.cwd() / output_dir_name
dir_check_make(output_dir, output_dir_name)


# Get source image dimensions
def get_image_dimensions(pil_img):
	width, height = pil_img.size
	
	desired_margin = int((height/10)+10)
	desired_caption_font_size = int(desired_margin/2)
	desired_date_font_size = int(desired_margin/4)
	desired_date_y_value = int(desired_margin/2.5)
	
	return desired_margin, desired_caption_font_size, desired_date_font_size, desired_date_y_value
	

# We can user getter function to get values from specific IIM codes
# https://iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
def get_caption():
	return iptc.get((2,5)).decode()


def get_date(pil_img2):
	for DateTimeOriginal in ExifTags.TAGS.keys():
		if ExifTags.TAGS[DateTimeOriginal]=='DateTimeOriginal':
			break
		
	exif=dict(pil_img2._getexif().items())
	date = str(exif[DateTimeOriginal])
	my_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
	printed_date = f'{str(my_date.strftime("%B"))} {str(my_date.year)}'
	return printed_date


def add_margin(pil_img, top, right, bottom, left, color):
	width, height = pil_img.size
	new_width = width + right + left
	new_height = height + top + bottom
	result = Image.new(pil_img.mode, (new_width, new_height), color)
	result.paste(pil_img, (left, top))
	return result
	
		
def add_caption(pil_img2, caption, desired_caption_font_size, desired_margin):
	width, height = pil_img2.size
	font = ImageFont.truetype("Avenir.ttc", desired_caption_font_size)
	draw = ImageDraw.Draw(pil_img2)
	text_width, text_height = draw.textsize(caption, font=font)
	if text_width > width:
		while text_width > (width - 500):
			print('Text width too great for image, slimming', desired_caption_font_size)
			desired_caption_font_size -= 2
			font = ImageFont.truetype("Avenir.ttc", desired_caption_font_size)
			text_width, text_height = draw.textsize(caption, font=font)
		result = draw.text(((width-text_width)/2, height-desired_margin), caption, (0,0,0), font=font)
	else:
		result = draw.text(((width-text_width)/2, height-desired_margin), caption, (0,0,0), font=font)
	return result	
	
def add_date(pil_img2, date, desired_date_y_value, desired_date_font_size):
	date = str(date)
	width, height = pil_img2.size
	font = ImageFont.truetype("Avenir.ttc", desired_date_font_size)
	draw = ImageDraw.Draw(pil_img2)
	text_width, text_height = draw.textsize(date, font=font)
	result = draw.text(((width-text_width)/2, height-desired_date_y_value), date, (0,0,0), font=font)
	return result


for sub_dir in Path(Path.cwd()).iterdir():
	if sub_dir.is_dir():
#		Skip over pre-existing newly_stamped_images folder
		if sub_dir.name == output_dir_name:
			pass
		else:
			print(f'''
############################################################
Processing images from subdirectory "{sub_dir.name}"
############################################################
''')
			
			output_sub_dir = output_dir / sub_dir.name
#			print(outputSubDir)
			
			try:
				dir_check_make(output_sub_dir, sub_dir.name)
			except:
				print(f'subdirectory creation failed')
	
			try:
				for filename in Path(sub_dir).iterdir():
					image_type = imghdr.what(filename)
# 					Optionally print identified file type for all files within subDir
#					print(imageType)
					if image_type == 'jpeg':
						try:
							im = Image.open(filename)
						except:
							print(f'Open image {filename} failed')
		
						try:
							iptc = IptcImagePlugin.getiptcinfo(im)
							caption = get_caption()
							print(f'{filename.name} \nCaption: {caption}')
						except:
							caption = sub_dir.name
							print(f'{filename.name}')
							print(f'''+++++++++++++ NO IPTC DATA +++++++++++++
I will use the subdirectory instead
Caption: {sub_dir.name}
++++++++++++++++++++++++++++++++++++++++''')

						try:
							date = get_date(im)
							print(f'Date: {date}')
						except Exception as e:
							print(f'''
----------------------------------------
---------- NO DATE AVAILABLE -----------
----------------------------------------''')
#							print('get_date error: ', e)
							manual_date = input('''
Manual date entry required!
Enter date as you wish text to appear on stamped photo
"Month Year", "January 2021" or "November 1980" (for example)
Please enter date: ''')
							date = str(manual_date)
						desired_margin, desired_caption_font_size, desired_date_font_size, desired_date_y_value = get_image_dimensions(im)
						
						try:
							img_new = add_margin(im, 0, 0, desired_margin, 0, (255,255,255))
							add_caption(img_new, caption, desired_caption_font_size, desired_margin)
							add_date(img_new, date, desired_date_y_value, desired_date_font_size)
						except Exception as e:
							print(f'margin/caption/date failure')
							print(e)
		
						try:
							output_filename = f'{filename.stem}-stamped.jpg'
							img_new.save(output_sub_dir / output_filename, quality=95)
							print('\n')
						except Exception as e:
							print(e)
							print(f'Adding border and filename to image {filename} failed')
			except:
				pass

print(f'''
####################
  PROCESS COMPLETE
####################
''')