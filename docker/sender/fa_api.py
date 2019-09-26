import datetime

from lxml import html


class TTClass(object):

    def __init__(self, session_token, group_id, config):
        self.config = config
        self.session_token = session_token
        self.group_id = group_id
        self.get_text_tt()
        self.get_json_tt()

    def get_text_tt(self):
        """
        Метод для получения расписания в виде текста
        """
        print("get_text_tt headers:", self.config["headers"])
        session = self.session_token
        today = datetime.datetime.today() + datetime.timedelta(hours=0)

        data = {
            "Date": today,
            "DateBegin": today.strftime('%d.%m.%Y'),
            "DateEnd": today.strftime('%d.%m.%Y'),
            "JobType": "GROUP",
            "GroupId": self.group_id
        }

        r = session.post(self.config["url"]+'/Job/SearchAjax', data=data, headers=self.config["headers"])
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
                disc['teachers_id'] = [int(item) for item in
                                       row.xpath('./td[@data-field="tutors"]/div/button/@data-id')]
                disc['teachers_name'] = [item.strip() for item in
                                         row.xpath('./td[@data-field="tutors"]/div/button/text()')]
                disc['groups'] = str(', '.join(
                    [item.strip() for item in row.xpath('./td[@data-field="groups"]/span/text()')]))
                schedule[current_date].append(disc)
        self.tt = schedule   