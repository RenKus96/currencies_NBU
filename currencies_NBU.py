# -*- coding: utf-8 -*-
import requests
from datetime import datetime

def in_log(s):
    log_out = open('log.txt', "a+")
    log_out.write('-----------------\n')
    log_out.write('Дата обработки: {}\n'.format(datetime.now()))
    log_out.write(s)
    log_out.close()

def getFromHTTP(fromHTTP):
    try:
        p = requests.get(fromHTTP)
    except requests.exceptions.RequestException as err:
        in_log("Нет доступа к данным {} по причине --> {}\n".format(fromHTTP, err))
        return False, None
    if p.status_code == 200:
        return True, p.json()
    else:
        if p.status_code == 404:
            in_log("Страница с данными не найдена.\n")
            return False, None
        else:
            in_log("Нет доступа к данным --> код ответа {}\n".format(p.status_code))
            return False, None

def getdate():
    while True:
        date = input('Введите дату (dd.mm.yyyy): ')
        try:
            return datetime.strptime(date, '%d.%m.%Y')
        except:
            print('Неверный формат даты: {}'.format(date))

def getvalute():
    while True:
        val = input('Введите сокращённое обозначение валюты (USD,EUR,...) или пусто для вывода всего списка:')
        if val=='' or (val.isalpha() and len(val)==3):
            return val.upper()
        else:
            print('Неверный формат валюты.')
            
def get_val():
    rate_date = getdate()
    val = getvalute()
#    res, rate = getFromHTTP("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&valcode={}&date={}".format(val,rate_date.strftime("%Y%m%d")))
    resOk, rate = getFromHTTP("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json")
    if resOk:
        out = open('currencies_NBU_{}.txt'.format(rate_date.strftime("%Y-%m-%d")), "w")
        out.write('Курси гривні до іноземної валюти станом на {}:\n'.format(rate_date.strftime("%d.%m.%Y")))
        find_val=False
        for valute in rate:
            out.write('{} ({}) to UAH: {}\n'.format(valute['txt'],valute['cc'],valute['rate']))
            if val=='' or val==valute['cc']:
                print('По состоянию на {} курс {} ({}) по отношению к UAH: {}'.format(rate_date.strftime("%d.%m.%Y"),valute['txt'],valute['cc'],valute['rate']))
                find_val = True
        if val!='':
            if not find_val: 
                print('Курс указанной валюты не был найден.')
            print('Список курсов гривны к иностранной валюте вы можете посмотреть в файле currencies_NBU_{}.txt'.format(rate_date.strftime("%Y-%m-%d")))
        out.close()
    else:
        print('Ошибка доступа к данным курса валют (см. файл log.txt)')	
        
if __name__ == '__main__':
	get_val()

    
    

