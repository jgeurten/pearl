import os
from PIL import Image
import PIL

path = '/Users/jordangeurten/Documents/GitHub/pearl/raw_images/Teeth/IMG_8130.jpg'

img = Image.open(path)
# img_1 = img.rotate(5,resample=Image.BICUBIC,expand=True)

gauss_img = img.filter(PIL.Image.ImageFilter.BLUR)
gauss_img.show()
stop

# converted to have an alpha layer
im2 = img.convert('RGBA')
# rotated image
rot = im2.rotate(22.2, expand=0)
# a white image same size as rotated image
fff = Image.new('RGBA', rot.size, (200,)*4)
# create a composite image using the alpha layer of rot as a mask
out = Image.composite(rot, im2, rot)
out.show()
# save your work (converting back to mode='1' or whatever..)
out.convert(img.mode).save('test2.bmp')

print(im2.size[0]*4)


# img = Image.new('RGB', (100, 100), 'red')
a = 1
b = 0
c = 25 #left/right (i.e. 5/-5)
d = 0
e = 1
f = 0 #up/down (i.e. 5/-5)
fff = Image.new('RGBA', img.size, (200,)*4)
_img = im2.transform(img.size, Image.AFFINE, (a, b, c, d, e, f))
_out = Image.composite(_img, fff, _img)

_img.show()
_out.show()
