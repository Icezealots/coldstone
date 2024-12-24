from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, 
    CarouselTemplate, CarouselColumn, LocationSendMessage, URITemplateAction, StickerSendMessage, ButtonsTemplate, ImageSendMessage
)
from urllib.parse import parse_qsl
import os

liffid = '2006620225-p5Ae3ykb'

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
handler = WebhookHandler(os.environ.get('Channel_Secret'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '台北據點':
        try:
            message = TemplateSendMessage(
                alt_text = "商品訂購",
                template = ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/H253Dss.jpg',
                    title='商品訂購',
                    text='歡迎訂購coldstone冰品。',
                    actions=[
                        URITemplateAction(label='商品訂購', uri='https://liff.line.me/' + liffid)  #開啟LIFF讓使用者輸入訂房資料
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤: {str(e)}'))

def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  # 取得 Postback 資料
    if backdata.get('action') == 'buy':
        sendBack_buy(event, backdata)
    elif backdata.get('action') == 'sell':
        sendBack_sell(event, backdata)

def sendCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/u0O4lst.jpeg',
                        text='酷黑女王',
                        actions=[
                            URITemplateAction(
                                label='產品連結',
                                uri='https://www.coldstone.com.tw/product/product_detail.aspx?p_id=IC130'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/IvsRhW6.jpeg',
                        text='酷黑法師',
                        actions=[
                            URITemplateAction(
                                label='產品連結',
                                uri='https://www.coldstone.com.tw/product/product_detail.aspx?p_id=IC131'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/H7SacYz.jpeg',
                        text='酷黑鬥士',
                        actions=[
                            URITemplateAction(
                                label='產品連結',
                                uri='https://www.coldstone.com.tw/product/product_detail.aspx?p_id=IC132'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/EnQE5j9.jpeg',
                        text='焙香蜜QQ',
                        actions=[
                            URITemplateAction(
                                label='產品連結',
                                uri='https://www.coldstone.com.tw/product/product_detail.aspx?p_id=IC129'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤: {str(e)}'))

def sendBack_buy(event, backdata):
    try:
        text1 = f"感謝您購買披薩，我們將盡快為您製作。\n(action的值為: {backdata.get('action')})"
        message = TextSendMessage(text=text1)
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤: {str(e)}'))

def sendBack_sell(event, backdata):
    try:
        message = TextSendMessage(text=f"點選的是賣: {backdata.get('item')}")
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤: {str(e)}'))

if __name__ == "__main__":
    app.run()
