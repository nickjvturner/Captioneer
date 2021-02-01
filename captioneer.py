#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, IptcImagePlugin, ExifTags
import os
from datetime import datetime
from pathlib import Path
import imghdr

# This script expects the following folder structure:
# +-- root folder
#     +-- this script.py
#     +-- folder 1
#         +-- picture 1.jpg
#         +-- picture 2.jpg
#         +-- picture 3.jpg
#     +-- folder 2
#         +-- picture 1.jpg
#         +-- picture 2.jpg
#         +-- picture 3.jpg
#     +-- folder 3
#         +-- picture 1.jpg
#         +-- picture 2.jpg
#         +-- picture 3.jpg


working_directory = Path.cwd()

# Create a new directory to house the newly stamped images
dirName = 'newly_stamped_images'
if not os.path.exists(dirName):
	os.mkdir(dirName)
	print('Directory', dirName, 'Created' + '\n')
else:
	print('Directory', dirName, 'already exists' + '\n')

sourcedir = working_directory
outputdir = Path.cwd() / dirName


# We can user getter function to get values from specific IIM codes
# https://iptc.org/std/photometadata/specification/IPTC-PhotoMetadata
def get_caption():
	return iptc.get((2,5)).decode()

def add_margin(pil_img, top, right, bottom, left, color):
	width, height = pil_img.size
	new_width = width + right + left
	new_height = height + top + bottom
	result = Image.new(pil_img.mode, (new_width, new_height), color)
	result.paste(pil_img, (left, top))
	return result
	
		
def add_caption(pil_img2, caption):
	width, height = pil_img2.size
	font = ImageFont.truetype("Avenir.ttc", 100)
	draw = ImageDraw.Draw(pil_img2)
	text_width, text_height = draw.textsize(caption, font=font)
	if text_width > width:
		font = ImageFont.truetype("Avenir.ttc", 100)
		text_width, text_height = draw.textsize(caption, font=font)
		result = draw.text((50, height-200), caption, (0,0,0), font=font)
	else:
		result = draw.text(((width-text_width)/2, height-200), caption, (0,0,0), font=font)
	return result

def get_date(pil_img2):
	for DateTimeOriginal in ExifTags.TAGS.keys():
		if ExifTags.TAGS[DateTimeOriginal]=='DateTimeOriginal':
			break
			
	exif=dict(pil_img2._getexif().items())
	date = str(exif[DateTimeOriginal])
	my_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
	printed_date = str(my_date.strftime('%B')) + ' ' + str(my_date.year)
	return printed_date
	
def add_date(pil_img2, date):
	date = str(date)
	width, height = pil_img2.size
	font = ImageFont.truetype("Avenir.ttc", 50)
	draw = ImageDraw.Draw(pil_img2)
	text_width, text_height = draw.textsize(date, font=font)
	result = draw.text(((width-text_width)/2, height-80), date, (0,0,0), font=font)
	return result

for subDir in Path(sourcedir).iterdir():
	if subDir.is_dir():
		if subDir.name == dirName:
			pass
		else:
			print(f'''############################################################
Processing images from subdirectory "{subDir.name}"
############################################################
''')
			outputSubDir = outputdir / subDir.name
	#		print(outputSubDir)
			
			try:
				if Path(outputSubDir).exists():
					print('Output subdirectory', outputSubDir, 'already exists' + '\n')
				else:
					Path(outputSubDir).mkdir()
					print('Output subdirectory', outputSubDir, 'Created' + '\n')
			except:
				print('subdirectory creation failed')
	
			try:
				for filename in Path(subDir).iterdir():
					imageType = imghdr.what(filename)
	#				print(imageType)                     # prints identified file type for all files within subDir
					if imageType == 'jpeg':
	#					print(imageType)                  prints identified file type for all jpegs
						try:
							im = Image.open(filename)
						except:
							print('Open image', filename, 'failed')
		
						try:
							iptc = IptcImagePlugin.getiptcinfo(im)
							caption = get_caption()
							print(f'{filename.name} \nCaption: {caption}')
						except:
							caption = subDir.name
							print(f'{filename.name}')
							print(f'''++++++++++++++++++++++++++++++++++++++++
This image has no iptc info, using subdirectory name as caption
Caption: {subDir.name}
++++++++++++++++++++++++++++++++++++++++''')

		
						try:
							date = get_date(im)
							print(f'Date: {date}')
						except:
							print("This image has no Date")
							date = ''
		
						try:
							img_new = add_margin(im, 0, 0, 200, 0, (255,255,255))
							add_caption(img_new, caption)
							add_date(img_new, date)
						except:
							print('margin/caption/date failure')
		
						try:
							outputFilename = filename.stem + '-stamped.jpg'
							img_new.save(outputSubDir / outputFilename, quality=95)
							print('\n')
						except Exception as e:
							print(e)
							print('Adding border and filename to image', filename, 'failed')
			except:
				pass

print(f'''####################
  PROCESS COMPLETE
####################
''')