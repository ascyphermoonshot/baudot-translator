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
        text=text.replace(r'\a','‽')
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
    print(text)
    baudtext=text_to_baud(text)
    baudint=int(baudtext,2)
    print(baudint)
    return baudtext
if __name__=='__main__':
    text=input('enter your text here: ')
    translate_to_baudot('text')
