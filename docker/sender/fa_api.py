import requests
import yaml
from lxml import html
import datetime

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

        data ={
            "Date" : today,
            "DateBegin" : today.strftime('%d.%m.%Y'),
            "DateEnd" : end_day.strftime('%d.%m.%Y'),
            "JobType" : "GROUP",
            "GroupId" : self.group_id
        }

        r = session.post('https://portal.fa.ru/Job/SearchAjax', data=data,headers=self.headers)
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
                current_date = row.xpath('./td[@data-field="datetime"]/text()')[0].split(' ')[0].replace("/", ".")
                schedule.update({current_date: []})
            else:
                disc = {}
                time_block = row.xpath('./td[@data-field="datetime"]/div/text()')
                disc['time_start'] = time_block[0]
                disc['time_end'] = time_block[1]
                disc['type'] = time_block[2] if len(time_block) > 2 else None
                disc['name'] = row.xpath('./td[@data-field="discipline"]/text()')[0].strip()
                disc['location'] = (lambda item: item[0] if item else None)(
                    row.xpath('./td[@data-field="tutors"]/div/div/i/small/text()'))
                disc['audience'] = ', '.join(
                    [i.strip()[:-1].strip() for i in row.xpath('./td[@data-field="tutors"]/div/div/i/text()') if
                    i.strip()[:-1] != '']
                ).strip()
                disc['teachers_id'] = [int(item) for item in row.xpath('./td[@data-field="tutors"]/div/button/@data-id')]
                disc['teachers_name'] = [item.strip() for item in row.xpath('./td[@data-field="tutors"]/div/button/text()')]
                disc['groups'] = ', '.join([item.strip() for item in row.xpath('./td[@data-field="groups"]/span/text()')])
                schedule[current_date].append(disc)
        self.tt = schedule