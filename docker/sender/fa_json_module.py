SMS_SUBJECT_LEN = 22

class JSONProcessingClass(object):
    """
    Класс для обработки JSON с расписанием от FA API
    """
    def __init__(self, group_name, tt):
        
        self.group_name = group_name
        self.tt = tt
        self.json_decoder()

    def json_decoder(self):
        outstring = "Расписание группы "+self.group_name + " "
        tt = self.tt
        for day in tt:
            outstring += day+"\a"
            for i in range(len(tt[day])):
                #Инициалы учителя
                teacher_name = tt[day][i]["teachers_name"][0].split(" ")
                new_teacher = teacher_name[0]+" "+teacher_name[1][0]+"."+teacher_name[2][0]+"."

                subject = tt[day][i]["name"]
                #Если сообщение слишком длинное, то принудительно сокращаем..
                addstring = str(i+1)+". "+subject +" "+tt[day][i]["time_start"]+"-"+tt[day][i]["time_end"] + \
                     "\n"+new_teacher+", "+tt[day][i]["audience"]+"\a"

                if len(addstring) > 70:
                    while len(addstring) > 70:
                        subject = subject[:len(subject)-3]+".."
                        addstring = str(i+1)+". "+subject +" "+tt[day][i]["time_start"]+"-"+tt[day][i]["time_end"] + \
                            "\n"+new_teacher+", "+tt[day][i]["audience"]+"\a"
                
                outstring += addstring
        self.outstring = outstring


def main():
    json = {'23.09.2019': [{'time_start': '11:50', 'time_end': '13:20', 'type': 'Семинар', 'name': 'Иностранный язык', 'location': 'Ул. Щербаковская/дом 38', 'audience': '410, 609а, 701, 703', 'teachers_id': ["24500", "168195", "151340", "142887"], 'teachers_name': ['Есина Людмила Сергеевна', 'Калмыкова Инна Игоревна', 'Амосов Николай Васильевич', 'Кувшинова Екатерина Евгеньевна'], 'groups': 'ПИ19-3, ПИ19-4, ПИ19-5'}, {'time_start': '14:00', 'time_end': '15:30', 'type': 'Лекция', 'name': 'Математика', 'location': 'Ул. Щербаковская/дом 38', 'audience': '602', 'teachers_id': ["1886"], 'teachers_name': ['Щиголев Владимир Викторович'], 'groups': 'ПИ19-3, ПИ19-4, ПИ19-5'}, {'time_start': '15:40', 'time_end': '17:10', 'type': 'Семинар', 'name': 'Дискретная математика', 'location': 'Ул. Щербаковская/дом 38', 'audience': '711', 'teachers_id': [24295], 'teachers_name': ['Чечкин Александр Витальевич'], 'groups': 'ПИ19-4'}, {'time_start': '17:20', 'time_end': '18:50', 'type': 'Семинар', 'name': 'Алгоритмы и структуры данных в языке Python (по выбору)', 'location': 'Ул. Щербаковская/дом 38', 'audience': '508(кк)', 'teachers_id': ["310739"], 'teachers_name': ['Петросов Давид Арегович'], 'groups': 'ПИ19-4'}]}
    json_alter = {'23.09.2019': [{'time_start': '08:30', 'time_end': '10:00', 'type': 'Семинар', 'name': 'Практикум по программированию', 'location': 'Ул. Щербаковская/дом 38', 'audience': '510(кк)', 'teachers_id': [167734], 'teachers_name': ['Милованов Даниил Михайлович'], 'groups': 'ПИ19-2'}, {'time_start': '10:10', 'time_end': '11:40', 'type': 'Семинар', 'name': 'Иностранный язык', 'location': 'Ул. Щербаковская/дом 38', 'audience': '701, 702, 703', 'teachers_id': [151340, 24500, 142887], 'teachers_name': ['Амосов Николай Васильевич', 'Есина Людмила Сергеевна', 'Кувшинова Екатерина Евгеньевна'], 'groups': 'ПИ19-1, ПИ19-2'}, {'time_start': '11:50', 'time_end': '13:20', 'type': 'Лекция', 'name': 'Дискретная математика', 'location': 'Ул. Щербаковская/дом 38', 'audience': '502', 'teachers_id': [24295], 'teachers_name': ['Чечкин Александр Витальевич'], 'groups': 'ПИ19-1, ПИ19-2'}, {'time_start': '14:00', 'time_end': '15:30', 'type': 'Семинар', 'name': 'Дискретная математика', 'location': 'Ул. Щербаковская/дом 38', 'audience': '711', 'teachers_id': [24295], 'teachers_name': ['Чечкин Александр Витальевич'], 'groups': 'ПИ19-2'}]}
    obj = JSONProcessingClass("ПИ19-4",json)

if __name__ == "__main__":
    main()