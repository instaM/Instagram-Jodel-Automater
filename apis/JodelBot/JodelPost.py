import  Post
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
class JodelPost(Post):

    def __init__(self,text,city,votes,color):
        self.text = text
        self.city = city
        self.votes = votes
        self.color = color
    def getImage(self):
        city = self.city
        text = self.text
        votes = self.votes
        crgb = tuple(int(self.color[i:i + 2], 16) for i in (0, 2, 4))
        back = Image.new("RGB", (640,640), crgb)
        front = Image.open( os.path.abspath(os.path.join(__file__, '..' ,"elements.png")))
        back.paste(front,(0,0),front)
        draw = ImageDraw.Draw(back)
        font = ImageFont.truetype(os.path.abspath(os.path.join(__file__, '..' ,"gbr.otf")), 28)
        fontVotes = ImageFont.truetype(os.path.abspath(os.path.join(__file__, '..' ,"gbr.otf")), 28)
        fontCity = ImageFont.truetype(os.path.abspath(os.path.join(__file__, '..' ,"gbr.otf")), 20)
        city.encode('iso-8859-1')
        city = city.replace("ue",u"ü")
        city = city.replace("ae", u"ä")
        city = city.replace("oe", u"ö")
        splitLength = 28
        text = text.replace("\n\n", "\n")
        textArray = text.split(" ")
        for i in range(0,len(textArray)):
            if len(textArray[i]) > splitLength:
                textArray[i] = textArray[i][:27] + '\n' + textArray[i][27:]
        tempS = ""
        newString = ""
        for x in textArray:
            x = x + " "
            if len(tempS) + len(x.replace('\n','')) < splitLength:
                    tempS = tempS + x
                    if '\n' in tempS:
                        newString = newString + tempS
                        tempS = ""
            else: #falls laenger als die Maximalezeilen laenge
                if x[0] != '\n':
                    newString = newString + tempS + '\n' #falls in x noch kein new line
                else:
                    newString = newString + tempS#falls x ein newline beginnt kein new line noetig
                tempS = x
        newString = newString + tempS #fuege den uebrig gebliebenen String hinzu
        newArray = newString.split('\n')
        offset = len(newArray) * -16
        for i in range(0, len(newArray)): #printe alle zeilen auf den screen
            draw.text((40, 277 + offset + 32 * i), newArray[i], (255, 255, 255), font=font)
        offset = len(str(votes)) * -7
        draw.text((575 + offset, 273), str(votes), (255, 255, 255), font=fontVotes)
        draw.text((65, 600), city, (255, 255, 255), font=fontCity)

        return back
    def getHashtags(self):
        #hashtag 1 = self.city
        raise Exception('Not Implemented yet')
