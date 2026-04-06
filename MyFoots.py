# ------ Бот ставок на фаворита ------------
import time
import requests
from dbase_football import Database
from datetime import datetime

from botConfig import BOT_ADRES_FOOTBALL_WIN, BOT_NAME_FOOTBALL_WIN, WTS_TOKEN_FOOTBALL_WIN
from teleBot import sends_telegram
from multiprocessing import Pool

BOT_INFO='''
Это бот для футбола. Ставка на Второй тайм. REQUESTS.
'''

BOT_TOKEN=WTS_TOKEN_FOOTBALL_WIN

def write_txt(file,data):
    with open(f'{file}', 'w', encoding='utf-8-sig') as f:
        f.write(data)
def read_txt(file):
    with open(f'{file}', encoding='utf-8-sig') as file:
        data = file.read()
    return data
def add_txt(file,data):
    with open(f'{file}', 'a', encoding='utf-8-sig') as f:
        f.write(data+'\n')
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


def sendVideo(data):   # data=['url_video', 'chat_id']
    url='https://api.telegram.org/bot'
    arr=''
    files = {'video': open(data[0], 'rb')}
    r=requests.post(f'{url}{BOT_TOKEN}/sendVideo?chat_id={data[1]}', files=files)
    arr+=str(data[1])+'-'+ str(r.json()['result']['message_id'])
    add_txt(f'mess_{data[1]}.txt',arr)
    return arr         # arr str 'chat_id - message_id'
def sendPhoto(data):   # data=['url_photo', 'chat_id']
    url='https://api.telegram.org/bot'
    arr=''
    files = {'photo': open(data[0], 'rb')}
    r=requests.post(f'{url}{BOT_TOKEN}/sendPhoto?chat_id={data[1]}', files=files)
    arr+=str(data[1])+'-'+ str(r.json()['result']['message_id'])
    add_txt(f'mess_{data[1]}.txt',arr)
    return arr         # arr str 'chat_id - message_id'
def sendMessage(data):  # data=['text', 'chat_id']
    url='https://api.telegram.org/bot'
    url+=BOT_TOKEN
    method=url+'/sendMessage'
    arr=''
    text=data[0]
    r=requests.post(method,data={
        'chat_id': data[1],
        'text': text,
        'parse_mode': 'HTML'
    })
    arr+=str(data[1])+'-'+ str(r.json()['result']['message_id'])
    add_txt(f'mess_{data[1]}.txt',arr)
    return arr         # arr str 'chat_id - message_id'
def delMessages(id):
    token=BOT_TOKEN
    url='https://api.telegram.org/bot'
    url+=token
    method=url+'/deleteMessage'
    file=f'mess_{id}.txt'
    strMess=read_txt(file)
    try:
        arrMess=strMess.split('\n')
        for mess in arrMess:
            mes=mess.split('-')
            print(mes)
        
            chat_id=mes[0]
            mess_id=mes[1]
            r=requests.post(method,data={
                'chat_id': chat_id,
                'message_id': mess_id,
                'parse_mode': 'HTML'
            })
    except:
        pass
    write_txt(file,'')


def poolDelMess(arraD):
    c=len(arraD)
    if c!=0:
        with Pool(c) as p:
            p.map(delMessages, arraD)
def poolVideo(strVid,arraV):
    c=len(arraV)
    if c!=0:
        mesRano=strVid
        r_ar=[]
        for id in arraV:
            rano_ar=[]
            rano_ar.append(mesRano)
            rano_ar.append(int(id))
            r_ar.append(rano_ar)
        print(c,r_ar)
        with Pool(c) as p:
            p.map(sendVideo, r_ar)
def poolPhoto(strPh,arraP):
    c=len(arraP)
    if c!=0:
        mesRano=strPh
        r_ar=[]
        for id in arraP:
            rano_ar=[]
            rano_ar.append(mesRano)
            rano_ar.append(int(id))
            r_ar.append(rano_ar)
        print(c,r_ar)
        with Pool(c) as p:
            p.map(sendPhoto, r_ar)
def poolMess(strMes,arraM):  # strMes-text  arraM=['1234', '4567', '6789']
    c=len(arraM)
    if c!=0:
        mesRano=strMes
        r_ar=[]
        for id in arraM:
            rano_ar=[]
            rano_ar.append(mesRano)
            rano_ar.append(int(id))
            r_ar.append(rano_ar)
        
        print(c,r_ar)
        with Pool(c) as p:
            p.map(sendMessage, r_ar)


