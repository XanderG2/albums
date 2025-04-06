from PIL import Image
import numpy as np
import math

with Image.open("albums4.png") as im:
    avgCols = {}
    print(im.size)
    for col3 in range(0, im.size[0]//300):
        avgCols[str(col3)] = {}
        col = col3*300
        for row3 in range(0, im.size[1]//300):
            row = row3*300
            box = (col, row, col+300, row+300)
            region = im.crop(box)
            np_img = np.array(region.convert("RGB"))
            avgCol = tuple(map(int, np_img.mean(axis=(0, 1))))
            brightness = math.sqrt(0.299*avgCol[0]**2 + 0.587*avgCol[1]**2 + 0.114*avgCol[2]**2)
            nimg = Image.new("RGB", (300, 300), avgCol)
            #im.paste(nimg, box)
            avgCols[str(col3)][str(row3)] = {"box": box, "avg": avgCol, "nimg": nimg, "region": region, "btns": brightness}
    #print(avgCols)
    #im.save("albums4a.png")
    reorderedList={}
    for col in avgCols.values():
        for row in col.values():
            brightness = row["btns"] * 10
            if brightness in reorderedList.keys():
                while True:
                    brightness += 1
                    if brightness in reorderedList.keys():
                        continue
                    break
            reorderedList[brightness] = row
    newimg = Image.new("RGB", im.size)
    simpimg = Image.new("RGB", im.size)
    i = 0
    s = sorted(reorderedList.keys())
    print(reorderedList[i] for i in s)
    for col3 in range(0, im.size[0]//300):
        col = col3*300
        for row3 in range(0, im.size[1]//300):
            row = row3*300
            try:
                nimg = reorderedList[s[i]]
                i += 1
                newimg.paste(nimg["region"], (col, row, col+300, row+300))
                simpimg.paste(Image.new("RGB", (300, 300), nimg["avg"]), (col, row, col+300, row+300))
            except IndexError:
                pass
    newimg.save("albums4a.png")
    simpimg.save("albums4s.png")
