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