db=Database('dBases/Foot2timeTotal.db')

headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}

response=requests.get('https://ad.betcity.ru/d/off/events',headers=headers)
res=response.json()

sport="1"
to_day_ts=int(datetime.now().timestamp())

kf=1.5
Timer=False

Int_start=44  # Через сколько минут после времени начала запускать запросы
Int_time=10  # Сколько минут после времени начала разрешать запросы

# list_0=read_txt('FootballChamps.txt')
# strChamps=list_0.split('\n')
# strChamps=strChamps.pop(0)
times_arr=[]

write_txt('timer_big.txt', str(to_day_ts))
write_txt('timer_sml.txt', str(to_day_ts))

# Получаем игру офлайн по номеру. На входе (json,вид спорта,чемп,номер игры, название чемпа). Запись в базу. На выходе строка. 
def get_game_ofline(result, spt, champ, game, ch_name):
    now_str=result['reply']['curr_time']
    now_ts=result['reply']['ntime_vg']
    # Игра за номером 11212104 дата, дата(тс), макс ставка, команда хозяев, команда гостей
    game_date=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['date_ev_str']
    game_date_ts=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['date_ev']
    try:
        maximum=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['maximum']
    except:
        maximum=0
    team_1=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['name_ht']
    team_2=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['name_at']
    
    game_date=result['reply']['sports'][sport]['chmps'][champ]['evts'][game]['date_ev_str']

    # Игра за номером game ставки на исход
    try:
        bets_main=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['main']['69']
        bets_main_name=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['main']['69']['name']
        win1=bets_main['data'][game]['blocks']['Wm']['P1']['kf']
        win2=bets_main['data'][game]['blocks']['Wm']['P2']['kf']
        xxx=bets_main['data'][game]['blocks']['Wm']['X']['kf']
    except:
        bets_main_name='No bets'
        win1='66.6'
        win2='66.6'
        xxx='---'
    

    # Игра за номером game основная фора
    try:
        bets_fora=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['main']['71']
        bets_fora_name=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['main']['71']['name']
        fora1how=bets_fora['data'][game]['blocks']['F1m']['F1']    # float
        fora1kf=bets_fora['data'][game]['blocks']['F1m']['Kf_F1']['kf']   # float
        fora2how=bets_fora['data'][game]['blocks']['F1m']['F2']    # float
        fora2kf=bets_fora['data'][game]['blocks']['F1m']['Kf_F2']['kf']   # float
    except:
        fora1how='No'
        fora1kf='---'
        fora2how='No' 
        fora2kf='---'

    # Игра за номером game основные тоталы
    strRes=''
    try:
        bets_total=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['main']['72']
        bets_total_name=result['reply']['sports'][spt]['chmps'][champ]['evts'][game]['main']['72']['name']
        total_how=bets_total['data'][game]['blocks']['T1m']['Tot']    # float
        total_big=bets_total['data'][game]['blocks']['T1m']['Tb']['kf']   # float
        total_lit=bets_total['data'][game]['blocks']['T1m']['Tm']['kf']   # float
        # print('Total: ',total_how)
        if float(total_how)>2.9 and float(total_big)<2.5:
            db.save_bet_in_db(int(game),int(champ),ch_name,now_str,now_ts,game_date,game_date_ts,maximum,team_1,team_2,str(win1),str(xxx),str(win2),str(fora1how),str(fora1kf),str(fora2kf),str(total_how),str(total_big),str(total_lit))
    except:
        pass
    
    return strRes

# id_game,id_ch,name_ch,time_rec_str,time_rec_ts,time_begin_str,time_begin_ts,maximum,team_1,team_2,P1,X,P2,FF,F1,F2,TT,TB,TM

# Получаем игры по номеру чемпа. На входе (json,вид спорта,чемп). 
def get_games_in_champ_off(result, sport, champ):
    ch_name=result['reply']['sports'][sport]['chmps'][champ]['name_ch']
    games_arr=result['reply']['sports'][sport]['chmps'][champ]['evts']
    games=[]
    for game in games_arr:
        games.append(game)
        get_game_ofline(result, sport, champ, game, ch_name)

