from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from random import shuffle, randrange, choice
from forms import InTextForm, InImageForm
from werkzeug.utils import secure_filename
from os import path, listdir
from PIL import Image

app = Flask(__name__)
app.config.from_pyfile("config.py")
TEXT_FILENAME = "text.txt"
IMAGE_DIR = "static/images"
MAXLINES = 10
SUB_CHANCE = 20
SUBSTITUTIONS = {
        "l" : "1",
        "e" : "3",
        "o" : "0",
        "t" : "7",
        "a" : ["@", "4"],
        "s" : ["5", "$"],
        }
FONTS = [
        "Courier",
        "Helvetica",
        "Times",
        ]
FONT_WEIGHTS = [
        "normal",
        "bold",
        "bolder",
        ]

@app.route('/', methods=["POST", "GET"])
def main():
    text = []
    with open(TEXT_FILENAME) as f:
        text = f.read().splitlines()

    images = listdir(IMAGE_DIR)

    intextform = InTextForm()
    inimageform = InImageForm()

    ### submitting text ###
    if intextform.validate_on_submit():
        text.append(intextform.inputtext.data)
        if len(text) > MAXLINES:
            text = text[1:]
        
        with open(TEXT_FILENAME, "w") as f:
            for t in text:
                f.write(f"{t}\n")
        return redirect(url_for("main"))

    ### submitting images ###
    if inimageform.validate_on_submit():
        image = inimageform.inputimage.data
        filename = f"{randrange(10000000, 999999999)}.png"
        pil_image = Image.open(image) 
        green = get_green_image(pil_image)
        green.save(path.join(IMAGE_DIR, filename), "png")

        return redirect(url_for("main"))

    ### text substitutions ###
    for i, t in enumerate(text):
        for j, c in enumerate(t):
            if c.lower() in SUBSTITUTIONS.keys() and randrange(0, 100) <= SUB_CHANCE:
                subchar = None
                possible_chars = SUBSTITUTIONS[c.lower()]
                if isinstance(possible_chars, list):
                    subchar = choice(possible_chars)
                else:
                    subchar = possible_chars
                changed_t = t[:j] + subchar + t[j+1:]
                text[i] = changed_t

    
    ### building textitems ###
    shuffle(text)
    textitems = []
    for t in text:
        item = {}
        item["text"] = t
        item["color"] = get_random_green()
        item["font"] = choice(FONTS)
        item["font-weight"] = choice(FONT_WEIGHTS)
        item["size"] = f"{randrange(16, 60)}px"
        item["left"] = f"{randrange(0, 70)}%"
        textitems.append(item)

    ### building imageitems ###
    imageitems = []
    for imagename in images:
        item = {}
        imagepath = path.join(IMAGE_DIR, imagename)
        item["imagepath"] = imagepath
        realwidth, realheight = Image.open(imagepath).size
        width = randrange(80, 300)
        height = int( width * float(realheight) / realwidth )
        item["width"] = width
        item["height"] = height
        item["opacity"] = randrange(15, 50)
        item["left"] = randrange(0, 70)
        item["top"] = randrange(0, 50)
        imageitems.append(item)
    
    return render_template(
            "index.html",
            intextform=intextform,
            inimageform=inimageform,
            textitems=textitems,
            imageitems=imageitems,
            )

def get_random_green():
    rgb = [randrange(50, 150), randrange(180, 256), randrange(50, 150)]
    return "#%02x%02x%02x" % tuple(rgb)

def get_green_image(image):
    width, height = image.size

    new_image = create_image(width, height)
    new_pixels = new_image.load()

    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)
            new_pixels[i, j] = (0, pixel[1], 0)

    return new_image

def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height:
        return None
    return image.getpixel((i, j))

def create_image(width, height):
    return Image.new("RGB", (width, height), "white")
