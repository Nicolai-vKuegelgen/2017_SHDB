import urllib.request
import requests
import json
import generate_city_id_files as setup
import os

from datetime import datetime, timedelta
from time import sleep

class ToSoonError(Exception):
    pass


class WeatherReport(object):
    def __init__(self, city_name=None):
        self.user_api = '6cd45213613a81b048857dbd9ca9fc4c'  # Obtain yours form: http://openweathermap.org/
        self.unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
        self.api = 'http://api.openweathermap.org/data/2.5/weather?id='  # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz

        self.lastuse = datetime.now() - timedelta(seconds=600)

        self.WeatherData = None

        self.files = ['city_codes/097-102.txt', 'city_codes/103-108.txt', 'city_codes/103-108.txt', 'city_codes/115-122.txt']
        if not all(os.path.isfile(f) for f in self.files):
            print('Generarting City ID code tables')
            target_folder = 'city_codes'
            setup.download_the_files()
            cities = setup.read_all_cities_into_dict()
            ordered_cities = setup.order_dict_by_city_id(cities)
            ssets = setup.split_keyset(ordered_cities)
            setup.write_subsets_to_files(ssets, target_folder)

        self.get_city_code(city_name)

        sleep(1)
        self.data_fetch()


    def get_city_code(self, name=None):

        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']

        c = ord(name[0].lower())
        files = []
        if c < 97:  # not a letter
            files = ['city_codes/097-102.txt', 'city_codes/103-108.txt', 'city_codes/103-108.txt', 'city_codes/115-122.txt']
        elif c in range(97, 103):  # from a to f
            files += ['city_codes/097-102.txt']
        elif c in range(103, 109):  # from g to l
            files += ['city_codes/103-108.txt']
        elif c in range(109, 115):  # from m to r
            files += ['city_codes/103-108.txt']
        elif c in range(115, 123):  # from s to z
            files += ['city_codes/115-122.txt']
        else:
            files = ['city_codes/097-102.txt', 'city_codes/103-108.txt', 'city_codes/103-108.txt', 'city_codes/115-122.txt']


        candidates = []
        if name is not None:
            with open(files[0]) as f:
                for line in f:
                    line = line.rstrip().split(',')
                    if name in line[0]:
                        candidates.append(line)
        else:
            for file in files:
                with open(file) as f:
                    for line in f:
                        line = line.rstrip().split(',')
                        candidates.append(line)

        def pos_dist(cand):
            x = (lon, lat)
            y = (float(cand[3]), float(cand[2]))
            return (x[0] - y[0])**2 + (x[1] - y[1])**2

        loc = min(candidates, key=pos_dist)

        self.location = loc


    def data_fetch(self):
        if self.lastuse  + timedelta(seconds=600) > datetime.now():
            # print(self.lastuse)
            # print(self.lastuse  + timedelta(seconds=600))
            # print(datetime.now())
            # print(self.lastuse  + timedelta(seconds=600) < datetime.now())
            raise ToSoonError
        else:
            self.lastuse = datetime.now()

        full_api_url = self.api + str(self.location[1]) + '&units=' + self.unit + '&APPID=' + self.user_api
        url = urllib.request.urlopen(full_api_url)
        output = url.read().decode('utf-8')
        url.close()
        self.WeatherData = eval(output)


    def get_cloudiness(self):
        """
        Current level of Cloudiness in Percent
        :return: int: [0-100]
        """
        try:
            self.data_fetch()
        except ToSoonError:
            pass

        return self.WeatherData['clouds']['all']


    def sunrise_time(self):
        """
        Time since sunrise and until sunset [possibly negative]
        :return: tuple: (seconds since sunrise[negative if before], seconds until sunset [negative if after sunset])
        """

        sr = datetime.fromtimestamp(float(self.WeatherData['sys']['sunrise']))
        ss = datetime.fromtimestamp(float(self.WeatherData['sys']['sunset']))

        td1 = datetime.now() - sr
        td2 = ss - datetime.now()

        return (int(td1.total_seconds()), int(td2.total_seconds()))



    def is_sun_up(self):
        """
        Return boolean to tell if the sun is currently up (=its day)
        :return: bool: True if daylight, False is
        """
        sr = datetime.fromtimestamp(float(self.WeatherData['sys']['sunrise']))
        ss = datetime.fromtimestamp(float(self.WeatherData['sys']['sunset']))

        return sr < datetime.now() < ss




if __name__ == '__main__':
    reporter = WeatherReport(city_name='Berlin')

    print(reporter.WeatherData)
    with open('test.txt', mode='w') as f:
        f.write(str(reporter.WeatherData))

    print('Cloudiness: {}%'.format(reporter.get_cloudiness()))