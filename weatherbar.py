import rumps

class WeatherBar(object):

    def __init__(self):
        self.app = rumps.App("WeatherBar")
        self.set_up_menu()

        self.setWeatherButton = rumps.MenuItem(title="Update Weather", callback=self.setWeather)
        self.app.menu = [self.setWeatherButton]

    def set_up_menu(self):
        self.app.title = "Weather"

    def setWeather(self, sender):
            sender.title = "Weather Updated"
            self.app.title = "Temperature"

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = WeatherBar()
    app.run()