# Получаем игры офлайн. На входе (вид спорта).       
def saved_ofline_games(sport,headers):
    list_0=read_txt('FootballChamps.txt')
    strChamps=list_0.split('\n')
    response=requests.get('https://ad.betcity.ru/d/off/events', headers)
    result=response.json()
    champs_arr=result['reply']['sports'][sport]['chmps']
    chmpes=[]
    for chm in champs_arr:
        cham=result['reply']['sports'][sport]['chmps'][chm]['name_ch']
        if cham in strChamps:
            chmpes.append(chm)
            get_games_in_champ_off(result, sport, chm)

# id_game,id_ch,name_ch,time_rec_str,time_rec_ts,time_begin_str,time_begin_ts,maximum,team_1,team_2,P1,P2,FF,F1,F2,TT,TB,TM
# ===========================================================================================================================

# ---- Игры, которые есть в базе офлайн -----------
def games_in_db_off():
    games_off=db.get_num_bets()
    list_games=[]
    for f_of in games_off:
        ch=db.get_ch_bet(f_of[0])
        g=str(f_of[0])+';'+str(ch[0])
        list_games.append(g) 
    return list_games   # ['11839590;567']
# -------------------------------------------------- 
# -- Игры, которые есть в моих играх офлайн --------
def mygames_in_db_off():
    games_off=db.get_num_mybets()
    list_games=[]
    for f_of in games_off:
        list_games.append(str(f_of[0])) 
    return list_games
# -------------------------------------------------- 
# -- Игры, которые идут сейчас онлайн --------------
def games_online(result, sport,headers):
    list_0=read_txt('FootballChamps.txt')
    strChamps=list_0.split('\n')
    champs_arr=result['reply']['sports'][sport]['chmps']
    chmpes=[]
    for chm in champs_arr:
        cham=result['reply']['sports'][sport]['chmps'][chm]['name_ch']
        if cham in strChamps:
            chmpes.append(chm)

    list_games=[]
    # game_a=[]
    for ch in chmpes:
        g_ch=result['reply']['sports'][sport]['chmps'][ch]['evts']
        for game in g_ch:
            g=str(game)+';'+str(ch)
            list_games.append(g)   # ['13107543;122157', '13016575;873', '13022156;11752']

    return list_games

def get_ofline_bet(id_game):
    data=db.get_bet(id_game)
    return data

def get_times_begin_array():
    t=[]
    times=db.get_times_begin()
    for t_time in times:
        t.append(t_time[0])
    t.sort()
    return t

def req_may_do(times_arr, to_day_ts_loop,Int_start,Int_time):
    if len(times_arr) == 0:
        # print('No Array')
        return False
    for t in times_arr:
        time_start=t+Int_start*60
        time_stop=time_start+Int_time*60
        if to_day_ts_loop>time_start and to_day_ts_loop<time_stop:
            return True
    # print(times_arr)
    return False

def get_total_kf(result,sport,champ,game,kf):
    try:
        tot_main=result['reply']['sports'][sport]['chmps'][champ]['evts'][game]['main']['72']['data'][game]['blocks']['T1m']['Tot']
    except:
        tot_main=0
    if tot_main==kf:
        koef_r=result['reply']['sports'][sport]['chmps'][champ]['evts'][game]['main']['72']['data'][game]['blocks']['T1m']['Tb']['kf']
        return koef_r
    else:
        try:
            tot_arr=result['reply']['sports'][sport]['chmps'][champ]['evts'][game]['ext']['112']['data']
            for tot in tot_arr:
                tot_1=result['reply']['sports'][sport]['chmps'][champ]['evts'][game]['ext']['112']['data'][tot]['blocks']['T']['Tot']
                if tot_1==kf:
                    koef_r=result['reply']['sports'][sport]['chmps'][champ]['evts'][game]['ext']['112']['data'][tot]['blocks']['T']['Tb']['kf']
                    return koef_r
                else:
                    pass
        except:
            pass
    return 0

