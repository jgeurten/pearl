from PIL import Image
import sys, os

angles = [-30, -20, -10, 10, 20, 30]
imgExtensions = {}

def defineImageExts():
    imgExtensions['jpeg'] = 0
    imgExtensions['jpg'] = 0
    imgExtensions['png'] = 0
    imgExtensions['tif'] = 0

def rotImage():
    #Rotate image x degrees defined in global angles
    return 0

def mirrorImage():
    #Mirror images about the center long and short axes
    return 0

if(len(sys.argv) < 2):
    print("Script command: python <script-path>/imgAugmenter.py <imageDir>")

else:
    imgDir = sys.argv[1]
    filenames = os.listdir(imgDir)
    imgFiles = []
    defineImageExts()
    for filename in filenames:
        if(filename[filename.find('.'):] in imgExtensions.keys()):
            #Acceptable file extension - else, some other filetype
            imgFiles.append(filename)

    print(filename[filename.find('.'):] in imgExtensions.keys())
