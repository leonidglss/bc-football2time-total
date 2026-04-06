import requests
from botConfig import BOT_ADRES_FOOTBALL_WIN, BOT_NAME_FOOTBALL_WIN, WTS_TOKEN_FOOTBALL_WIN
import time

def send_telegram(text: str):
    token=WTS_TOKEN_FOOTBALL_WIN
    # token=BOT_TOKEN_FOOTBALL
    url='https://api.telegram.org/bot'
    ids=['5788711040', '6031644436']
    chat_id='6031644436' # 5058889035

    # for id in ids:
    url+=token
    method=url+'/sendMessage'

    r=requests.post(method,data={
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    })
    if r.status_code!=200:
        raise Exception('post_text error')
        # time.sleep(3)

def sends_telegram(text: str, chat_id):
    token=WTS_TOKEN_FOOTBALL_WIN
    # token=BOT_TOKEN_FOOTBALL
    url='https://api.telegram.org/bot'
    
    # chat_id='6031644436' # 5058889035

    # for id in ids:
    url+=token
    method=url+'/sendMessage'
    try:
        r=requests.post(method,data={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        })
    except:
        pass
    # if r.status_code!=200:
    #     raise Exception('post_text error')
        # time.sleep(3)

def main():
    send_telegram('Hello I am bot from Hockey Totals!')

if __name__=='__main__':
    main()