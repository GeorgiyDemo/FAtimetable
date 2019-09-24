import requests
import datetime
import time
import yaml
from lxml import html

YAML_FILE = "groups.yml"

class YamlClass(object):
    def __init__(self, d):
        self.d = d
        self.y_get()
        # self.y_set()

    def y_get(self):
        # Чтение из файла
        with open(YAML_FILE, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        self.result = data_loaded

    def y_set(self):
        # Запись в файл
        with open(YAML_FILE, 'w') as outfile:
            yaml.safe_dump(self.d, outfile, default_flow_style=False, allow_unicode=True)

class FATokenClass(object):
    """
    Класс для получения токена и id пользователя ИОП 

    - Авторизуется с логином/паролем в settings.yaml
    - В self.user_data отдаёт tuple с токеном и id пользователя
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }
        self.get_token_site()

    def get_token_site(self):
        session = requests.session()
        session.cookies['ASP.NET_SessionId'] = self.get_cookies_site()

        # Устанавливаем сессию requests с токеном
        self.user_token = session

    def get_cookies_site(self):
        """
        Получение cookies по логину и паролю на сайте ИОП
        """
        session = requests.session()
        response = session.post('https://portal.fa.ru/CoreAccount/LogOn',
                                data={'Login': 191770, 'Pwd': "Demka_1234"},
                                headers=self.headers, allow_redirects=True)
        data = session.cookies['ASP.NET_SessionId']
        session.close()
        if response.url == 'https://portal.fa.ru/CoreAccount/Portal':
            return data
        else:
            raise ValueError('Не могу авторизоваться!')

class TTClass(object):

    def __init__(self, session_token, group_id):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }
        self.session_token = session_token
        self.group_id = group_id
        self.get_text_tt()
        self.get_json_tt()

    def get_text_tt(self):
        """
        Метод для получения расписания в виде текста
        """
        session = self.session_token
        today = datetime.datetime.today() + datetime.timedelta(hours=0)
        end_day = today + datetime.timedelta(days=1, hours=0)

        data = {
            "Date": today,
            "DateBegin": today.strftime('%d.%m.%Y'),
            "DateEnd": end_day.strftime('%d.%m.%Y'),
            "JobType": "GROUP",
            "GroupId": self.group_id
        }

        r = session.post('https://portal.fa.ru/Job/SearchAjax', data=data, headers=self.headers)
        self.tt = r.text

    def get_json_tt(self):
        """
        Метод который полностью стырили у Димы @FlymeDllVa
        По-хорошему потом надо его переписать с bs4
        """
        table = html.fromstring(self.tt)
        schedule = {}
        current_date = ''
        for row in table.xpath('//tr[@class="rowDisciplines"] | //tr[@class="rowDate warning"]'):
            if row.classes.pop() == 'rowDate':
                current_date = str(row.xpath('./td[@data-field="datetime"]/text()')[0].split(' ')[0].replace("/", "."))
                schedule.update({current_date: []})
            else:
                disc = {}
                time_block = row.xpath('./td[@data-field="datetime"]/div/text()')
                disc['time_start'] = str(time_block[0])
                disc['time_end'] = str(time_block[1])
                disc['type'] = str(time_block[2]) if len(time_block) > 2 else None
                disc['name'] = str(row.xpath('./td[@data-field="discipline"]/text()')[0].strip())
                disc['location'] = str((lambda item: item[0] if item else None)(
                    row.xpath('./td[@data-field="tutors"]/div/div/i/small/text()')))
                disc['audience'] = str(', '.join(
                    [i.strip()[:-1].strip() for i in row.xpath('./td[@data-field="tutors"]/div/div/i/text()') if
                     i.strip()[:-1] != '']
                ).strip())
                disc['teachers_id'] = str([int(item) for item in
                                       row.xpath('./td[@data-field="tutors"]/div/button/@data-id')])
                disc['teachers_name'] = str([item.strip() for item in
                                         row.xpath('./td[@data-field="tutors"]/div/button/text()')])
                disc['groups'] = str(', '.join(
                    [item.strip() for item in row.xpath('./td[@data-field="groups"]/span/text()')]))
                schedule[current_date].append(disc)
        self.tt = schedule    

def main():

    UNIVERSAL_DICT = {}

    login_obj = FATokenClass()
    obj = YamlClass("")
    #Словарь с группами
    GROUP_DICT = obj.result

    for e in GROUP_DICT:
        GROUP_ID = GROUP_DICT[e]
        fa = TTClass(login_obj.user_token, GROUP_ID)
        print("Расписание",e,GROUP_DICT[e])
        print(fa.tt)
        UNIVERSAL_DICT[GROUP_ID]= fa.tt
        with open("tt.yml", 'w') as outfile:
            yaml.safe_dump(UNIVERSAL_DICT, outfile, default_flow_style=False, allow_unicode=True)


    
if __name__ == "__main__":
    main()