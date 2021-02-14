# Captioneer

Stamp your photos with captions and photo taken date, so that this information can be displayed when presented using a digital photo frame.

## Requirements

Python3
[Pillow](https://pillow.readthedocs.io)

#### Install Pillow

[Installation Instructions](https://pillow.readthedocs.io/en/stable/installation.html)

##### macOS
```python
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

## Usage

Captioneer expects the following folder structure:
```
+-- root folder
	+-- captioneer.py
	
	+-- folder 1
		+-- picture 1.jpg
		+-- picture 2.jpg
		+-- picture 3.jpg
	+-- folder 2
		+-- picture 1.jpg
		+-- picture 2.jpg
		+-- picture 3.jpg
	+-- folder 3
		+-- picture 1.jpg
		+-- picture 2.jpg
		+-- picture 3.jpg
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)