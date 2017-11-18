from math import log as Ln
from WeatherData import WeatherReport


def constrainRGB(val):
    return min(max(0, int(round(val))), 255)


def KelvinToRGB(temp=5000):

    if temp < 1000 or temp > 40000:
        raise ValueError('Outside or mapping range')

    #algorihtm taken from: http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    #updated to values from: http://www.zombieprototypes.com/?p=210

    temp = temp / 100.

    if temp <= 66:
        r = 255.

        if temp < 10:
            g = 0.
        else:
            g = temp - 2
            g = -155.25485562709179 - 0.44596950469579133 * g + 104.49216199393888 * Ln(g)

        if temp < 20:
            b = 0.
        else:
            b = temp - 10
            b = -254.76935184120902 + 0.8274096064007395 * b + 115.67994401066147 * Ln(b)

    else:
        r = temp - 55
        r = 351.97690566805693 + 0.114206453784165 * r - 40.25366309332127 * Ln(r)

        g = temp - 50
        g = 325.4494125711974 + 0.07943456536662342 * g - 28.0852963507957 * Ln(g)

        b = 255.

    return tuple(map(constrainRGB, (r,g,b)))



class LightControl(object):
    def __init__(self):
        self.presets = {
            'Summer-Daylight': KelvinToRGB(6500),
            'Open-Shade': KelvinToRGB(7500),
            'Sky-Blue': KelvinToRGB(15000),
            'Sky-Blue-deep': KelvinToRGB(30000)
        }


        self.cloud_factor = 10
        self.night_value = -2000
        self.weather = WeatherReport('Berlin')

        self.corrections = {'clouds': 0, 'night': 0}

        self.T = 6500
        self.color = KelvinToRGB(self.T + sum(self.corrections.values()))


    def getColor(self):
        self.color = KelvinToRGB(self.T + sum(self.corrections.values()))
        return self.color


    def setNightCorrection(self, value):
        self.night_value = value

    def setCloudCorrection(self, value):
        self.cloud_factor = value


    def setBaseTemperature(self, K):
        if isinstance(K, int):
            self.T = K
        elif isinstance(K, str) and K in self.presets:
            self.T = self.presets[K]
        else:
            raise ValueError

        self.color = KelvinToRGB(self.T + sum(self.corrections.values()))


    def NightCorrecion(self, active=True):
        if active and not self.weather.is_sun_up():
            self.corrections['night'] = self.night_value
        else:
            self.corrections['night'] = 0

        self.color = KelvinToRGB(self.T + sum(self.corrections.values()))


    def CloudCorrection(self, active=True):
        if active:
            clouds = self.weather.get_cloudiness()
            self.corrections['clouds'] = clouds * self.cloud_factor
        else:
            self.corrections['clouds'] = 0

        self.color = KelvinToRGB(self.T  + sum(self.corrections.values()))