def games_online_score(result, sport, list_games):
    if list_games!=[]:
        for game in list_games:
            g=game.split(';')
            try:
                time_name=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['time_name']
                
            except:
                time_name=''
            try:
                time_min=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['min']
            except:
                time_min=1

            if time_name=='перерыв':
                sc_ev=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['sc_ev']   
                sc=sc_ev.split(':')
                goals=int(sc[0])+int(sc[1])
                if goals<kf:
                    last=get_ofline_bet(g[0])
                    last_tot=last[16]

                    if goals==0:
                        kf_p=1.5
                        kf_tb=get_total_kf(result,sport,g[1],g[0],kf_p)
                        tt=f'Тотал Больше({kf_p})'
                    elif goals==1:
                        kf_p=2.5
                        kf_tb=get_total_kf(result,sport,g[1],g[0],kf_p)
                        tt=f'Тотал Больше({kf_p})'
                    elif goals==2:
                        kf_p=3
                        kf_tb=get_total_kf(result,sport,g[1],g[0],kf_p)
                        tt=f'Тотал Больше({kf_p})'

                    if kf_tb==0:
                        pass
                    else:
                        st=f'{last[2]}\n{last[8]} - {last[9]} {sc[0]} : {sc[1]}.\nДо игры:\nП1({last[10]}) Х({last[11]}) П2({last[12]}) Тотал({last_tot}) Меньше: {last[18]} Больше: {last[17]}\nСейчас:\n{tt}: {kf_tb}'
                        if db.game_exists_in_myDb(g[0], tt)==False:
                            db.save_my_bet(g[0],g[1],last[2],last[5],last[8],last[9],tt,kf_tb)
                            # send_telegram(st)
                            print(st)
                        pass
                else:
                    st=''
                    print(f'Game {g[0]}.NoNoNo ... ',st)
    else:
        print('Игр нет....')

def get_result(sport,date):
    
    # print(tday)
    res=requests.get(f'https://ad.betcity.ru/d/score?rev=5&date={date}')
    # res=requests.get('https://ad.betcity.ru/d/score?rev=5&date=2023-05-05')
    result=res.json()

    my_bets_arr_games=db.get_num_mybets()   #15352
    my_bets_arr_chs=db.get_mybets_ch()
    len_bet=len(my_bets_arr_games)
    i=0

    while i<len_bet:
        try:     
            score=result['reply']['sports'][sport]['chmps'][str(my_bets_arr_chs[i][0])]['evts'][str(my_bets_arr_games[i][0])]['sc_ev']
            # print(f'Game {my_bets_arr_games[i][0]},{my_bets_arr_chs[i][0]} - {score}')
            db.update_res(id_game=my_bets_arr_games[i][0],score=score)
        except:
            pass
        pass
        i+=1
    return


def games_online_total(result, sport, list_games, ids):
    to_day_ts=int(datetime.now().timestamp())
    if list_games!=[]:
        for game in list_games:
            g=game.split(';')
            try:
                # time_name=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['time_name']
                # date_ts
                date_ev=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['date_ev']
            except:
                # "time_name": "Перерыв",
                # time_per=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['time_name']
                date_ev=0
            try:
                time_min=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['min']
            except:
                time_min=1
            try:
               time_per=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['time_name']
            except:
               time_per='NoNoNo'  

            # if to_day_ts>date_ev+10*60 and to_day_ts<date_ev+100*60:  # 1699119900  date_ev
            if time_per=="Перерыв":
                score_tec=db.get_score(g[0])
                sc_t=score_tec.split(':')
                sc_t_all=int(sc_t[0])+int(sc_t[1])
                sc_ev=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['sc_ev']   
                sc=sc_ev.split(':')
                goals=int(sc[0])+int(sc[1])

                # if goals>sc_t_all:
                if sc_t_all==20:
                    try:
                        bets_main=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['main']['69']
                        win1=bets_main['data'][g[0]]['blocks']['Wm']['P1']['kf']
                        win2=bets_main['data'][g[0]]['blocks']['Wm']['P2']['kf']
                        xxx=bets_main['data'][g[0]]['blocks']['Wm']['X']['kf']
                    except:
                        win1=0
                        win2=0
                        xxx=0
                    try:    
                        bets_total=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['main']['72']
                        bets_total_name=result['reply']['sports'][sport]['chmps'][g[1]]['evts'][g[0]]['main']['72']['name']
                        total_how=bets_total['data'][g[0]]['blocks']['T1m']['Tot']    # float
                        total_big=bets_total['data'][g[0]]['blocks']['T1m']['Tb']['kf']   # float
                        total_lit=bets_total['data'][g[0]]['blocks']['T1m']['Tm']['kf']   # float
                    except:
                        total_how=0
                        total_big=0
                        total_lit=0

                    db.set_score(g[0],sc_ev)  
                    last=get_ofline_bet(g[0])
                    last_tot=last[16]  # total
                    last_w1=last[10]   # P1
                    last_w2=last[12]   # P2

                    # if float(last_w1)<1.5 and float(win1)>float(last_w1):
                    if True:
                        tt='П1'
                        st=f'{last[2]}\n{last[8]} - {last[9]} {sc[0]} : {sc[1]}.\nДо игры:\nП1({last[10]}) Х({last[11]}) П2({last[12]}) Тотал({last_tot}) Меньше: {last[18]} Больше: {last[17]}\nСейчас:\n П1: {win1}  П2: {win2} Тотал({total_how}) Меньше: {total_lit} Больше: {total_big}\n----------------------------------------------------------\n'
                        # if db.game_exists_in_myDb(g[0], tt)==False:
                        #     db.save_my_bet(g[0],g[1],last[2],last[5],last[8],last[9],tt,win1)
                        # send_telegram(st)
                        # ids=['5788711040', '6031644436']
                        # ids=['5788711040', '6031644436', '5058889035']
                        ids=['5788711040']
                        for chat_id in ids:
                            sends_telegram(st, chat_id)
                            time.sleep(2)
                        print(st)
            else:
                st=''
                print(f'Game {g[0]}.No PERERIV ... ',st)
    else:
        print('Игр нет....')

