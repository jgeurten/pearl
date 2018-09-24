import progressbar, sys, os, PIL, random
from PIL import Image

angles = [-30, -20, -10, 10, 20, 30, 180]
imgExtensions = {}

SCALE_ON = 1
ROTATE_ON = 1
CROP_ON = 1
TRANSLATE_ON = 1


def defineImageExts():
    imgExtensions['jpeg'] = 0
    imgExtensions['jpg'] = 0
    imgExtensions['png'] = 0
    imgExtensions['tif'] = 0

def createTargetDir(imgDir):
    #Branch off of dir
    for el in range(len(imgDir)-2, -1, -1):
        if(imgDir[el] == '/'):
            targetPath = imgDir[:el+1] + 'augmentedImgs/'
            if not(os.path.isdir(targetPath)):
                os.mkdir(targetPath)
            return targetPath

def rotateImage(filePath, targetPath):
    #Rotate image x degrees defined in global angles
    a, fileNameExt = os.path.split(filePath)
    fileName, fileExt = os.path.splitext(fileNameExt)
    image = Image.open(filePath)

    for i, angle in enumerate(angles):
        # im_rot = image.rotate(angle)

        im2 = image.convert('RGBA')
        rot = im2.rotate(angle, expand=0)

        # a grey image same size as rotated image - if fill background with solid color
        fff = Image.new('RGBA', rot.size, (200,)*4)

        # create a composite image using the alpha layer of rot as a mask
        im_rot = Image.composite(rot, im2, rot)

        im_rot.convert(image.mode).save(targetPath + fileName + '_1_' + str(i+1) + fileExt)
        mirrorImage(targetPath + fileName + '_1_' + str(i+1), fileExt, im_rot.convert(image.mode))
        im_rot.close()
    image.save(targetPath + fileNameExt)
    image.close()
    return i+1

def mirrorImage(filePath, fileExt, img_handle):
    #Mirror images about the center short axis
    im_mirror = img_handle.transpose(PIL.Image.FLIP_LEFT_RIGHT)
    im_mirror.save(filePath + '_1' + fileExt)
    im_mirror.close()

def flipImage(filePath, fileExt, img_handle):
    #Mirror images about the long axiss
    im_mirror = img_handle.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    im_mirror.save(filePath + '_2' + fileExt)
    im_mirror.close()

def scaleImage(filePath, targetPath):
    #Scale the image by a random factor [0.8, 1.2]
    a, fileNameExt = os.path.split(filePath)
    fileName, fileExt = os.path.splitext(fileNameExt)
    image = Image.open(filePath)

    factor = random.randint(8,12)
    size = (int(round(image.size[0]*factor/10)), int(round(image.size[1]*factor/10)))
    im_resize = image.resize(size, resample=PIL.Image.BICUBIC)
    im_resize.save(targetPath + fileName + '_2_'  + fileExt)
    mirrorImage(targetPath + fileName + '_2_' + str(i+1), fileExt, im_resize)
    flipImage(targetPath + fileName + '_2_' + str(i+1), fileExt, im_resize)
    im_resize.close()

def cropImage(filePath, targetPath):
    #Crop the image in 4 random locations. Mirror each one
    a, fileNameExt = os.path.split(filePath)
    fileName, fileExt = os.path.splitext(fileNameExt)
    image = Image.open(filePath)
    im_size = image.size

    for i in range(0,4):
        startX = random.randint(0,im_size[0]/2)
        startY = random.randint(0, im_size[1]/2)
        endX = int(startX + im_size[0]/2 - 1)
        endY = int(startY + im_size[1]/2 - 1)
        box = (startX, startY, endX, endY)
        crop_im = image.crop(box)
        crop_im.save(targetPath + fileName + '_3_' + str(i+1) + fileExt)
        mirrorImage(targetPath + fileName + '_3_' + str(i+1), fileExt, crop_im)
        flipImage(targetPath + fileName + '_3_' + str(i+1), fileExt, crop_im)
        crop_im.close()

def translateImage(filePath, targetPath):
    a, fileNameExt = os.path.split(filePath)
    fileName, fileExt = os.path.splitext(fileNameExt)
    image = Image.open(filePath)
    im_rgba = image.convert('RGBA')
    im_size = image.size

    for i in range(0,4):
        a = 1
        b = 0
        c = random.randint(-1*round(im_size[0]*0.2),round(im_size[0]*0.2)) #left/right (i.e. 5/-5)
        d = 0
        e = 1
        f = random.randint(-1*round(im_size[1]*0.2),round(im_size[1]*0.2)) #up/down (i.e. 5/-5)

        background = Image.new('RGBA', image.size, (200,)*4)
        trans_img = im_rgba.transform(image.size, Image.AFFINE, (a, b, c, d, e, f))
        img_out = Image.composite(trans_img, background, trans_img)
        img_out.convert(image.mode).save(targetPath + fileName + '_4_' + str(i+1) + fileExt)
        mirrorImage(targetPath + fileName + '_4_' + str(i+1), fileExt, img_out.convert(image.mode))
        flipImage(targetPath + fileName + '_4_' + str(i+1), fileExt, img_out.convert(image.mode))
        img_out.close()

    image.close()

def addGaussNoise():
    #TODO: finish me
    return 0

if(len(sys.argv) < 2):
    print("Script command: python <script-path>/imgAugmenter.py <imageDir>")

else:
    imgDir = sys.argv[1]
    filenames = os.listdir(imgDir)
    imgFiles = []
    defineImageExts()
    targetPath = createTargetDir(imgDir)

    for filename in filenames:
        if(filename[filename.find('.')+1:] in imgExtensions.keys()):
            #Acceptable file extension - else, some other filetype
            imgFiles.append(filename)

    nOperations = len(imgFiles)*len(angles)*2 + len(imgFiles)*SCALE_ON*3 + \
    + len(imgFiles)*CROP_ON*4*3 + len(imgFiles)*TRANSLATE_ON*4*3

    if(len(imgFiles) > 100):
        print('Augmenting ' + str(len(imgFiles)) + ' to ' + str(nOperations) + ' Images. This will take a few minutes.' + '\n')
    else:
        print('Augmenting ' + str(len(imgFiles)) + ' to ' + str(nOperations) +  ' Images.' + '\n')

    bar = progressbar.ProgressBar(maxval=nOperations, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

    bar.start()
    for i, imgFile in enumerate(imgFiles):

        if(ROTATE_ON):
            rotateImage(imgDir + '/' + imgFile, targetPath)
        if(SCALE_ON):
            scaleImage(imgDir + '/' + imgFile, targetPath)
        if(CROP_ON):
            cropImage(imgDir + '/' + imgFile, targetPath)
        if(TRANSLATE_ON):
            translateImage(imgDir + '/' + imgFile, targetPath)
        bar.update(i*nOperations/len(imgFiles))

    bar.finish()
    print("Saved Augmented Images at " + targetPath + '\n')
