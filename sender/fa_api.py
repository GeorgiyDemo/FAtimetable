import requests
import yaml

class GetSettingsClass(object):

    def __init__(self):
        self.get_settings()

    def get_settings(self):
        with open("./settings_dev.yml", 'r') as stream:
            self.config = yaml.safe_load(stream)

class FaClass(object):

    def __init__(self):

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
        }
        s = GetSettingsClass()
        self.login = str(s.config["login"])
        self.passwd = str(s.config["password"])
        self.url = s.config["url"]
        self.__get_token()

    def __get_token(self):
        """
        Получение токена авторизации по логину и паролю
        """
        raw_data = "Login="+self.login+"&Pwd="+self.passwd
        r = requests.post(self.url+"mCoreAccount/Auth", data=raw_data, headers=self.headers).json()
        if r["ResultCode"] != -100:
            self.token = r["Data"]["Token"]
            self.id = r["Data"]["Id"]
            self.login = ""
            self.passwd = ""
        else:
            raise Exception("Ошибка авторизации")
    
    def get_group(self):
        """
        Получение группы пользователя
        """
        raw_data = "Id="+str(self.id)+"&Token="+self.token
        r = requests.post(self.url+"mGosvpoAccount/Groups", data=raw_data, headers=self.headers).json()
        return r

    def get_userinfo(self):
        """
        Получение основной информации о пользователе
        """
        raw_data = "Id="+str(self.id)+"&Token="+self.token
        r = requests.post(self.url+"mCore/UserInfo", data=raw_data, headers=self.headers).json()
        return r
    
    def get_photo(self):
        """
        Получение фото профиля пользователя
        """
        r = requests.get(self.url+"mCore/UserImg?Token="+self.token+"&Id="+self.id).content
        return r
    
    #TODO Нет прав доступа к указанной группе
    def get_tutor_program(self):
        """
        Получение информации о профиле подготовки
        """
        raw_data = "Id="+str(self.id)+"&Token="+self.token
        r = requests.post(self.url+"mGosvpoGroup/Info", data=raw_data, headers=self.headers).json()
        return r

    #TODO исправить ссылку
    def get_full_tutor_program(self, stage):
        """
        Получение учебного плана по семестрам 
        - Принимает номер семестра stage
        """
        raw_data = "Token="+self.token+"&Id="+str(self.id)+"&Stage="+str(stage)
        r = requests.post(self.url+"mCore/UserInfo", data=raw_data, headers=self.headers).json()
        return r

    def get_timetable_byday(self, date):
        """
        Получение информации о расписании на конкретную дату date
        - Принимает дату date в формате 01.01.2018
        """
        raw_data = "UserId="+str(self.id)+"&Token="+self.token+"&Date="+date
        r = requests.post(self.url+"mGosvpoAccount/TimeTable", data=raw_data, headers=self.headers).json()
        return r
    
    def get_marks_bystage(self, group_id, stage):
        """
        Получение оценок в зачётке по семестрам
        - Принимает id группы group_id с метода get_group
        - Принимает номер семестра stage
        """
        raw_data = "UserId="+str(self.id)+"&Token="+self.token+"&GroupId="+str(group_id)+"&Stage="+str(stage)
        r = requests.post(self.url+"mFaAccount/MarksByStage", data=raw_data, headers=self.headers).json()
        return r

    def log_off_user(self):
        """
        Выход из приложения (обнуление токена авторизации)
        """
        raw_data = "Token=GMy3CH744qunaTCBib27isA"
        r = requests.post(self.url+"mCoreAccount/LogOff", data=raw_data, headers=self.headers).json()
        return r

    #TODO Допилить другие методы