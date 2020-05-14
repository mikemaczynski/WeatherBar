import rumps
import pyowm


class WeatherBar(object):
    api = "f68c7296446b5dfeb8e20c1806ea3e97"
    cityName = "Chicago"

    degreeSymbol = u'\N{DEGREE SIGN}'
    unit = "fahrenheit"
    unitTitle = f"{degreeSymbol}F | {degreeSymbol}C"
    minutes = 20
    interval = minutes * 60

    def __init__(self):
        self.setLocationButton = rumps.MenuItem(title="Change Location", callback=self.setLocation)
        self.setWeatherButton = rumps.MenuItem(title="Refresh", callback=self.callUpdateWeather)
        self.setUnitButton = rumps.MenuItem(title=self.unitTitle, callback=self.setCurrentUnit)
        self.setAPIKeyButton = rumps.MenuItem(title="Settings", callback=self.setAPIKey)
        self.refreshTimer = rumps.Timer(self.callUpdateWeather, self.interval)
        self.refreshTimer.start()

        self.app = rumps.App("WeatherBar")
        self.app.title = "️"

        self.initializeMenu()

    def initializeMenu(self):
        self.app.menu.add(self.setUnitButton)
        self.app.menu.add(self.setLocationButton)
        self.app.menu.add(self.setWeatherButton)
        self.app.menu.add(rumps.separator)
        self.app.menu.add(self.setAPIKeyButton)

        if self.api == '':
            self.app.title = "Set API Key in 'Settings'"
        else:
            self.refreshWeather()
        self.app.run()

    def refreshWeather(self):
        openWeatherMap = pyowm.OWM(self.api)
        location = openWeatherMap.weather_at_place(f'{self.cityName}')
        currentWeather = location.get_weather()
        temperature = currentWeather.get_temperature(self.unit)['temp']

        currentUnit = self.unit[0].upper()
        self.app.title = f'{round(temperature)}{self.degreeSymbol}{currentUnit}'

    def callUpdateWeather(self, sender):
        self.refreshWeather()

    def setAPIKey(self, sender):
        updateAPI = rumps.Window(
            message='Enter your API key from OpenWeatherMap.',
            title='Weather API Key',
            ok="Update API Key",
            dimensions=(300, 23)
        )
        updateAPI.icon = "windy-weather.png"
        updateAPIButton = updateAPI.run()

        if updateAPIButton.clicked:
            self.api = updateAPIButton.text
            if self.api == '':
                self.app.title = "Set API Key in 'Settings'"
            else:
                self.refreshWeather()

    def setLocation(self, sender):
        setLocationWindow = rumps.Window(
            message='Enter a city below to retrieve the current temperature.',
            title='Change Location',
            dimensions=(300, 23)
        )
        setLocationWindow.icon = "location.png"
        updateButton = setLocationWindow.run()

        if updateButton.clicked:
            self.cityName = updateButton.text
            if self.api == '':
                self.app.title = "Set API Key in 'Settings'"
            elif updateButton.text != '':
                self.refreshWeather()

    def setCurrentUnit(self, sender):
        if self.unit == "fahrenheit":
            self.unit = "celsius"
            self.refreshWeather()
        else:
            self.unit = "fahrenheit"
            self.refreshWeather()

if __name__ == '__main__':
    app = WeatherBar()
    app.run()
