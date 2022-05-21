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
    
def get_key():
    import hashlib
    import time
    from secrets import choice
    from orderedset import OrderedSet
    key=input('insert your passphrase: ')
    tstamp=int(time.time())
    hkey=hashlib.sha256(key.encode())
    hhkey=hkey.hexdigest()
    inkey=int(hhkey,16)
    def adper(num):
        while num>25:
            snum = str(num)
            sdigits = list(snum)
            digits = [int(x) for x in sdigits]
            num = sum(digits)
        return num
    (r,l)=tuple((adper(inkey),adper(inkey*tstamp)))
    def shift_alpha(shift):
       oalpha=''
       alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ ∆-:$3!&#8\'().,9014‽57;2/6"'
       while len(oalpha)<=len(alpha):
           for char in alpha:
            oalpha+=alpha[shift::adper(len(key))]
            shift+=1
       oalpha=OrderedSet(list(oalpha))
       for char in alpha:
           if char not in oalpha:
               oalpha.add(char)
       return (oalpha)
    left=shift_alpha(l)
    right=shift_alpha(r)
    while left==right:
        right=shift_alpha(r+choice(range(1,25)))
    sleft=''
    sright=''
    for char in left:
        sleft+=char
    for char in right:
        sright+=char
    return (tuple((sleft,sright)))

def main(lalpha,ralpha,msg): 
    print("L:", lalpha)
    print("R:", ralpha)
    print("I:", msg)
    msg=msg.replace('\n','∆')
    return do_chao(msg, lalpha, ralpha, 1)
 
def do_chao(msg, lalpha, ralpha, en=1):
    msg = msg.upper()
    out = ""    
    for L in msg:
        if en:
            lalpha, ralpha = rotate_wheels(lalpha, ralpha, L)
            out += lalpha[0]
        else:
            ralpha, lalpha = rotate_wheels(ralpha, lalpha, L)
            out += ralpha[0]
        lalpha, ralpha = scramble_wheels(lalpha, ralpha)
    return out
 
def permu(alp, num):
    alp = alp[:num], alp[num:]
    return "".join(alp[::-1])
 
def rotate_wheels(lalph, ralph, key):
    try:
        newin = ralph.index(key)
    except:
        print(r.key, 'was not found')
        newin = ralph.find(key)
    return permu(lalph, newin), permu(ralph, newin)    
 
def scramble_wheels(lalph, ralph):
    # LEFT = cipher wheel 
    # Cycle second[1] through nadir[14] forward
    lalph = list(lalph)
    lalph = "".join([*lalph[0],
                    *lalph[2:26],
                    lalph[1],
                    *lalph[26:]])
 
    # RIGHT = plain wheel                    
    # Send the zenith[0] character to the end[25],
    # cycle third[2] through nadir[14] characters forward
    ralph = list(ralph)
    ralph = "".join([*ralph[1:3],
                     *ralph[4:27],
                     ralph[3],
                     *ralph[27:],
                     ralph[0]])
    return lalph, ralph

def translate_to_baudot(untranslatedtext):
    from textwrap import wrap
    def getdic():
        chars=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ ∆-:$3!&#8\'().,9014‽57;2/6"') #‽ is bell and ∆ is new line
        baud=["11000","10011","01110","10010","10000","10110","01011","00101","01100","11010","11110","01001","00111","00110","00011","01101","11101","01010","10100","00001","11100","01111","11001","10111","10101","10001","00100","01000","11000","10011","01110","10010","10000","10110","01011","00101","01100","11010","11110","01001","00111","00110","00011","01101","11101","01010","10100","00001","11100","01111","11001","10111","10101","10001"]
        baudic={chars[i]: baud[i] for i in range(len(chars))}
        return baudic
    def add_shift(text,charnum):
        if charnum>0:
            if text[charnum-1] in'ABCDEFGHIJKLMNOPQRSTUVWXYZ ∆' and text[charnum] not in'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                return '11111'
            elif text[charnum-1] not in'ABCDEFGHIJKLMNOPQRSTUVWXYZ ∆' and text[charnum] in'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                return '11011'
            else:
                return ""
        elif charnum==0 and text[0] not in'ABCDEFGHIJKLMNOPQRSTUVWXYZ ':
            return '11111'
        else:
            return ""
    def bell_check(text):
        text=text.replace('\a','‽')
        return text
    def line_check(text):
        text=text.replace('\n','∆')
        return text
    def strip_non_baud(text):
        for char in text:
            if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ-:$3!&#8\'().,9014‽57;2/6" ∆':
                text=text.replace('char','')
        return text
    def text_to_baud(text):
        baudic=getdic()
        baudtext=''
        charnum=0
        for char in text:
            baudtext+=add_shift(text,charnum)
            baudtext+=baudic[char]
            charnum+=1
        return baudtext
    text=untranslatedtext
    text=bell_check(text)
    text=line_check(text)
    text=text.upper()
    text='‽‽‽∆'+strip_non_baud(text)+'∆‽‽‽'
    #print(text)
    baudtext=text_to_baud(text)
    baudint=int(baudtext,2)
    print(baudint)
    return baudtext
if __name__=='__main__':
    filepth='/storage/emulated/0/Download/images - 2022-05-06T235127.533.jpeg'
    (lalpha,ralpha)=get_key()
    msg=baudot_art(filepth,300)
    cyphertext=main(lalpha,ralpha,msg)
    baud=translate_to_baudot(cyphertext)
    print(('\n'*5)+str(len(baud)))