sss=0

print(BOT_INFO)
while True:
    
    
    # ids=['5788711040', '6031644436', '5058889035']
    # for chat_id in ids:
    #     sends_telegram('Привет. Я помощник ставок на Футбол. Анализ игр в Онлайне на Победу фаворита.', chat_id)
    time.sleep(1)
    to_day_ts_loop=int(datetime.now().timestamp())
    data_big=int(read_txt('timer_big.txt'))
    data_sml=int(read_txt('timer_sml.txt'))
    
    if to_day_ts_loop>data_big:
        # Большой цикл (3 часа)
        print('Read DataBig:  ',data_big)
        t=to_day_ts_loop+3*60*60
        write_txt('timer_big.txt', str(t))
        print('NowBig: ',t)
        db.delete_game_by_time(to_day_ts_loop)
        print('Удалили из базы старую инфу....')
        saved_ofline_games(sport,headers)
        print('Записали в базу новую инфу....')
        g_db=games_in_db_off()
        times_arr=get_times_begin_array()
        # print('Times: ',times_arr)  #  [1683241200, 1683214200, 1683215400]
    else:
        # print('No big Circle') 9388083807  106647335+leonidglss@users.noreply.github.com
        pass

    Razr_requesst=req_may_do(times_arr, to_day_ts_loop,Int_start,Int_time)
    # print('Razre: ',Razr_requesst)
    if Razr_requesst:
        if to_day_ts_loop>data_sml:
            sss+=1
            ids=db.users_is_online()
            print('Array Users: ', ids)
            # Малый цикл (3 минуты)
            print(f'Read DataSmall {sss}:  ',data_sml)
            ts=to_day_ts_loop+3*60
            write_txt('timer_sml.txt', str(ts))
            print('NowSml: ',ts)

            response=requests.get('https://ad.betcity.ru/d/on_air/bets?rev=8&add=dep_event', headers=headers)
            result=response.json()

            gamesOnLineFromlist=games_online(result=result ,sport=sport,headers=headers)
            common = [x for x in g_db if x in gamesOnLineFromlist]
            # print('Список игр сейчас онлайн', gamesOnLineFromlist)
            # print('Список игр из БД', g_db)
            print('Объед список игр',common)

            # Список игр сейчас онлайн ['13114838;151962']
            # Список игр из БД ['11839576', '11839590', '13115058', '13058703', '11877525', '13107546', '13112491', '13112492']
            games_online_total(result, sport, common, ids)
        
        else:
            pass
    else:
        # print('No small Circle')
        pass


    # Timer=True

    # data_rec=int(read_txt('timer_record.txt'))
    # if to_day_ts_loop>data_rec:
    #     Timer=True
    #     data_rec+=24*60*60
    #     write_txt('timer_record.txt', str(data_rec))
    # if Timer:
    #     # Запись результатов
    #     # 1683323100  -  2023-05-06 00:45   
    #     today=str(datetime.now()).split(' ')[0]
    #     ts=int(TSfromDate(today))-24*60*60
    #     yday=dateFromTS(ts)
    #     get_result(sport,yday)
    #     pass
    #     Timer=False
        
       


    time.sleep(2)


