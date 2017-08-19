from flask import Flask, request

from google.appengine.api import urlfetch
import json
import telegram
import logging

app = Flask(__name__)

# todo: change token to implement
bot = telegram.Bot(token='')


@app.route('/fruit_analysis', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        file = bot.getFile(update.message.photo[1].file_id)

        try:
            response = ''

            # todo: change url connection to implement
            url = 'url_tensor_photo_xray' + file.file_path

            response = json.loads(urlfetch.fetch(url).content)
            if response:
                for i in response:
                    for key in i:
                        if int(i[key]) > 50:
                            chat_id = update.message.chat.id

                            text = "your breakfast include " + key + " wow!"

                            bot.sendMessage(chat_id=chat_id, text=text)
                            break
                    else:
                        continue
                    break

        except:
            logging.error('Response: %s', response)
            raise

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    # todo: change url connection to implement
    s = bot.setWebhook('url_hook_telegram')
    if s:
        return "web_hook config ok"
    else:
        return "web_hook config failed"


if __name__ == '__main__':
    app.run(debug=True)
