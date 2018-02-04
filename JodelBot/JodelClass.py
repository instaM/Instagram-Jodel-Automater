
import jodel_api
from geopy.geocoders import Nominatim
class JodelBot:

    def __init__(self):
        self.lat, self.lng, self.city = 48.148434, 11.567867, "Munich"
        self.access_token = "81490906-56920392-3f8cb7a3-4604-42c7-9455-c797fe5a0831"
        self.expiration_date= 1518386290
        self.distinct_id = "5a7781f268566e001735a74e"
        self.device_uid= "d37e23334c45cf8d867ea7bc556b1e0e6d357e10eea0a22926b776c7b0031dcd"
        self.refresh_token = "a19ad214-425b-4dc7-a19e-06aa0f9c12a8"
        self.j = jodel_api.JodelAccount(lat=self.lat, lng=self.lng, city=self.city,access_token=self.access_token, expiration_date=self.expiration_date,
                               refresh_token=self.refresh_token, distinct_id= self.distinct_id, device_uid=self.device_uid, is_legacy=False)
    def getTopPost(self, city):
        geolocator = Nominatim()
        self.j.set_location(geolocator.geocode(city).latitude,geolocator.geocode(city).longitude,city)
        temp = self.j.get_posts_popular(skip=0, limit=1, after=None, mine=False, hashtag=None, channel=None)

        return temp[1]['posts'][0]['message'] + " mit " + str(temp[1]['posts'][0]['vote_count']) + " Votes aus " + city
    def accdata(self):
        print(self.j.get_account_data())
        return


jbot = JodelBot()
print(jbot.getTopPost("Dusseldorf"))

