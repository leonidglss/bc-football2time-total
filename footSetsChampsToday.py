import time
import requests
# from champs_football import strChamps
from dbase_football import Database
from datetime import datetime
import jmespath
# from botConfig import BOT_ADRES_BASKET, BOT_NAME_BASKET, BOT_TOKEN_BASKET

# db=Database('basket.db')
db=Database('dBases/football.db')
to_day_ts=int(datetime.now().timestamp())


headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}

response=requests.get('https://ad.betcity.ru/d/off/events')
result=response.json()

sport="1"
fileChamps='FootballChamps.txt'

# 1683323100  -  2023-05-06 00:45
def dateFromTS(ts):
    dateti=datetime.fromtimestamp(ts)
    year=dateti.year
    month=dateti.month
    day=dateti.day
    dayStr=str(year)+'-'+str(month)+'-'+str(day)
    return dayStr
def TSfromDate(strDt):
    s=strDt.replace('-','/')
    stamp=time.mktime(datetime.strptime(s, "%Y/%m/%d").timetuple())  # timestamp 1683234000.0
    return stamp
def write_txt(file,data):
    with open(f'{file}', 'w', encoding='utf-8-sig') as f:
        f.write(data)
def add_txt(file,data):
    with open(f'{file}', 'a', encoding='utf-8-sig') as f:
        f.write(data+'\n')
def read_txt(file):
    with open(f'{file}', encoding='utf-8-sig') as file:
        data = file.read()
    return data

# Все чемпионаты офлайн для списка. На входе (вид спорта). На выходе массив ['Имя чемпа 1','Имя чемпа 2'....]
def update_champs(result,sport,file):
    write_txt(file,'')
    list_0=read_txt(file)
    list_1=list_0.split('\n')[::-1]
    
    champs_arr=result['reply']['sports'][sport]['chmps']
    chmpes=[]
    for chm in champs_arr:
        name_ch=result['reply']['sports'][sport]['chmps'][chm]['name_ch']

        if 'Победитель' in name_ch or 'Итоги' in name_ch or 'из какой страны' in name_ch or 'голов' in name_ch or 'Кто выше' in name_ch or 'Лучший' in name_ch or 'Статистика' in name_ch or 'по итогам' in name_ch or 'клубы выиграют' in name_ch or 'cравнение' in name_ch or 'забьёт' in name_ch or 'команды' in name_ch or 'Выход' in name_ch or '3x3' in name_ch or '5x5' in name_ch or '7x7' in name_ch or 'команда' in name_ch or 'Кол-во' in name_ch or 'выиграет' in name_ch or 'Специальные' in name_ch or 'Результаты сборной' in name_ch or 'независимо от' in name_ch or 'Физический этап' in name_ch or 'Спец. ставки' in name_ch or 'забьет гол' in name_ch or 'Киберфутбол' in name_ch or 'Кол-во очков' in name_ch or 'под руководством' in name_ch or 'Специальные ставки' in name_ch or 'Видеопросмотры' in name_ch or 'нет в старт. сост.' in name_ch or 'ни одного трофея' in name_ch or 'Лидер' in name_ch or 'рекорд' in name_ch or 'Сравнение' in name_ch or 'Какие' in name_ch or 'Пара' in name_ch or 'хет-трик' in name_ch:
            pass
        else:
            if "'" in name_ch:
                name_ch=name_ch.replace("'", "-")
            elif '"' in name_ch:
                name_ch=name_ch.replace('"', '-')
            else:
                pass
            
            if name_ch in list_1:
                pass
            else:
                chmpes.append(name_ch)
                add_txt(file,name_ch)
    return chmpes


data=update_champs(result, sport,fileChamps)
print(data)


