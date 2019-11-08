from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = 'OeUcBaukfBDjXEukC3bvqOzvA/2NRBPNgxv1RGuVCgn93HE7ih0RZlwGVfav+hge/X2otNc2NGHA40blHg6bctERa8e6Z2KMAvfKzGKkH/BXa17/vnZya3KzpNJCj8fTet3r2WmLW7aiz949bSL8ugdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '12cd193da30c66d6debbff7ed6fd0e0c'


line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    textin = event.message.text

    if '好嗎' in textin:
        textout = '很好'
    elif '天氣' in textin:
        textout = '今天天氣很好'
    elif '八卦' in textin:
        textout = getBagua()
    elif '美食' in textin:
        textout = getPTT('FOOD')
    else:
        textout = '我不懂你說什麼，請再說一次'
    
    #textout = textin


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=textout))

def getPTT(board):
    result = requests.get('https://www.ptt.cc/bbs/'+board+'/index.html')
    soup = BeautifulSoup(result.text, 'lxml')
    print(soup.title.text)
    selector = "div.title a"
    tags = soup.select(selector) # 取得一組 bs4.element.Tag 的 list
    host = 'https://www.ptt.cc'
    s = []
    for tag in tags:
        # , host+tag['href'])    
        s.append(tag.text)
    return '\n'.join(s)


def getBagua():
    payload = {
        'from': 'bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    host = 'https://www.ptt.cc'
    rs = requests.session()
    result = rs.post(host+'/ask/over18', data=payload)

    result = rs.get(host+'/bbs/Gossiping/index.html')
    soup = BeautifulSoup(result.text, 'lxml')
    selector = 'div.title a'
    tags = soup.select(selector)
    s = []
    for tag in tags:
        # , host+tag['href'])    
        s.append(tag.text)
    return '\n'.join(s)

if __name__ == "__main__":
    app.run()
