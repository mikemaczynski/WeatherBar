import rumps

class WeatherBar(object):

    def __init__(self):
        self.app = rumps.App("WeatherBar")
        self.app.title = "Weather"

        self.setAPIKeyButton = rumps.MenuItem(title="Set API Key", callback=self.setAPIKey)
        self.app.menu.add(self.setAPIKeyButton)
        self.setWeatherButton = rumps.MenuItem(title="Refresh Weather", callback=self.setWeather)
        self.app.menu.add(self.setWeatherButton)
        self.app.menu.add(rumps.separator)
        self.app.run()

    def setWeather(self, sender):
        sender.title = "Weather Updated"
        self.app.title = "Temperature"

    def setAPIKey(self, sender):
        updateAPI = rumps.Window(
            message='Enter your weather API key',
            title='Weather API Key',
            ok="Update API Key",
            dimensions=(300, 23)
        )
        updateAPI.icon = "location.png"
        updateButton = updateAPI.run()

        if updateButton.clicked:
            print(updateButton.text)
        
if __name__ == '__main__':
    app = WeatherBar()
