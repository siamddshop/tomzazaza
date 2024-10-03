const express = require('express');
const { Client, middleware } = require('@line/bot-sdk');
const bodyParser = require('body-parser');

// ใส่ข้อมูล Channel Access Token และ Channel Secret ที่ได้จาก Line Developers
const config = {
    channelAccessToken: 'o2RQa+7jbZMcwO6rvoPdfHvkXQ/Wkkyo5uhyXuX42uhu5ZbzOobgqVdywPPR+qgFhTfsL1TKk9i8HJVUqQ3h/rrEPqRJv7D/iAj3Un/+SaX9MfTRHEA94/YQhLa+2lZP47F4j7t3wja6r44TfsH9fwdB04t89/1O/w1cDnyilFU=',
    channelSecret: 'ad65ac36735cff21dd2ea8db7ae38fe1'
};

const client = new Client(config);
const app = express();

app.use(middleware(config));
app.use(bodyParser.json());

// ฟังก์ชันการรับ Webhook และการประมวลผล
app.post('/callback', (req, res) => {
    Promise
        .all(req.body.events.map(handleEvent))
        .then((result) => res.json(result))
        .catch((err) => {
            console.error(err);
            res.status(500).end();
        });
});

// ฟังก์ชันสำหรับการจัดการข้อความและขอโลเคชั่น
function handleEvent(event) {
    if (event.type !== 'message' || event.message.type !== 'text') {
        return Promise.resolve(null);
    }

    // ถ้าผู้ใช้พิมพ์ 'share location' จะทำการส่ง Quick Reply ให้ส่งโลเคชั่น
    if (event.message.text.toLowerCase() === 'share location') {
        const message = {
            type: 'text',
            text: 'Please share your location',
            quickReply: {
                items: [
                    {
                        type: 'action',
                        action: {
                            type: 'location',
                            label: 'Send location'
                        }
                    }
                ]
            }
        };
        return client.replyMessage(event.replyToken, message);
    }

    // ตอบกลับข้อความปกติหากไม่ได้ขอโลเคชั่น
    return client.replyMessage(event.replyToken, {
        type: 'text',
        text: 'กรุณาพิมพ์ "share location" เพื่อส่งโลเคชั่นของคุณ'
    });
}

// ฟังก์ชันรับข้อมูลโลเคชั่นเมื่อผู้ใช้ส่ง
function handleLocationMessage(event) {
    if (event.message.type === 'location') {
        const latitude = event.message.latitude;
        const longitude = event.message.longitude;
        const address = event.message.address;

        const replyText = `ขอบคุณที่ส่งโลเคชั่น!\nพิกัดของคุณคือ:\nละติจูด: ${latitude}\nลองจิจูด: ${longitude}\nที่อยู่: ${address}`;

        return client.replyMessage(event.replyToken, {
            type: 'text',
            text: replyText
        });
    }
}

// ทำการเริ่มเซิร์ฟเวอร์
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
