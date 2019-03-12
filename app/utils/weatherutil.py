import requests
from app.utils import status

def getWeather(city):
    if not city:
        return {'code': status.CODE_EMPTY}
    try:
        url = 'https://free-api.heweather.com/s6/weather?key=3bdb079579b7450580ae02a4efa72c09&location={city}'.format(
            city = city
        )
        resp = requests.get(url)
        res = resp.json()['HeWeather6'][0]

        if res['status'] ==  "unknown location":
            return {'code' : status.CODE_NOT_EXIST}
        elif res['status'] !=  'ok':
            return {'code' : status.CODE_UNKNOW}

        today_forecast = res['daily_forecast'][0]
        today_lifestyle = res['lifestyle']

        _city = res['basic']['location']
        _time = today_forecast['date']
        _rays = today_forecast['uv_index']

        _temp_min = today_forecast['tmp_min']
        _temp_max = today_forecast['tmp_max']
        _temp = "{}~{}℃".format(_temp_min, _temp_max)

        _day = today_forecast['cond_txt_d']
        _night = today_forecast['cond_txt_n']
        _weather = "白天：{}，晚上：{}".format(_day, _night)

        _wind_sc = today_forecast['wind_sc']
        _wind_dir = today_forecast['wind_dir']
        _wind = "{}，{}级".format(_wind_dir, _wind_sc)

        _flud, _suggest = "", ""
        for style in today_lifestyle:
            if style['type'] == "flu":
                _flud, _suggest = style['brf'], style['txt']

        result = {
            'city' : '【城市】' + _city,
            'tempture' : '【气温】' + _temp,
            'time' : '【时间】' + _time,
            'wind' : '【风向】' + _wind,
            'weather' : '【天气】' + _weather,
            'rays' : '【紫外线】' + _rays,
            'flud' : '【感冒指数】' + _flud,
            'suggest' : '【温馨建议】' + _suggest
        }
        return {'code' : status.CODE_SUCCESS, 'data' : result}
    except:
        return {'code' : status.CODE_FAILED}
    

if __name__ == '__main__':
    print(getWeather('保定'))
