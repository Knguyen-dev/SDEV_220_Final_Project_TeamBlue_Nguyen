import time
from urllib.request import urlopen  # only to stop the time

from PIL import Image, ImageTk, ImageDraw
import tkinter
import io

HAVE_PIC = "no"  # "yes" # or let create a pic if you have none

root = tkinter.Tk()


response = urlopen('https://www.apple.com/ac/structured-data/images/open_graph_logo.png')
data = response.read()
image = Image.open(io.BytesIO(data))

def masking_1(image):  # faster

    mask = image.copy()
    mask.putalpha(1)

    mask.paste(image, (0, 0), image)

    # img.paste(img,(0, 0), mask)

    image = mask.copy()
    return image


def masking_2(image):  # better quality

    datas = image.getdata()

    newData = []
    for item in datas:
        if item[3] == 0:
            newData.append((item[0], item[1], item[2], 1))
        else:
            newData.append(item)

    image.putdata(newData)

    return image


def image_draw():  # creates the test pic

    width = 300  # the bigger the slower
    height = 300
    colour = "green"  # "#519ae7"
    image = Image.new('RGBA', (width, height))
    imd = ImageDraw.Draw(image, 'RGBA')

    y = 0
    while y < height:
        x = y % 2
        while x < width:
            imd.point((x, y), colour)
            x += 2
        y += 1
    return image


if HAVE_PIC == "yes":
    img = Image.open(image)  # insert your problem pic
    img = img.convert("RGBA")  # make sure, it has alphachannel
else:
    img = image_draw()  # creates test pic


start = time.process_time()
print(time.process_time() - start, "after image.open")
img.show()  # to show that it is the same image
photo_image = ImageTk.PhotoImage(img, master=root)  # too slow
print(time.process_time() - start, "after PhotoImage")


start = time.process_time()
print(time.process_time() - start, "before masking_1")
pic = masking_1(img)
pic.show()
photo_image = ImageTk.PhotoImage(pic, master=root)
print(time.process_time() - start, "after masking_1")

start = time.process_time()
print(time.process_time() - start, "before masking_2")
pic = masking_2(img)
pic.show()
photo_image = ImageTk.PhotoImage(pic, master=root)
print(time.process_time() - start, "after masking_2")