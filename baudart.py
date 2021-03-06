def baudot_art(filepath,newsize):
    import PIL.Image
    image=None
    def closest(myList, myNumber):
        from bisect import bisect_left
        pos = bisect_left(myList, myNumber)
        if pos == 0:
            return myList[0]
        if pos == len(myList):
            return myList[-1]
        before = myList[pos - 1]
        after = myList[pos]
        if after - myNumber < myNumber - before:
            return after
        else:
            return before
    def resize(image, new_width=300):
        width, height = image.size
        new_height = int((new_width * height / width)/2.5)
        return image.resize((int(round(new_width)), int(round(new_height))))
    def to_greyscale(image):
        return image.convert("L")
    def pixel_to_ascii(image):
        pixels = image.getdata()
        a=list('$8&#OAHKBDPQWM0ZCVUNXRJFT/()1-I!LI;:,"\'. '[::-1])
        pixlist=list(pixels)
        minp=min(pixlist)
        maxp=max(pixlist)
        vals=[]
        lst=list(range(minp,maxp+1))
        def chunks(lst, n):
            import numpy as np
            return np.array_split(lst,n)
        lchunks=list(chunks(lst,len(a)))
        for chunk in lchunks:
            vals.append(chunk[0])
        avals= {vals[i]: a[i] for i in range(len(vals))}
        ascii_str = "";    
        for pixel in pixels:
            ascii_str += avals[closest(vals,pixel)];
        return ascii_str
    image = PIL.Image.open(filepath)
    image = resize(image,newsize);
    greyscale_image = to_greyscale(image)
    ascii_str = pixel_to_ascii(greyscale_image)
    img_width = greyscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img=""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    return ascii_img