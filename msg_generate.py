import requests
import datetime
import re
import data


class msg:
    def __init__(self):
        self.weather_url = 'http://apis.juhe.cn/simpleWeather/query'
        self.says_url = 'https://apis.juhe.cn/fapig/soup/query'

        self.weather_key = 'fdf53412a291ea6dda2d112e299a8a49'
        self.says_key = '22f01ff7b766b6be7aa940ad6e4a1c0f'

        self.push_url = ''
        self.push_key = 'AT_qCPXJLwngGvyaEuCzGL5uzSdAN3tmN96'

        # emoji
        self.sun = '\U0001F31E'
        self.rain = '\U00002614'
        self.sunrise = '\U0001F305'
        self.wind = '\U0001F343'
        self.foggy = '\U0001F301'

    @staticmethod
    def date():
        week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        date = datetime.date.today()
        date_msg = re.findall(r'\d+', str(date))
        date_msg.append(week_list[datetime.date(int(date_msg[0]), int(date_msg[1]), int(date_msg[2])).weekday()])
        return date_msg

    def fetcher(self):
        params = {
            'city': '北京',
            'key': self.weather_key
        }
        weather_respond = requests.get(self.weather_url, params).json()

        params = {
            'key': self.says_key
        }
        says_respond = requests.get(self.says_url, params).json()

        print(weather_respond)
        print(says_respond)

        return weather_respond, says_respond

    @staticmethod
    def air_quality(index):
        if 0 <= index <= 50:
            return '优'
        elif 50 < index <= 100:
            return '良'
        elif 100 < index <= 150:
            return '轻度污染'
        elif 150 < index <= 200:
            return '中度污染'
        elif 200 < index <= 300:
            return '重度污染'
        elif index > 300:
            return '严重污染'

    def msg_generate(self):
        res = self.fetcher()
        weather_respond = res[0]
        says_respond = res[1]

        # only for test use
        # weather_respond = data.weather_respond
        # says_respond = data.says_respond
        if weather_respond['reason'] != '查询成功!':
            print('failed1')
            return 0
        if says_respond['reason'] != 'success':
            print('failed2')
            return 0

        weather_realtime = weather_respond['result']['realtime']
        weather_today = weather_respond['result']['future'][0]

        air_index = int(weather_realtime['aqi'])
        wind_power = weather_realtime['power']
        wind_num = re.findall(r'\d+', wind_power)

        weather = '天气：' + weather_today['weather'] + ' ' + weather_realtime['direct'] + weather_realtime[
            'power'] + '，空气质量：' + self.air_quality(air_index)
        text = says_respond['result']['text']
        reminder = '\n\n'
        date_list = self.date()
        if '雨' in weather_today['weather']:
            reminder += '今天会下雨' + self.rain + self.rain + '，记得带伞哦！'
        elif air_index > 100:
            reminder += '空气污染' + self.foggy + self.foggy + '，记得带好口罩'
        elif int(wind_num[0]) > 3:
            reminder += '大风降温' + self.wind + self.wind + '，记得多穿衣服哦'

        date = '{0}年{1}月{2}日{3} \n\n'.format(int(date_list[0]), int(date_list[1]), int(date_list[2]), date_list[3])
        msg = self.sunrise + '早啊! 一日之计在于晨\n' + self.sun + date + weather + reminder + '\n\n' + text

        print(date)
        print(msg)
        return msg

    def pusher(self):
        reminder_uids = [
            "UID_7okP3g4zL5BZSOczzPsbJYSQY19E",
        ]

        # the_uids = 'UID_7okP3g4zL5BZSOczzPsbJYSQY19E'

        url = 'http://wxpusher.zjiecode.com/api/send/message'
        post_data = {
            "appToken": self.push_key,
            "content": self.msg_generate(),
            "contentType": 1,
            "uids": reminder_uids
        }
        data = self.post_third_api(url, post_data)
        return data

    @staticmethod
    def post_third_api(url, data):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        res = requests.post(
            url=url,
            json=data,
            headers=headers
        )

        try:
            return res.json()
        except:
            return False


if __name__ == '__main__':
    m = msg()
    m.pusher()
