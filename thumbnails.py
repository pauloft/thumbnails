""" create thumbnails of images in a given folder """
import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS

albumdir = "~/Pictures/album"
thumbdir = albumdir + "/thumbs"

def mkdir(dirname):
    """ Create a directory with name dirname IF it doesn't exist """
    try:
        os.mkdir(dirname)
    except Exception:
        pass


def maxSize(image, maxSize, method=3):
    imAspect = float(image.size[0])/float(image.size[1])
    outAspect = float(maxSize[0])/float(maxSize[1])
    if imAspect >= outAspect:
        return image.resize((maxSize[0], int((float(maxSize[0])/imAspect) + 0.5)), method)
    else:
        return image.resize((int((float(maxSize[1])*imAspect) + 0.5), maxSize[1]), method)


def processImage(imgdir, fname):
    img = Image.open(imgdir+fname)
    exif = img._getexif()
    if exif is not None:
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "Orientation":
                if value == 3:
                    img = img.rotate(180)
                if value == 6:
                    img.rotate(270)
                if value == 8:
                    img.rotate(90)
                break
    img = maxSize(img, (1024, 768), Image.ANTIALIAS)
    img.save(albumdir + "/" + fname, "JPEG", quality=100)
    img.thumbnail((192, 192), Image.ANTIALIAS)
    img.save(thumbdir + "/" + fname, "JPEG")


def main():
    if len(sys.argv) < 3:
        print("Usage: thumbnails.py <imgdir> <outdir>")
        exit(0)
    else:
        imgdir = sys.argv[1] + '/'
        albumdir = sys.arg[2] + '/'

    mkdir(albumdir)
    mkdir(thumbdir)
    files = os.listdir(imgdir)

    for fname in files:
        if fname.lower().endswith('.jpg'):
            processImage(imgdir, fname)

    print("I'm done!")

if __name__ == "__main__":
    main()