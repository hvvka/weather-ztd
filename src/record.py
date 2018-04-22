import math


class Record:

    def __init__(self, date, time, station_id, pressure_marker, lat, lon, x_coord, y_coord, aerial_height, wrf_height,
                 temperature, humidity_relative, pressure):
        self.date = date
        self.time = time
        self.station_id = station_id
        self.pressure_marker = pressure_marker  # 2m/interp
        self.lat = lat
        self.lon = lon
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.aerial_height = aerial_height
        self.wrf_height = wrf_height
        self.temperature = temperature
        self.humidity_relative = humidity_relative
        self.pressure = pressure

    def count_ztd(self):
        e_sat = 6.112 * math.exp(
            (17.67 * (float(self.temperature) - 273.15) / ((float(self.temperature) - 273.15) + 243.5)))
        r = 8.31432  # [N*m/mol*K]
        gamma = 0.0065  # temperature gradient
        e = float(self.humidity_relative) * e_sat / 100
        g = 9.8063 * (1 - pow(10, -7) * (float(self.wrf_height) + float(self.aerial_height)) / 2 * (
                1 - 0.0026373 * math.cos(2 * math.radians(float(self.lat)))) + 5.9 * pow(10, -6) * pow(
            math.cos(2 * math.radians(float(self.lat))), 2))
        m = 0.0289644  # [kg/mol]
        if self.pressure_marker == "2m":
            p = float(self.pressure) * pow((float(self.temperature) - gamma * (
                    float(self.aerial_height) - float(self.wrf_height)) / float(self.temperature)),
                                           g * m / r * gamma)
        else:
            p = float(self.pressure)
        zdt = 0.002277 * (p + (1255 / float(self.temperature) + 0.05) * e)
        return zdt

    def get_date(self):
        return str(self.date + " " + self.time)
