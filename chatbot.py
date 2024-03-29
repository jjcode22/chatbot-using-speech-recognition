import random
import datetime
import webbrowser
import pyttsx3
import wikipedia
from pygame import mixer
import pyowm
import config
import requests, json
import speech_recognition as sr
from google_places import (
    change_location_query,
    filter_sentence,
    get_location,
    nearby_places,
    requests,
)
import pyjokes
from googletrans import Translator
# importing geopy library
from geopy.geocoders import Nominatim

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

# entering the location name
getLoc = loc.geocode("Sion Mumbai")

# printing address
print(getLoc.address)
lat=getLoc.latitude
long=getLoc.longitude

# printing latitude and longitude
print("Latitude = ", getLoc.latitude, "\n")
print("Longitude = ", getLoc.longitude)



from voice_conf import *
# from speech_recognition.__main__ import r, audio
from intentClassification.intent_classification import IntentClassification

greetings = ['hey there', 'hello', 'hi', 'Hai', 'hey!', 'hey', 'hi there!']
question = ['How are you?', 'How are you doing?', 'What\'s up?']
responses = ['Okay', "I'm fine"]
var1 = ['who made you', 'who created you']
var2 = ['I_was_created_by_Edward_right_in_his_computer.',
        'Edward', 'Some_guy_whom_i_never_got_to_know.']
var3 = ['what time is it', 'what is the time', 'time']
var4 = ['who are you', 'what is you name']
var5 = ['date', 'what is the date', 'what date is it', 'tell me the date']
cmd1 = ['open browser', 'open google']
cmd2 = ['play music', 'play songs', 'play a song', 'open music player']
cmd3 = [
    'tell a joke',
    'tell me a joke',
    'say something funny',
    'tell something funny']
cmd4 = ['open youtube', 'i want to watch a video']
cmd5 = [
    'tell me the weather',
    'weather',
    'what about the weather',
    'what\'s the weather']
cmd6 = ['exit', 'close', 'goodbye', 'nothing', 'catch you later', 'bye']
cmd7 = [
    "what is your color",
    "what is your colour",
    "your color",
    "your color?",
]
colrep = [
    "Right now its rainbow",
    "Right now its transparent",
    "Right now its non chromatic",
]
cmd8 = ["what is you favourite colour", "what is your favourite color"]
cmd9 = ["thank you"]
cmd10 = ["Play spotify","play on spotify","open spotify"]


repfr9 = ["youre welcome", "glad i could help you"]

intentClassifier = IntentClassification()

personalized, longitude, latitude = get_location()
stores = []
stores_data = {}

print("hi ", "Setting location through ip bias, Change location?")
change_location = False

language_conf = input('Language(en-US): ')
if language_conf == '':
    language_conf = "en-US"
voice_language = getVoiceID(language_conf[:2])

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voice_language)
volume = engine.getProperty('volume')
engine.setProperty('volume', 10.0)
rate = engine.getProperty('rate')

engine.setProperty('rate', rate - 25)

translator = Translator()

