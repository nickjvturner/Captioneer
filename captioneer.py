#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, IptcImagePlugin, ExifTags
from datetime import datetime
from pathlib import Path
import imghdr

# Create a new directory to house the newly stamped images
outputDirName = 'newly_stamped_images'
outputDir = Path.cwd() / outputDirName
if not Path(outputDir).is_dir():
	outputDir.mkdir()
	print(f'Directory {outputDirName} Created\n')
else:
	print(f'Directory {outputDirName} already exists\n')


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

sourcedir = Path.cwd()

for subDir in Path(sourcedir).iterdir():
	if subDir.is_dir():
		# Skip over pre-existing newly_stamped_images folder
		if subDir.name == outputDirName:
			pass
		else:
			print(f'''
############################################################
Processing images from subdirectory "{subDir.name}"
############################################################
''')
			outputSubDir = outputDir / subDir.name
	#		print(outputSubDir)
			
			try:
				if Path(outputSubDir).exists():
					print(f'Output subdirectory {outputSubDir} already exists\n')
				else:
					Path(outputSubDir).mkdir()
					print(f'Output subdirectory {outputSubDir} Created\n')
			except:
				print(f'subdirectory creation failed')
	
			try:
				for filename in Path(subDir).iterdir():
					imageType = imghdr.what(filename)
#					print(imageType)                      # prints identified file type for all files within subDir
					if imageType == 'jpeg':
#						print(imageType)                  # prints identified file type for all jpegs
						try:
							im = Image.open(filename)
						except:
							print(f'Open image {filename} failed')
		
						try:
							iptc = IptcImagePlugin.getiptcinfo(im)
							caption = get_caption()
							print(f'{filename.name} \nCaption: {caption}')
						except:
							caption = subDir.name
							print(f'{filename.name}')
							print(f'''
++++++++++++++++++++++++++++++++++++++++
This image has no iptc info, using subdirectory name as caption
Caption: {subDir.name}
++++++++++++++++++++++++++++++++++++++++
''')

		
						try:
							date = get_date(im)
							print(f'Date: {date}')
						except Exception as e:
							print(f'This image has no Date')
							print(e)
							date = ''
		
						try:
							img_new = add_margin(im, 0, 0, 200, 0, (255,255,255))
							add_caption(img_new, caption)
							add_date(img_new, date)
						except Exception as e:
							print(f'margin/caption/date failure')
							print(e)
		
						try:
							outputFilename = filename.stem + '-stamped.jpg'
							img_new.save(outputSubDir / outputFilename, quality=95)
							print(f'\n')
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