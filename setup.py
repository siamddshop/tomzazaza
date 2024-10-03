from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage, QuickReply, QuickReplyButton, LocationAction

app = Flask(__name__)

# ใส่ Channel Access Token และ Channel Secret ที่ได้จาก Line Developers
LINE_CHANNEL_ACCESS_TOKEN = 'o2RQa+7jbZMcwO6rvoPdfHvkXQ/Wkkyo5uhyXuX42uhu5ZbzOobgqVdywPPR+qgFhTfsL1TKk9i8HJVUqQ3h/rrEPqRJv7D/iAj3Un/+SaX9MfTRHEA94/YQhLa+2lZP47F4j7t3wja6r44TfsH9fwdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'ad65ac36735cff21dd2ea8db7ae38fe1'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # รับข้อมูล webhook
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# ฟังก์ชันสำหรับขอให้ลูกค้าส่งโลเคชั่น
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text.lower() == "share location":
        # ส่ง Quick Reply ขอโลเคชั่น
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Please share your location',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=LocationAction(label="Send location")
                        )
                    ]
                )
            )
        )
    else:
        # ตอบกลับข้อความปกติ
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please type 'Share location' to send your location")
        )

# ฟังก์ชันสำหรับรับโลเคชั่นจากลูกค้า
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    latitude = event.message.latitude
    longitude = event.message.longitude
    address = event.message.address

    # ตอบกลับพร้อมพิกัดโลเคชั่นที่ได้รับ
    reply_text = f"ขอบคุณที่ส่งโลเคชั่นให้ครับ!\nพิกัดของคุณคือ:\nละติจูด: {latitude}\nลองจิจูด: {longitude}\nที่อยู่: {address}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(port=8000)