while True:
    speech_type = input("Speech/Text: ")
    if speech_type.lower() != "speech":
        translate = input("Type: ")
    else:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            t = translator.translate('Hi i am a Chat bot! Give me an Order.Tell me something to do', dest=language_conf[:2])
            print(t.text)
            engine.say(t.text)
            engine.runAndWait()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                translate = r.recognize_google(audio, language=language_conf)
                print("You said:- " + translate)
            except sr.UnknownValueError:
                print("Could not understand audio")
                engine.say("I didnt get that. Rerun the code")
                engine.runAndWait()
    intent = intentClassifier.intent_identifier(translate)
    print("Intent:", intent)
    # TODO:: entity based weather output
    if intent == "weather":
        url = "https://yahoo-weather5.p.rapidapi.com/weather"

        querystring = {"lat":lat,"long":long,"format":"json","u":"f"}

        headers = {
            "X-RapidAPI-Key": "22fb713a8fmshceedc40408df3e0p1f2252jsnbc890ecc3252",
            "X-RapidAPI-Host": "yahoo-weather5.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

                # parse x:
        y = json.loads(response.text)
        weather = str(y["current_observation"])

        # the result is a Python dictionary:
        print(y["current_observation"])

    


        engine.say(weather)
        engine.runAndWait()
        # owm = pyowm.OWM(config.weather_api_key)
        # observation = owm.weather_at_place("Bangalore, IN")
        # observation_list = owm.weather_around_coords(12.972442, 77.580643)
        # w = observation.get_weather()
        # w.get_wind()
        # w.get_humidity()
        # w.get_temperature("celsius")
        # print(w)
        # print(w.get_wind())
        # print(w.get_humidity())
        # print(w.get_temperature("celsius"))
        # engine.say(w.get_wind())
        # engine.runAndWait()
        # engine.say("humidity")
        # engine.runAndWait()
        # engine.say(w.get_humidity())
        # engine.runAndWait()
        # engine.say("temperature")
        # engine.runAndWait()
        # engine.say(w.get_temperature("celsius"))
        # engine.runAndWait()
    if intent == "music":
        engine.say("please wait")
        engine.runAndWait()
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.play()
       
        engine.runAndWait()
    # if intent == "music":
    #     url = "https://musiclinkssapi.p.rapidapi.com/apiSearch/track"

    #     querystring = {"query":translate}

    #     headers = {
    #             "X-RapidAPI-Key": "c607ce4b44mshf7cdc16120027e0p183be7jsn37acb1ed9913",
    #             "X-RapidAPI-Host": "musiclinkssapi.p.rapidapi.com"
    #         }

    #     response = requests.request("GET", url, headers=headers, params=querystring)
    #     s=json.loads(response.text)
    #     songurl=str(s['platforms'][0]['url'])
    #     webbrowser.open(songurl)

    #     print(songurl)


    if intent == "restaurant":
        url = "https://nearby-places.p.rapidapi.com/nearby"

        querystring = {"lat":lat,"lng":long,"type":"cafe","radius":"600"}


        headers = {
            "X-RapidAPI-Key": "0b8e8ae0a7msh52f9b71b43e7b4fp1038a9jsn3fa25365e2ea",
            "X-RapidAPI-Host": "nearby-places.p.rapidapi.com"
        }

#         headers = {
# 	"X-RapidAPI-Key": "c607ce4b44mshf7cdc16120027e0p183be7jsn37acb1ed9913",
# 	"X-RapidAPI-Host": "nearby-places.p.rapidapi.com"
# }

        response = requests.request("GET", url, headers=headers, params=querystring)

        r= json.loads(response.text)
        rest1 = []
        for x in range(6):
            restname = str(r[x]['name'])
            restadd = str(r[x]['address'])
            restdist = str(r[x]['distanceMeter'])
            
            rest1.append(restname)
            rest1.append("address "+restadd)
            rest1.append(restdist+"meters from here")
        print(rest1)
        engine.say(rest1)
        engine.runAndWait()

    if intent == "spotify":
        url = "https://musiclinkssapi.p.rapidapi.com/apiSearch/track"

        querystring = {"query":translate}

        headers = {
                "X-RapidAPI-Key": "c607ce4b44mshf7cdc16120027e0p183be7jsn37acb1ed9913",
                "X-RapidAPI-Host": "musiclinkssapi.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        s=json.loads(response.text)
        songurl=str(s['platforms'][0]['url'])
        webbrowser.open(songurl)

        print(songurl)


        
            

    if translate in greetings:
        random_greeting = random.choice(greetings)
        print(random_greeting)
    elif translate.lower() == "yes":
        change_location = True
        print("Location?")
    elif change_location is True:
        personalized = change_location_query(translate, config.google_api_key)
        change_location = False
    elif translate in question:
        print("I am fine")
    elif translate in var1:
        reply = random.choice(var2)
        print(reply)
    elif translate in cmd9:
        print(random.choice(repfr9))
    elif translate in cmd7:
        print(random.choice(colrep))
        print("It keeps changing every micro second")
    elif translate in cmd8:
        print(random.choice(colrep))
        print("It keeps changing every micro second")
    elif translate in cmd2:
        mixer.init()
        mixer.music.load("music.mp3")
        mixer.music.play()
    elif translate in var4:
        engine.say("I am a bot, silly")
        engine.runAndWait()
    elif translate in cmd4:
        webbrowser.open("http://www.youtube.com")
    elif translate in cmd6:
        print("see you later")
        exit()
    elif translate in cmd5:
        print("here")
        url = (
            "http://api.openweathermap.org/data/2.5/weather?" +
            "lat={}&lon={}&appid={}&units={}"
        ).format(
            latitude,
            longitude,
            config.weather_api_key,
            config.weather_temperature_format,
        )
        r = requests.get(url)
        x = r.json()
        city = x["name"]
        windSpeed = x["wind"]["speed"]
        skyDescription = x["weather"][0]["description"]
        maxTemperature = x["main"]["temp_max"]
        minTemperature = x["main"]["temp_min"]
        temp = x["main"]["temp"]
        humidity = x["main"]["humidity"]
        pressure = x["main"]["pressure"]
        # use the above variables based on user needs
        print(
            "Weather in {} is {} "
            "with temperature {} celsius"
            ", humidity in the air is {} "
            "and wind blowing at a speed of {}".format(
                city, skyDescription, temp, humidity, windSpeed
            )
        )
        engine.say(
            "Weather in {} is {} "
            "with temperature {} celsius"
            ", humidity in the air is {} "
            "and wind blowing at a speed of {}".format(
                city, skyDescription, temp, humidity, windSpeed
            )
        )
        engine.runAndWait()
    elif translate in var3 or translate in var5:
        current_time = datetime.datetime.now()
        if translate in var3:
            print(current_time.strftime("The time is %H:%M"))
            engine.say(current_time.strftime("The time is %H:%M"))
            engine.runAndWait()
        elif translate in var5:
            print(current_time.strftime("The date is %B %d, %Y"))
            engine.say(current_time.strftime("The date is %B %d %Y"))
            engine.runAndWait()
    elif translate in cmd1:
        webbrowser.open("http://www.google.com")
    elif translate in cmd3:
        jokrep = pyjokes.get_joke()
        print(jokrep)
        engine.say(jokrep)
        engine.runAndWait()
    elif ("them" in translate.split(" ") or
          "popular" in translate.split(" ")) and stores:
        sorted_stores_data = sorted(
            stores_data, key=lambda x: x["rating"], reverse=True
        )
        sorted_stores = [x["name"] for x in sorted_stores_data][:5]
        if "order" in translate:
            print("These are the stores: ")
            for store in sorted_stores:
                print(store)
            engine.say(sorted_stores)
            engine.runAndWait()
        if "popular" in translate:
            print("Most popular one is: ", sorted_stores[0])
        if "go" in translate:
            lat = sorted_stores_data[0]["geometry"]["location"]["lat"]
            lng = sorted_stores_data[0]["geometry"]["location"]["lng"]
            url = "http://maps.google.com/maps?q={},{}".format(lat, lng)
            webbrowser.open_new(url)
            engine.say(
                "Showing you directions to the store {}".format(
                    sorted_stores[0]
                )
            )
            engine.runAndWait()
    elif (
        "stores" in translate.split(" ") or
        "food" in translate.split(" ") or
        "restaurant" in translate
    ):
        stores = []
        stores_data = {}
        query = filter_sentence(translate)
        stores, stores_data = nearby_places(
            config.google_api_key,
            personalized.city,
            query,
            personalized.latitude,
            personalized.longitude,
        )
        print("These are the stores: ")
        for store in stores:
            print(store)
        engine.say(stores)
        engine.runAndWait()
        print("Where do you want to go:")
        engine.say("Where do you want to go:")
        engine.runAndWait()
    else:
        engine.say("please wait")
        engine.runAndWait()
        print(wikipedia.summary(translate))
        engine.say(wikipedia.summary(translate))
        engine.runAndWait()
        userInput3 = input("or else search in google")
        webbrowser.open_new("http://www.google.com/search?q=" + userInput3)
