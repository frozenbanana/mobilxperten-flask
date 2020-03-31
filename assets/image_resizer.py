import glob
from PIL import Image

from resizeimage import resizeimage


images = glob.glob("deviceImages/*")

for img in images:
	print(img)
	with open(img, 'r+b') as f:
		with Image.open(f) as image:
			imgf = resizeimage.resize_cover(image, [350, 350])
			imgf = resizeimage.resize_crop(imgf,[320,320])
			output_path = 'cropped/'+img[img.find('/')+1:]
			imgf.save(output_path, image.format)
