import datetime as dt
import os
import tkinter.messagebox as messagebox

import Wetter
import requests


def getInfo():
    # ---------------------------Set your personal data------------------------------#
    api_key = "None"  # Your Api-Key  Goto https://openweathermap.org/api/, create a account and get an Api_Key
    city = "None"  # Your City Name
    # ------------------------------------------------------------------------------#
    if city == "None" or api_key == "None":
        print("Please specify a city or an api key")
        quit()
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}appid={api_key}&q={city}"

    while True:  # return error if no internetconnection
        try:
            global response
            response = requests.get(url).json()  # collect information and convert to json
            break
        except:
            message = messagebox.askquestion("Fehler",
                                             "Es konnte keine Verbindung mit openweathermap.org aufgebaut "
                                             "werden\nÜberprüfe deine Internetverbindung und deine Firewall "
                                             "Einstellungen\n\nJa: Erneut versuchen\nNein: Beenden",
                                             icon="error")
            if message == "no":
                quit()

    def kToC(kelvin):  # Kelvin to Celsius
        return f"{(kelvin - 273.15):.2f}"

    try:  # pick the important data
        temp_kelvin = response["main"]["temp"]
        temp = kToC(temp_kelvin)
        feels_like_kelvin = response["main"]["feels_like"]
        feels_like = kToC(feels_like_kelvin)
        humidity = response["main"]["humidity"]
        description = response["weather"][0]["main"]
        description2 = response["weather"][0]["description"]
        sunrise_time = dt.datetime.utcfromtimestamp(response["sys"]["sunrise"] + response["timezone"])
        sunset_time = dt.datetime.utcfromtimestamp(response["sys"]["sunset"] + response["timezone"])
        wind_speed = response["wind"]["speed"]
        icon = response["weather"][0]["icon"]
    except KeyError:  # Api returns an error code
        messagebox.showerror("Fehler",
                             "Fehler beim Api-Aufruf\nMögliche Fehler:\n\t1.Ungüliger Api-Key\n"
                             "\t2.Zu viele Api-Aufrufe für den gekauften Api-Plan\n"
                             "\t3.Server Fehler auf openweathermap.org!\n\n"
                             f"Das Programm schließt sich jetzt automatisch!\n\nNähere Informationen: {response}")
        os._exit(0)
    data = {"Temperatur": temp, "Gefühlte Temperatur": feels_like, "Feuchtigkeit": humidity,
            "Beschreibung": description,
            "Genaue Beschreibung": description2, "Sonnenaufgang": sunrise_time,
            "Sonnenuntergang": sunset_time, "Windgeschwindigkeit": wind_speed, "iconname": icon}

    return data


if __name__ == '__main__':
    getInfo()  # Test
