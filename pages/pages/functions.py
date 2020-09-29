from datetime import datetime, timedelta



def convert_meteo_data(json_data, realtime_data):
    """Converts part of the data from wlgexp.json and realtime.txt into a readable dictionary"""
    data = {
        #'last_boot': datetime.fromtimestamp(json_data['lastboot']),
        #'uptime': datetime.fromtimestamp(json_data['lastboot']+json_data['uptime']) - datetime.fromtimestamp(json_data['lastboot']),
        #'datetime': datetime.fromtimestamp(json_data['loctime']),
        'temperature': {
            "unit": "C",
            "now": realtime_data['temp_now'],
            "max": {
                "value": realtime_data['temp_max'],
                "time": realtime_data['temp_max_time'],
            },
            "min": {
                "value":realtime_data['temp_min'],
                "time": realtime_data['temp_min_time'],
            },
        },
        "humidity": {
            "unit": "%",
            "now": json_data["humout"],
            "max": {
                "value": "MISSING",
                "time": "MISSING",
            },
            "min": {
                "value": "MISSING",
                "time": "MISSING",
            },
        },
        "wind": {
            "unit": "km/h",
            "now": {
                "speed": realtime_data["wind_now"],
                "dir": realtime_data["wind_dir"],
            },
            #"2min_avg": {
            #    json_data["windavg2"],
            #},
            #"10min_avg": {
            #    json_data["windavg10"],
            #},
            "gust": {
                "speed": realtime_data["gust_speed"],  #Seems wrong
                "dir": degrees_to_dir(json_data["gustdir"]),
                "time": realtime_data["gust_speed_time"],
            },
            "chill": {
                "now": realtime_data["wind_chill"],
                "min": {
                    "value": "MISSING",
                    "time": "MISSING",
                },
            },
        },
        "station_condition": {
            "temperature": farhenheit_to_celsius(json_data["tempin"]),
            "humidity": json_data['humin'],
        },
        "pressure": {
            "unit": "bar",
            "now": inches_hg_to_bar(json_data["bar"]),
            "max": {
                "value": realtime_data["pressure_max"],
                "time": realtime_data["pressure_max_time"]
            },
            "min": {
                "value": realtime_data["pressure_min"],
                "time": realtime_data["pressure_min_time"]
            }
,
        },
        "dew_point": {
            "now": farhenheit_to_celsius(json_data["cdew"]),
            "max": {
                "value": "MISSING",
                "time": "MISSING",
            },
            "min": {
                "value": "MISSING",
                "time": "MISSING",
            },
        },
        "heat_index": { #https://www.weather.gov/safety/heat-index
            "now": realtime_data["heat_index"],
            "max": {
                "value": "MISSING",
                "time": "MISSING",
            },
        },
        "rain": {
            "now": inches_to_mm(json_data["rainr"]),
            "storm": inches_to_mm(json_data["storm"]),
            "15min_avg": inches_to_mm(json_data["rain15"]),
            "1h_avg": inches_to_mm(json_data["rain1h"]),
            "today": inches_to_mm(json_data["raind"]),
            "24h_avg": inches_to_mm(json_data["rain24"]),
            "month": inches_to_mm(json_data["rainmon"]),
            "year": inches_to_mm(json_data["rainyear"]),
        },
        "evapotransporation": {
            "today": json_data["etday"],
            "month": json_data["etmon"],
            "year": json_data["etyear"],
        },
    }
    for key, value in data.items():
        for key, value in value.items():
            print(key, type(key), type(value))
    return data


def farhenheit_to_celsius(farhenheit):
    return (float(farhenheit) - 32.0) / 1.8

def ms_to_kmh(ms):
    return float(ms) * 3.6

def inches_to_mm(inch):
    return float(inch) * 25.4

def inches_hg_to_bar(hg):
    return 0.03386388158 * float(hg)

def degrees_to_dir(degrees):
    """
    Cardinal Direction 	Degrees
    N 	0
    NNE 	22.5
    NE 	45
    ENE 	67.5
    E 	90
    ESE 	112.5
    SE 	135
    SSE 	157.5
    S 	180
    SSW 	202.5
    SW 	225
    WSW 	247.5
    W 	270
    WNW 	292.5
    NW 	315
    NNW 	337.5
    """
    degrees = 180 - float(degrees)
    if degrees <= 11.25:
        return "N"
    elif degrees > 11.25:
        return "NNE"
    elif degrees > 33.75:
        return "NE"
    elif degrees > 56.25:
        return "ENE"
    elif degrees > 78.75:
        return "E"
    elif degrees > 101.25:
        return "ESE"
    elif degrees > 123.75:
        return "SE"
    elif degrees > 146.25:
        return "SSE"
    elif degrees > 168.75:
        return "S"
    elif degrees > 191.25:
        return "SSW"
    elif degrees > 213.75:
        return "SW"
    elif degrees > 236.25:
        return "WSW"
    elif degrees > 258.75:
        return "W"
    elif degrees > 281.25:
        return "WNW"
    elif degrees > 303.75:
        return "NW"
    elif degrees > 326.25:
        return "NNW"
    elif degrees > 348.75 and degrees < 360:
        return "N" 
    else:
        raise ValueError("Degrees must be included in the interval [0, 360]")