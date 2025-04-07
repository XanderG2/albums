from PIL import Image
import numpy as np
import math
import colorsys

imagepath = ("albums/albums4", ".png")
sizeofeachimage = 300

def luminance(im, avgCols):
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
    for col3 in range(0, im.size[0]//sizeofeachimage):
        col = col3*sizeofeachimage
        for row3 in range(0, im.size[1]//sizeofeachimage):
            row = row3*sizeofeachimage
            try:
                nimg = reorderedList[s[i]]
                i += 1
                newimg.paste(nimg["region"], (col, row, col+sizeofeachimage, row+sizeofeachimage))
                simpimg.paste(Image.new("RGB", (sizeofeachimage, sizeofeachimage), nimg["avg"]), (col, row, col+sizeofeachimage, row+sizeofeachimage))
            except IndexError:
                print("index error")
    newimg.save(imagepath[0]+"a"+imagepath[1])
    simpimg.save(imagepath[0]+"s"+imagepath[1])

def hsl(im, avgCols):
    reformattedList = {}
    for col in avgCols.values():
        for row in col.values():
            avg = row["avg"]
            avghls = colorsys.rgb_to_hls(avg[0]/255, avg[1]/255, avg[2]/255)
            avghl = (avghls[0], avghls[1])
            if avghl[1] not in reformattedList.keys():
                reformattedList[avghl[1]] = {}
            reformattedList[avghl[1]] = {"box": row["box"], "avg": avghl, "avgrgb": avg,"nimg": row["nimg"], "region": row["region"]}
    newimg = Image.new("RGB", im.size)
    simpimg = Image.new("RGB", im.size)
    i = 0
    s = sorted(reformattedList.keys())
    orderedlist = [reformattedList[x] for x in s]
    cols = im.size[0] // sizeofeachimage 
    groupsOfCol = [[] for _ in range(cols)]
    chunk_size = len(orderedlist) // cols
    for i in range(cols):
        start = i * chunk_size
        end = start + chunk_size+1
        groupsOfCol[i] = orderedlist[start:end]
    for coli in range(len(groupsOfCol)):
        col = groupsOfCol[coli]
        hues = {x["avg"]: x for x in col}
        huesorted = list(hues.values())
        groupsOfCol[coli] = huesorted
    for col3 in range(0, im.size[0]//sizeofeachimage):
        col = col3*sizeofeachimage
        for row3 in range(0, im.size[1]//sizeofeachimage):
            row = row3*sizeofeachimage
            nimg = groupsOfCol[col3][row3]
            newimg.paste(nimg["region"], (col, row, col+sizeofeachimage, row+sizeofeachimage))
            simpimg.paste(Image.new("RGB", (sizeofeachimage, sizeofeachimage), nimg["avgrgb"]), (col, row, col+sizeofeachimage, row+sizeofeachimage))
    newimg.save(imagepath[0]+"a2"+imagepath[1])
    simpimg.save(imagepath[0]+"s2"+imagepath[1])

with Image.open("".join(imagepath)) as im:
    avgCols = {}
    for col3 in range(0, im.size[0]//sizeofeachimage):
        avgCols[str(col3)] = {}
        col = col3*sizeofeachimage
        for row3 in range(0, im.size[1]//sizeofeachimage):
            row = row3*sizeofeachimage
            box = (col, row, col+sizeofeachimage, row+sizeofeachimage)
            region = im.crop(box)
            np_img = np.array(region.convert("RGB"))
            avgCol = tuple(map(int, np_img.mean(axis=(0, 1))))
            brightness = math.sqrt(0.299*avgCol[0]**2 + 0.587*avgCol[1]**2 + 0.114*avgCol[2]**2)
            nimg = Image.new("RGB", (sizeofeachimage, sizeofeachimage), avgCol)
            avgCols[str(col3)][str(row3)] = {"box": box, "avg": avgCol, "nimg": nimg, "region": region, "btns": brightness}
    luminance(im, avgCols)
    hsl(im, avgCols)

