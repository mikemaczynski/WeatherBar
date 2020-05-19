import rumps
import pyowm


class WeatherBar(object):
    api = "f68c7296446b5dfeb8e20c1806ea3e97"  # my api key
    cityName = "Arlington Heights"  # default city name

    degreeSymbol = u'\N{DEGREE SIGN}'
    unit = "fahrenheit"
    unitTitle = f"{degreeSymbol}F | {degreeSymbol}C"
    minutes = 20
    interval = minutes * 60

    def __init__(self):
        self.setLocationButton = rumps.MenuItem(title="Change Location", callback=self.setLocation)
        self.setWeatherButton = rumps.MenuItem(title="Refresh", callback=self.callUpdateWeather)  # initialize the menu
        self.setUnitButton = rumps.MenuItem(title=self.unitTitle, callback=self.setCurrentUnit)   # buttons and settings
        self.setAPIKeyButton = rumps.MenuItem(title="Settings", callback=self.setAPIKey)
        self.refreshTimer = rumps.Timer(self.callUpdateWeather, self.interval)
        self.refreshTimer.start()  # begin the timer at startup (used to determine when to refresh the temperature)

        self.app = rumps.App("WeatherBar")

        self.initializeMenu()

    def initializeMenu(self):
        self.app.menu.add(self.setUnitButton)
        self.app.menu.add(self.setLocationButton)  # Add the previously initialized menu
        self.app.menu.add(self.setWeatherButton)   # buttons to the drop-down menu bar
        self.app.menu.add(rumps.separator)
        self.app.menu.add(self.setAPIKeyButton)

        if self.api == '':    # ensure that an api key has been set before attempting to pull the temperature
            self.app.title = "Set API Key in 'Settings'"
        else:
            self.refreshWeather()
        self.app.run()

    def refreshWeather(self):  # function that pulls data from the openweathermap api
        openWeatherMap = pyowm.OWM(self.api)
        location = openWeatherMap.weather_at_place(f'{self.cityName}')   # code snippet that pulls the temperature based
        currentWeather = location.get_weather()                          # on the users location and specified unit
        temperature = currentWeather.get_temperature(self.unit)['temp']

        currentUnit = self.unit[0].upper()
        self.app.title = f'{round(temperature)}{self.degreeSymbol}{currentUnit}' # sets the title to the temperature and chosen unit

    def callUpdateWeather(self, sender):
        self.refreshWeather()

    def setAPIKey(self, sender):  # function to allow the user to set their weather api key
        updateAPI = rumps.Window( # create a popup window to prompt the user to enter their api key
            message='Enter your API key from OpenWeatherMap.',
            title='Weather API Key',
            ok="Update API Key",
            dimensions=(300, 23)
        )
        updateAPI.icon = "windy-weather.png"
        updateAPIButton = updateAPI.run()

        if updateAPIButton.clicked:
            self.api = updateAPIButton.text  # ensure that the user has actually inputted an api key
            if self.api == '':
                self.app.title = "Set API Key in 'Settings'"
            else:
                self.refreshWeather()

    def setLocation(self, sender):  # function to allow the user to change their location
        setLocationWindow = rumps.Window(  # create a popup window to prompt the user to enter their location
            message='Enter a city below to retrieve the current temperature.',
            title='Change Location',
            dimensions=(300, 23)
        )
        setLocationWindow.icon = "location.png"
        updateButton = setLocationWindow.run()

        if updateButton.clicked:
            self.cityName = updateButton.text
            if self.api == '':   # if the api hasn't been updated yet, notify the user
                self.app.title = "Set API Key in 'Settings'"
            elif updateButton.text != '':
                self.refreshWeather()

    def setCurrentUnit(self, sender):  # Toggle switch to allow the user to switch
        if self.unit == "fahrenheit":  # between celsius and fahrenheit on the fly
            self.unit = "celsius"
            self.refreshWeather()
        else:
            self.unit = "fahrenheit"
            self.refreshWeather()


if __name__ == '__main__':  # default function to run the program
    app = WeatherBar()
    app.run()
