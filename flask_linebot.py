from flask import Flask, request, abort

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
    else:
        textout = '我不懂你說什麼，請再說一次'
    
    #textout = textin


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=textout))


if __name__ == "__main__":
    app.run()
