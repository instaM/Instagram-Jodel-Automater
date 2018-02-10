# -*- coding: iso-8859-1 -*-
import jodel_api
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from geopy.geocoders import Nominatim
from DBwrapper import DBWrapper

class JodelBot:
    def __init__(self):
        self.scanabtastrate = 8
        self.scanradius = 2
        self.db = DBWrapper(os.path.abspath(os.path.join(__file__,"..",'jodel.db')))
        self.citylist = ["Muenchen","Duesseldorf","Berlin","Hamburg","Rostock",
                         "Frankfurt am Main","Koeln","Wien",
                         "Stuttgart","Dortmund","Bremen","Essen","Bern","Heidelberg","Tuebingen"]
        self.lat, self.lng, self.city = 48.148434, 11.567867, "Munich"
        self.access_token = "81490906-56920392-3f8cb7a3-4604-42c7-9455-c797fe5a0831"
        self.expiration_date= 1518386290
        self.distinct_id = "5a7781f268566e001735a74e"
        self.device_uid= "d37e23334c45cf8d867ea7bc556b1e0e6d357e10eea0a22926b776c7b0031dcd"
        self.refresh_token = "a19ad214-425b-4dc7-a19e-06aa0f9c12a8"
        self.j = jodel_api.JodelAccount(lat=self.lat, lng=self.lng, city=self.city,access_token=self.access_token, expiration_date=self.expiration_date,
                               refresh_token=self.refresh_token, distinct_id= self.distinct_id, device_uid=self.device_uid, is_legacy=False)
    def getBestImage(self,used = False):
        post = self.db.getTop(used)
        if post is None:
            
            return
        return self.getImage(post[0],post[1],post[2],post[3])
    def getImage(self,text,votes,city,color):
        crgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        back = Image.new("RGB", (640,640), crgb)
        front = Image.open( os.path.abspath(os.path.join(__file__, '..' ,"elements.png")))
        back.paste(front,(0,0),front)
        draw = ImageDraw.Draw(back)
        font = ImageFont.truetype(os.path.abspath(os.path.join(__file__, '..' ,"gbr.otf")), 28)
        fontVotes = ImageFont.truetype(os.path.abspath(os.path.join(__file__, '..' ,"gbr.otf")), 28)
        fontCity = ImageFont.truetype(os.path.abspath(os.path.join(__file__, '..' ,"gbr.otf")), 20)
        #city = city.replace("ue","ü")
        #city = city.replace("ae", "ä")
        #city = city.replace("oe", "ö")
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
        
        return (back,city)

    def getTopPost(self, city):
        geolocator = Nominatim()
        clat = geolocator.geocode(city).latitude - self.scanradius *self.scanabtastrate * 0.00898
        clong = geolocator.geocode(city).longitude - self.scanradius*self.scanabtastrate * 0.00899
        self.j.set_location(clat,clong,city)
        temp = self.j.get_posts_popular(skip=0, limit=1, after=None, mine=False, hashtag=None, channel=None)
        print("Scanning " + city)
        for x in range(0,self.scanradius * 2):
            for y in range(0,self.scanradius * 2):
                self.j.set_location(clat,clong,city)
                temp2 = self.j.get_posts_popular(skip=0, limit=1, after=None, mine=False, hashtag=None, channel=None)
                #print(temp[1]['posts'][0]['message'])
                if temp2[1]['posts'][0]['vote_count'] > temp[1]['posts'][0]['vote_count']:
                    temp = temp2
                clong = clong + self.scanabtastrate * 0.00899
            clat = clat + self.scanabtastrate * 0.00898
        return (temp[1]['posts'][0]['message'],temp[1]['posts'][0]['vote_count'],temp[1]['posts'][0]['color'])
    def scanTopPost(self,minVotes):
        for c in self.citylist:
           temp = self.getTopPost(c)
           if temp[1] >= minVotes:
              self.db.addTop(temp[0],temp[1],temp[2],c)

    def accdata(self):
        print(self.j.get_account_data())
        return



